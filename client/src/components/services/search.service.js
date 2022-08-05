import axios from "axios"
class SearchService {
    

    getPredict(list)
    {
      var url="http://127.0.0.1:5000/predict/"+list
      return axios({
         method: "GET",
         url:url,
       })    .then((response) => {
         return response
       }).catch(function (error) {
        return error;
      });
    }

    getSearch(str)
    {
         var url="http://127.0.0.1:5000/search/"+str
         return axios({
            method: "GET",
            url:url,
          })    .then((response) => {
            return response
          }).catch(function (error) {
           return error;
         });
          
      
        }

 
}
export default new SearchService