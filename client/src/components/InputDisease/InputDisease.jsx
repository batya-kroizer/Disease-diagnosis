import { useFormik } from 'formik';
import * as Yup from 'yup';
import {  useRef } from 'react';
import { useDispatch, useSelector} from 'react-redux';
import { setDisease } from '../../Redux/actions'
import searchService from '../services/search.service';
import {useState} from 'react'

export default function InputDisease(props){
const searchStore=useSelector(store=>store.disease)

const _inputDisease = useRef();


const _dispatch = useDispatch();

const _mySubmit = () => {
const diseaseValues = {
        name: _inputDisease.current.value,
    }
    _dispatch(setDisease(diseaseValues))
props.funcParent()
}
const validationSubject=Yup.object().shape({
    name:Yup.string().required('disease is required')

}) 

const formik=useFormik(
    {
        initialValues:{name:searchStore.name}, 
        onSubmit:_mySubmit,
        validationSchema:validationSubject
    }
)

return(


<div className="row justify-content-center">
<div className="col-12 col-md-10 col-lg-8">
    <div onSubmit={formik.handleSubmit} className="card card-sm">
        <div className="card-body row no-gutters align-items-center">
            <div className="col-auto">
                <i className="fas fa-search h4 text-body"></i>
            </div>
            <div className="col">
                <input ref={_inputDisease} defaultValue={searchStore.name}  className="form-control form-control-lg form-control-borderless" type="search" placeholder="Search disease"/>
            </div>
            <div className="col-auto">
                <button onClick={_mySubmit} className="btn btn-lg btn-success" >Detail</button>
            </div>
        </div>
    </div>
</div>
    


 
</div>
)
}