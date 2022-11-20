import React, { useState, useEffect } from 'react'
import { Button, Dimmer, Grid, Icon, Loader, Segment } from 'semantic-ui-react'
import { BiomarkerType, MoleculesSectionData, MoleculeSectionItem } from '../../types'
import './moleculeSectionStyles.css'
import { SearchMoleculesInput } from './searchMoleculesInput/SearchMoleculesInput'

interface MoleculeSectionProps {
    title: BiomarkerType,
    biomarkerFormData: MoleculeSectionItem,
    handleRemoveMolecule: (section: BiomarkerType, molecule: MoleculesSectionData) => void,
    handleSelectOptionMolecule: (mol: MoleculesSectionData, section: BiomarkerType, itemSelected: string) => void,
}
export const MoleculeSection = ({ title, biomarkerFormData, handleRemoveMolecule, handleSelectOptionMolecule }: MoleculeSectionProps) => {
    const [dataToShow, setDataToShow] = useState<MoleculesSectionData[]>([])
    const orderData = (data: MoleculesSectionData[]) => {
        return data.sort((a, b) => {
            const cond = Number(a.isValid) - Number(b.isValid)
            if (cond !== 0) {
                return cond
            }
            return Array.isArray(a.value) ? 1 : -1
        })
    }
    const handleSearchData = (searchInput: string) => {
        const moleculeToSearch = searchInput.toUpperCase()
        const orderedData = orderData(biomarkerFormData.data)
        const searchInputData = orderedData.map((item, index) => {
            if (Array.isArray(item.value)) {
                let dataOfArray
                item.value.forEach(itemValue => {
                    if (itemValue.startsWith(moleculeToSearch)) {
                        dataOfArray = orderedData[index]
                    }
                })
                return dataOfArray
            }
            if (item.value.startsWith(moleculeToSearch)) {
                return orderedData[index]
            }
        }).filter(item => item)
        setDataToShow(searchInputData)
    }
    useEffect(() => {
        setDataToShow(orderData(biomarkerFormData.data))
    }, [biomarkerFormData.data])

    return (
        <Grid.Column width={8} className='biomarkers--molecules--container--grid'>
            <h5>{title}</h5>
            <SearchMoleculesInput handleSearchData={handleSearchData} />
            <Segment className='biomarkers--molecules--container'>
                <Dimmer active={biomarkerFormData.isLoading} inverted>
                    <Loader />
                </Dimmer>
                {dataToShow.map((mol, index) => (
                    mol.isValid
                        ? <div className='biomarkers--molecules--container--item' key={title + mol.value}>
                            <Button color='green' onClick={() => handleRemoveMolecule(title, mol)} compact className='biomarkers--molecules--container--item'>{mol.value}   <Icon link name='close' /></Button>
                        </div>
                        : Array.isArray(mol.value)
                            ? <Segment key={index + title + mol.value.length} className="biomarkers--molecules--container--item">
                                {mol.value.map((item, i) => (
                                    <Button key={title + item + i} color='yellow' compact onClick={() => handleSelectOptionMolecule(mol, title, item)} >
                                        {item}
                                    </Button>
                                ))}
                            </Segment>
                            : <div className='biomarkers--molecules--container--item' key={title + mol.value}>
                                <Button color='red' compact onClick={() => handleRemoveMolecule(title, mol)}>{mol.value}     <Icon link name='close' /></Button>
                            </div>
                ))}
            </Segment>
        </Grid.Column>
    )
}
