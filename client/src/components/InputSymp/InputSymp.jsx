import { useRef } from "react"

export default function InputSymp(props){

const _delete=()=>{
    props.myDelete(props.num)
}
    return(
<div id={props.num} className="input-group w-80">
  
              <input  ref={props.refw} type="text" className="form-control" placeholder="Enter symptom" aria-label="Enter symptom" aria-describedby="basic-addon1"/>
          
            </div>
         )
            }