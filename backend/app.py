from flask import Flask, jsonify, request
import joblib
from featureExtraction import website

#importamos el modelo de ML ya entrenado
modelRF = joblib.load('randomForest-model.sav')

app = Flask(__name__)

@app.route("/")
def server():
    return jsonify({"mensaje":"Bienvenidos, ingresa a la ruta predict para empezar la predicción"})

@app.route("/predict", methods=["GET","POST"])
def predict():
    respuesta = request.json
    if respuesta:
        x = website(respuesta["url"])
        x.getFeatures()
        prediction=modelRF.predict([x.features])
        return jsonify({"result":int(prediction[0])})
    else:
        return jsonify({"error":"Es necesario el parámetro url"})

if __name__=="__main__":
    app.run(debug=True)