import Text from '../Text/Text'
import { useState } from 'react'

export default function List(props){
    const[input,setInput]=useState(false)

    const[classDiv,setClassDiv]=useState('collapse')
    const[classButton,setClassButton]=useState('btn btn-secondary')
    const[aria,setAria]=useState(false)

    const myFunc=()=>{
    if(classDiv=='collapse'){
        setClassDiv("collapse show")
        setClassButton("btn btn-secondary collapsed")
        setAria(true)}
    else{
        setClassDiv("collapse")
        setClassButton("btn btn-secondary")
        setAria(false)
    }

}
    const item=props.list
    return(
    <>    
     {<div><Text text={item.item}></Text>
      <p>


        <button onClick={myFunc} className={classButton} type="button" data-toggle="collapse" data-target="#collapseExample" aria-expanded={aria} aria-controls="collapseExample">
      {/* <img src='src/60938.png'\> */}
      <div >read more...</div>

         </button>
   </p>
 <div className={classDiv} id="collapseExample">
   <div className="card card-body">
    {item.type=='text'?Array.isArray(item.details)?item.details.map(text=><><Text text={text}></Text><br></br><br></br></>):<Text text={item.details}></Text>:item.type=='dict'?<Dict dict={item.details}></Dict>
    :item.type=='list'?<>{item.details.map(listObj=><List list={listObj}></List>)}</>:'not fuond'}
   </div>
 </div>
 </div>
}
 </>

)
}