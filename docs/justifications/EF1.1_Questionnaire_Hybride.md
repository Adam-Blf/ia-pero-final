# EF1.1 - Questionnaire Hybride

## Exigence RNCP
> Le questionnaire doit combiner des questions numeriques (echelle de Likert pour l'auto-declaration de niveau) et des questions ouvertes pour la collecte de preuves contextuelles.

## Implementation dans L'IA Pero

### 1. Texte Libre (Question Ouverte)
**Fichier:** `src/app.py` - Fonction `render_cocktail_input()`

```python
query = st.text_input(
    label="Votre commande",
    placeholder="Un cocktail fruite et rafraichissant...",
    label_visibility="collapsed",
    key="cocktail_query"
)
```

L'utilisateur peut decrire librement son envie de cocktail en langage naturel. Cette entree est ensuite analysee semantiquement par SBERT.

### 2. Echelle de Likert (7 Dimensions Gustatives)
**Fichier:** `src/app.py` - Fonction `render_cocktail_input()`

```python
with st.expander("Affiner mon profil gustatif", expanded=False):
    st.session_state.taste_preferences["Douceur"] = st.slider(
        "Douceur", 1, 5, st.session_state.taste_preferences.get("Douceur", 3),
        help="Niveau de sucrosite souhaite"
    )
    # ... 6 autres dimensions
```

Les 7 dimensions Likert implementees:
| Dimension | Echelle | Description |
|-----------|---------|-------------|
| Douceur | 1-5 | Niveau de sucrosite |
| Acidite | 1-5 | Fraicheur citronnee |
| Amertume | 1-5 | Complexite amere |
| Force | 1-5 | Puissance alcool |
| Fraicheur | 1-5 | Sensation rafraichissante |
| Complexite | 1-5 | Sophistication aromatique |
| Exotisme | 1-5 | Caractere tropical |

### 3. Questions Guidees (Dropdown Budget)
```python
budget = st.selectbox(
    label="Budget",
    options=[
        "Economique (< 8EUR)",
        "Modere (8-15EUR)",
        "Premium (15-25EUR)",
        "Luxe (> 25EUR)"
    ]
)
```

### 4. Bouton Surprise (Decouverte)
```python
surprise = st.button("Surprends-moi !", use_container_width=True)
```

## Preuves de Conformite

### Captures d'ecran
- Interface avec champ texte libre visible
- Expander "Affiner mon profil gustatif" avec 7 sliders
- Dropdown budget

### Tests Automatises
**Fichier:** `tests/test_scoring.py`

```python
def test_short_query_enriched(self):
    """Une requete courte doit etre enrichie avec les preferences."""
    preferences = {"Douceur": 5, "Acidite": 3, ...}
    query = "mojito"
    enriched = enrich_short_query(query, preferences)
    assert len(enriched) > len(query)
```

## Conclusion
L'exigence EF1.1 est **VALIDEE** avec:
- Texte libre semantique
- 7 sliders Likert (1-5)
- Dropdown budget structure
- Bouton decouverte aleatoire
