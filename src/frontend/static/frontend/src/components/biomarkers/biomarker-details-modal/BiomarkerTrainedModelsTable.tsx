import React, { useState } from 'react'
import { PaginatedTable } from '../../common/PaginatedTable'
import { Biomarker, TrainedModel } from '../types'
import { Button, Form, Icon, Modal, Table } from 'semantic-ui-react'
import { TableCellWithTitle } from '../../common/TableCellWithTitle'
import { formatDateLocale } from '../../../utils/util_functions'
import { Nullable } from '../../../utils/interfaces'
import { NewTrainedModelForm } from './trained-models/NewTrainedModelForm'

declare const urlBiomarkerTrainedModels: string

/** BiomarkerTrainedModelsTable props. */
interface BiomarkerTrainedModelsProps {
    /** Selected Biomarker instance to retrieve its TrainedModel instances. */
    selectedBiomarker: Biomarker,
    /** If `true`, shows a button to add a new TrainedModel. */
    allowFullManagement: boolean,
    /** Selected TrainedModel instance. */
    selectedTrainedModel?: Nullable<TrainedModel>,
    /** Callback to update the selected TrainedModel instance. */
    selectTrainedModel?: (newSelectedTrainedModel: TrainedModel) => void
}

/**
 * Renders a paginated table to select a TrainedModel instance.
 * @param props Component props.
 * @returns Component.
 */
export const BiomarkerTrainedModelsTable = (props: BiomarkerTrainedModelsProps) => {
    const [showNewTrainedModelModal, setShowNewTrainedModelModal] = useState(false)

    return (
        <>
            {/* New TrainedModel modal */}
            <Modal
                onClose={() => setShowNewTrainedModelModal(false)}
                onOpen={() => setShowNewTrainedModelModal(true)}
                closeOnEscape={false}
                closeOnDimmerClick={false}
                closeOnDocumentClick={false}
                closeIcon={<Icon name='close' size='large' />}
                open={showNewTrainedModelModal}
            >
                <Modal.Header>
                    <Icon name='code branch' />
                    Create new trained model
                </Modal.Header>
                <Modal.Content>
                    <NewTrainedModelForm selectedBiomarker={props.selectedBiomarker} />
                </Modal.Content>
                <Modal.Actions>
                    <Button onClick={() => setShowNewTrainedModelModal(false)}>Cancel</Button>
                </Modal.Actions>
            </Modal>

            {/* TrainedModels table. */}
            <PaginatedTable<TrainedModel>
                headerTitle='Trained models'
                headers={[
                    { name: 'Name', serverCodeToSort: 'name', width: 3 },
                    { name: 'Description', serverCodeToSort: 'description', width: 4 },
                    { name: 'Date', serverCodeToSort: 'created' },
                    { name: 'Best fitness', serverCodeToSort: 'best_fitness_value' }
                ]}
                defaultSortProp={{ sortField: 'upload_date', sortOrderAscendant: false }}
                queryParams={{ biomarker_pk: props.selectedBiomarker.id }}
                customElements={[
                    <Form.Field key={1} className='biomarkers--button--modal' title='Add new Biomarker'>
                        <Button primary icon onClick={() => { setShowNewTrainedModelModal(true) }}>
                            <Icon name='add' />
                        </Button>
                    </Form.Field>
                ]}
                showSearchInput
                searchLabel='Name'
                searchPlaceholder='Search by name'
                urlToRetrieveData={urlBiomarkerTrainedModels}
                updateWSKey='update_trained_models'
                mapFunction={(biomarkerTrainedModel: TrainedModel) => {
                    return (
                        <Table.Row
                            key={biomarkerTrainedModel.id as number}
                            className={props.selectTrainedModel ? 'clickable' : undefined}
                            active={biomarkerTrainedModel.id === props.selectedTrainedModel?.id}
                            onClick={() => {
                                if (props.selectTrainedModel) {
                                    props.selectTrainedModel(biomarkerTrainedModel)
                                }
                            }}
                        >
                            <TableCellWithTitle value={biomarkerTrainedModel.name} />
                            <TableCellWithTitle value={biomarkerTrainedModel.description ?? ''} />
                            <TableCellWithTitle value={formatDateLocale(biomarkerTrainedModel.created as string, 'LLL')} />
                            <Table.Cell>{biomarkerTrainedModel.best_fitness_value.toFixed(4)}</Table.Cell>
                        </Table.Row>
                    )
                }}
            />
        </>
    )
}
