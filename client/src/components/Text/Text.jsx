// import SearchService from "../services/search.service";
export default function Text(props){
    return(
        // <div className="text-justify justify-content-center"  dangerouslySetInnerHTML={{ __html: props.text }} />
<div>{props.text}</div>
    //  <div className="text-justify d-flex justify-content-center" dangerouslySetInnerHTML={{ __html: SearchService.cleanClassAndStyle(props.text) }} />
    )
}