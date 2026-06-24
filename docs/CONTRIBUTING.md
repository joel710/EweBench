# Contributing to ÈwéBench

[English](#english) • [Français](#français)

---

## English

Thank you for your interest in contributing to ÈwéBench! This project thrives on community input, especially from Ewe native speakers.

### Ways to Contribute

#### 1. Add New Tests
- Read [TEST_FORMAT.md](TEST_FORMAT.md) for the JSON format
- Ensure tests are culturally accurate and linguistically valid
- Native speaker validation is highly valued
- Submit a PR with new tests added to the appropriate category file

#### 2. Validate Existing Tests
- Review tests for Ewe accuracy (grammar, vocabulary, naturalness)
- Flag tests with incorrect expected keywords
- Suggest better evaluation criteria

#### 3. Submit Benchmark Results
- Run ÈwéBench on your model
- Submit the results JSON in a PR to `results/`
- Include model details (name, size, training data description)

#### 4. Improve Evaluation Methods
- The `ewe_quality` heuristic can be improved
- Propose new evaluation methods
- Contribute linguistic rules for Ewe validation

#### 5. Report Issues
- Found a bad test? Open an issue
- Scoring seems wrong? Let us know
- Documentation unclear? Submit a fix

### Guidelines

- Tests MUST be in valid JSON format
- Ewe text must be authentic (not machine-translated from French)
- Include `description` field explaining what each test evaluates
- Test IDs must follow the pattern: `category_NNN`
- One PR per category/feature (keep PRs focused)

### Pull Request Process

1. Fork the repository
2. Create a branch: `git checkout -b add-cultural-tests`
3. Make your changes
4. Test locally: `python run_benchmark.py --category <your_category> -v`
5. Submit PR with a clear description

---

## Français

Merci de votre intérêt pour contribuer à ÈwéBench ! Ce projet vit grâce aux contributions de la communauté, en particulier des locuteurs natifs Ewe.

### Comment contribuer

#### 1. Ajouter des tests
- Lire [TEST_FORMAT.md](TEST_FORMAT.md) pour le format JSON
- S'assurer que les tests sont culturellement précis et linguistiquement valides
- La validation par des locuteurs natifs est très appréciée
- Soumettre une PR avec les nouveaux tests

#### 2. Valider les tests existants
- Vérifier la précision de l'Ewe (grammaire, vocabulaire, naturel)
- Signaler les tests avec des mots-clés attendus incorrects
- Suggérer de meilleurs critères d'évaluation

#### 3. Soumettre des résultats
- Exécuter ÈwéBench sur votre modèle
- Soumettre le JSON de résultats dans une PR vers `results/`
- Inclure les détails du modèle

#### 4. Améliorer les méthodes d'évaluation
- L'heuristique `ewe_quality` peut être améliorée
- Proposer de nouvelles méthodes d'évaluation
- Contribuer des règles linguistiques pour la validation de l'Ewe

#### 5. Signaler des problèmes
- Test incorrect ? Ouvrir une issue
- Scoring semble faux ? Faites-le savoir
- Documentation peu claire ? Soumettez un fix

### Processus de Pull Request

1. Forker le repo
2. Créer une branche : `git checkout -b ajout-tests-culturels`
3. Faire vos modifications
4. Tester localement : `python run_benchmark.py --category <categorie> -v`
5. Soumettre la PR avec une description claire

---

## Code of Conduct

- Be respectful and inclusive
- Value linguistic diversity
- Credit native speakers who validate content
- No commercial use without permission (CC BY-NC 4.0)
