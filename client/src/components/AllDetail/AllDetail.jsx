import { useSelector} from 'react-redux'
import searchService from '../services/search.service'
import Results from '../Results/Results'
import Render from '../Render/Render'
import React,{useState, useEffect} from 'react'

export default function AllDetail(props)
{  const [result,setResult]=useState()
  const [endSearch,setEndSearch]=useState(false)

    const[found,setFound]=useState(false)
    const searchStore=useSelector(store=>store.disease)
    useEffect(() => {
          loadDataOnlyOnce();
    },[searchStore]);
      
      
    const loadDataOnlyOnce= async() =>
    {
      setFound(false)
      setEndSearch(false)
     const search=await searchService.getSearch(searchStore.name);
debugger
     if(search.status==200)
     {
        setResult(search)
        setFound(true);

     }
    else
        setResult(search);
        setEndSearch(true)

    };
    return(
        <>
        {endSearch?found?<Results results={result.data}></Results>:<div class="alert alert-danger" role="alert">
        Error on net
</div>:<Render></Render>}
        </>
    )
}