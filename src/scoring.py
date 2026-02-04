"""
Module de Scoring Pondere pour L'IA Pero
=========================================

Ce module implemente la formule de scoring RNCP:
    Coverage Score = ΣWi*Si / ΣWi

Il gere:
- Le calcul des scores par bloc/categorie (taste dimensions)
- La ponderation configurable des dimensions
- Le scoring final agrege
- La generation de profil utilisateur

Auteurs: Adam Beloucif & Amina Medjdoub
Projet: RNCP Bloc 2 - Expert en Ingenierie de Donnees
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

# =============================================================================
# CONFIGURATION DES BLOCS DE COMPETENCES (Dimensions gustatives)
# =============================================================================

# Blocs de competences adaptes au domaine des cocktails
# Chaque bloc contient des descripteurs semantiques pour l'analyse
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

# Poids par defaut pour les preferences utilisateur (echelle Likert)
DEFAULT_USER_WEIGHTS = {
    "Douceur": 3,
    "Acidite": 3,
    "Amertume": 3,
    "Force": 3,
    "Fraicheur": 3,
    "Complexite": 3,
    "Exotisme": 3
}


@dataclass
class ScoringResult:
    """Resultat du calcul de score avec details par bloc"""
    coverage_score: float  # Score global 0-100
    block_scores: Dict[str, float]  # Scores par dimension
    weighted_scores: Dict[str, float]  # Scores ponderes
    matched_keywords: Dict[str, List[str]]  # Mots-cles matches par bloc
    profile_summary: str  # Resume du profil
    recommendations: List[str]  # Dimensions a explorer


def calculate_block_similarity(
    query_embedding: np.ndarray,
    block_keywords: List[str],
    model
) -> Tuple[float, List[str]]:
    """
    Calcule la similarite semantique entre une requete et un bloc de competences.

    Args:
        query_embedding: Embedding de la requete utilisateur
        block_keywords: Liste des mots-cles du bloc
        model: Modele SBERT pour encoder les keywords

    Returns:
        Tuple (score_similarite, mots_cles_matches)
    """
    from sentence_transformers import util

    # Encoder les keywords du bloc
    keyword_embeddings = model.encode(block_keywords, convert_to_numpy=True)

    # Calculer la similarite cosinus avec chaque keyword
    similarities = util.cos_sim(query_embedding, keyword_embeddings).numpy().flatten()

    # Identifier les keywords matches (similarite > 0.3)
    matched = [kw for kw, sim in zip(block_keywords, similarities) if sim > 0.3]

    # Score du bloc = moyenne des Top-3 similarites
    top_similarities = sorted(similarities, reverse=True)[:3]
    block_score = float(np.mean(top_similarities)) if top_similarities else 0.0

    return block_score, matched


def calculate_weighted_coverage_score(
    query: str,
    user_preferences: Dict[str, int],
    model
) -> ScoringResult:
    """
    Calcule le Coverage Score pondere selon la formule RNCP:
        Coverage Score = ΣWi*Si / ΣWi

    Args:
        query: Requete utilisateur en texte libre
        user_preferences: Preferences Likert (1-5) par dimension
        model: Modele SBERT

    Returns:
        ScoringResult avec tous les details du calcul
    """
    # Encoder la requete utilisateur
    query_embedding = model.encode(query, convert_to_numpy=True)

    block_scores = {}
    weighted_scores = {}
    matched_keywords = {}

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

        # Stocker les resultats
        block_scores[block_name] = round(score * 100, 1)  # En pourcentage
        weighted_scores[block_name] = round(score * final_weight * 100, 1)
        matched_keywords[block_name] = matched

        # Accumuler pour le score global
        total_weighted_score += score * final_weight
        total_weight += final_weight

    # Formule RNCP: Coverage Score = ΣWi*Si / ΣWi
    coverage_score = (total_weighted_score / total_weight * 100) if total_weight > 0 else 0.0

    # Generer le resume du profil
    profile_summary = generate_profile_summary(block_scores, user_preferences)

    # Identifier les dimensions a explorer (scores faibles mais preferences elevees)
    recommendations = identify_exploration_areas(block_scores, user_preferences)

    return ScoringResult(
        coverage_score=round(coverage_score, 1),
        block_scores=block_scores,
        weighted_scores=weighted_scores,
        matched_keywords=matched_keywords,
        profile_summary=profile_summary,
        recommendations=recommendations
    )


def generate_profile_summary(
    block_scores: Dict[str, float],
    user_preferences: Dict[str, int]
) -> str:
    """
    Genere un resume textuel du profil gustatif de l'utilisateur.

    Args:
        block_scores: Scores par dimension
        user_preferences: Preferences utilisateur

    Returns:
        Texte de synthese du profil
    """
    # Identifier les dimensions dominantes (score > 60%)
    dominant = [name for name, score in block_scores.items() if score > 60]

    # Identifier les preferences fortes (Likert >= 4)
    preferences_fortes = [name for name, pref in user_preferences.items() if pref >= 4]

    # Construire le resume
    if dominant:
        dominant_str = ", ".join(dominant[:3])
        summary = f"Profil oriente vers: {dominant_str}. "
    else:
        summary = "Profil equilibre avec des gouts varies. "

    if preferences_fortes:
        pref_str = ", ".join(preferences_fortes[:2])
        summary += f"Preferences marquees pour: {pref_str}."

    return summary


def identify_exploration_areas(
    block_scores: Dict[str, float],
    user_preferences: Dict[str, int]
) -> List[str]:
    """
    Identifie les dimensions a explorer pour le plan de progression.

    Logique: dimensions avec preference elevee mais score faible
    = opportunite de decouverte

    Returns:
        Liste des dimensions recommandees a explorer
    """
    recommendations = []

    for name, pref in user_preferences.items():
        score = block_scores.get(name, 0)
        # Preference >= 4 mais score < 40% = a explorer
        if pref >= 4 and score < 40:
            recommendations.append(f"Explorer des cocktails plus {name.lower()}")

    # Si pas de recommandations specifiques, suggerer les dimensions faibles
    if not recommendations:
        weak_dims = sorted(block_scores.items(), key=lambda x: x[1])[:2]
        recommendations = [f"Decouvrir la dimension {name}" for name, _ in weak_dims]

    return recommendations[:3]  # Max 3 recommandations


def enrich_short_query(query: str, preferences: Dict[str, int]) -> str:
    """
    Enrichit une requete courte (<5 mots) avec le contexte des preferences.

    Cette fonction repond a l'exigence EF4.1 du cahier des charges:
    "Enrichir les phrases d'entree utilisateur jugees trop courtes"

    Args:
        query: Requete originale de l'utilisateur
        preferences: Preferences Likert de l'utilisateur

    Returns:
        Requete enrichie avec contexte semantique
    """
    words = query.split()

    if len(words) >= 5:
        # Requete assez longue, pas besoin d'enrichissement
        return query

    # Construire le contexte d'enrichissement
    context_parts = []

    # Ajouter les preferences fortes (>= 4)
    for dim, pref in preferences.items():
        if pref >= 4:
            if dim == "Douceur":
                context_parts.append("doux et sucre")
            elif dim == "Acidite":
                context_parts.append("acidule et frais")
            elif dim == "Amertume":
                context_parts.append("avec une touche amere")
            elif dim == "Force":
                context_parts.append("plutot fort en alcool")
            elif dim == "Fraicheur":
                context_parts.append("rafraichissant")
            elif dim == "Complexite":
                context_parts.append("elabore et sophistique")
            elif dim == "Exotisme":
                context_parts.append("tropical et depaysant")

    # Ajouter les preferences faibles (< 2)
    for dim, pref in preferences.items():
        if pref <= 2:
            if dim == "Amertume":
                context_parts.append("pas trop amer")
            elif dim == "Force":
                context_parts.append("leger en alcool")

    if context_parts:
        enriched = f"{query}, {', '.join(context_parts[:3])}"
        logger.info(f"Query enriched: '{query}' -> '{enriched}'")
        return enriched

    return query


def generate_progression_plan(
    current_cocktail: dict,
    block_scores: Dict[str, float],
    recommendations: List[str]
) -> str:
    """
    Genere un plan de progression personnalise (EF4.2).

    Args:
        current_cocktail: Cocktail actuellement genere
        block_scores: Scores par dimension
        recommendations: Dimensions a explorer

    Returns:
        Texte du plan de progression
    """
    cocktail_name = current_cocktail.get("name", "ce cocktail")

    plan = f"**Plan de Decouverte apres {cocktail_name}:**\n\n"

    # Identifier les points forts
    strong_dims = [name for name, score in block_scores.items() if score > 60]
    if strong_dims:
        plan += f"- Vos points forts: {', '.join(strong_dims)}\n"

    # Ajouter les recommandations
    plan += "\n**Prochaines explorations recommandees:**\n"
    for i, rec in enumerate(recommendations, 1):
        plan += f"{i}. {rec}\n"

    # Suggerer des types de cocktails
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


def generate_taste_bio(
    user_preferences: Dict[str, int],
    block_scores: Dict[str, float],
    history: List[str] = None
) -> str:
    """
    Genere une biographie du profil gustatif (EF4.3).

    Style "Executive Summary" comme demande dans le cahier des charges.

    Args:
        user_preferences: Preferences Likert
        block_scores: Scores de la derniere requete
        history: Historique des cocktails (optionnel)

    Returns:
        Bio du profil gustatif
    """
    # Identifier le type de palais
    prefs = user_preferences

    if prefs.get("Douceur", 3) >= 4 and prefs.get("Force", 3) <= 2:
        palate_type = "Amateur de douceur"
        description = "Vous appreciez les cocktails doux et accessibles, avec des saveurs fruitees et sucrees."
    elif prefs.get("Amertume", 3) >= 4 and prefs.get("Force", 3) >= 4:
        palate_type = "Connaisseur averti"
        description = "Vous avez un palais raffine qui apprecie la complexite et les saveurs intenses."
    elif prefs.get("Fraicheur", 3) >= 4 and prefs.get("Acidite", 3) >= 4:
        palate_type = "Esprit frais"
        description = "Vous recherchez la fraicheur et le peps, avec une preference pour les notes acidulees."
    elif prefs.get("Exotisme", 3) >= 4:
        palate_type = "Explorateur tropical"
        description = "Le depaysement vous attire, avec une affection pour les cocktails exotiques et colores."
    else:
        palate_type = "Eclectique equilibre"
        description = "Votre palais est versatile et apprecie une variete de profils gustatifs."

    # Construire la bio
    bio = f"**{palate_type}**\n\n"
    bio += f"{description}\n\n"

    # Ajouter des details basés sur les scores
    strong = [k for k, v in block_scores.items() if v > 50]
    if strong:
        bio += f"*Affinites detectees:* {', '.join(strong)}\n"

    # Signature
    bio += "\n*Profil genere par L'IA Pero - Votre Barman IA*"

    return bio
