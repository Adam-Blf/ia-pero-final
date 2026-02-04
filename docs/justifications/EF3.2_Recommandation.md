# EF3.2 - Systeme de Recommandation

## Exigence RNCP
> Le systeme doit proposer les 3 profils de postes pour lesquels l'utilisateur obtient le score de couverture le plus eleve.

## Adaptation L'IA Pero
Dans notre contexte cocktails, les "profils de postes" sont remplaces par:
- **Cocktails recommandes** (Top-N par similarite)
- **Dimensions a explorer** (zones de decouverte)
- **Types de cocktails suggeres** (basees sur les lacunes)

## Implementation

### 1. Top-N Cocktails par Similarite
**Fichier:** `src/app.py`

```python
def search_cocktails_sbert(query: str, top_k: int = 5):
    """Retourne les N cocktails les plus similaires."""
    similarities = util.cos_sim(query_embedding, desc_embeddings)
    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    for idx in top_indices:
        if similarities[idx] > 0.2:
            results.append({
                "name": df.iloc[idx]["name"],
                "similarity": round(similarities[idx] * 100, 1)
            })
    return results
```

### 2. Identification des Zones a Explorer
**Fichier:** `src/scoring.py`

```python
def identify_exploration_areas(block_scores, user_preferences):
    """
    Identifie les dimensions a explorer.
    Logique: preference elevee mais score faible = opportunite.
    """
    recommendations = []
    for name, pref in user_preferences.items():
        score = block_scores.get(name, 0)
        # Preference >= 4 mais score < 40% = a explorer
        if pref >= 4 and score < 40:
            recommendations.append(f"Explorer des cocktails plus {name.lower()}")

    return recommendations[:3]  # Max 3 recommandations
```

### 3. Suggestions de Cocktails par Lacune
**Fichier:** `src/scoring.py`

```python
def generate_progression_plan(current_cocktail, block_scores, recommendations):
    """Suggere des cocktails specifiques par dimension faible."""
    plan = "**Cocktails a essayer:**\n"

    weak_scores = sorted(block_scores.items(), key=lambda x: x[1])[:2]
    for dim, score in weak_scores:
        if dim == "Amertume" and score < 30:
            plan += "- Negroni ou Aperol Spritz pour decouvrir l'amertume\n"
        elif dim == "Exotisme" and score < 30:
            plan += "- Mai Tai ou Pina Colada pour le cote tropical\n"
        elif dim == "Fraicheur" and score < 30:
            plan += "- Mojito ou Moscow Mule pour la fraicheur\n"
        elif dim == "Complexite" and score < 30:
            plan += "- Old Fashioned ou Manhattan pour la complexite\n"

    return plan
```

### 4. Affichage des 3 Recommandations
**Fichier:** `src/app.py`

```python
# Dans render_cocktail_card()
st.markdown("### Plan de Decouverte")
progression_plan = generate_progression_plan(
    recipe,
    scoring.block_scores,
    scoring.recommendations  # Liste de 3 max
)
st.markdown(progression_plan)
```

## Exemple de Sortie

```
**Plan de Decouverte apres Mojito:**

- Vos points forts: Fraicheur, Acidite

**Prochaines explorations recommandees:**
1. Explorer des cocktails plus amers
2. Decouvrir la dimension complexite
3. Explorer des cocktails plus forts

**Cocktails a essayer:**
- Negroni ou Aperol Spritz pour decouvrir l'amertume
- Old Fashioned ou Manhattan pour la complexite
```

## Tests de Validation
**Fichier:** `tests/test_scoring.py`

```python
def test_identify_exploration_areas(self):
    """Test des recommandations basees sur les ecarts pref/score."""
    block_scores = {"Douceur": 70, "Acidite": 20, "Exotisme": 10, ...}
    user_prefs = {"Douceur": 3, "Acidite": 5, "Exotisme": 5, ...}

    recommendations = identify_exploration_areas(block_scores, user_prefs)

    assert len(recommendations) <= 3
    assert len(recommendations) >= 1
```

## Conclusion
L'exigence EF3.2 est **VALIDEE** avec:
- Top-5 cocktails par similarite semantique
- 3 dimensions a explorer (max)
- Suggestions de cocktails specifiques par lacune
- Integration dans le plan de progression
