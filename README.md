<div align="center">

# ÈwéBench 🇹🇬

### The Reference Benchmark for Evaluating LLMs in Ewe Language

*Le benchmark de référence pour l'évaluation de LLMs en langue Ewe*

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-orange.svg)](LICENSE)
[![Tests: 107](https://img.shields.io/badge/Tests-107-blue.svg)](#categories)
[![Categories: 10](https://img.shields.io/badge/Categories-10-green.svg)](#categories)
[![Version: 1.0](https://img.shields.io/badge/Version-1.0-purple.svg)](CHANGELOG.md)

[English](#english) • [Français](#français) • [Documentation](docs/) • [Leaderboard](#leaderboard)

---

</div>

## English

### What is ÈwéBench?

ÈwéBench is the **first standardized benchmark** for evaluating Large Language Models (LLMs) on the **Ewe language** (ɛʋɛgbɛ) — a Kwa language spoken by ~7 million people in Togo and Ghana.

Unlike generic multilingual benchmarks that treat African languages as afterthoughts, ÈwéBench is **designed from the ground up** for Ewe, with culturally relevant tests, native speaker validation, and evaluation criteria that understand Ewe's unique linguistic features (tonality, agglutination, proverbs).

### Why ÈwéBench?

- **No existing benchmark** specifically evaluates LLM capabilities in Ewe
- Generic multilingual benchmarks (MMLU, HellaSwag) don't capture Ewe's nuances
- African languages need **dedicated evaluation tools** to track real progress
- Researchers and developers need a **common standard** to compare models

### Key Features

| Feature | Description |
|---------|-------------|
| **10 categories** | From linguistic comprehension to agentic capabilities |
| **107 tests** | Manually crafted, culturally grounded |
| **Weighted scoring** | ÈwéScore — single metric, weighted by category importance |
| **Any model** | Works with any OpenAI-compatible API (local or cloud) |
| **CLI & API** | Run from terminal or integrate into CI/CD |
| **Leaderboard** | Track and compare model progress |
| **Presets** | One-command evaluation for DeepSeek, Gemini, local models |

### Quick Start

```bash
# Clone the repo
git clone https://github.com/joel710/EweBench.git
cd EweBench

# Install dependencies
pip install -r requirements.txt

# Run with a preset
python run_benchmark.py --preset deepseek --verbose

# Run with a custom endpoint
python run_benchmark.py --endpoint http://localhost:11434/v1/chat/completions \
                        --model yawo-v10 --verbose

# Compare two results
python run_benchmark.py --compare results/model_a.json results/model_b.json

# View leaderboard
python run_benchmark.py --leaderboard
```

### Categories

| # | Category | Tests | Weight | Description |
|---|----------|-------|--------|-------------|
| 1 | Linguistic Comprehension | 15 | 15% | Grammar, vocabulary, tonality, morphology |
| 2 | Text Generation | 12 | 15% | Fluency, coherence, natural Ewe output |
| 3 | Reasoning | 12 | 12% | Logical reasoning expressed in Ewe |
| 4 | Translation | 12 | 12% | Bidirectional FR↔Ewe, EN↔Ewe |
| 5 | Cultural Knowledge | 10 | 10% | Proverbs, traditions, Ewe/Togolese history |
| 6 | Instruction Following | 10 | 10% | Complex instruction compliance |
| 7 | Multi-turn | 8 | 8% | Context coherence across turns |
| 8 | Agentic | 10 | 8% | Function calling, tool use |
| 9 | Style Adaptation | 8 | 5% | Register switching (formal/informal) |
| 10 | Robustness | 10 | 5% | Consistency under adversarial inputs |
| | **Total** | **107** | **100%** | |

### Scoring — ÈwéScore

The **ÈwéScore** is a single number (0-100) representing overall Ewe language capability:

```
ÈwéScore = Σ (category_score × category_weight) / Σ active_weights
```

Each test is scored 0.0-1.0 using evaluation methods:
- **exact_match** — Normalized string comparison
- **keywords** — Presence of expected Ewe keywords
- **multiple_choice** — QCM answer detection
- **format** — Output format compliance (markdown, function_call, etc.)
- **ewe_quality** — Heuristic Ewe linguistic quality (character usage, vocabulary, structure)
- **composite** — Weighted combination of multiple methods

**Passing threshold**: A test is "passed" if score ≥ 0.7

### Evaluation Methods

| Method | Use case | How it works |
|--------|----------|--------------|
| `exact_match` | Factual QA | Normalized comparison with expected answer |
| `keywords` | Open-ended | Checks presence of expected Ewe keywords in response |
| `multiple_choice` | QCM | Detects correct answer letter (A/B/C/D) |
| `format` | Structured output | Validates format (markdown, function_call, length) |
| `ewe_quality` | Free generation | Scores Ewe character usage, vocabulary, sentence structure |
| `composite` | Complex tests | Average of keywords + ewe_quality + format |

### API Compatibility

ÈwéBench works with any API implementing the OpenAI chat completions format:

```
POST /v1/chat/completions
{
  "model": "model-name",
  "messages": [{"role": "user", "content": "..."}],
  "temperature": 0.3,
  "max_tokens": 1024
}
```

**Tested providers:**
- DeepSeek API
- Google Gemini (OpenAI-compatible endpoint)
- Ollama (local)
- vLLM (local)
- Any OpenAI-compatible server

---

## Français

### Qu'est-ce qu'ÈwéBench ?

ÈwéBench est le **premier benchmark standardisé** pour évaluer les grands modèles de langage (LLMs) sur la **langue Ewe** (ɛʋɛgbɛ) — une langue Kwa parlée par ~7 millions de personnes au Togo et au Ghana.

Contrairement aux benchmarks multilingues génériques qui traitent les langues africaines comme des détails, ÈwéBench est **conçu de zéro** pour l'Ewe, avec des tests culturellement pertinents, une validation par des locuteurs natifs, et des critères d'évaluation qui comprennent les particularités linguistiques de l'Ewe (tonalité, agglutination, proverbes).

### Pourquoi ÈwéBench ?

- **Aucun benchmark existant** n'évalue spécifiquement les capacités LLM en Ewe
- Les benchmarks multilingues génériques (MMLU, HellaSwag) ne capturent pas les nuances de l'Ewe
- Les langues africaines ont besoin d'**outils d'évaluation dédiés** pour mesurer les vrais progrès
- Les chercheurs et développeurs ont besoin d'un **standard commun** pour comparer les modèles

### Démarrage rapide

```bash
# Cloner le repo
git clone https://github.com/joel710/EweBench.git
cd EweBench

# Installer les dépendances
pip install -r requirements.txt

# Configurer (optionnel — pour les presets cloud)
cp .env.example .env
# Ajouter vos clés API dans .env

# Lancer avec un preset
python run_benchmark.py --preset deepseek --verbose

# Lancer sur un modèle local
python run_benchmark.py --endpoint http://localhost:11434/v1/chat/completions \
                        --model yawo-v10 --verbose

# Évaluer une seule catégorie
python run_benchmark.py --preset deepseek --category cultural_knowledge -v

# Comparer deux modèles
python run_benchmark.py --compare results/deepseek.json results/yawo.json

# Voir le classement
python run_benchmark.py --leaderboard
```

### Catégories

| # | Catégorie | Tests | Poids | Description |
|---|-----------|-------|-------|-------------|
| 1 | Compréhension Linguistique | 15 | 15% | Grammaire, vocabulaire, tons, morphologie |
| 2 | Génération de Texte | 12 | 15% | Fluence, cohérence, naturel du texte Ewe |
| 3 | Raisonnement | 12 | 12% | Raisonnement logique exprimé en Ewe |
| 4 | Traduction | 12 | 12% | Bidirectionnelle FR↔Ewe, EN↔Ewe |
| 5 | Connaissance Culturelle | 10 | 10% | Proverbes, traditions, histoire Ewe/togolaise |
| 6 | Suivi d'Instructions | 10 | 10% | Respect d'instructions complexes |
| 7 | Multi-tour | 8 | 8% | Cohérence contextuelle sur plusieurs échanges |
| 8 | Agentique | 10 | 8% | Function calling, utilisation d'outils |
| 9 | Adaptation Stylistique | 8 | 5% | Registres formel/informel, technique/simple |
| 10 | Robustesse | 10 | 5% | Cohérence face aux entrées adverses |
| | **Total** | **107** | **100%** | |

### Scoring — ÈwéScore

L'**ÈwéScore** est un nombre unique (0-100) représentant la capacité globale en Ewe :

```
ÈwéScore = Σ (score_catégorie × poids_catégorie) / Σ poids_actifs
```

**Seuil de réussite** : Un test est "réussi" si le score ≥ 0.7

---

## Leaderboard

| # | Model | ÈwéScore | Tests Passed | Date |
|---|-------|----------|--------------|------|
| 🥇 | *En attente de soumissions* | — | — | — |

> **Soumettre vos résultats** : Exécutez le benchmark, puis ouvrez une PR avec votre fichier de résultats dans `results/`.

---

## Project Structure

```
EweBench/
├── README.md              # This file (bilingual EN/FR)
├── LICENSE                # CC BY-NC 4.0
├── requirements.txt       # Python dependencies
├── .env.example           # API keys template
├── ewe_bench.py           # Core benchmark engine
├── run_benchmark.py       # CLI runner with presets
├── leaderboard.json       # Public leaderboard data
├── tests/                 # Test suites (107 tests)
│   ├── linguistic_comprehension.json (15)
│   ├── text_generation.json (12)
│   ├── reasoning.json (12)
│   ├── translation.json (12)
│   ├── cultural_knowledge.json (10)
│   ├── instruction_following.json (10)
│   ├── multi_turn.json (8)
│   ├── agentic.json (10)
│   ├── style_adaptation.json (8)
│   └── robustness.json (10)
├── results/               # Benchmark results (gitignored)
├── docs/
│   ├── METHODOLOGY.md     # Scoring methodology details
│   ├── CONTRIBUTING.md    # How to contribute tests
│   └── TEST_FORMAT.md     # Test JSON format specification
└── .github/
    └── ISSUE_TEMPLATE.md
```

---

## Contributing

We welcome contributions! See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for details.

Ways to contribute:
- **Add tests** — More tests improve coverage
- **Validate translations** — Native speaker review
- **Submit results** — Run on your model and share
- **Report issues** — Found a bad test? Let us know

---

## License

**CC BY-NC 4.0** — Creative Commons Attribution-NonCommercial 4.0 International

- ✅ Free to use for research, education, and evaluation
- ✅ Free to modify and redistribute (with attribution)
- ⚠️ Commercial use requires explicit permission from Joel Elisée ADZONYA / Strive AI

---

## Citation

```bibtex
@misc{ewebench2026,
  author = {Joel Elisée ADZONYA},
  title = {ÈwéBench: A Reference Benchmark for Evaluating LLMs in Ewe Language},
  year = {2026},
  publisher = {Strive AI},
  howpublished = {\url{https://github.com/joel710/EweBench}}
}
```

---

<div align="center">

**Created by [Joel Elisée ADZONYA](https://joel.adzonya.strivenew.com) — [Strive AI](https://github.com/joel710)**

*L'IA au service des langues africaines* 🌍

</div>
