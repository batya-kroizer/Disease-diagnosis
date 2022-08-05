import Text from '../Text/Text'
import Links from '../Links/Links'
import List from '../List/List'
import Dict from '../Dict/Dict'
import Image from '../Image/Image'

import Header from '../Header/Header'
export default function OneResult(props){
    let kind=props.result.kind.toString().trim()
    kind=kind.split(' ').join('-')
    let id="v-pills-"+kind
    let aria="v-pills-"+kind+"-tab"
    let className="tab-pane fade"
    if(kind=="defination")
    {
      className="tab-pane fade show active"
    }

    return(
        <>
    <div className={className} id={id} role="tabpanel" aria-labelledby={aria}>
        {props.result.result?props.result.type=='link'?<Links links={props.result.result}></Links>
        :props.result.type=='image'?<Image image={props.result.result}></Image>
        :props.result.type=='dict'?<Dict dict={props.result.result}></Dict>
        :props.result.type=='list'?<>{props.result.result.map(listObj=><List list={listObj}></List>)}</>
        :<Text text={props.result.result}></Text>:<div class="alert alert-danger" role="alert">
not found</div>}</div>

        </>
    )
}