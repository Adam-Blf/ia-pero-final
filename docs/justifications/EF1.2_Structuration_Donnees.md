# EF1.2 - Structuration des Donnees

## Exigence RNCP
> Les reponses collectees doivent etre stockees dans un format structure (CSV, JSON, ou base de donnees locale) pour le traitement NLP.

## Implementation dans L'IA Pero

### 1. Dataset CSV Principal
**Fichier:** `data/cocktails.csv`

Structure du fichier CSV (600 cocktails generes):
```csv
name,description_semantique,ingredients,taste_profile,source
"Mojito Tropical","cocktail frais menthe citron vert rhum...","Rhum blanc,Menthe,...","{...}","generated"
```

**Colonnes:**
| Colonne | Type | Description |
|---------|------|-------------|
| name | string | Nom du cocktail |
| description_semantique | string | Texte riche pour embeddings SBERT |
| ingredients | string | Liste CSV des ingredients |
| taste_profile | JSON | Profil gustatif 7 dimensions |
| source | string | 'generated' ou 'kaggle' |

### 2. Dataset Kaggle Enrichi
**Fichier:** `data/kaggle_cocktails_enriched.csv`

1000+ cocktails supplementaires avec profils gustatifs calcules automatiquement.

### 3. Cache JSON pour API GenAI
**Fichier:** `data/cache.json`

```json
{
  "a1b2c3...": {
    "query": "cocktail tropical",
    "response": {...},
    "timestamp": "2026-01-15T14:30:00"
  }
}
```

### 4. Analytics JSON
**Fichier:** `data/analytics.json`

```json
[
  {
    "timestamp": "2026-01-16T14:23:45",
    "query": "tropical refreshing cocktail",
    "cocktail_name": "Caribbean Sunset",
    "duration_ms": 1523.45,
    "cached": false,
    "status": "ok"
  }
]
```

### 5. Session State (Memoire de Session)
**Fichier:** `src/app.py` - Fonction `init_session_state()`

```python
st.session_state.history = []  # 10 derniers cocktails
st.session_state.metrics = {
    "total_requests": 0,
    "cache_hits": 0,
    "total_time": 0
}
st.session_state.taste_preferences = {...}  # Likert
st.session_state.last_scoring = None  # ScoringResult
```

## Code de Chargement
**Fichier:** `src/app.py` - Fonction `load_cocktails_csv()`

```python
@st.cache_data
def load_cocktails_csv():
    datasets = []
    if COCKTAILS_CSV.exists():
        generated_df = pd.read_csv(COCKTAILS_CSV)
        generated_df['source'] = 'generated'
        datasets.append(generated_df)
    # Merge avec Kaggle...
    return pd.concat(datasets, ignore_index=True)
```

## Tests de Validation
**Fichier:** `scripts/test_integration.py`

```python
[TEST 4] Integration dans l'app...
  [OK] Dataset fusionne: 615 cocktails total
    - Generes: 600
    - Kaggle: 15
```

## Conclusion
L'exigence EF1.2 est **VALIDEE** avec:
- CSV structure pour le referentiel (600+ cocktails)
- JSON pour le cache API et analytics
- Session state pour les donnees utilisateur temps reel
- Fusion de sources multiples (generated + kaggle)
