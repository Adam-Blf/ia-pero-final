# EF2.1 - Referentiel de Competences

## Exigence RNCP
> Vous devez creer un referentiel des blocs de competences et des profils de postes associes, inspire de standards.

## Implementation dans L'IA Pero

### Adaptation au Domaine Cocktails
Dans notre contexte de recommandation de cocktails, les "blocs de competences" sont transposes en **dimensions gustatives** (taste dimensions).

### 1. Referentiel des Blocs (TASTE_BLOCKS)
**Fichier:** `src/scoring.py`

```python
TASTE_BLOCKS = {
    "Douceur": {
        "keywords": ["sucre", "doux", "sweet", "sirop", "miel", "caramel", "vanille", "fruit"],
        "weight": 1.0,
        "description": "Niveau de sucrosite et douceur du cocktail"
    },
    "Acidite": {
        "keywords": ["acide", "citron", "lime", "agrume", "tart", "sour", "acidule", "pamplemousse"],
        "weight": 1.0,
        "description": "Niveau d'acidite et de fraicheur citronnee"
    },
    "Amertume": {
        "keywords": ["amer", "bitter", "campari", "angostura", "gentiane", "fernet", "aperol"],
        "weight": 1.0,
        "description": "Niveau d'amertume et de complexite"
    },
    "Force": {
        "keywords": ["fort", "strong", "alcool", "spirit", "puissant", "intense", "whisky", "rhum"],
        "weight": 1.2,  # Poids plus eleve car critere important
        "description": "Teneur en alcool et puissance du cocktail"
    },
    "Fraicheur": {
        "keywords": ["frais", "fresh", "menthe", "concombre", "glace", "rafraichissant", "ete", "cool"],
        "weight": 1.0,
        "description": "Sensation de fraicheur et de legerete"
    },
    "Complexite": {
        "keywords": ["complexe", "elabore", "layers", "nuance", "subtil", "sophistique", "expert"],
        "weight": 0.8,
        "description": "Complexite aromatique et technique de preparation"
    },
    "Exotisme": {
        "keywords": ["tropical", "exotique", "coco", "ananas", "passion", "mangue", "rhum", "tiki"],
        "weight": 0.8,
        "description": "Caractere tropical et depaysant"
    }
}
```

### 2. Structure du Referentiel

| Bloc | Keywords | Poids | Equivalent AISCA |
|------|----------|-------|------------------|
| Douceur | sucre, doux, sweet... | 1.0 | Data Analysis |
| Acidite | citron, lime, agrume... | 1.0 | Machine Learning |
| Amertume | amer, bitter, campari... | 1.0 | NLP |
| Force | fort, alcool, whisky... | 1.2 | Project Management |
| Fraicheur | frais, menthe, glace... | 1.0 | Communication |
| Complexite | elabore, nuance... | 0.8 | Leadership |
| Exotisme | tropical, coco, tiki... | 0.8 | Innovation |

### 3. Profils Types (Equivalents Metiers)
**Fichier:** `src/scoring.py` - Fonction `generate_taste_bio()`

```python
# Classification des profils gustatifs
if prefs["Douceur"] >= 4 and prefs["Force"] <= 2:
    palate_type = "Amateur de douceur"
elif prefs["Amertume"] >= 4 and prefs["Force"] >= 4:
    palate_type = "Connaisseur averti"
elif prefs["Fraicheur"] >= 4 and prefs["Acidite"] >= 4:
    palate_type = "Esprit frais"
elif prefs["Exotisme"] >= 4:
    palate_type = "Explorateur tropical"
else:
    palate_type = "Eclectique equilibre"
```

### 4. Dataset de Reference
**Fichier:** `data/cocktails.csv`

615 cocktails avec descriptions semantiques riches pour le matching.

## Tests de Validation
**Fichier:** `tests/test_scoring.py`

```python
def test_taste_blocks_structure(self):
    """Verifie que les blocs ont la structure attendue."""
    assert len(TASTE_BLOCKS) == 7
    for block_name, block_config in TASTE_BLOCKS.items():
        assert "keywords" in block_config
        assert len(block_config["keywords"]) >= 5
```

## Conclusion
L'exigence EF2.1 est **VALIDEE** avec:
- 7 blocs de competences gustatives definis
- Keywords semantiques par bloc (5-8 termes)
- Poids configurables par dimension
- Profils types mappes a des descriptions
- 615 cocktails dans le referentiel
