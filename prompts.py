"""
prompts.py – Gestion du prompt envoyé au LLM (Personne A)

Ce module centralise la construction du prompt système et utilisateur
pour la génération de roadmaps personnalisées.
"""

import json


# ──────────────────────────────────────────────
# Schéma JSON attendu en sortie
# ──────────────────────────────────────────────
SCHEMA_SORTIE = {
    "objectif": "string – l'objectif tech de l'utilisateur",
    "duree_totale_semaines": "integer – durée totale estimée en semaines",
    "message_personnalise": "string – message d'encouragement adapté au profil",
    "etapes": [
        {
            "titre": "string – nom de l'étape",
            "duree_semaines": "integer – durée estimée pour cette étape",
            "competences": ["list of strings – compétences acquises"],
            "ressources": ["list of resource IDs from the provided list"],
            "mini_projet": "string – projet concret à réaliser"
        }
    ]
}

# ──────────────────────────────────────────────
# Prompt système (rôle du LLM)
# ──────────────────────────────────────────────
SYSTEM_PROMPT = """Tu es un conseiller en carrière tech pour des apprenants africains.
Tu crées des roadmaps personnalisées, pratiques et réalistes.

Règles ABSOLUES :
1. Réponds UNIQUEMENT en JSON valide, sans texte autour, sans balises markdown, sans explication.
2. Choisis les ressources UNIQUEMENT parmi la liste fournie (utilise les identifiants exacts).
3. Saute les compétences déjà acquises mentionnées dans le profil.
4. Adapte la durée de chaque étape au temps disponible par semaine.
5. Si la connexion est faible, privilégie les ressources légères et les vidéos courtes.
6. Si le budget est zéro, n'inclus QUE des ressources gratuites.
7. Chaque étape DOIT avoir un mini-projet concret et réalisable.
8. Ordonne les étapes du plus fondamental au plus avancé.
9. Inclus 1 à 3 identifiants de ressources par étape (pas plus).
10. Le JSON doit respecter exactement le schéma fourni."""


def construire_prompt_utilisateur(profil: dict, ressources_disponibles: dict) -> str:
    """
    Construit le message utilisateur envoyé au LLM.

    Args:
        profil: dict contenant les réponses du formulaire
        ressources_disponibles: dict des ressources vérifiées

    Returns:
        str: le prompt utilisateur formaté
    """
    # Construire la liste des ressources disponibles (IDs + titres)
    liste_ressources = []
    for rid, info in ressources_disponibles.items():
        tags = ", ".join(info.get("tags", []))
        langue = info.get("langue", "?")
        liste_ressources.append(
            f'- ID: "{rid}" | Titre: "{info["titre"]}" | Langue: {langue} | Tags: {tags}'
        )
    ressources_str = "\n".join(liste_ressources)

    # Construire le schéma JSON attendu
    schema_str = json.dumps(SCHEMA_SORTIE, ensure_ascii=False, indent=2)

    prompt = f"""Voici le profil de l'apprenant :
- Objectif : {profil.get('objectif', 'Non précisé')}
- Niveau actuel : {profil.get('niveau', 'Débutant')}
- Compétences déjà acquises : {profil.get('competences_acquises', 'Aucune')}
- Temps disponible : {profil.get('temps_semaine', '5')} heures par semaine
- Contraintes : {profil.get('contraintes', 'Aucune')}
- Langue préférée : {profil.get('langue', 'Français')}

Liste des ressources disponibles (utilise UNIQUEMENT ces IDs) :
{ressources_str}

Schéma JSON de sortie à respecter EXACTEMENT :
{schema_str}

Génère la roadmap personnalisée en JSON valide uniquement."""

    return prompt


def construire_prompt_correction(json_invalide: str, erreur: str) -> str:
    """
    Prompt de correction en cas de JSON invalide renvoyé par le LLM.

    Args:
        json_invalide: la réponse incorrecte du LLM
        erreur: le message d'erreur de parsing

    Returns:
        str: prompt demandant au LLM de corriger son JSON
    """
    schema_str = json.dumps(SCHEMA_SORTIE, ensure_ascii=False, indent=2)

    return f"""Ta réponse précédente n'était pas un JSON valide. Erreur : {erreur}

Ta réponse incorrecte :
{json_invalide}

Corrige et renvoie UNIQUEMENT le JSON valide selon ce schéma :
{schema_str}

IMPORTANT : Aucun texte avant ou après le JSON. Commence directement par {{ et termine par }}."""
