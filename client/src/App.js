
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import { useSelector} from 'react-redux'
import React,{useState, useEffect} from 'react'
import InputDisease from './components/InputDisease/InputDisease';
import 'bootstrap'
import Render from './components/Render/Render'
import AllDetail from './components/AllDetail/AllDetail'
import searchService from './components/services/search.service';
import InputSymps from './components/InputSymps/InputSymps'
import'./App.css'
function App() {
  const[state,setState]=useState(false)
  const[state2,setState2]=useState(0)
  useEffect(() => {
    debugger
    const id = setInterval(() => {
      setState2(state2 + 1)
    }, 1000)
    return () => clearInterval(id)
  }, [state2])
const showResult=()=>{

    setState(true);
  }

  return (
    state2<=5?<><i className="fas fa-car-side fa-3x" data-mdb-toggle="animation" data-mdb-animation-reset="true" data-mdb-animation="slide-out-right"></i><img className="first-window" src='	http://localhost:3000/static/media/precision-health-stock.b5e93996.jpg' alt="Responsive image"/></>    :
    <div className="App">
      <header className="App-header container p-3 my-3 border">

       <ul className="nav nav-pills mb-3" id="pills-tab" role="tablist">
  <li className="nav-item" role="presentation">
    <button className="nav-link active my-nav" id="pills-home-tab" data-bs-toggle="pill" data-bs-target="#pills-home" type="button" role="tab" aria-controls="pills-home" aria-selected="true">predict disease</button>
  </li>
  <li className="nav-item" role="presentation">
    <button className="nav-link my-nav" id="pills-profile-tab" data-bs-toggle="pill" data-bs-target="#pills-profile" type="button" role="tab" aria-controls="pills-profile" aria-selected="false">detail about disease</button>
  </li>

</ul>
<div className="tab-content" id="pills-tabContent">
  <div className="tab-pane fade show active" id="pills-home" role="tabpanel" aria-labelledby="pills-home-tab"> <InputSymps ></InputSymps></div>
  <div className="tab-pane fade" id="pills-profile" role="tabpanel" aria-labelledby="pills-profile-tab"><InputDisease funcParent={showResult}></InputDisease>
        {state?<AllDetail></AllDetail>:''}</div>
</div>
 
      </header>
    </div>
  );
}

export default App;
