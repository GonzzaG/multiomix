import React from 'react'
import { Icon } from 'semantic-ui-react'
import { StateIconInfo } from '../../../utils/interfaces'
import { BiomarkerState } from '../types'

/** BiomarkerStateLabel props. */
interface BiomarkerStateLabelProps {
    /** Biomarker's state. */
    biomarkerState: BiomarkerState
}

/**
 * Renders a Label for the Biomarker's state
 * @param props Component props.
 * @returns Component.
 */
export const BiomarkerStateLabel = (props: BiomarkerStateLabelProps) => {
    let stateIcon: StateIconInfo
    switch (props.biomarkerState) {
        case BiomarkerState.COMPLETED:
            stateIcon = {
                iconName: 'check',
                color: 'green',
                loading: false,
                title: 'The experiment is complete'
            }
            break
        case BiomarkerState.FINISHED_WITH_ERROR:
            stateIcon = {
                iconName: 'times',
                color: 'red',
                loading: false,
                title: 'The experiment has finished with errors. Try again'
            }
            break
        case BiomarkerState.WAITING_FOR_QUEUE:
            stateIcon = {
                iconName: 'wait',
                color: 'yellow',
                loading: false,
                title: 'The process of this experiment will start soon'
            }
            break
        case BiomarkerState.NO_SAMPLES_IN_COMMON:
            stateIcon = {
                iconName: 'user outline',
                color: 'red',
                loading: false,
                title: 'Datasets don\'t have samples in common'
            }
            break
        case BiomarkerState.IN_PROCESS:
            stateIcon = {
                iconName: 'sync alternate',
                color: 'yellow',
                loading: true,
                title: 'The experiment is being processed'
            }
            break
        case BiomarkerState.STOPPING:
            stateIcon = {
                iconName: 'stop',
                loading: false,
                title: 'The experiment is being stopped',
                className: 'experiment-stopping-icon'
            }
            break
        case BiomarkerState.STOPPED:
            stateIcon = {
                iconName: 'stop',
                color: 'red',
                loading: false,
                title: 'The experiment was stopped'
            }
            break
        case BiomarkerState.REACHED_ATTEMPTS_LIMIT:
            stateIcon = {
                iconName: 'undo',
                color: 'red',
                loading: false,
                title: 'The experiment has failed several times. Try changing some parameters and try again.'
            }
            break
        case BiomarkerState.NO_FEATURES_FOUND:
            stateIcon = {
                iconName: 'times rectangle',
                color: 'red',
                loading: false,
                title: 'No features were found. Try changing some parameters and try again.'
            }
            break
    }

    return (
        <Icon
            title={stateIcon.title}
            className={stateIcon.className}
            name={stateIcon.iconName}
            color={stateIcon.color}
            loading={stateIcon.loading}
        />
    )
}
