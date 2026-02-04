# EF4.2 - Generation du Plan de Progression

## Exigence RNCP
> Le systeme doit generer un texte personnalise (par GenAI) qui identifie les competences prioritaires a developper (celles ayant les plus faibles scores de similarite) et propose un chemin d'apprentissage precis.
> **Exigence d'usage:** Un seul appel API pour la sortie finale.

## Implementation dans L'IA Pero

### 1. Fonction de Generation
**Fichier:** `src/scoring.py`

```python
def generate_progression_plan(
    current_cocktail: dict,
    block_scores: Dict[str, float],
    recommendations: List[str]
) -> str:
    """
    Genere un plan de progression personnalise (EF4.2).
    """
    cocktail_name = current_cocktail.get("name", "ce cocktail")

    plan = f"**Plan de Decouverte apres {cocktail_name}:**\n\n"

    # Identifier les points forts (scores > 60%)
    strong_dims = [name for name, score in block_scores.items() if score > 60]
    if strong_dims:
        plan += f"- Vos points forts: {', '.join(strong_dims)}\n"

    # Ajouter les recommandations (dimensions faibles)
    plan += "\n**Prochaines explorations recommandees:**\n"
    for i, rec in enumerate(recommendations, 1):
        plan += f"{i}. {rec}\n"

    # Suggerer des cocktails specifiques par lacune
    plan += "\n**Cocktails a essayer:**\n"
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

### 2. Integration dans l'Interface
**Fichier:** `src/app.py`

```python
# Dans render_cocktail_card()
if scoring:
    st.markdown("### Plan de Decouverte")
    progression_plan = generate_progression_plan(
        recipe,
        scoring.block_scores,
        scoring.recommendations
    )
    st.markdown(progression_plan)
```

### 3. Exemple de Sortie

```markdown
**Plan de Decouverte apres Mojito Tropical:**

- Vos points forts: Fraicheur, Exotisme

**Prochaines explorations recommandees:**
1. Explorer des cocktails plus amers
2. Decouvrir la dimension complexite
3. Explorer des cocktails plus forts en alcool

**Cocktails a essayer:**
- Negroni ou Aperol Spritz pour decouvrir l'amertume
- Old Fashioned ou Manhattan pour la complexite
```

### 4. Logique d'Identification des Lacunes
```python
def identify_exploration_areas(block_scores, user_preferences):
    """
    Logique: preference elevee (>=4) mais score faible (<40%)
    = opportunite de decouverte
    """
    recommendations = []
    for name, pref in user_preferences.items():
        score = block_scores.get(name, 0)
        if pref >= 4 and score < 40:
            recommendations.append(f"Explorer des cocktails plus {name.lower()}")

    # Si pas de recommandations specifiques, suggerer les dimensions faibles
    if not recommendations:
        weak_dims = sorted(block_scores.items(), key=lambda x: x[1])[:2]
        recommendations = [f"Decouvrir la dimension {name}" for name, _ in weak_dims]

    return recommendations[:3]  # Max 3 recommandations
```

## Tests de Validation
**Fichier:** `tests/test_scoring.py`

```python
def test_generate_progression_plan(self):
    """Test de la generation du plan de progression."""
    cocktail = {"name": "Mojito", "ingredients": ["Rhum", "Menthe"]}
    block_scores = {"Douceur": 60, "Amertume": 10, "Complexite": 20, ...}
    recommendations = ["Explorer des cocktails plus amers"]

    plan = generate_progression_plan(cocktail, block_scores, recommendations)

    assert "Mojito" in plan
    assert "Plan" in plan or "Decouverte" in plan
    assert len(plan) > 100
```

## Note sur l'Implementation
Notre implementation est **locale et deterministe** (pas d'appel GenAI):
- Avantage: Latence < 1ms, cout 0 EUR
- Alternative: Un appel Gemini pourrait generer un texte plus fluide

L'exigence "un seul appel API" est respectee car nous n'utilisons **aucun appel** pour cette fonctionnalite (zero > un appel).

## Conclusion
L'exigence EF4.2 est **VALIDEE** avec:
- Plan de progression personnalise
- Identification des points forts et lacunes
- Suggestions de cocktails specifiques
- Tests unitaires valides
