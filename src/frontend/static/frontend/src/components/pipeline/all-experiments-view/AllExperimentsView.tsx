import React from 'react'
import { Table, TableCell, Icon, DropdownItemProps } from 'semantic-ui-react'
import { AllExperimentsTableControl, Nullable } from '../../../utils/interfaces'
import { DjangoExperiment, DjangoTag, ExperimentState, ExperimentType, CorrelationMethod } from '../../../utils/django_interfaces'
import { getExperimentTypeSelectOptions, getCorrelationMethodSelectOptions, formatDateLocale, getExperimentTypeObj, getExperimentCorrelationMethodInfo, getExperimentStateObj } from '../../../utils/util_functions'
import { PaginatedTable, PaginationCustomFilter } from '../../common/PaginatedTable'
import { TableCellWithTitle } from '../../common/TableCellWithTitle'
import { SourcePopup } from './SourcePopup'
import { ClinicalSourcePopup } from './ClinicalSourcePopup'
import { SeeResultButton } from './SeeResultButton'
import { StopExperimentButton } from './StopExperimentButton'
import { DeleteExperimentButton } from './DeleteExperimentButton'

declare const urlUserExperiments: string
declare const urlDownloadFullResult: string

// Defined in gem.html
declare const urlClinicalSourceUserFileCRUD: string
declare const urlUnlinkClinicalSourceUserFile: string

/**
 * Component's props
 */
interface AllExperimentsViewProps {
    allExperiments: DjangoExperiment[],
    allExperimentsTableControl: AllExperimentsTableControl,
    gettingAllExperiments: boolean,
    tags: DjangoTag[],
    getAllUserExperiments: (retryIfNotFound?: boolean) => void,
    seeResult: (experiment: DjangoExperiment) => void,
    editExperiment: (experiment: DjangoExperiment) => void,
    confirmExperimentDeletion: (experiment: DjangoExperiment) => void,
    confirmExperimentStop: (experiment: DjangoExperiment) => void,
    handleSortAllExperiments: (headerServerCodeToSort: string) => void,
    handleTableControlChangesAllExperiments: (name: string, value: any, resetPagination?: boolean) => void
}

/**
 * Component's state
 */
interface AllExperimentsViewState {
    /** Id of the experiment which clinical source popup must be opened */
    clinicalPopupOpenId: Nullable<number>
}

/**
 * Renders a table with filters and an experiment results rows
 * @param experiment Component's experiment
 * @returns Component
 */
export class AllExperimentsView extends React.Component<AllExperimentsViewProps, AllExperimentsViewState> {
    constructor (props) {
        super(props)

        this.state = {
            clinicalPopupOpenId: null
        }
    }

    /**
     * Generates default table's Filters
     * @returns Default object for table's Filters
     */
    getDefaultFilters (): PaginationCustomFilter[] {
        const tagOptions: DropdownItemProps[] = this.props.tags.map((tag) => {
            const id = tag.id as number
            return { key: id, value: id, text: tag.name }
        })

        tagOptions.unshift({ key: 'no_tag', text: 'No tag' })

        // Get Experiment type select options, with 'All' option included
        const experimentTypeOptions = getExperimentTypeSelectOptions()

        // Get Correlation Method select options, with 'All' option included
        const selectCorrelationMethodsOptions = getCorrelationMethodSelectOptions()

        return [
            { label: 'Tag', keyForServer: 'tag', defaultValue: '', placeholder: 'Select an existing Tag', options: tagOptions, width: 3 },
            {
                label: 'Experiment type',
                keyForServer: 'type',
                defaultValue: ExperimentType.ALL,
                options: experimentTypeOptions,
                clearable: false,
                width: 2
            },
            {
                label: 'Correlation method',
                keyForServer: 'correlation_method',
                defaultValue: CorrelationMethod.ALL,
                options: selectCorrelationMethodsOptions,
                clearable: false,
                width: 2
            }
        ]
    }

    /**
     * Opens popup to add/edit clinical source data for a specific Experiment
     * @param experimentId ID of the experiment to show popup
     */
    openPopup = (experimentId: number) => { this.setState({ clinicalPopupOpenId: experimentId }) }

    /**
     * Closes the current popup
     */
    closePopup = () => { this.setState({ clinicalPopupOpenId: null }) }

    render (): JSX.Element {
        return (
            <div>
                <PaginatedTable<DjangoExperiment>
                    headerTitle='GEM'
                    updateWSKey='update_experiments'
                    defaultSortProp={{ sortField: 'submit_date', sortOrderAscendant: false }}
                    headers={[
                        { name: 'Name', serverCodeToSort: 'name' },
                        { name: 'Description', serverCodeToSort: 'description', width: 3 },
                        { name: 'Date', serverCodeToSort: 'submit_date' },
                        { name: 'State', serverCodeToSort: 'state', width: 1, textAlign: 'center' },
                        { name: 'Type', serverCodeToSort: 'type' },
                        { name: 'Cor. Method', serverCodeToSort: 'correlation_method' },
                        { name: 'N° Combinations', serverCodeToSort: 'result_final_row_count' },
                        { name: 'Clinical', width: 1, textAlign: 'center' },
                        { name: 'Tag', serverCodeToSort: 'tag', width: 1 },
                        { name: 'Sources' },
                        { name: 'Actions' }
                    ]}
                    customFilters={this.getDefaultFilters()}
                    showSearchInput
                    urlToRetrieveData={urlUserExperiments}
                    mapFunction={(experiment: DjangoExperiment) => {
                        // Generates Experiment's state info
                        const experimentState = getExperimentStateObj(experiment.state)

                        const isInProcess = experiment.state === ExperimentState.IN_PROCESS ||
                            experiment.state === ExperimentState.WAITING_FOR_QUEUE

                        // Generates ExperimentType info
                        const experimentTypeInfo = getExperimentTypeObj(experiment.type, 'ExperimentType')

                        // Generates Experiment correlation method info
                        const experimentCorrelationMethodInfo = getExperimentCorrelationMethodInfo(experiment.correlation_method)

                        // Number of combinations
                        const finalRowCount = experiment.result_final_row_count ?? '-'
                        const evaluatedRowCount = experiment.evaluated_row_count ?? finalRowCount

                        return (
                            <Table.Row key={experiment.id as number}>
                                <TableCellWithTitle value={experiment.name} />
                                <TableCellWithTitle value={experiment.description} />
                                <TableCellWithTitle value={formatDateLocale(experiment.submit_date, 'L')} />
                                <TableCell textAlign='center'>
                                    <Icon
                                        title={experimentState.title}
                                        className={experimentState.className}
                                        name={experimentState.iconName}
                                        color={experimentState.color}
                                        loading={experimentState.loading}
                                    />
                                </TableCell>
                                <TableCell>{experimentTypeInfo.description}</TableCell>
                                <TableCell>{experimentCorrelationMethodInfo.description}</TableCell>
                                <TableCell
                                    title={
                                        `The result consists of ${finalRowCount} combinations obtained from a total of ${evaluatedRowCount} evaluated combinations`
                                    }
                                >{finalRowCount} / {evaluatedRowCount}
                                </TableCell>
                                <TableCell textAlign='center'>
                                    <ClinicalSourcePopup
                                        experiment={experiment}
                                        experimentType='correlation'
                                        // It's not necessary to have survival tuples as user could want to link clinical data for CorrelationGraph
                                        showOnlyClinicalDataWithSurvivalTuples={false}
                                        urlClinicalSourceAddOrEdit={urlClinicalSourceUserFileCRUD}
                                        urlUnlinkClinicalSource={urlUnlinkClinicalSourceUserFile}
                                        showPopup={this.state.clinicalPopupOpenId === experiment.id}
                                        openPopup={this.openPopup}
                                        closePopup={this.closePopup}
                                        onSuccessCallback={this.props.getAllUserExperiments}
                                    />
                                </TableCell>
                                <TableCell>{experiment.tag ? experiment.tag.name : '-'}</TableCell>
                                <TableCell>
                                    {/* Download mRNA */}
                                    <SourcePopup
                                        source={experiment.mRNA_source}
                                        iconName='file'
                                        iconColor='blue'
                                        downloadButtonTitle='Download source mRNA file'
                                    />

                                    {/* Download GEM file */}
                                    <SourcePopup
                                        source={experiment.gem_source}
                                        iconName='file alternate'
                                        iconColor='teal'
                                        downloadButtonTitle={`Download ${getExperimentTypeObj(experiment.type, 'ExperimentType').description} source file`}
                                    />
                                </TableCell>
                                <TableCell>
                                    {/* See results button */}
                                    <SeeResultButton experiment={experiment} seeResult={this.props.seeResult} />

                                    {/* Download button */}
                                    <Icon
                                        name='cloud download'
                                        color='blue'
                                        className='clickable margin-left-5'
                                        title='Download result'
                                        onClick={() => window.open(`${urlDownloadFullResult}/${experiment.id}`, '_blank')}
                                        disabled={experiment.state !== ExperimentState.COMPLETED || !experiment.result_final_row_count}
                                    />

                                    {/* Edit button */}
                                    <Icon
                                        name='pencil'
                                        className='clickable margin-left-5'
                                        color='yellow'
                                        title='Edit'
                                        onClick={() => this.props.editExperiment(experiment)}
                                        disabled={experiment.state !== ExperimentState.COMPLETED}
                                    />

                                    {/* Stop button */}
                                    {isInProcess &&
                                        <StopExperimentButton
                                            title='Stop experiment'
                                            onClick={() => this.props.confirmExperimentStop(experiment)}
                                        />
                                    }

                                    {/* Delete button */}
                                    {!isInProcess &&
                                        <DeleteExperimentButton
                                            title='Delete experiment'
                                            onClick={() => this.props.confirmExperimentDeletion(experiment)}
                                        />
                                    }
                                </TableCell>
                            </Table.Row>
                        )
                    }}
                />
            </div>
        )
    }
}
