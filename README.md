# NLP Sentiment Stress Test Framework

A multi-model transformer-based framework for stress testing sentiment classifiers.

This project compares fine-tuned BERT, RoBERTa, and DistilBERT models on linguistically difficult sentiment inputs. It supports both interactive sentence evaluation and labeled dataset benchmarking.

---

## Overview

This framework allows you to:

- Run real-time sentiment prediction on custom text input
- Evaluate models on labeled datasets (CSV or JSON)
- Compare BERT, RoBERTa, and DistilBERT
- Measure accuracy, precision, recall, and F1-score
- Use ensemble majority voting
- Measure inter-model agreement
- Stress test models with sarcasm, negation, contradiction, and subtle phrasing

The models used are fine-tuned sentiment classifiers trained on the IMDB dataset.

---

## Supported Models

- `textattack/bert-base-uncased-imdb`
- `textattack/roberta-base-imdb`
- `textattack/distilbert-base-uncased-imdb`

Each model predicts:

- `negative`
- `positive`

---

## Installation

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

From the project's root directory

```bash
streamlit run app/gui.py
```

This launches the interactive GUI in the browser

## Usage Modes

### 1. Custom Input Mode

- Enter one sentence per line

- Each line is evaluated separately

- See prediction and confidence per model

- Optional ensemble voting

Example:

I loved the cinematography.
The plot was painfully dull.
It wasn't terrible, but not great either.

### 2. Dataset Upload Mode

Upload a CSV or JSON file with:

- A text column

- A label column

Example CSV:

text,label
"This movie was amazing",positive
"I hated it",negative

The system will:

Encode labels

Run predictions

Compute metrics

Show agreement between models

Show ensemble performance

## Metrics Reported

- Accuracy
- Precision (weighted)
- Recall (weighted)
- F1-score (weighted)
- Model agreement score
- Ensemble performance
- What This Project Is

This is a sentiment robustness testing framework.

It is designed to evaluate how well transformer models handle:

- Sarcasm
- Double negation
- Mixed sentiment
- Contradictory phrasing
- Subtle polarity
- Linguistic traps

## What This Project Is Not

It does not train models

It does not fine-tune models

It does not perform hyperparameter optimization

All models are pretrained sentiment classifiers.

## Example Stress Case

### Input:

```I absolutely loved how boring this masterpiece was.```

- This allows you to observe:
- Model disagreement
- Confidence instability
- Ensemble behavior