
export default function OneButton(props){
    let kind=props.result.kind.toString().trim()
    kind=kind.split(' ').join('-')

   let id="v-pills-"+kind+"-tab"
   let data="#v-pills-"+kind
   let aria="v-pills-"+kind
   let selected="false"
   let className="nav-link"
   if(kind=="defination")
   {
    className="nav-link active"
    selected="true"

   }

    return(
        <>
        <button className={className} id={id} data-bs-toggle="pill" data-bs-target={data} type="button" role="tab" aria-controls={aria} aria-selected={selected}>{props.result.kind.trim()}</button>

        </>
    )
}