from flask import Flask, render_template, url_for, request
import pandas as pd
import xgboost as xgb
import numpy as np
import preprocess
import pickle
import inverse_transform as it
import imp
imp.reload(it)


app = Flask(__name__)

@app.route('/predict-tlkm', methods=['POST'])
def predictTLKM():
    model = xgb.XGBRegressor()
    model.load_model("./models/tlkm.json")
    preprocessObj = preprocess.PreprocessIndependentVariables('TLKM.JK')
    df = preprocessObj.getDF()
    prediction = model.predict(df)

    with open('./scalers/scaler_close_tlkm.obj', 'rb') as fh:
        loadedScaler = pickle.load(fh)
    
    inversedPrediction = loadedScaler.inverseTransform(prediction.reshape(-1,1))
    return inversedPrediction.tolist()[0]

if __name__ == '__main__':
    app.run(debug=True)