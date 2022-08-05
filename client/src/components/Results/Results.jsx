import {useSelector} from 'react-redux'
import OneRsult from '../OneResult/OneResult'
import OneButton from '../OneButton/OneButton'

export default function Results(props){

return(


<div className="d-flex align-items-start">
  <div className="my-nav-result nav flex-column nav-pills me-3" id="v-pills-tab" role="tablist" aria-orientation="vertical">
    {props.results.map(result=><OneButton result={result} ></OneButton>)}
</div>
  <div className="tab-content" id="v-pills-tabContent">
    {props.results.map(result=><OneRsult result={result}></OneRsult>)}
  </div>
</div>
)
}