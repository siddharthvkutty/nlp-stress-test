# NLP Stress Test

Robustness testing and adversarial attack toolkit for modern NLP models

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=flat&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PyTorch-2.0%2B-orange?style=flat&logo=pytorch" alt="PyTorch">
  <img src="https://img.shields.io/badge/HuggingFace-Transformers-purple?style=flat&logo=huggingface" alt="Transformers">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat" alt="License: MIT">
  <img src="https://img.shields.io/github/last-commit/siddharthvkutty/nlp-stress-test?style=flat" alt="Last commit">
</p>

**nlp-stress-test** is a modular, extensible framework to evaluate how well current NLP models (especially LLMs and classic transformers) hold up under adversarial conditions, distribution shift, edge cases, typos, noise, paraphrasing, and targeted attacks.

Goal: help researchers & practitioners understand real-world failure modes before deploying models in production.

## ✨ Key Features

- Modular attack & perturbation generators (text-based adversarial examples)
- Support for classification, sequence labeling, generation, and embedding tasks
- Black-box and white-box attack methods
- Multiple evaluation metrics: accuracy drop, attack success rate, BLEU/ROUGE/BERTScore degradation, etc.
- Built-in support for Hugging Face models + custom PyTorch modules
- Easy to extend with new perturbations / attacks / datasets
- Jupyter notebooks with visualizations and failure case analysis

## 🛠️ Implemented Perturbations & Attacks (so far)

| Category              | Method                              | Target task(s)              | Status    |
|-----------------------|-------------------------------------|-----------------------------|-----------|
| Character-level       | Typos (keyboard distance)           | All                         | ✓         |
|                       | OCR/speech errors                   | All                         | ✓         |
| Word-level            | Synonym replacement                 | Classification, NLI         | ✓         |
|                       | Word insertion/deletion             | All                         | ✓         |
|                       | Antonym / negation injection        | NLI, sentiment              | ✓         |
| Sentence-level        | Back-translation paraphrasing       | All                         | ✓         |
|                       | Syntax tree manipulations           | Parsing-sensitive tasks     | Planned   |
| Adversarial (targeted)| TextFooler / BERT-Attack style      | Classification              | ✓         |
|                       | Prompt injection / jailbreak-style  | Generation, chat            | ✓         |
| Distribution shift    | Domain adaptation stress (reviews → medical, tweets → legal, …) | All              | ✓         |
| Robustness benchmarks | ANLI, AdvGLUE, CheckList-inspired   | NLI, sentiment, QA          | Partial   |

## Quick Start

```bash
# Recommended: use uv / conda / venv
git clone https://github.com/siddharthvkutty/nlp-stress-test.git
cd nlp-stress-test

# Install dependencies
pip install -r requirements.txt
# or with uv / pipx / poetry if you prefer