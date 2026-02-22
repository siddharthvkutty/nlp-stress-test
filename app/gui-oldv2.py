# app/gui.py

import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
import pandas as pd

from models.bert_model import BERTModel
from models.roberta_model import RoBERTaModel
from models.distilbert_model import DistilBERTModel

from data.dataset_loader import DatasetLoader
from evaluation.metrics import compute_basic_metrics
from evaluation.ensemble import ensemble_batch
from evaluation.agreement import agreement_score


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(page_title="NLP Stress Test v2", layout="wide")

st.title("NLP Stress Test Framework")
st.write("Compare BERT, RoBERTa, and DistilBERT interactively.")


# --------------------------------------------------
# LOAD MODELS
# --------------------------------------------------

@st.cache_resource
def load_models():
    return {
        "BERT": BERTModel(),
        "RoBERTa": RoBERTaModel(),
        "DistilBERT": DistilBERTModel(),
    }


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

mode = st.sidebar.radio("Mode", ["Custom Input", "Dataset Upload"])

selected_models = st.sidebar.multiselect(
    "Select Models",
    ["BERT", "RoBERTa", "DistilBERT"],
    default=["BERT", "RoBERTa", "DistilBERT"]
)

use_ensemble = st.sidebar.checkbox("Enable Ensemble Voting", value=True)


# ==================================================
# CUSTOM INPUT MODE (RESTORED)
# ==================================================

if mode == "Custom Input":

    st.header("Custom Text Evaluation")

    user_text = st.text_area("Enter text to evaluate")

    if st.button("Run Models"):

        if not user_text.strip():
            st.warning("Please enter text.")
        else:
            models = load_models()

            results = {}

            for name in selected_models:
                result = models[name].predict(user_text)
                results[name] = result

            st.subheader("Results")

            for name, result in results.items():
                st.write(
                    f"**{name}** → "
                    #f"Prediction: {result['prediction']} | "
                    f"Prediction: {result['label']} | "
                    f"Confidence: {result['confidence']:.4f}"
                )

            if use_ensemble and len(results) > 1:
                ensemble_pred = max(
                    set([r["prediction"] for r in results.values()]),
                    key=[r["prediction"] for r in results.values()].count
                )

                st.subheader("Ensemble Result")
                #uncomment following line for binary 0 or 1 output for pos and neg
                #st.write(f"Final Prediction: {ensemble_pred}")
                st.write(f"Final Prediction: {result['label']}")


# ==================================================
# DATASET MODE
# ==================================================

elif mode == "Dataset Upload":

    st.header("Dataset Evaluation")

    uploaded_file = st.file_uploader("Upload CSV or JSON", type=["csv", "json"])

    if uploaded_file:

        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_json(uploaded_file)

        st.write("Preview:", df.head())

        text_column = st.selectbox("Select Text Column", df.columns)
        label_column = st.selectbox("Select Label Column", df.columns)

        if st.button("Run Evaluation"):

            loader = DatasetLoader(
                file_path=uploaded_file.name,
                text_column=text_column,
                label_column=label_column
            )

            loader.df = df
            loader._validate_columns()
            loader._clean_data()
            loader.encode_labels()

            summary = loader.summary()
            st.write("Dataset Summary:", summary)

            X_train, X_test, y_train, y_test = loader.split()

            num_labels = len(set(y_train))
            models = load_models()

            predictions_dict = {}

            for name in selected_models:
                batch_results = models[name].predict_batch(X_test)

                encoded_preds = [r["prediction"] for r in batch_results]
                decoded_preds = loader.decode_labels(encoded_preds)

                predictions_dict[name] = encoded_preds

                metrics = compute_basic_metrics(y_test, encoded_preds)

                st.subheader(f"{name} Metrics")
                st.write(metrics)

                st.write(f"{name} Sample Predictions:")
                st.write(decoded_preds[:10])

            if use_ensemble and len(predictions_dict) > 1:

                ensemble_preds = ensemble_batch(predictions_dict)
                ensemble_metrics = compute_basic_metrics(y_test, ensemble_preds)

                decoded_ensemble = loader.decode_labels(ensemble_preds)

                st.subheader("Ensemble Metrics")
                st.write(ensemble_metrics)

                st.write("Ensemble Sample Predictions:")
                st.write(decoded_ensemble[:10])

            if len(predictions_dict) > 1:
                agree_score = agreement_score(predictions_dict)
                st.subheader("Model Agreement")
                st.write(f"Agreement Score: {agree_score:.4f}")