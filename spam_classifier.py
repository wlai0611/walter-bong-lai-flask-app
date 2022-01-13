import pickle
import pandas as pd

from flask import request, jsonify

LOCAL_CACHE = {}

def predict():
    if ("loaded_model" not in LOCAL_CACHE or "tfidf_vectorizer" not in LOCAL_CACHE):
        with open("./model/model.pkl","rb") as model_file:
            LOCAL_CACHE["loaded_model"] = pickle.load(model_file)
        with open("./model/tfidf-vect.pkl","rb") as tfidf_vect_file:
            LOCAL_CACHE["tfidf_vectorizer"] = pickle.load(tfidf_vect_file) 
    try:
        comments = [[comment] for comment in request.json]
        if (len(comments) > 0):
            comments_df = pd.DataFrame(data=comments, columns=["CONTENT"])
            comments_tfidf = LOCAL_CACHE["tfidf_vectorizer"].transform(comments_df["CONTENT"])
            predictions = LOCAL_CACHE["loaded_model"].predict(comments_tfidf).tolist()

        else:
            predictions=[]
        return jsonify(predictions=predictions), 200

    except Exception as e:
        print(e)
        return jsonify(message=e), 400