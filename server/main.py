# coding=utf8

from flask import Flask, json
from flask_cors import CORS
from function import predict_disease,disease_search

from datetime import datetime
app = Flask(__name__)
CORS(app)









#print(disease_search("polio"))

# search details about the disease
@app.route("/search/<disease>", methods=['GET'])
def search(disease: str):
    now=datetime.now()
    current_time=now.strftime('%H:%M:%S')
    print(current_time)
    # search detail about disease
    search = disease_search(disease)
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')
    print(current_time)
    # if the program not find the disease as a disease
    if(search==False):
        return json.dumps({"error": str(disease)+'is not a disease'}), 500
    return json.dumps(search)

# predic disease by symptoms
@app.route("/predict/<symptoms>", methods=['GET'])
def predict(symptoms: list):
    # predict the disease name by the symptoms
    disease=predict_disease(symptoms)[0]
    return json.dumps({'disease':disease})




if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)






