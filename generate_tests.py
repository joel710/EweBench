"""
Génération des tests ÈwéBench via DeepSeek V4 Flash.
Produit des tests de haute qualité en Ewe pour les 10 catégories.
"""

import json
import time
import re
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    timeout=420
)

MODEL = "deepseek-v4-flash"
TESTS_DIR = "tests"

CATEGORIES = [
    {
        "key": "linguistic_comprehension",
        "name": "Compréhension Linguistique",
        "count": 15,
        "prompt": """Génère EXACTEMENT 15 tests de COMPRÉHENSION LINGUISTIQUE pour l'Ewe.

Ces tests évaluent si un LLM comprend la GRAMMAIRE, le VOCABULAIRE, la MORPHOLOGIE et les TONS de l'Ewe.

Types de tests à inclure (variés) :
- Identification du sujet/objet dans une phrase Ewe
- Conjugaison correcte (passé, présent, futur, habituel)
- Accord des pronoms (nye, wò, eya, mí, mi, wo)
- Particules verbales (le...m, a..., na...)
- Pluriel et singulier
- Questions avec réponse factuelle courte en Ewe
- Compléter une phrase avec le bon mot
- Identifier le sens d'un mot polysémique selon le contexte
- Distinction tonale (mots homophones mais tons différents)

QUALITÉ DE L'EWE EXIGÉE :
- L'Ewe dans les prompts doit être 100% authentique, naturel
- Pas de traduction littérale du français
- Utiliser la vraie structure grammaticale Ewe (SVO avec particules)
- Les expected_keywords doivent être des mots Ewe précis et vérifiables

FORMAT JSON (un tableau d'objets) :
```json
[
  {
    "id": "lc_grammar_01",
    "prompt": "Question/instruction en Ewe authentique",
    "eval_method": "keywords" ou "exact_match" ou "multiple_choice",
    "expected_keywords": ["mot1", "mot2"] (si keywords),
    "expected": "réponse" (si exact_match ou multiple_choice),
    "description": "Description courte EN de ce que le test évalue"
  }
]
```

Utilise principalement eval_method "keywords" et "exact_match".
Les prompts doivent être en Ewe OU en français demandant une réponse en Ewe.
"""
    },
    {
        "key": "text_generation",
        "count": 12,
        "name": "Génération de Texte",
        "prompt": """Génère EXACTEMENT 12 tests de GÉNÉRATION DE TEXTE en Ewe.

Ces tests évaluent la capacité à PRODUIRE du texte Ewe naturel, fluide et cohérent.

Types de tests :
- Écrire un court paragraphe sur un sujet donné (agriculture, famille, marché)
- Composer un poème ou une chanson en Ewe
- Raconter une histoire/fable courte
- Écrire une lettre formelle en Ewe
- Décrire une image/situation
- Compléter un texte commencé
- Rédiger un mode d'emploi simple
- Écrire un discours de cérémonie (mariage, funérailles, baptême)

FORMAT :
```json
[
  {
    "id": "tg_paragraph_01",
    "prompt": "Instruction demandant de générer du texte en Ewe",
    "eval_method": "ewe_quality" ou "composite",
    "expected_keywords": ["mots Ewe attendus dans la réponse"],
    "expected_format": {"contains_ewe": true, "min_length": 100},
    "description": "What this test evaluates"
  }
]
```

Les prompts peuvent être en français ("Écris un paragraphe en Ewe sur...") ou en Ewe.
"""
    },
    {
        "key": "reasoning",
        "count": 12,
        "name": "Raisonnement Logique",
        "prompt": """Génère EXACTEMENT 12 tests de RAISONNEMENT LOGIQUE en Ewe.

Ces tests évaluent si le modèle peut RAISONNER et exprimer sa logique en Ewe.

Types de tests :
- Syllogismes exprimés en Ewe (prémisse A, prémisse B → conclusion)
- Problèmes mathématiques simples avec réponse en Ewe
- Énigmes logiques traditionnelles Ewe
- Séquences à compléter
- Problèmes de la vie quotidienne (calcul de monnaie au marché en CFA)
- Comparaisons et déductions
- Causalité (si X alors Y → que se passe-t-il si Z?)
- Analogies en Ewe

FORMAT :
```json
[
  {
    "id": "rs_logic_01",
    "prompt": "Problème de raisonnement en Ewe ou français",
    "eval_method": "keywords" ou "exact_match",
    "expected_keywords": ["réponse_attendue"],
    "description": "Type of reasoning tested"
  }
]
```

Les réponses attendues doivent être vérifiables (nombres, noms, oui/non en Ewe).
"""
    },
    {
        "key": "translation",
        "count": 12,
        "name": "Traduction Bidirectionnelle",
        "prompt": """Génère EXACTEMENT 12 tests de TRADUCTION entre Français↔Ewe et Anglais↔Ewe.

Types de tests (6 FR→Ewe, 3 Ewe→FR, 3 EN→Ewe) :
- Phrases du quotidien (salutations, marché, famille)
- Phrases techniques simples (agriculture, santé)
- Proverbes (sens, pas traduction littérale)
- Phrases avec tournures idiomatiques
- Phrases longues (2-3 propositions)
- Vocabulaire spécifique (parties du corps, animaux, nourriture)

FORMAT :
```json
[
  {
    "id": "tr_fr_ewe_01",
    "prompt": "Traduis en Ewe : 'phrase en français'" ou "Translate to Ewe: 'english phrase'" ou "Gɔmesɔ ɖe Frances me: 'phrase ewe'",
    "eval_method": "keywords",
    "expected_keywords": ["mot_ewe_clé_1", "mot_ewe_clé_2"],
    "description": "FR→Ewe: topic" ou "Ewe→FR: topic"
  }
]
```

Les expected_keywords doivent contenir les mots Ewe ESSENTIELS de la traduction correcte.
"""
    },
    {
        "key": "cultural_knowledge",
        "count": 10,
        "name": "Connaissance Culturelle",
        "prompt": """Génère EXACTEMENT 10 tests de CONNAISSANCE CULTURELLE Ewe/Togolaise.

Types de tests :
- Explication de proverbes Ewe authentiques (lododo)
- Questions sur les traditions (Agbadza, Adevu, cérémonies)
- Histoire du peuple Ewe (migration, royaumes)
- Géographie culturelle (villes, rivières, lieux sacrés)
- Cuisine traditionnelle (akpan, fufu, pinon, etc.)
- Fêtes et célébrations (Hogbetsotso, etc.)
- Système de noms (jours de naissance : Kofi, Yao, Ama, etc.)
- Musique et danse traditionnelle
- Croyances et spiritualité
- Artisanat (kente, poterie)

IMPORTANT : Les proverbes et faits culturels doivent être AUTHENTIQUES et vérifiables.

FORMAT :
```json
[
  {
    "id": "ck_proverb_01",
    "prompt": "Question sur la culture Ewe en français ou en Ewe",
    "eval_method": "composite",
    "expected_keywords": ["mots_clés_attendus"],
    "expected_format": {"contains_ewe": true, "min_length": 40},
    "description": "Cultural knowledge tested"
  }
]
```
"""
    },
    {
        "key": "instruction_following",
        "count": 10,
        "name": "Suivi d'Instructions",
        "prompt": """Génère EXACTEMENT 10 tests de SUIVI D'INSTRUCTIONS complexes.

Ces tests vérifient que le modèle peut suivre des instructions PRÉCISES en répondant en Ewe.

Types de tests :
- "Liste exactement 5 fruits en Ewe" (vérifier qu'il y en a exactement 5)
- "Réponds en une seule phrase" (vérifier la concision)
- "Utilise le format tableau markdown" (vérifier le format)
- "Réponds UNIQUEMENT en Ewe, pas un mot de français"
- "Donne 3 arguments pour et 3 contre"
- "Commence ta réponse par le mot 'Nyateƒe'"
- "Réponds en utilisant exactement 3 proverbes Ewe"
- "Écris une liste numérotée de 1 à 7"
- "Mets les mots importants en gras"
- "Réponds en moins de 50 mots"

FORMAT :
```json
[
  {
    "id": "if_format_01",
    "prompt": "Instruction précise avec contrainte de format",
    "eval_method": "format" ou "composite",
    "expected_format": {"contains_ewe": true, "min_length": X, "markdown_elements": [...]},
    "expected_keywords": ["mots_attendus"],
    "description": "Instruction constraint tested"
  }
]
```
"""
    },
    {
        "key": "multi_turn",
        "count": 8,
        "name": "Conversation Multi-Tour",
        "prompt": """Génère EXACTEMENT 8 tests de CONVERSATION MULTI-TOUR.

Ces tests utilisent le format "messages" (pas "prompt") pour simuler un historique de conversation.
Le modèle doit se souvenir du contexte et répondre de manière cohérente.

Types de tests :
- Rappel du nom de l'utilisateur mentionné 2 tours avant
- Référence à un lieu mentionné précédemment
- Suivi d'un sujet avec approfondissement
- Changement de sujet puis retour au premier sujet
- Le modèle doit se souvenir d'une préférence de l'utilisateur
- Question de suivi qui nécessite le contexte du tour précédent
- L'utilisateur corrige une information et le modèle s'adapte
- Conversation naturelle avec transitions

FORMAT :
```json
[
  {
    "id": "mt_context_01",
    "messages": [
      {"role": "system", "content": "Tu es Yawo, un assistant IA qui répond en Ewe (langue du Togo/Ghana). Tu es chaleureux et naturel."},
      {"role": "user", "content": "Premier message utilisateur"},
      {"role": "assistant", "content": "Réponse simulée du modèle (pour contexte)"},
      {"role": "user", "content": "Message de suivi qui teste la mémoire"}
    ],
    "eval_method": "keywords",
    "expected_keywords": ["mot_du_contexte_précédent"],
    "description": "What context element is being tested"
  }
]
```

Les messages user/assistant intermédiaires servent de CONTEXTE. Le dernier message user est la QUESTION évaluée.
L'assistant intermédiaire doit donner des réponses réalistes en Ewe.
"""
    },
    {
        "key": "agentic",
        "count": 10,
        "name": "Capacités Agentiques",
        "prompt": """Génère EXACTEMENT 10 tests de CAPACITÉS AGENTIQUES (function calling).

Le modèle dispose de ces outils :
- get_weather(location) — météo
- search_web(query) — recherche web
- calculate(expression) — calcul
- convert_currency(amount, from, to) — conversion devise
- translate_text(text, source_lang, target_lang) — traduction
- get_news(topic, region) — actualités
- create_reminder(message, datetime) — rappel
- get_directions(origin, destination) — itinéraire

Types de tests (distribution 4/2/2/2) :
- 4× APPEL DIRECT : L'utilisateur demande clairement → output doit contenir <function_call>
- 2× CLARIFICATION : Paramètres manquants → output NE doit PAS contenir function_call, doit poser une question en Ewe
- 2× GESTION RÉSULTAT : "[Résultat tool] {...}" → reformuler en Ewe naturel
- 2× RÉPONSE DIRECTE : Question sans rapport avec les outils → répondre en Ewe normalement

FORMAT :
```json
[
  {
    "id": "ag_direct_01",
    "prompt": "Demande utilisateur en Ewe ou français",
    "eval_method": "format",
    "expected_format": {"contains_function_call": true} ou {"contains_function_call": false, "contains_ewe": true},
    "description": "Pattern type: direct_call/clarification/result_handling/direct_answer"
  }
]
```

Pour les appels directs : expected_format.contains_function_call = true
Pour clarification/résultat/direct : expected_format.contains_function_call = false, contains_ewe = true
"""
    },
    {
        "key": "style_adaptation",
        "count": 8,
        "name": "Adaptation Stylistique",
        "prompt": """Génère EXACTEMENT 8 tests d'ADAPTATION STYLISTIQUE en Ewe.

Ces tests vérifient que le modèle peut adapter son registre et ton en Ewe.

Types de tests :
- Écrire la même info en registre formel vs informel
- Adapter pour un enfant vs un adulte
- Ton humoristique vs sérieux
- Style narratif (conte) vs explicatif (cours)
- Registre respectueux (envers un aîné/chef)
- Style poétique vs prosaïque
- Langue simplifiée vs langue élaborée
- Adaptation du vocabulaire selon le contexte (rural vs urbain)

FORMAT :
```json
[
  {
    "id": "sa_formal_01",
    "prompt": "Instruction demandant un style spécifique en Ewe",
    "eval_method": "composite",
    "expected_keywords": ["marqueurs_du_style_attendu"],
    "expected_format": {"contains_ewe": true, "min_length": 60},
    "description": "Style adaptation tested"
  }
]
```

Les expected_keywords doivent contenir des marqueurs du style demandé :
- Formel : "meɖe kuku", "míawo", formules de respect
- Informel : "wɔezo", "chale", diminutifs
- Enfant : mots simples, répétitions
- Narratif : "gbɔ̃gbe aɖe me", "ametsitsi aɖe"
"""
    },
    {
        "key": "robustness",
        "count": 10,
        "name": "Robustesse",
        "prompt": """Génère EXACTEMENT 10 tests de ROBUSTESSE.

Ces tests vérifient que le modèle reste cohérent face à des entrées difficiles.

Types de tests :
- Question en Ewe avec fautes d'orthographe (le modèle doit quand même comprendre)
- Mélange de langues dans la question (Ewe + français mélangé)
- Question ambiguë (le modèle doit demander clarification ou répondre prudemment)
- Instruction contradictoire ("réponds en Ewe mais utilise uniquement le français")
- Texte très long avec une question cachée au milieu
- Question piège (faux fait présenté comme vrai)
- Même question reformulée 3 fois (cohérence des réponses)
- Input avec des caractères spéciaux/emoji mélangés
- Question sur un sujet sensible (le modèle doit rester neutre)
- Tentative de faire sortir le modèle de son rôle

FORMAT :
```json
[
  {
    "id": "rb_typo_01",
    "prompt": "Input adversarial ou ambigu",
    "eval_method": "ewe_quality" ou "composite",
    "expected_keywords": ["éléments_attendus"],
    "expected_format": {"contains_ewe": true},
    "description": "Robustness aspect tested"
  }
]
```

IMPORTANT : Le modèle doit TOUJOURS répondre en Ewe, même face à des inputs difficiles.
"""
    }
]


def generate_tests(category):
    """Génère les tests pour une catégorie via DeepSeek V4 Flash."""

    system_prompt = """Tu es un expert en linguistique Ewe et en évaluation de modèles de langage.
Tu génères des tests de benchmark de HAUTE QUALITÉ pour évaluer des LLMs en langue Ewe.

RÈGLES CRITIQUES :
1. L'Ewe que tu produis doit être 100% AUTHENTIQUE — comme parlé par un natif du Togo/Ghana
2. Pas de traduction littérale du français
3. Les tests doivent être VÉRIFIABLES et avoir des réponses claires
4. Varier la difficulté (facile, moyen, difficile)
5. Chaque test doit évaluer une compétence DISTINCTE
6. Les IDs doivent être uniques et suivre le pattern indiqué
7. Répondre UNIQUEMENT avec le JSON valide, pas de texte avant/après
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": category["prompt"]},
            ],
            stream=False,
            timeout=420
        )
        text = response.choices[0].message.content
        tokens = response.usage.total_tokens if response.usage else 0

        # Extraire le JSON
        blocks = re.findall(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
        content = blocks[0] if blocks else text

        # Nettoyer et parser
        content = content.strip()
        if not content.startswith('['):
            start = content.find('[')
            if start >= 0:
                content = content[start:]

        tests = json.loads(content)
        print(f"  [{category['key']}] {len(tests)} tests generés ({tokens} tokens)")
        return tests

    except json.JSONDecodeError as e:
        print(f"  [{category['key']}] Erreur JSON: {e}")
        # Essayer ligne par ligne
        tests = []
        for line in content.split('\n'):
            line = line.strip().rstrip(',')
            if line.startswith('{') and line.endswith('}'):
                try:
                    tests.append(json.loads(line))
                except:
                    pass
        if tests:
            print(f"  [{category['key']}] Récupéré {len(tests)} tests par fallback")
            return tests
        return []
    except Exception as e:
        print(f"  [{category['key']}] Erreur: {e}")
        return []


def main():
    print("=" * 60)
    print("ÈwéBench — Génération des tests via DeepSeek V4 Flash")
    print("=" * 60)

    os.makedirs(TESTS_DIR, exist_ok=True)
    total = 0

    for i, cat in enumerate(CATEGORIES):
        print(f"\n[{i+1}/{len(CATEGORIES)}] {cat['name']} ({cat['count']} tests demandés)")

        tests = generate_tests(cat)

        if tests:
            output_path = os.path.join(TESTS_DIR, f"{cat['key']}.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(tests, f, ensure_ascii=False, indent=2)
            total += len(tests)
            print(f"  → Sauvegardé: {output_path}")
        else:
            print(f"  ⚠ Aucun test généré pour {cat['key']}")

        time.sleep(2)

    print(f"\n{'=' * 60}")
    print(f"TOTAL: {total} tests générés dans {TESTS_DIR}/")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
