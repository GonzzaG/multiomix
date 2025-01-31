import React, { useState } from 'react'
import { Header, Icon } from 'semantic-ui-react'
import { DjangoExperiment } from '../../../../../utils/django_interfaces'
import { ClinicalSourcePopup } from '../../../all-experiments-view/ClinicalSourcePopup'
import { InferenceExperimentForTable } from '../../../../biomarkers/types'

/**
 * Component's props
 */
interface NoClinicalDataProps {
    /** Experiment object to send its id and show some info */
    experiment: DjangoExperiment | InferenceExperimentForTable,
    /** To know if it's an experiment or an inference experiment and make some checks. */
    experimentType: 'correlation' | 'inference',
    /** URL to add/edit a clinical dataset. */
    urlClinicalSourceAddOrEdit: string,
    /** URL to unlink the clinical dataset. */
    urlUnlinkClinicalSource: string,
    /** Callback to refresh experiment info on clinical source changes */
    refreshExperimentInfo: (experimentId: number) => void
}

export const NoClinicalData = (props: NoClinicalDataProps) => {
    const [showPopup, setShowPopup] = useState(false)

    return (
        <Header size='huge' icon textAlign='center'>
            <Icon name='users' />

            No clinical data found

            <Header.Subheader>
                Click the icon below to upload clinical data

                <ClinicalSourcePopup
                    experiment={props.experiment}
                    experimentType={props.experimentType}
                    // In survival analysis tabs is necessary to have survival tuples
                    showOnlyClinicalDataWithSurvivalTuples
                    showPopup={showPopup}
                    urlClinicalSourceAddOrEdit={props.urlClinicalSourceAddOrEdit}
                    urlUnlinkClinicalSource={props.urlUnlinkClinicalSource}
                    position='bottom center'
                    iconExtraClassNames='margin-top-5'
                    openPopup={() => setShowPopup(true)}
                    closePopup={() => setShowPopup(false)}
                    onSuccessCallback={() => props.refreshExperimentInfo(props.experiment.id)}
                />
            </Header.Subheader>
        </Header>
    )
}
