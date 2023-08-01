import logging
import os
import time
from typing import Optional, Any, Dict
from celery.contrib.abortable import AbortableTask
from django.conf import settings
from pymongo.errors import ServerSelectionTimeoutError
from biomarkers.models import Biomarker, BiomarkerState, TrainedModelState, BiomarkerOrigin
from common.exceptions import NumberOfSamplesFewerThanCVFolds, ExperimentStopped, NoSamplesInCommon, ExperimentFailed
from feature_selection.fs_service import prepare_and_compute_fs_experiment
from feature_selection.models import FSExperiment, FitnessFunction
from multiomics_intermediate.celery import app
from celery.exceptions import SoftTimeLimitExceeded


@app.task(bind=True, base=AbortableTask, acks_late=True, reject_on_worker_lost=True,
          soft_time_limit=settings.FS_SOFT_TIME_LIMIT)
def eval_feature_selection_experiment(self, experiment_pk: int, fit_fun_enum: FitnessFunction,
                                      fitness_function_parameters: Dict[str, Any],
                                      algorithm_parameters: Dict[str, Any],
                                      cross_validation_parameters: Dict[str, Any]):
    """
    Computes a Feature Selection experiment.
    @param experiment_pk: FSExperiment's PK to be processed.
    @param fit_fun_enum: Selected fitness function to compute.
    @param fitness_function_parameters: Parameters of the fitness function to compute.
    @param algorithm_parameters: Parameters of the FS algorithm (Blind Search, BBHA, PSO, etc.) to compute.
    @param cross_validation_parameters: Parameters of the CrossValidation process.
    """
    def __create_target_biomarker(fs_experiment: FSExperiment):
        """Creates a new Biomarker and assigns it to the FSExperiment instance."""
        origin_biomarker = fs_experiment.origin_biomarker
        new_biomarker = Biomarker.objects.create(
            name=f'"{origin_biomarker.name}" (FS optimized {fs_experiment.pk})',
            description=origin_biomarker.description,
            origin=BiomarkerOrigin.FEATURE_SELECTION,
            state=BiomarkerState.IN_PROCESS,
            user=origin_biomarker.user
        )
        fs_experiment.created_biomarker = new_biomarker
        fs_experiment.save()

    # Due to Celery getting old jobs from the queue, we need to check if the experiment still exists
    try:
        experiment: FSExperiment = FSExperiment.objects.get(pk=experiment_pk)
    except FSExperiment.DoesNotExist:
        logging.error(f'Experiment {experiment_pk} does not exist')
        return

    # Creates the resulting Biomarker
    __create_target_biomarker(experiment)

    # Resulting Biomarker instance from the FS experiment.
    biomarker: Biomarker = experiment.created_biomarker

    # Computes the experiment
    molecules_temp_file_path: Optional[str] = None
    clinical_temp_file_path: Optional[str] = None
    try:
        logging.warning(f'ID FSExperiment -> {experiment.pk}')

        # Computes Feature Selection experiment
        start = time.time()
        molecules_temp_file_path, clinical_temp_file_path, running_in_spark = prepare_and_compute_fs_experiment(
            experiment, fit_fun_enum, fitness_function_parameters, algorithm_parameters,
            cross_validation_parameters, self.is_aborted
        )
        total_execution_time = time.time() - start
        logging.warning(f'FSExperiment {experiment.pk} total time -> {total_execution_time} seconds')

        # If user cancel the experiment, discard changes
        if self.is_aborted():
            raise ExperimentStopped
        else:
            # Saves some data about the result of the experiment
            # If it's running in Spark, the execution time is not saved here because it's not known yet and
            # the state is set from the /aws-notification endpoint asynchronously
            if not running_in_spark:
                experiment.execution_time = total_execution_time
                biomarker.state = BiomarkerState.COMPLETED
    except NoSamplesInCommon:
        logging.error('No samples in common')
        biomarker.state = BiomarkerState.NO_SAMPLES_IN_COMMON
    except ExperimentFailed:
        logging.error(f'FSExperiment {experiment.pk} has failed. Check logs for more info')
        biomarker.state = BiomarkerState.FINISHED_WITH_ERROR
    except ServerSelectionTimeoutError:
        logging.error('MongoDB connection timeout!')
        biomarker.state = BiomarkerState.WAITING_FOR_QUEUE
    except NumberOfSamplesFewerThanCVFolds as ex:
        logging.error(f'ValueError raised due to number of member of each class being fewer than number '
                      f'of CV folds: {ex}')
        biomarker.state = BiomarkerState.NUMBER_OF_SAMPLES_FEWER_THAN_CV_FOLDS
    except ExperimentStopped:
        # If user cancel the experiment, discard changes
        logging.warning(f'FSExperiment {experiment.pk} was stopped')
        biomarker.state = BiomarkerState.STOPPED
    except SoftTimeLimitExceeded as e:
        # If celery soft time limit is exceeded, sets the experiment as TIMEOUT_EXCEEDED
        logging.warning(f'FSExperiment {experiment.pk} has exceeded the soft time limit')
        logging.exception(e)
        biomarker.state = BiomarkerState.TIMEOUT_EXCEEDED
    except Exception as e:
        logging.exception(e)
        logging.warning(f'Setting BiomarkerState.FINISHED_WITH_ERROR to biomarker {biomarker.pk}')
        biomarker.state = BiomarkerState.FINISHED_WITH_ERROR
    finally:
        # Removes the temporary files
        if molecules_temp_file_path is not None:
            os.unlink(molecules_temp_file_path)

        if clinical_temp_file_path is not None:
            os.unlink(clinical_temp_file_path)

    # Saves changes in DB
    biomarker.save()
    experiment.save()

    # Maybe the experiment didn't find any feature. NOTE: needs to be checked after saving the experiment
    # Checks if experiment has best_model prop
    if hasattr(experiment, 'best_model') and experiment.best_model.state == TrainedModelState.NO_FEATURES_FOUND:
        biomarker.state = BiomarkerState.NO_FEATURES_FOUND
        biomarker.save(update_fields=['state'])