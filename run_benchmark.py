#!/usr/bin/env python3
"""
Runner CLI pour ÈwéBench.

Usage:
    python run_benchmark.py --endpoint URL --model MODEL_NAME [--api-key KEY] [--verbose]
    python run_benchmark.py --preset deepseek [--verbose]
    python run_benchmark.py --preset local --endpoint http://localhost:8080/v1/chat/completions
    python run_benchmark.py --compare result1.json result2.json

Presets disponibles:
    deepseek  — DeepSeek API (nécessite DEEPSEEK_API_KEY dans .env)
    gemini    — Google Gemini (nécessite GEMINI_API_KEY dans .env)
    local     — Modèle local (ollama, vllm, etc.)
    custom    — API custom (nécessite --endpoint)
"""

import sys
import os
import json
import argparse
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from ewe_bench import EweBench, RESULTS_DIR


PRESETS = {
    "deepseek": {
        "endpoint": "https://api.deepseek.com/chat/completions",
        "model": "deepseek-chat",
        "api_key_env": "DEEPSEEK_API_KEY"
    },
    "deepseek-v4": {
        "endpoint": "https://api.deepseek.com/chat/completions",
        "model": "deepseek-ai/DeepSeek-V4-0324",
        "api_key_env": "DEEPSEEK_API_KEY"
    },
    "gemini": {
        "endpoint": "https://generativelanguage.googleapis.com/v1beta/chat/completions",
        "model": "gemini-2.0-flash",
        "api_key_env": "GEMINI_API_KEY"
    },
    "local": {
        "endpoint": "http://localhost:11434/v1/chat/completions",
        "model": "local-model",
        "api_key_env": None
    }
}


def print_comparison(report_a: dict, report_b: dict):
    """Affiche une comparaison visuelle entre deux rapports."""
    print(f"\n{'='*70}")
    print(f"  ÈwéBench — Comparaison de Modèles")
    print(f"{'='*70}")
    print(f"\n  {'Catégorie':<30} {'Model A':<12} {'Model B':<12} {'Delta':<10}")
    print(f"  {'':-<30} {'':-<12} {'':-<12} {'':-<10}")

    model_a = report_a.get("model", "Model A")
    model_b = report_b.get("model", "Model B")

    print(f"  {'':30} {model_a:<12} {model_b:<12}")
    print()

    cats_a = report_a.get("categories", {})
    cats_b = report_b.get("categories", {})

    all_cats = set(list(cats_a.keys()) + list(cats_b.keys()))

    for cat in sorted(all_cats):
        score_a = cats_a.get(cat, {}).get("score", 0)
        score_b = cats_b.get(cat, {}).get("score", 0)
        delta = score_a - score_b
        indicator = "↑" if delta > 0 else "↓" if delta < 0 else "="
        cat_display = cat.replace("_", " ").title()[:28]
        print(f"  {cat_display:<30} {score_a:<12.1f} {score_b:<12.1f} {indicator} {abs(delta):.1f}")

    print(f"\n  {'─'*70}")
    score_a = report_a.get("ewe_score", 0)
    score_b = report_b.get("ewe_score", 0)
    delta = score_a - score_b
    indicator = "↑" if delta > 0 else "↓" if delta < 0 else "="
    print(f"  {'ÈwéScore GLOBAL':<30} {score_a:<12.1f} {score_b:<12.1f} {indicator} {abs(delta):.1f}")
    print(f"\n  Gagnant: {model_a if score_a > score_b else model_b} (+{abs(delta):.1f})")
    print(f"{'='*70}\n")


def print_leaderboard():
    """Affiche le leaderboard de tous les résultats existants."""
    if not RESULTS_DIR.exists():
        print("Aucun résultat trouvé.")
        return

    results = []
    for f in RESULTS_DIR.glob("ewebench_*.json"):
        with open(f, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            results.append({
                "model": data.get("model", "?"),
                "score": data.get("ewe_score", 0),
                "tests": data.get("summary", {}).get("total_tests", 0),
                "passed": data.get("summary", {}).get("total_passed", 0),
                "date": data.get("timestamp", "?")[:10],
                "file": f.name
            })

    if not results:
        print("Aucun résultat trouvé.")
        return

    results.sort(key=lambda x: x["score"], reverse=True)

    print(f"\n{'='*70}")
    print(f"  ÈwéBench — Leaderboard")
    print(f"{'='*70}")
    print(f"\n  {'#':<4} {'Modèle':<25} {'ÈwéScore':<10} {'Tests':<12} {'Date':<12}")
    print(f"  {'':-<4} {'':-<25} {'':-<10} {'':-<12} {'':-<12}")

    for i, r in enumerate(results, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f" {i}"
        pass_rate = f"{r['passed']}/{r['tests']}"
        print(f"  {medal:<4} {r['model']:<25} {r['score']:<10.1f} {pass_rate:<12} {r['date']:<12}")

    print(f"\n{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(
        description="ÈwéBench Runner — Évalue un LLM sur le benchmark Ewe",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument("--preset", choices=list(PRESETS.keys()),
                       help="Utiliser un preset de configuration")
    parser.add_argument("--endpoint", help="URL de l'API du modèle")
    parser.add_argument("--model", help="Nom du modèle")
    parser.add_argument("--api-key", help="Clé API")
    parser.add_argument("--verbose", "-v", action="store_true", help="Mode détaillé")
    parser.add_argument("--category", "-c", help="Évaluer une seule catégorie")
    parser.add_argument("--compare", nargs=2, metavar="FILE",
                       help="Comparer deux fichiers de résultats")
    parser.add_argument("--leaderboard", "-l", action="store_true",
                       help="Afficher le leaderboard")

    args = parser.parse_args()

    if args.leaderboard:
        print_leaderboard()
        return

    if args.compare:
        with open(args.compare[0], "r") as f:
            report_a = json.load(f)
        with open(args.compare[1], "r") as f:
            report_b = json.load(f)
        print_comparison(report_a, report_b)
        return

    endpoint = args.endpoint
    model = args.model
    api_key = args.api_key

    if args.preset:
        preset = PRESETS[args.preset]
        endpoint = endpoint or preset["endpoint"]
        model = model or preset["model"]
        if not api_key and preset["api_key_env"]:
            api_key = os.getenv(preset["api_key_env"])
            if not api_key:
                print(f"Erreur: {preset['api_key_env']} non trouvé dans .env")
                sys.exit(1)

    if not endpoint or not model:
        print("Erreur: --endpoint et --model requis (ou utilisez --preset)")
        parser.print_help()
        sys.exit(1)

    print(f"\n  Initialisation ÈwéBench...")
    print(f"  Endpoint: {endpoint}")
    print(f"  Modèle: {model}")
    print(f"  Catégorie: {args.category or 'TOUTES'}\n")

    bench = EweBench(endpoint, model, api_key)

    if args.category:
        result = bench.run_category(args.category, verbose=args.verbose)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        report = bench.run_full_benchmark(verbose=args.verbose)
        bench.results = report
        print(f"\n  ÈwéScore: {report['ewe_score']}/100")


if __name__ == "__main__":
    main()
