export default function Header(props){
    return(
        <>
        <br></br>
        <a href={"https://www.google.com/search?q="+props.header} className="h2 d-flex justify-content-center">{props.header}</a>
        <br/>
        </>
    )
}