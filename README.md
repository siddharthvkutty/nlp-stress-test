# Stress Testing NLP Models on Linguistically Challenging Reviews

This project evaluates sentiment analysis models under controlled linguistic stressors such as sarcasm, negation, contrast, and implicit sentiment.

## Models
- DistilBERT (SST-2)
- BERT-base (SST-2)
- RoBERTa (Twitter sentiment)

## Pipeline
1. Define stress inputs (`data/raw`)
2. Run models (`experiments/run_stress_test.py`)
3. Normalize outputs (`experiments/compute_metrics.py`)
4. Analyze failures (`analysis/metrics.py`, `analysis/plots.py`)

## Key Insight
Model confidence and agreement degrade significantly under pragmatic and implicit sentiment conditions.
