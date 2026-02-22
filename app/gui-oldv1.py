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
# LOAD MODELS (Cached)
# --------------------------------------------------

@st.cache_resource
def load_models(num_labels):
    return {
        "BERT": BERTModel(num_labels=num_labels),
        "RoBERTa": RoBERTaModel(num_labels=num_labels),
        "DistilBERT": DistilBERTModel(num_labels=num_labels),
    }


# --------------------------------------------------
# MODE SELECTION
# --------------------------------------------------

mode = st.sidebar.radio("Mode", ["Custom Input", "Dataset Upload"])

selected_models = st.sidebar.multiselect(
    "Select Models",
    ["BERT", "RoBERTa", "DistilBERT"],
    default=["BERT", "RoBERTa", "DistilBERT"]
)

use_ensemble = st.sidebar.checkbox("Enable Ensemble Voting", value=True)

# --------------------------------------------------
# CUSTOM INPUT MODE
# --------------------------------------------------

if mode == "Custom Input":

    st.header("Custom Text Evaluation")

    user_text = st.text_area("Enter text to evaluate")

    if st.button("Run Models"):

        if not user_text.strip():
            st.warning("Please enter text.")
        else:
            models = load_models(num_labels=2)

            results = {}

            for name in selected_models:
                result = models[name].predict(user_text)
                results[name] = result

            st.subheader("Results")

            for name, result in results.items():
                st.write(
                    f"**{name}** → Prediction: {result['prediction']} | "
                    f"Confidence: {result['confidence']:.4f}"
                )

            if use_ensemble and len(results) > 1:
                ensemble_pred = max(
                    set([r["prediction"] for r in results.values()]),
                    key=[r["prediction"] for r in results.values()].count
                )

                st.subheader("Ensemble Result")
                st.write(f"Final Prediction: {ensemble_pred}")


# --------------------------------------------------
# DATASET MODE
# --------------------------------------------------

if mode == "Dataset Upload":

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

            # Use dataframe directly (since file already loaded)
            loader.df = df
            loader._validate_columns()
            loader._clean_data()
            loader.encode_labels()

            summary = loader.summary()
            st.write("Dataset Summary:", summary)

            X_train, X_test, y_train, y_test = loader.split()

            num_labels = len(set(y_train))
            models = load_models(num_labels=num_labels)

            predictions_dict = {}

            for name in selected_models:
                batch_results = models[name].predict_batch(X_test)
                predictions = [r["prediction"] for r in batch_results]
                predictions_dict[name] = predictions

                metrics = compute_basic_metrics(y_test, predictions)

                st.subheader(f"{name} Metrics")
                st.write(metrics)

            if use_ensemble and len(predictions_dict) > 1:

                ensemble_preds = ensemble_batch(predictions_dict)
                ensemble_metrics = compute_basic_metrics(y_test, ensemble_preds)

                st.subheader("Ensemble Metrics")
                st.write(ensemble_metrics)

            if len(predictions_dict) > 1:
                agree_score = agreement_score(predictions_dict)
                st.subheader("Model Agreement")
                st.write(f"Agreement Score: {agree_score:.4f}")