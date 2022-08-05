
const intialState = {
    disease:{
        name:''}
}

export default function reducer(state = intialState, action) {
    switch (action.type) {
        case 'SET_DISEASE':
            {
    
            state= {...state,disease:action.payload}
            return {...state}
        }
        default:
            break;
    }
    return state;
}

