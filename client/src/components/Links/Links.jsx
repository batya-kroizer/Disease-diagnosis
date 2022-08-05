export default function Links(props){
    return(
     <div>{props.links.map(link=><><a className="d-flex justify-content-center" href={link}>{link}</a><br></br></>)}</div>

    )
}