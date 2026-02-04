# Justifications RNCP - L'IA Pero

## Resume du Projet
**L'IA Pero** - Agent Intelligent Semantique et Generatif pour la Recommandation de Cocktails

**Auteurs:** Adam BELOUCIF & Amina MEDJDOUB
**Formation:** Mastere Data Engineering et IA - EFREI Paris
**Tutrice:** Sarah MALAEB
**Annee:** 2025-2026

---

## Tableau de Conformite RNCP

| Exigence | Description | Statut | Fichier |
|----------|-------------|--------|---------|
| **EF1.1** | Questionnaire Hybride (Likert + texte) | VALIDE | [EF1.1_Questionnaire_Hybride.md](EF1.1_Questionnaire_Hybride.md) |
| **EF1.2** | Structuration des donnees (CSV/JSON) | VALIDE | [EF1.2_Structuration_Donnees.md](EF1.2_Structuration_Donnees.md) |
| **EF2.1** | Referentiel de competences | VALIDE | [EF2.1_Referentiel_Competences.md](EF2.1_Referentiel_Competences.md) |
| **EF2.2** | Modelisation semantique (SBERT) | VALIDE | [EF2.2_Modelisation_Semantique.md](EF2.2_Modelisation_Semantique.md) |
| **EF2.3** | Mesure de similarite (Cosinus) | VALIDE | [EF2.3_Mesure_Similarite.md](EF2.3_Mesure_Similarite.md) |
| **EF3.1** | Formule de score ponderee | VALIDE | [EF3.1_Formule_Score.md](EF3.1_Formule_Score.md) |
| **EF3.2** | Systeme de recommandation | VALIDE | [EF3.2_Recommandation.md](EF3.2_Recommandation.md) |
| **EF4.1** | Enrichissement requetes courtes | VALIDE | [EF4.1_Enrichissement_Requetes.md](EF4.1_Enrichissement_Requetes.md) |
| **EF4.2** | Plan de progression | VALIDE | [EF4.2_Plan_Progression.md](EF4.2_Plan_Progression.md) |
| **EF4.3** | Synthese de profil (Bio) | VALIDE | [EF4.3_Synthese_Profil.md](EF4.3_Synthese_Profil.md) |

---

## Tests Automatises

| Suite | Tests | Statut |
|-------|-------|--------|
| test_guardrail.py | 3 tests Playwright E2E | 3/3 PASSED |
| test_scoring.py | 16 tests unitaires | 16/16 PASSED |
| test_integration.py | 5 tests Kaggle | 5/5 PASSED |
| **TOTAL** | **24 tests** | **24/24 PASSED** |

---

## Architecture Technique

```
ia-pero/
├── src/
│   ├── app.py              # Interface Streamlit (EF1.1, EF3.2)
│   ├── backend.py          # Moteur SBERT + GenAI (EF2.2, EF2.3)
│   ├── scoring.py          # Module scoring RNCP (EF3.1, EF4.x)
│   └── ...
├── data/
│   ├── cocktails.csv       # 600 cocktails (EF1.2, EF2.1)
│   ├── kaggle_cocktails_enriched.csv
│   ├── cache.json          # Cache API
│   └── analytics.json      # Logs
├── tests/
│   ├── test_guardrail.py   # Tests E2E
│   ├── test_scoring.py     # Tests unitaires
│   └── conftest.py
├── docs/
│   └── justifications/     # Ce dossier
└── ...
```

---

## Formule de Scoring RNCP

```
Coverage Score = SUM(Wi * Si) / SUM(Wi)
```

- **Si** = Score de similarite semantique pour le bloc i (0-1)
- **Wi** = Poids du bloc i (preference Likert / 3 * poids base)

### Blocs de Competences (7 dimensions)

| Bloc | Poids Base | Keywords |
|------|------------|----------|
| Douceur | 1.0 | sucre, doux, sweet, sirop... |
| Acidite | 1.0 | citron, lime, agrume, sour... |
| Amertume | 1.0 | amer, bitter, campari... |
| Force | 1.2 | fort, alcool, whisky, rhum... |
| Fraicheur | 1.0 | frais, menthe, glace... |
| Complexite | 0.8 | elabore, nuance, sophistique... |
| Exotisme | 0.8 | tropical, coco, ananas, tiki... |

---

## Stack Technique

| Composant | Technologie |
|-----------|-------------|
| Frontend | Streamlit |
| NLP | Sentence-Transformers (SBERT) |
| Modele | all-MiniLM-L6-v2 (384 dim) |
| GenAI | Google Gemini API |
| Visualisation | Plotly (Radar Chart) |
| Tests | Pytest + Playwright |
| Data | Pandas, NumPy |

---

## Execution des Tests

```bash
# Tous les tests
python -m pytest tests/ -v

# Tests specifiques
python -m pytest tests/test_scoring.py -v
python -m pytest tests/test_guardrail.py -v

# Tests d'integration
python scripts/test_integration.py
```

---

## Lancement de l'Application

```bash
streamlit run src/app.py
# URL: http://localhost:8501
```

---

*Document genere automatiquement - L'IA Pero v2.0*
