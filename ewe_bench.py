"""
ÈwéBench   Benchmark de référence pour l'évaluation de LLMs en langue Ewe.

Catégories d'évaluation:
1. Compréhension linguistique (grammaire, vocabulaire, tonalité)
2. Génération de texte (fluence, cohérence, naturel)
3. Raisonnement logique en Ewe
4. Traduction bidirectionnelle (Français↔Ewe, Anglais↔Ewe)
5. Connaissance culturelle (proverbes, traditions, histoire)
6. Suivi d'instructions complexes
7. Conversation multi-tour
8. Capacités agentiques (function calling)
9. Adaptation stylistique
10. Robustesse et cohérence

Métriques:
- Score par catégorie (0-100)
- Score global pondéré (ÈwéScore)
- BLEU/ROUGE pour la génération
- Accuracy pour le QA
- F1 pour la classification
- Human-eval score (optionnel)
"""

import json
import os
import time
import re
from pathlib import Path
from datetime import datetime
from typing import Optional
import requests

BENCHMARK_DIR = Path(__file__).parent
TESTS_DIR = BENCHMARK_DIR / "tests"
RESULTS_DIR = BENCHMARK_DIR / "results"


class EweBench:
    """Moteur principal du benchmark ÈwéBench."""

    VERSION = "1.0.0"

    CATEGORIES = {
        "linguistic_comprehension": {
            "name": "Compréhension Linguistique",
            "weight": 0.15,
            "description": "Grammaire, vocabulaire, tons, morphologie de l'Ewe"
        },
        "text_generation": {
            "name": "Génération de Texte",
            "weight": 0.15,
            "description": "Fluence, cohérence, naturel du texte généré en Ewe"
        },
        "reasoning": {
            "name": "Raisonnement Logique",
            "weight": 0.12,
            "description": "Capacité de raisonnement exprimée en Ewe"
        },
        "translation": {
            "name": "Traduction Bidirectionnelle",
            "weight": 0.12,
            "description": "Qualité de traduction FR↔Ewe et EN↔Ewe"
        },
        "cultural_knowledge": {
            "name": "Connaissance Culturelle",
            "weight": 0.10,
            "description": "Proverbes, traditions, histoire Ewe et togolaise"
        },
        "instruction_following": {
            "name": "Suivi d'Instructions",
            "weight": 0.10,
            "description": "Respect précis d'instructions complexes"
        },
        "multi_turn": {
            "name": "Conversation Multi-Tour",
            "weight": 0.08,
            "description": "Cohérence et contexte sur plusieurs échanges"
        },
        "agentic": {
            "name": "Capacités Agentiques",
            "weight": 0.08,
            "description": "Function calling, planification, chaînage d'outils"
        },
        "style_adaptation": {
            "name": "Adaptation Stylistique",
            "weight": 0.05,
            "description": "Registres formel/informel, technique/simple"
        },
        "robustness": {
            "name": "Robustesse",
            "weight": 0.05,
            "description": "Cohérence face aux ambiguïtés, adversarial inputs"
        }
    }

    def __init__(self, model_endpoint: str, model_name: str, api_key: Optional[str] = None,
                 headers: Optional[dict] = None):
        self.model_endpoint = model_endpoint
        self.model_name = model_name
        self.api_key = api_key
        self.headers = headers or {}
        self.results = {}
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        if api_key and "Authorization" not in self.headers:
            self.headers["Authorization"] = f"Bearer {api_key}"
        if "Content-Type" not in self.headers:
            self.headers["Content-Type"] = "application/json"

    def query_model(self, messages: list, temperature: float = 0.3, max_tokens: int = 1024) -> str:
        """Envoie une requête au modèle et retourne la réponse."""
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            resp = requests.post(
                self.model_endpoint,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[ERROR] {str(e)}"

    def load_test_suite(self, category: str) -> list:
        """Charge les tests d'une catégorie depuis le fichier JSON."""
        test_file = TESTS_DIR / f"{category}.json"
        if not test_file.exists():
            return []
        with open(test_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def evaluate_exact_match(self, expected: str, response: str) -> float:
        """Score par correspondance exacte (normalisée)."""
        expected_norm = expected.strip().lower()
        response_norm = response.strip().lower()
        return 1.0 if expected_norm == response_norm else 0.0

    def evaluate_contains(self, expected_keywords: list, response: str) -> float:
        """Score par présence de mots-clés attendus."""
        response_lower = response.lower()
        found = sum(1 for kw in expected_keywords if kw.lower() in response_lower)
        return found / len(expected_keywords) if expected_keywords else 0.0

    def evaluate_multiple_choice(self, correct_answer: str, response: str) -> float:
        """Score pour les QCM (détecte la lettre de réponse)."""
        response_clean = response.strip().upper()
        correct = correct_answer.strip().upper()

        if correct in response_clean[:5]:
            return 1.0
        patterns = [
            rf'\b{correct}\b',
            rf'{correct}\)',
            rf'{correct}\.',
            rf'réponse.*{correct}',
        ]
        for p in patterns:
            if re.search(p, response_clean):
                return 1.0
        return 0.0

    def evaluate_format_compliance(self, expected_format: dict, response: str) -> float:
        """Vérifie la conformité au format demandé."""
        score = 0.0
        checks = 0

        if "contains_ewe" in expected_format:
            ewe_markers = ["ɖe", "nye", "wò", "mí", "ɛ", "ɔ", "ƒe", "kple", "dzi", "le"]
            has_ewe = any(m in response.lower() for m in ewe_markers)
            score += 1.0 if has_ewe else 0.0
            checks += 1

        if "min_length" in expected_format:
            score += 1.0 if len(response) >= expected_format["min_length"] else 0.0
            checks += 1

        if "max_length" in expected_format:
            score += 1.0 if len(response) <= expected_format["max_length"] else 0.0
            checks += 1

        if "contains_function_call" in expected_format:
            has_fc = "<function_call>" in response
            score += 1.0 if has_fc else 0.0
            checks += 1

        if "markdown_elements" in expected_format:
            md_checks = expected_format["markdown_elements"]
            md_found = 0
            if "table" in md_checks and "|" in response and "---" in response:
                md_found += 1
            if "header" in md_checks and re.search(r'^#{1,3}\s', response, re.MULTILINE):
                md_found += 1
            if "list" in md_checks and re.search(r'^[\-\*]\s', response, re.MULTILINE):
                md_found += 1
            if "bold" in md_checks and "**" in response:
                md_found += 1
            score += md_found / len(md_checks) if md_checks else 0.0
            checks += 1

        return score / checks if checks > 0 else 0.0

    def evaluate_ewe_quality(self, response: str) -> float:
        """Évalue la qualité linguistique Ewe (heuristique)."""
        if not response or response.startswith("[ERROR]"):
            return 0.0

        score = 0.0

        ewe_chars = set("ɖɛɔƒŋɣ")
        has_ewe_chars = any(c in response for c in ewe_chars)
        if has_ewe_chars:
            score += 0.3

        ewe_common = ["nye", "wò", "mí", "ɖe", "le", "kple", "dzi", "ƒe", "gbɔ",
                      "aɖe", "ame", "esia", "eya", "mele", "woɖo", "afi", "nyo"]
        words_found = sum(1 for w in ewe_common if w in response.lower())
        score += min(0.4, words_found * 0.05)

        french_words = ["le", "la", "les", "de", "du", "des", "un", "une", "est", "sont",
                       "pour", "dans", "avec", "cette", "voici"]
        french_count = sum(1 for w in french_words
                         if re.search(rf'\b{w}\b', response.lower()))
        if french_count > 5:
            score -= 0.2

        sentences = response.split('.')
        if len(sentences) > 1:
            score += 0.2

        if len(response) > 20:
            score += 0.1

        return max(0.0, min(1.0, score))

    def run_category(self, category: str, verbose: bool = False) -> dict:
        """Exécute tous les tests d'une catégorie."""
        tests = self.load_test_suite(category)
        if not tests:
            return {"score": 0.0, "total": 0, "passed": 0, "details": [], "skipped": True}

        results = []
        total_score = 0.0

        for i, test in enumerate(tests):
            if "messages" in test:
                messages = test["messages"]
            else:
                messages = [
                    {"role": "system", "content": test.get("system", "Tu es Yawo, un assistant IA qui répond en Ewe.")},
                    {"role": "user", "content": test["prompt"]}
                ]

            response = self.query_model(messages, temperature=test.get("temperature", 0.3))

            eval_method = test.get("eval_method", "keywords")

            if eval_method == "exact_match":
                score = self.evaluate_exact_match(test["expected"], response)
            elif eval_method == "multiple_choice":
                score = self.evaluate_multiple_choice(test["expected"], response)
            elif eval_method == "keywords":
                score = self.evaluate_contains(test.get("expected_keywords", []), response)
            elif eval_method == "format":
                score = self.evaluate_format_compliance(test.get("expected_format", {}), response)
            elif eval_method == "ewe_quality":
                score = self.evaluate_ewe_quality(response)
            elif eval_method == "composite":
                s1 = self.evaluate_contains(test.get("expected_keywords", []), response)
                s2 = self.evaluate_ewe_quality(response)
                s3 = self.evaluate_format_compliance(test.get("expected_format", {}), response)
                score = (s1 + s2 + s3) / 3
            else:
                score = self.evaluate_ewe_quality(response)

            total_score += score
            result_entry = {
                "test_id": test.get("id", f"{category}_{i}"),
                "score": round(score, 3),
                "response_preview": response[:200] if not verbose else response
            }
            results.append(result_entry)

            if verbose:
                status = "✓" if score >= 0.7 else "✗"
                print(f"  {status} [{i+1}/{len(tests)}] {test.get('id', f'test_{i}')}: {score:.2f}")

        avg_score = total_score / len(tests) if tests else 0.0

        return {
            "score": round(avg_score * 100, 1),
            "total": len(tests),
            "passed": sum(1 for r in results if r["score"] >= 0.7),
            "details": results,
            "skipped": False
        }

    def run_full_benchmark(self, verbose: bool = True) -> dict:
        """Exécute le benchmark complet sur toutes les catégories."""
        print(f"\n{'='*60}")
        print(f"  ÈwéBench v{self.VERSION}   Benchmark d'évaluation LLM en Ewe")
        print(f"  Modèle: {self.model_name}")
        print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")

        category_results = {}
        ewe_score_weighted = 0.0

        for cat_key, cat_info in self.CATEGORIES.items():
            print(f"\n▸ {cat_info['name']} (poids: {cat_info['weight']*100:.0f}%)")
            print(f"  {cat_info['description']}")

            result = self.run_category(cat_key, verbose=verbose)
            category_results[cat_key] = result

            if result["skipped"]:
                print(f"  ⚠ Aucun test trouvé   catégorie ignorée")
            else:
                weighted = result["score"] * cat_info["weight"]
                ewe_score_weighted += weighted
                print(f"  Score: {result['score']:.1f}/100 ({result['passed']}/{result['total']} tests réussis)")

        active_weight = sum(
            info["weight"] for key, info in self.CATEGORIES.items()
            if not category_results.get(key, {}).get("skipped", True)
        )
        if active_weight > 0:
            ewe_score = ewe_score_weighted / active_weight
        else:
            ewe_score = 0.0

        final_report = {
            "benchmark": "ÈwéBench",
            "version": self.VERSION,
            "run_id": self.run_id,
            "model": self.model_name,
            "endpoint": self.model_endpoint,
            "timestamp": datetime.now().isoformat(),
            "ewe_score": round(ewe_score, 1),
            "categories": category_results,
            "summary": {
                "total_tests": sum(r["total"] for r in category_results.values()),
                "total_passed": sum(r["passed"] for r in category_results.values()),
                "categories_evaluated": sum(1 for r in category_results.values() if not r.get("skipped")),
                "categories_skipped": sum(1 for r in category_results.values() if r.get("skipped")),
            }
        }

        print(f"\n{'='*60}")
        print(f"  ÈwéScore Global: {ewe_score:.1f}/100")
        print(f"  Tests: {final_report['summary']['total_passed']}/{final_report['summary']['total_tests']} réussis")
        print(f"  Catégories évaluées: {final_report['summary']['categories_evaluated']}/10")
        print(f"{'='*60}\n")

        self._save_results(final_report)
        return final_report

    def _save_results(self, report: dict):
        """Sauvegarde les résultats du benchmark."""
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        filename = f"ewebench_{self.model_name}_{self.run_id}.json"
        filepath = RESULTS_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"  Résultats sauvegardés: {filepath}")

    def compare_models(self, other_report_path: str) -> dict:
        """Compare les résultats avec un autre modèle."""
        with open(other_report_path, "r", encoding="utf-8") as f:
            other = json.load(f)

        comparison = {
            "model_a": self.model_name,
            "model_b": other["model"],
            "score_a": self.results.get("ewe_score", 0),
            "score_b": other["ewe_score"],
            "categories": {}
        }

        for cat_key in self.CATEGORIES:
            a_score = self.results.get("categories", {}).get(cat_key, {}).get("score", 0)
            b_score = other.get("categories", {}).get(cat_key, {}).get("score", 0)
            comparison["categories"][cat_key] = {
                "model_a": a_score,
                "model_b": b_score,
                "delta": round(a_score - b_score, 1)
            }

        return comparison


def run_quick_eval(endpoint: str, model: str, api_key: str = None):
    """Lance une évaluation rapide (subset de tests)."""
    bench = EweBench(endpoint, model, api_key)
    return bench.run_full_benchmark(verbose=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ÈwéBench   Benchmark LLM pour l'Ewe")
    parser.add_argument("--endpoint", required=True, help="URL de l'API du modèle")
    parser.add_argument("--model", required=True, help="Nom du modèle")
    parser.add_argument("--api-key", help="Clé API (optionnel)")
    parser.add_argument("--verbose", action="store_true", help="Affichage détaillé")
    parser.add_argument("--category", help="Évaluer une seule catégorie")

    args = parser.parse_args()

    bench = EweBench(args.endpoint, args.model, args.api_key)

    if args.category:
        result = bench.run_category(args.category, verbose=args.verbose)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        bench.run_full_benchmark(verbose=args.verbose)
