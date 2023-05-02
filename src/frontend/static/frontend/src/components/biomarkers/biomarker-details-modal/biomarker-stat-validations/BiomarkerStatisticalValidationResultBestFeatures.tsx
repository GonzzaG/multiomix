
import React, { useEffect, useState } from 'react'
import { MoleculeWithCoefficient, StatisticalValidationForTable } from '../../types'
import { Nullable } from '../../../../utils/interfaces'
import ky from 'ky'
import { alertGeneralError } from '../../../../utils/util_functions'
import { Card, Placeholder } from 'semantic-ui-react'
import ReactApexChart from 'react-apexcharts'

/** Epsilon to add to the min/max value of coefficients. */
const EPSILON = 1

declare const urlStatisticalValidationBestFeatures: string

/** BiomarkerStatisticalValidationResultBestFeatures props. */
interface BiomarkerStatisticalValidationResultBestFeaturesProps {
    /** Selected StatisticalValidationForTable instance to retrieve all its data. */
    selectedStatisticalValidation: StatisticalValidationForTable,
}

/**
 * Renders a panel with all the best features with their coefficient for a StatisticalValidation.
 * @param props Component's props
 * @returns Component
 */
export const BiomarkerStatisticalValidationResultBestFeatures = (props: BiomarkerStatisticalValidationResultBestFeaturesProps) => {
    const [loading, setLoading] = useState(false)
    const [statValidationData, setStatValidationData] = useState<Nullable<MoleculeWithCoefficient[]>>(null)

    /**
     * Every time the StatisticalValidation changes retrieves
     * its data from the backend
     */
    useEffect(() => {
        if (props.selectedStatisticalValidation.id) {
            getStatValidationBestFeatures()
        }
    }, [props.selectedStatisticalValidation.id])

    /** Retrieve all the data of the selected StatisticalValidation instance. */
    const getStatValidationBestFeatures = () => {
        setLoading(true)

        const searchParams = { statistical_validation_pk: props.selectedStatisticalValidation.id }
        ky.get(urlStatisticalValidationBestFeatures, { searchParams }).then((response) => {
            response.json().then((statValidation: MoleculeWithCoefficient[]) => {
                setStatValidationData(statValidation)
            }).catch((err) => {
                alertGeneralError()
                console.log('Error parsing JSON ->', err)
            })
        }).catch((err) => {
            alertGeneralError()
            console.log('Error getting StatisticalValidation best features', err)
        }).finally(() => {
            setLoading(false)
        })
    }

    // Generates the chart config
    const coefficients = statValidationData ? statValidationData.map((elem) => elem.coeff) : []
    // TODO: report this bug, when specified as {x: ..., y: ...} the min, max value does not work!
    // const coefficients = statValidationData ? statValidationData.map((elem) => ({
    //     x: elem.identifier,
    //     y: elem.coeff,
    //     fillColor: elem.coeff > 0 ? '#008FFB' : '#FF4560'
    // })) : []
    const moleculesNames = statValidationData ? statValidationData.map((elem) => elem.identifier) : []

    const chartSeries: ApexAxisChartSeries = [{
        name: 'Expression',
        data: coefficients
    }]

    const chartOptions: ApexCharts.ApexOptions = {
        chart: {
            type: 'bar',
            height: 440,
            stacked: false
        },
        plotOptions: {
            bar: {
                horizontal: true,
                barHeight: '80%'
            }
        },
        dataLabels: {
            enabled: true,
            formatter: function (val: number) {
                return val.toFixed(4)
            }
        },
        stroke: {
            width: 1,
            colors: ['black']
        },
        grid: {
            xaxis: {
                lines: {
                    show: false
                }
            }
        },
        yaxis: {
            title: {
                text: 'Molecule'
            }
        },
        tooltip: {
            shared: false,
            y: {
                formatter: function (val: number) {
                    return val.toFixed(4)
                }
            }
        },
        xaxis: {
            categories: moleculesNames,
            title: {
                text: 'Coefficient'
            },
            type: 'category',
            min: Math.ceil(Math.min.apply(Math, coefficients) - EPSILON),
            max: Math.ceil(Math.max.apply(Math, coefficients) + EPSILON)
        }
    }

    return (
        <>
            {loading &&
                <Card>
                    <Placeholder>
                        <Placeholder.Image square />
                    </Placeholder>

                    <Card.Content>
                        <Placeholder>
                            <Placeholder.Header>
                                <Placeholder.Line length='very short' />
                                <Placeholder.Line length='medium' />
                            </Placeholder.Header>
                            <Placeholder.Paragraph>
                                <Placeholder.Line length='short' />
                            </Placeholder.Paragraph>
                        </Placeholder>
                    </Card.Content>
                </Card>
            }

            {(!loading && statValidationData !== null) &&
                <React.Fragment>
                    <div className='align-center margin-top-5'>
                        <ReactApexChart options={chartOptions} series={chartSeries} type="bar" height={440} />
                    </div>
                </React.Fragment>
            }
        </>
    )
}
