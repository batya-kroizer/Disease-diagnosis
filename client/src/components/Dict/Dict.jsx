import Text from '../Text/Text'
import List from '../List/List'

export default function Dict(props){
    return(
    <dl className="row">

    {(Object.keys(props.dict)).map(key=> <> <dt className="col-sm-3"><Text text={key}></Text></dt> <dd className="col-sm-9"><ul>{props.dict[key].map(val=>
        <List list={val}></List>)
        }</ul></dd></>)} 

</dl>
    )
}