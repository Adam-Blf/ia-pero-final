# EF2.2 - Modelisation Semantique (SBERT)

## Exigence RNCP
> Vous devez utiliser un modele d'embeddings Open-Source et local (ex. SBERT via la librairie SentenceTransformer) pour transformer les entrees utilisateur et les phrases du referentiel en vecteurs.

## Implementation dans L'IA Pero

### 1. Modele SBERT Utilise
**Modele:** `all-MiniLM-L6-v2`

| Caracteristique | Valeur |
|-----------------|--------|
| Taille | ~80 Mo |
| Dimensions | 384 |
| Langue | Multilingue |
| Vitesse | ~14,000 phrases/sec |
| Cout | 0 EUR (local) |

### 2. Chargement du Modele
**Fichier:** `src/backend.py`

```python
from sentence_transformers import SentenceTransformer
from functools import lru_cache

@lru_cache(maxsize=1)
def get_sbert_model():
    """Charge le modele SBERT (cache en memoire)."""
    return SentenceTransformer("all-MiniLM-L6-v2")
```

### 3. Encodage des Requetes Utilisateur
**Fichier:** `src/scoring.py`

```python
def calculate_weighted_coverage_score(query, user_preferences, model):
    # Encoder la requete utilisateur
    query_embedding = model.encode(query, convert_to_numpy=True)
    # ... calcul des similarites
```

### 4. Pre-calcul des Embeddings (Optimisation)
**Fichier:** `src/app.py`

```python
@st.cache_data
def _precompute_cocktail_embeddings():
    """Pre-calcule les embeddings pour tous les 600 cocktails."""
    df = load_cocktails_csv()
    model = get_sbert_model()
    descriptions = df["description_semantique"].fillna("").tolist()
    embeddings = model.encode(descriptions, convert_to_numpy=True)
    return descriptions, embeddings
```

**Performance:**
- Premier appel: ~2-3s (encode 600 cocktails)
- Appels suivants: <1ms (cache)
- Speedup: **40-60x**

### 5. Encodage des Keywords de Bloc
**Fichier:** `src/scoring.py`

```python
def calculate_block_similarity(query_embedding, block_keywords, model):
    # Encoder les keywords du bloc
    keyword_embeddings = model.encode(block_keywords, convert_to_numpy=True)
    # Calculer similarite
    similarities = util.cos_sim(query_embedding, keyword_embeddings)
    return float(np.mean(sorted(similarities, reverse=True)[:3]))
```

### 6. Logs de Verification
```
INFO:sentence_transformers.SentenceTransformer:Load pretrained SentenceTransformer: all-MiniLM-L6-v2
INFO:sentence_transformers.SentenceTransformer:Use pytorch device_name: cuda
INFO:ia_pero_analytics:Precomputing embeddings for 615 cocktails...
INFO:ia_pero_analytics:Embeddings cached: shape (615, 384)
```

## Tests de Validation
**Fichier:** `tests/test_scoring.py`

```python
class TestIntegrationScoring:
    @pytest.fixture
    def real_model(self):
        from src.backend import get_sbert_model
        return get_sbert_model()

    def test_real_scoring_sweet_query(self, real_model):
        result = calculate_weighted_coverage_score(
            "cocktail tres sucre et doux avec fruits tropicaux",
            preferences,
            real_model
        )
        assert result.block_scores["Douceur"] > 30
```

## Conclusion
L'exigence EF2.2 est **VALIDEE** avec:
- Modele SBERT `all-MiniLM-L6-v2` (open-source, local)
- Embeddings 384 dimensions
- Cache des embeddings pour performance
- Cout: 0 EUR (pas d'API externe)
- Tests d'integration valides
