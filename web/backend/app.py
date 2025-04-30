import json
import os
import joblib
import pandas as pd
import requests
from keras.models import load_model
from flask import Flask, request
# from flask_cors import CORS
from user_data_parse import UserData

app = Flask(__name__)
BASE_DIR = os.path.dirname(__file__)
DIEASE_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir, "disease_files"))
# CORS(app)  # Allow CORS for all routes

# Load ML models
# xgb_model = joblib.load('disease_files/model_file/xgb_model.pkl')
# ensemble_model = joblib.load('disease_files/model_file/ensemble_model.pkl')
# cnn_model = load_model('disease_files/model_file/cnn_model.h5')

@app.route('/api/submit', methods=['POST'])
def submit():
    print("received request", flush=True)
    data = request.get_json()
    print("########## Received Data ##########")
    print(json.dumps(data, indent=4))
    print("########## End of Data ##########", flush=True)
    input_df = pd.DataFrame([data]).astype(float)


    disease_map = {
        "AB34": ("new_ab34_model_new.pkl", "ab34_features.pkl"),# HEART DISEASE
        "AB22V2": ("AB22V2_model.h5", "ab22v2_features.pkl"),# DIABETES
        "AB29V2": ("new_ab29v2_model_new.pkl", "ab29v2_features.pkl"),# HIGH BLOOD PRESSURE
        "AB154": ("nb_model.pkl", "ab154_features.pkl")# HIGH CHOLESTEROL

    }

    disease_name_map = {
        "AB34": "HEART DISEASE",
        "AB22V2": "DIABETES",
        "AB29V2": "HIGH BLOOD PRESSURE",
        "AB154": "HIGH CHOLESTEROL"
    }


    all_required_features = set()
    for _, feature_file in disease_map.values():
        features = joblib.load(os.path.join(DIEASE_DIR, "feature_file", feature_file))
        all_required_features.update(features)

    for feat in all_required_features:
        if feat not in input_df.columns:
            input_df[feat] = 0

    results = {}
    for disease, (model_file, feature_file) in disease_map.items():
        model_path = os.path.join(DIEASE_DIR, "model_file", model_file)
        feature_path = os.path.join(DIEASE_DIR, "feature_file", feature_file)

        feature_list = joblib.load(feature_path)
        X = input_df[feature_list]

        ext = os.path.splitext(model_file)[1]

        if ext == '.pkl':
            model = joblib.load(model_path)
            print(type(model))
            prob = model.predict_proba(X)[0][1]

        elif ext == '.h5':
            keras_model = load_model(model_path)
            prob = round(float(keras_model.predict(X, verbose=0)[0][0]), 4)

        results[disease_name_map[disease]] = float(round(prob, 4))


    print("✅ Predicted Probabilities:")
    for disease_code, prob in results.items():
        name = disease_name_map.get(disease_code, disease_code)
        print(f"{name}: {prob:.4f}")
    print(results)

    advices = get_advices(results, data)
    print("✅ Advices:")
    print(advices, flush=True)

    response = {
        "status": "success",
        "predictions": results,
        "advices": advices
    }

    return response


def get_advices(disease_prob, user_data):
    MODEL = "gemma3:12b"
    API_URL = "http://ollama:11434/v1/chat/completions"
    SYSTEM_PROMPT = "You are a knowledgeable virtual health advisor. You help users understand potential health issues and give practical, non-judgmental suggestions for improving their lifestyle. Keep responses clear, actionable, and encouraging. This is not a chat, do not ask user for further questions. Do not include greeting or introductions."

    disease_description = ", ".join(f"{name}: {prob:.4f}" for name, prob in disease_prob.items())
    disease_description = f"Based on the prediction model, the user has the following probables of developing {disease_description}."

    user_data_o = UserData(user_data)

    user_key_info = {
        "Age": user_data_o.get_age(),
        "Gender": user_data_o.get_gender(),
        "Marital status": user_data_o.get_marital(),
        "Occupation": user_data_o.get_occupation(),
        "Weight": user_data_o.get_weight(),
        "BMI": user_data_o.get_bmi(),
        "Cigarette use frequency": user_data_o.get_cigarette_freq(),
        "Last time drank alcohol": user_data_o.get_last_drink(),
        "Physical activity in past week": user_data_o.get_physical_activity(),
        "Number of cigarettes per day": user_data_o.get_num_cigarettes_per_day(),
        "Binge drinking in past month": user_data_o.get_binge_drinking()
    }
    user_info = ", ".join(f"{k}: {v}" for k, v in user_key_info.items())
    user_info = f"The user's key information is [{user_info}]."

    prompt = f"{disease_description} {user_info}"

    payload = {
        "model": MODEL,
        "temperature": 0.7,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    print(json.dumps(payload))

    response = requests.post(API_URL, json=payload)
    response_json = response.json()
    advices = response_json["choices"][0]["message"]["content"]
    return advices


if __name__ == "__main__":
    app.run(host="0.0.0.0")
