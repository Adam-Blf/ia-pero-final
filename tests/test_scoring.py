"""
Tests pour le module de Scoring Pondere RNCP
=============================================

Ce module teste les fonctionnalites EF1.1, EF3.1, EF4.1-4.3 du cahier des charges.

Auteurs: Adam Beloucif & Amina Medjdoub
Projet: RNCP Bloc 2 - Expert en Ingenierie de Donnees
"""

import pytest
import numpy as np
from unittest.mock import MagicMock, patch

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scoring import (
    TASTE_BLOCKS,
    DEFAULT_USER_WEIGHTS,
    ScoringResult,
    calculate_block_similarity,
    calculate_weighted_coverage_score,
    generate_profile_summary,
    identify_exploration_areas,
    enrich_short_query,
    generate_progression_plan,
    generate_taste_bio
)


class TestTasteBlocks:
    """Tests pour la configuration des blocs de competences."""

    def test_taste_blocks_structure(self):
        """Verifie que les blocs ont la structure attendue."""
        assert len(TASTE_BLOCKS) == 7, "Doit avoir 7 dimensions gustatives"

        required_keys = ["keywords", "weight", "description"]
        for block_name, block_config in TASTE_BLOCKS.items():
            for key in required_keys:
                assert key in block_config, f"Bloc {block_name} manque la cle {key}"
            assert len(block_config["keywords"]) >= 5, f"Bloc {block_name} doit avoir >= 5 keywords"
            assert 0.5 <= block_config["weight"] <= 1.5, f"Poids {block_name} hors limites"

    def test_default_weights(self):
        """Verifie les poids par defaut (Likert 3)."""
        assert len(DEFAULT_USER_WEIGHTS) == 7
        for dim, weight in DEFAULT_USER_WEIGHTS.items():
            assert weight == 3, f"Poids par defaut de {dim} doit etre 3"
            assert dim in TASTE_BLOCKS, f"Dimension {dim} doit exister dans TASTE_BLOCKS"


class TestEnrichShortQuery:
    """Tests pour l'enrichissement des requetes courtes (EF4.1)."""

    def test_short_query_enriched(self):
        """Une requete courte doit etre enrichie avec les preferences."""
        preferences = {
            "Douceur": 5,  # Preference forte
            "Acidite": 3,
            "Amertume": 1,  # Preference faible
            "Force": 2,  # Preference faible
            "Fraicheur": 4,
            "Complexite": 3,
            "Exotisme": 3
        }
        query = "mojito"
        enriched = enrich_short_query(query, preferences)

        assert len(enriched) > len(query), "La requete doit etre enrichie"
        assert "mojito" in enriched, "La requete originale doit etre preservee"
        # Preferences fortes ajoutees
        assert "doux" in enriched.lower() or "sucre" in enriched.lower()
        # Preferences faibles evitees
        assert "amer" in enriched.lower() or "leger" in enriched.lower()

    def test_long_query_not_enriched(self):
        """Une requete de 5+ mots ne doit pas etre enrichie."""
        preferences = {"Douceur": 5, "Acidite": 3, "Amertume": 3, "Force": 3, "Fraicheur": 3, "Complexite": 3, "Exotisme": 3}
        query = "un cocktail tropical fruite et rafraichissant"
        enriched = enrich_short_query(query, preferences)

        assert enriched == query, "Requete longue ne doit pas etre modifiee"

    def test_neutral_preferences_no_enrichment(self):
        """Des preferences neutres (3) ne doivent pas enrichir."""
        preferences = {dim: 3 for dim in DEFAULT_USER_WEIGHTS}
        query = "negroni"
        enriched = enrich_short_query(query, preferences)

        assert enriched == query, "Preferences neutres = pas d'enrichissement"


class TestProfileGeneration:
    """Tests pour la generation de profil (EF4.3)."""

    def test_generate_profile_summary_dominant(self):
        """Test du resume avec dimensions dominantes."""
        block_scores = {"Douceur": 75, "Acidite": 30, "Amertume": 20, "Force": 40, "Fraicheur": 80, "Complexite": 25, "Exotisme": 50}
        user_prefs = {"Douceur": 4, "Acidite": 3, "Amertume": 2, "Force": 3, "Fraicheur": 5, "Complexite": 3, "Exotisme": 3}

        summary = generate_profile_summary(block_scores, user_prefs)

        assert "Douceur" in summary or "Fraicheur" in summary, "Dimensions dominantes mentionnees"
        assert len(summary) > 20, "Le resume ne doit pas etre vide"

    def test_generate_profile_summary_balanced(self):
        """Test du resume avec profil equilibre."""
        block_scores = {dim: 40 for dim in TASTE_BLOCKS}
        user_prefs = {dim: 3 for dim in TASTE_BLOCKS}

        summary = generate_profile_summary(block_scores, user_prefs)

        assert "equilibre" in summary.lower() or "varie" in summary.lower()


class TestExplorationAreas:
    """Tests pour l'identification des zones a explorer."""

    def test_identify_exploration_areas(self):
        """Test des recommandations basees sur les ecarts pref/score."""
        block_scores = {"Douceur": 70, "Acidite": 20, "Amertume": 15, "Force": 50, "Fraicheur": 30, "Complexite": 25, "Exotisme": 10}
        user_prefs = {"Douceur": 3, "Acidite": 5, "Amertume": 4, "Force": 3, "Fraicheur": 3, "Complexite": 3, "Exotisme": 5}

        recommendations = identify_exploration_areas(block_scores, user_prefs)

        assert len(recommendations) <= 3, "Max 3 recommandations"
        assert len(recommendations) >= 1, "Au moins 1 recommandation"
        # Acidite (pref 5, score 20) et Exotisme (pref 5, score 10) doivent etre recommandes
        recs_lower = " ".join(recommendations).lower()
        assert "acidite" in recs_lower or "exotisme" in recs_lower or "amertume" in recs_lower


class TestProgressionPlan:
    """Tests pour le plan de progression (EF4.2)."""

    def test_generate_progression_plan(self):
        """Test de la generation du plan de progression."""
        cocktail = {"name": "Mojito", "ingredients": ["Rhum", "Menthe", "Citron vert"]}
        block_scores = {"Douceur": 60, "Acidite": 70, "Amertume": 10, "Force": 40, "Fraicheur": 80, "Complexite": 20, "Exotisme": 50}
        recommendations = ["Explorer des cocktails plus amers", "Decouvrir la complexite"]

        plan = generate_progression_plan(cocktail, block_scores, recommendations)

        assert "Mojito" in plan, "Le nom du cocktail doit apparaitre"
        assert "Plan" in plan or "Decouverte" in plan, "Titre du plan present"
        assert len(plan) > 100, "Le plan doit etre detaille"


class TestTasteBio:
    """Tests pour la bio gustative (EF4.3)."""

    def test_generate_taste_bio_sweet_lover(self):
        """Test bio pour amateur de douceur."""
        prefs = {"Douceur": 5, "Acidite": 3, "Amertume": 2, "Force": 1, "Fraicheur": 3, "Complexite": 3, "Exotisme": 3}
        scores = {"Douceur": 80, "Acidite": 40, "Amertume": 20, "Force": 30, "Fraicheur": 50, "Complexite": 30, "Exotisme": 40}

        bio = generate_taste_bio(prefs, scores)

        assert "douceur" in bio.lower() or "doux" in bio.lower() or "sucre" in bio.lower()
        assert "L'IA Pero" in bio, "Signature presente"

    def test_generate_taste_bio_expert(self):
        """Test bio pour connaisseur averti."""
        prefs = {"Douceur": 2, "Acidite": 3, "Amertume": 5, "Force": 5, "Fraicheur": 3, "Complexite": 4, "Exotisme": 3}
        scores = {"Douceur": 30, "Acidite": 50, "Amertume": 70, "Force": 80, "Fraicheur": 40, "Complexite": 60, "Exotisme": 35}

        bio = generate_taste_bio(prefs, scores)

        assert "averti" in bio.lower() or "raffine" in bio.lower() or "intense" in bio.lower()


class TestScoringResult:
    """Tests pour la dataclass ScoringResult."""

    def test_scoring_result_structure(self):
        """Verifie la structure de ScoringResult."""
        result = ScoringResult(
            coverage_score=75.5,
            block_scores={"Douceur": 80, "Acidite": 60},
            weighted_scores={"Douceur": 26.7, "Acidite": 20.0},
            matched_keywords={"Douceur": ["sucre", "doux"], "Acidite": ["citron"]},
            profile_summary="Profil oriente douceur",
            recommendations=["Explorer l'amertume"]
        )

        assert result.coverage_score == 75.5
        assert len(result.block_scores) == 2
        assert len(result.matched_keywords["Douceur"]) == 2


class TestWeightedCoverageScore:
    """Tests pour le calcul du Coverage Score (EF3.1)."""

    @pytest.fixture
    def mock_model(self):
        """Mock du modele SBERT."""
        model = MagicMock()
        # Simule un embedding de dimension 384
        model.encode.return_value = np.random.rand(384).astype(np.float32)
        return model

    def test_coverage_score_formula(self, mock_model):
        """Test de la formule Coverage Score = SWi*Si / SWi."""
        with patch('src.scoring.calculate_block_similarity') as mock_sim:
            # Simule des scores fixes pour chaque bloc
            mock_sim.return_value = (0.5, ["keyword1"])

            preferences = {dim: 3 for dim in TASTE_BLOCKS}  # Tous neutres
            result = calculate_weighted_coverage_score("test query", preferences, mock_model)

            assert isinstance(result, ScoringResult)
            assert 0 <= result.coverage_score <= 100
            assert len(result.block_scores) == 7

    def test_coverage_score_with_preferences(self, mock_model):
        """Test que les preferences influencent le score."""
        with patch('src.scoring.calculate_block_similarity') as mock_sim:
            mock_sim.return_value = (0.6, ["sweet"])

            # Preferences elevees
            high_prefs = {dim: 5 for dim in TASTE_BLOCKS}
            result_high = calculate_weighted_coverage_score("sweet cocktail", high_prefs, mock_model)

            # Preferences basses
            low_prefs = {dim: 1 for dim in TASTE_BLOCKS}
            result_low = calculate_weighted_coverage_score("sweet cocktail", low_prefs, mock_model)

            # Le score brut devrait etre similaire (meme similarite)
            # mais les weighted_scores different
            assert result_high.coverage_score > 0
            assert result_low.coverage_score > 0


class TestIntegrationScoring:
    """Tests d'integration avec le vrai modele SBERT."""

    @pytest.fixture
    def real_model(self):
        """Charge le vrai modele SBERT (peut etre lent)."""
        try:
            from src.backend import get_sbert_model
            return get_sbert_model()
        except Exception:
            pytest.skip("SBERT model not available")

    def test_real_scoring_sweet_query(self, real_model):
        """Test avec une vraie requete orientee douceur."""
        preferences = {"Douceur": 5, "Acidite": 2, "Amertume": 1, "Force": 2, "Fraicheur": 3, "Complexite": 3, "Exotisme": 4}

        result = calculate_weighted_coverage_score(
            "cocktail tres sucre et doux avec fruits tropicaux",
            preferences,
            real_model
        )

        assert result.coverage_score > 0
        assert result.block_scores["Douceur"] > 30, "Douceur doit etre detectee"
        assert result.block_scores["Exotisme"] > 20, "Exotisme doit etre detecte"
        assert len(result.recommendations) > 0

    def test_real_scoring_bitter_query(self, real_model):
        """Test avec une vraie requete orientee amertume."""
        preferences = {"Douceur": 2, "Acidite": 3, "Amertume": 5, "Force": 4, "Fraicheur": 2, "Complexite": 4, "Exotisme": 2}

        result = calculate_weighted_coverage_score(
            "negroni amer avec campari et gin",
            preferences,
            real_model
        )

        assert result.coverage_score > 0
        assert result.block_scores["Amertume"] > 30, "Amertume doit etre detectee"
        assert result.block_scores["Force"] > 20, "Force doit etre detectee"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
