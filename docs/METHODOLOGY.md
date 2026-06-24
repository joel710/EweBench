# ÈwéBench   Scoring Methodology

[English](#english) • [Français](#français)

---

## English

### Overview

ÈwéBench uses a **weighted multi-category scoring** system. Each model receives a single **ÈwéScore** (0-100) that represents its overall capability in Ewe.

### Formula

```
ÈwéScore = Σ (category_score × category_weight) / Σ active_weights
```

Where:
- `category_score` = average test score within a category (0-100)
- `category_weight` = importance weight of that category
- `active_weights` = sum of weights for categories that were actually evaluated (handles partial runs)

### Weight Rationale

| Category | Weight | Justification |
|----------|--------|---------------|
| Linguistic Comprehension | 15% | Core: understanding Ewe grammar, tones, morphology |
| Text Generation | 15% | Core: producing natural, fluent Ewe text |
| Reasoning | 12% | Important: expressing logical thought in Ewe |
| Translation | 12% | Important: practical bilingual capability |
| Cultural Knowledge | 10% | Valuable: proverbs, traditions, history |
| Instruction Following | 10% | Practical: real-world usability |
| Multi-turn | 8% | Advanced: conversation coherence |
| Agentic | 8% | Advanced: tool use and planning |
| Style Adaptation | 5% | Bonus: register switching |
| Robustness | 5% | Bonus: adversarial resilience |

Weights sum to **100%**. Categories are ordered by importance: language mastery first, then practical capabilities, then advanced features.

### Test Scoring

Each individual test is scored **0.0 to 1.0** using one of these methods:

#### 1. Exact Match (`exact_match`)
```python
score = 1.0 if normalize(expected) == normalize(response) else 0.0
```
Used for factual questions with a single correct answer.

#### 2. Keyword Presence (`keywords`)
```python
score = count(found_keywords) / count(expected_keywords)
```
Used for open-ended questions where specific Ewe terms should appear.

#### 3. Multiple Choice (`multiple_choice`)
```python
score = 1.0 if correct_letter detected in response else 0.0
```
Used for QCM-style tests with A/B/C/D options.

#### 4. Format Compliance (`format`)
Checks multiple format criteria:
- `contains_ewe`   Response has Ewe characters (ɖ, ɛ, ɔ, ƒ, ŋ, ɣ)
- `min_length` / `max_length`   Response length bounds
- `contains_function_call`   Has `<function_call>` tag
- `markdown_elements`   Has tables, headers, lists, bold

#### 5. Ewe Quality Heuristic (`ewe_quality`)
Composite heuristic scoring:
- +0.3 for Ewe special characters presence
- +0.05 per common Ewe word found (max +0.4)
- -0.2 if too many French words detected (>5)
- +0.2 for multi-sentence structure
- +0.1 for minimum response length

#### 6. Composite (`composite`)
```python
score = (keywords_score + ewe_quality_score + format_score) / 3
```
Used for complex tests requiring multiple evaluation dimensions.

### Pass/Fail Threshold

A test is **passed** if `score >= 0.7`.

This threshold balances:
- Not too strict (some Ewe variability is expected)
- Not too lenient (ensures meaningful output quality)

### Category Score

```
category_score = (sum of test scores / number of tests) × 100
```

---

## Français

### Vue d'ensemble

ÈwéBench utilise un système de **scoring multi-catégories pondéré**. Chaque modèle reçoit un **ÈwéScore** unique (0-100) représentant sa capacité globale en Ewe.

### Formule

```
ÈwéScore = Σ (score_catégorie × poids_catégorie) / Σ poids_actifs
```

### Justification des poids

| Catégorie | Poids | Justification |
|-----------|-------|---------------|
| Compréhension Linguistique | 15% | Cœur : compréhension grammaire, tons, morphologie Ewe |
| Génération de Texte | 15% | Cœur : production de texte Ewe naturel et fluide |
| Raisonnement | 12% | Important : expression de la pensée logique en Ewe |
| Traduction | 12% | Important : capacité bilingue pratique |
| Connaissance Culturelle | 10% | Précieux : proverbes, traditions, histoire |
| Suivi d'Instructions | 10% | Pratique : utilisabilité réelle |
| Multi-tour | 8% | Avancé : cohérence conversationnelle |
| Agentique | 8% | Avancé : utilisation d'outils et planification |
| Adaptation Stylistique | 5% | Bonus : changement de registre |
| Robustesse | 5% | Bonus : résilience adversariale |

### Seuil de réussite

Un test est **réussi** si `score >= 0.7`.

### Score par catégorie

```
score_catégorie = (somme des scores de tests / nombre de tests) × 100
```

---

## Known Limitations

1. **Ewe quality heuristic** is rule-based, not learned   it can miss valid Ewe or reward superficial patterns
2. **Keyword matching** doesn't account for synonyms or paraphrasing
3. **No human evaluation** in automated runs   ÈwéScore is an approximation
4. **Tonal accuracy** cannot be verified in written text (Ewe is tonal but rarely written with tone marks)

These limitations are documented so users interpret scores with appropriate context. We plan to add human evaluation protocols in v2.0.
