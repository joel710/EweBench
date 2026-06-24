# Test Format Specification

[English](#english) • [Français](#français)

---

## English

### Overview

Each test category is a JSON file in `tests/` containing an array of test objects.

### Standard Test Format

```json
{
  "id": "category_001",
  "prompt": "The user message to send to the model",
  "system": "Optional system prompt (defaults to Yawo system prompt)",
  "eval_method": "keywords",
  "expected_keywords": ["keyword1", "keyword2"],
  "temperature": 0.3,
  "description": "Human-readable description of what this test evaluates"
}
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | ✅ | Unique test identifier (format: `category_NNN`) |
| `prompt` | string | ✅* | User message sent to the model |
| `messages` | array | ✅* | Full message array for multi-turn tests |
| `system` | string | ❌ | System prompt (default: Yawo standard prompt) |
| `eval_method` | string | ✅ | Scoring method to use |
| `temperature` | float | ❌ | Generation temperature (default: 0.3) |
| `description` | string | ❌ | What this test evaluates |

*Either `prompt` or `messages` is required, not both.

### Evaluation Method Fields

#### `exact_match`
```json
{
  "eval_method": "exact_match",
  "expected": "The exact expected answer"
}
```

#### `keywords`
```json
{
  "eval_method": "keywords",
  "expected_keywords": ["word1", "word2", "word3"]
}
```

#### `multiple_choice`
```json
{
  "eval_method": "multiple_choice",
  "expected": "B"
}
```

#### `format`
```json
{
  "eval_method": "format",
  "expected_format": {
    "contains_ewe": true,
    "min_length": 50,
    "max_length": 2000,
    "contains_function_call": false,
    "markdown_elements": ["header", "list", "bold"]
  }
}
```

#### `ewe_quality`
```json
{
  "eval_method": "ewe_quality"
}
```
No additional fields needed   scored by heuristic.

#### `composite`
```json
{
  "eval_method": "composite",
  "expected_keywords": ["word1", "word2"],
  "expected_format": {
    "contains_ewe": true,
    "min_length": 100
  }
}
```

### Multi-turn Test Format

For conversation tests, use `messages` instead of `prompt`:

```json
{
  "id": "multi_turn_001",
  "messages": [
    {"role": "system", "content": "Tu es Yawo..."},
    {"role": "user", "content": "First user message"},
    {"role": "assistant", "content": "Expected first response context"},
    {"role": "user", "content": "Follow-up question"}
  ],
  "eval_method": "composite",
  "expected_keywords": ["reference_to_first_turn"],
  "expected_format": {"contains_ewe": true}
}
```

### Complete Example

```json
[
  {
    "id": "cultural_001",
    "prompt": "Gblɔ lododo Ewe aɖe nam si fia be dɔ wɔwɔ le vevi",
    "system": "Tu es Yawo, un assistant IA expert en culture Ewe. Réponds en Ewe.",
    "eval_method": "composite",
    "expected_keywords": ["lododo", "dɔ", "agbe"],
    "expected_format": {
      "contains_ewe": true,
      "min_length": 50
    },
    "temperature": 0.5,
    "description": "Can the model produce an authentic Ewe proverb about hard work?"
  }
]
```

---

## Français

### Vue d'ensemble

Chaque catégorie de tests est un fichier JSON dans `tests/` contenant un tableau d'objets test.

### Format standard

```json
{
  "id": "categorie_001",
  "prompt": "Le message utilisateur envoyé au modèle",
  "system": "System prompt optionnel",
  "eval_method": "keywords",
  "expected_keywords": ["motcle1", "motcle2"],
  "temperature": 0.3,
  "description": "Description lisible de ce que le test évalue"
}
```

### Champs

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `id` | string | ✅ | Identifiant unique (format: `categorie_NNN`) |
| `prompt` | string | ✅* | Message utilisateur |
| `messages` | array | ✅* | Tableau complet pour les tests multi-tour |
| `system` | string | ❌ | System prompt (défaut: prompt Yawo standard) |
| `eval_method` | string | ✅ | Méthode de scoring |
| `temperature` | float | ❌ | Température de génération (défaut: 0.3) |
| `description` | string | ❌ | Ce que le test évalue |

### Ajouter un test

1. Choisir la catégorie appropriée dans `tests/`
2. Ajouter l'objet test au tableau JSON
3. S'assurer que l'`id` est unique
4. Tester avec `python run_benchmark.py --category <category> -v`
5. Soumettre une PR
