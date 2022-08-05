import InputSymp from '../InputSymp/InputSymp'
import { useState, useEffect } from 'react'
import { useRef } from 'react'
import searchService from '../services/search.service'
import { useDispatch, useSelector } from 'react-redux';
import { setDisease } from '../../Redux/actions'
import './InputSymps.css'

export default function InputSymps(props) {
    const searchStore=useSelector(store=>store.disease)
    const refs = useRef();
    const _dispatch = useDispatch();

    const[predict,setPredict]=useState('')
    const[state,setState]=useState(false)
    const[found,setFound]=useState(false)

    useEffect(() => {
        refs.current = []
        setNum(1)

    },[]);

    const [num,setNum]=useState(0)



    const addInput = () => {
        setState(false)
        setNum(num+1)

    }

    const myClick = async() => {
        setFound(false)

        setState(false)
        
        let temp = []
        refs.current.map(x => temp.push(x.value))
 let pred=await searchService.getPredict(temp)
 if(pred.status==200)
{ setPredict(pred.data.disease)
 const predictDisease = {
    name:pred.data.disease,
}
_dispatch(setDisease(predictDisease))
setFound(true)
setState(true)

    }
else
    setState(true)
}
const addToRefs = (el) => {
        if (!Array.isArray(refs.current)) {
            refs.current = [""]
        }
        if (el && !refs.current.includes(el)) {
            refs.current.push(el);
        }
    };
    return (
        <>
        {Array(num).fill(1).map(() => <InputSymp refw={addToRefs}></InputSymp>)}
        <button onClick={addInput} className="btn btn-sm btn-secondary " id="basic-addon1">add symptom
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-plus" viewBox="0 0 16 16">
                <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"></path>
            </svg>
        </button>   
        <div className="d-grid gap-2 d-md-flex justify-content-md-end">
        <button onClick={myClick} className="btn  btn-lg btn-success">predict</button>    
        </div>
        {state?found ?<div className="p-3 mb-2 bg-secondary text-white predict-result">The predict disease is {searchStore.name}</div>
        :<div className="alert alert-danger" role="alert">Error on net</div>: ''}
        </>
    )
}