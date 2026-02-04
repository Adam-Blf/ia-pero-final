# Guide du Projet - L'IA Pero

## Structure du Projet

```
ia-pero/
├── src/                    # Code source principal
├── scripts/                # Scripts utilitaires
├── tests/                  # Tests automatises
├── data/                   # Donnees cocktails
├── assets/                 # Images et logos
├── .streamlit/             # Configuration Streamlit
└── docs/                   # Documentation
```

---

## Code Source (src/)

| Fichier | Description |
|---------|-------------|
| `src/app.py` | Application Streamlit principale (interface utilisateur) |
| `src/backend.py` | Logique metier: generation IA, guardrail, cache |
| `src/embeddings.py` | Gestion des embeddings SBERT |
| `src/generate_data.py` | Generation du dataset de cocktails |
| `src/ingredient_profiler.py` | Profilage des ingredients |
| `src/kaggle_integration.py` | Integration des donnees Kaggle |
| `src/utils.py` | Fonctions utilitaires |

---

## Scripts Utilitaires (scripts/)

| Fichier | Description |
|---------|-------------|
| `scripts/download_kaggle.py` | Telecharge les donnees Kaggle |
| `scripts/enrich_kaggle.py` | Enrichit les cocktails Kaggle |
| `scripts/export_known_ingredients.py` | Exporte la liste des ingredients |
| `scripts/test_integration.py` | Test d'integration complet |

---

## Tests (tests/)

| Fichier | Description |
|---------|-------------|
| `tests/test_guardrail.py` | Tests E2E Playwright (guardrail, generation) |
| `tests/conftest.py` | Configuration pytest et fixtures |

---

## Donnees (data/)

| Fichier | Description |
|---------|-------------|
| `data/cocktails.csv` | 600 cocktails generes par IA |
| `data/kaggle_cocktails_enriched.csv` | Cocktails Kaggle enrichis |
| `data/kaggle_raw.csv` | Donnees Kaggle brutes |

---

## Documentation

| Fichier | Description |
|---------|-------------|
| `README.md` | Presentation du projet et installation |
| `RAPPORT_FINAL.md` | Rapport complet du projet (source) |
| `ARCHITECTURE.md` | Architecture technique detaillee |
| `QUICK_START.md` | Guide de demarrage rapide |
| `KAGGLE_INTEGRATION.md` | Documentation integration Kaggle |
| `RESUME_IMPLEMENTATION.md` | Resume de l'implementation |
| `SOUTENANCE_SLIDES.md` | Slides de presentation |

---

## Livrables PDF

| Fichier | Description |
|---------|-------------|
| `L'IA Pero - Rapport Projet IA Generative - Adam Beloucif & Amina Medjdoub.pdf` | Rapport final |
| `L'IA Pero - Lien GitHub - Adam Beloucif & Amina Medjdoub.pdf` | Lien depot GitHub |
| `SOUTENANCE_SLIDES.pdf` | Slides de soutenance |

---

## Configuration

| Fichier | Description |
|---------|-------------|
| `.env` | Cle API Google Gemini (ne pas commiter) |
| `.env.example` | Template pour le fichier .env |
| `.streamlit/config.toml` | Configuration theme Streamlit |
| `requirements.txt` | Dependances Python |
| `.gitignore` | Fichiers ignores par Git |

---

## Lancer le Projet

```bash
# 1. Installer les dependances
pip install -r requirements.txt

# 2. Configurer la cle API
cp .env.example .env
# Editer .env avec votre cle Google Gemini

# 3. Lancer l'application
streamlit run src/app.py
```

---

## Lancer les Tests

```bash
# Tests E2E avec Playwright
pytest tests/test_guardrail.py -v
```

---

## Points Cles

- **Guardrail**: Seuil de pertinence a 0.30 (`src/backend.py` ligne ~45)
- **Cache LRU**: 100 recettes en memoire (`src/backend.py`)
- **SBERT**: Modele `all-MiniLM-L6-v2` pour la recherche semantique
- **API Gemini**: Modeles `gemini-2.5-flash-lite` et `gemini-2.0-flash`

---

Cree par Adam Beloucif & Amina Medjdoub
RNCP Bloc 2 - Expert en Ingenierie de Donnees
