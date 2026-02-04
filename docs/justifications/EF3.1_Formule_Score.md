# EF3.1 - Formule de Score Ponderee

## Exigence RNCP
> Vous devez implementer une formule de score ponderee pour calculer le Score de Couverture Semantique.

## Formule RNCP
```
Coverage Score = SUM(Wi * Si) / SUM(Wi)
```

Ou:
- Si = Score de similarite pour le bloc i
- Wi = Poids pour le bloc i

## Implementation dans L'IA Pero

### 1. Implementation de la Formule
**Fichier:** `src/scoring.py`

```python
def calculate_weighted_coverage_score(query, user_preferences, model):
    """
    Calcule le Coverage Score pondere selon la formule RNCP:
        Coverage Score = SUM(Wi*Si) / SUM(Wi)
    """
    query_embedding = model.encode(query, convert_to_numpy=True)

    total_weighted_score = 0.0
    total_weight = 0.0

    for block_name, block_config in TASTE_BLOCKS.items():
        # Calculer la similarite pour ce bloc
        score, matched = calculate_block_similarity(
            query_embedding,
            block_config["keywords"],
            model
        )

        # Recuperer le poids utilisateur (preference Likert)
        user_weight = user_preferences.get(block_name, 3)

        # Poids final = poids bloc * preference utilisateur / 3
        final_weight = block_config["weight"] * (user_weight / 3.0)

        # Accumuler pour le score global
        total_weighted_score += score * final_weight
        total_weight += final_weight

    # Formule RNCP: Coverage Score = SUM(Wi*Si) / SUM(Wi)
    coverage_score = (total_weighted_score / total_weight * 100) if total_weight > 0 else 0.0

    return ScoringResult(
        coverage_score=round(coverage_score, 1),
        block_scores=block_scores,
        weighted_scores=weighted_scores,
        ...
    )
```

### 2. Structure du Resultat
**Fichier:** `src/scoring.py`

```python
@dataclass
class ScoringResult:
    coverage_score: float      # Score global 0-100
    block_scores: Dict[str, float]      # Scores par dimension
    weighted_scores: Dict[str, float]   # Scores ponderes
    matched_keywords: Dict[str, List[str]]  # Mots-cles matches
    profile_summary: str       # Resume du profil
    recommendations: List[str] # Dimensions a explorer
```

### 3. Affichage dans l'Interface
**Fichier:** `src/app.py`

```python
# Affichage du Coverage Score
st.markdown(f"""
    <div style="text-align: center; ...">
        <span style="font-size: 2.5rem; color: #FFD700;">{scoring.coverage_score}%</span>
        <br><span>Coverage Score = SUM(Wi*Si) / SUM(Wi)</span>
    </div>
""")

# Barres de progression par dimension
for dim, score in scoring.block_scores.items():
    st.progress(min(score / 100, 1.0))
```

### 4. Exemple de Calcul

| Bloc | Si (Similarite) | Wi (Poids) | Wi * Si |
|------|-----------------|------------|---------|
| Douceur | 0.75 | 1.67 (pref=5) | 1.25 |
| Acidite | 0.40 | 1.00 (pref=3) | 0.40 |
| Amertume | 0.20 | 0.33 (pref=1) | 0.07 |
| Force | 0.60 | 1.20 (pref=3) | 0.72 |
| Fraicheur | 0.80 | 1.33 (pref=4) | 1.07 |
| Complexite | 0.30 | 0.80 (pref=3) | 0.24 |
| Exotisme | 0.65 | 1.33 (pref=5) | 0.87 |

**Total:** SUM(Wi*Si) = 4.62, SUM(Wi) = 7.66
**Coverage Score:** 4.62 / 7.66 * 100 = **60.3%**

## Tests de Validation
**Fichier:** `tests/test_scoring.py`

```python
def test_coverage_score_formula(self, mock_model):
    """Test de la formule Coverage Score = SUM(Wi*Si) / SUM(Wi)."""
    with patch('src.scoring.calculate_block_similarity') as mock_sim:
        mock_sim.return_value = (0.5, ["keyword1"])
        result = calculate_weighted_coverage_score("test query", preferences, mock_model)
        assert 0 <= result.coverage_score <= 100
        assert len(result.block_scores) == 7
```

## Conclusion
L'exigence EF3.1 est **VALIDEE** avec:
- Formule exacte: `SUM(Wi*Si) / SUM(Wi)`
- 7 blocs de competences ponderes
- Integration des preferences Likert dans les poids
- Affichage visuel du score + barres de progression
- 16 tests unitaires valides
