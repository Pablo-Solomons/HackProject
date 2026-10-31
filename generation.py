"""
generation.py – Logique d'appel au LLM via Groq API (Personne A)

Ce module gère :
- Le chargement de la base de ressources vérifiées
- L'appel à l'API Groq (openai/gpt-oss-120b)
- La validation et la correction automatique du JSON
- L'enrichissement de la roadmap avec les vraies URLs
"""

import json
import os
import re

from groq import Groq

from prompts import SYSTEM_PROMPT, construire_prompt_utilisateur, construire_prompt_correction


# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────
RESSOURCES_FILE = "ressources.json"
MAX_RETRIES = 2          # Nombre de tentatives en cas de JSON invalide
MODEL = "openai/gpt-oss-120b"


# ──────────────────────────────────────────────
# Chargement des ressources
# ──────────────────────────────────────────────
def charger_ressources() -> dict:
    """
    Charge et renvoie la base de ressources vérifiées depuis ressources.json.

    Returns:
        dict: dictionnaire {id_ressource: {titre, url, langue, ...}}

    Raises:
        FileNotFoundError: si ressources.json est introuvable
        ValueError: si le JSON est malformé
    """
    if not os.path.exists(RESSOURCES_FILE):
        raise FileNotFoundError(
            f"Fichier '{RESSOURCES_FILE}' introuvable. "
            "Assurez-vous qu'il se trouve dans le même dossier que l'application."
        )

    with open(RESSOURCES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("ressources", {})


# ──────────────────────────────────────────────
# Appel au LLM
# ──────────────────────────────────────────────
def _appeler_llm(client: Groq, messages: list) -> str:
    """Appelle l'API Groq et retourne le contenu texte brut de la réponse."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.3,      # Faible température pour un JSON cohérent
        max_tokens=4096,
        response_format={"type": "json_object"},  # Force le mode JSON
    )
    return response.choices[0].message.content


def _extraire_json(texte: str) -> dict:
    """
    Tente d'extraire un objet JSON depuis un texte brut.
    Gère les cas où le LLM ajoute du texte avant/après le JSON.
    """
    # Essai direct
    try:
        return json.loads(texte)
    except json.JSONDecodeError:
        pass

    # Recherche d'un bloc JSON avec regex
    match = re.search(r'\{.*\}', texte, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Impossible d'extraire un JSON valide depuis la réponse : {texte[:300]}...")


def _valider_roadmap(roadmap: dict) -> None:
    """
    Valide la structure minimale de la roadmap générée.

    Raises:
        ValueError: si un champ obligatoire est manquant ou mal typé
    """
    champs_obligatoires = ["objectif", "duree_totale_semaines", "etapes"]
    for champ in champs_obligatoires:
        if champ not in roadmap:
            raise ValueError(f"Champ obligatoire manquant dans la roadmap : '{champ}'")

    if not isinstance(roadmap["etapes"], list) or len(roadmap["etapes"]) == 0:
        raise ValueError("La roadmap doit contenir au moins une étape.")

    for i, etape in enumerate(roadmap["etapes"]):
        champs_etape = ["titre", "duree_semaines", "competences", "ressources", "mini_projet"]
        for champ in champs_etape:
            if champ not in etape:
                raise ValueError(f"Étape {i+1} : champ obligatoire manquant '{champ}'")


# ──────────────────────────────────────────────
# Enrichissement des ressources
# ──────────────────────────────────────────────
def enrichir_roadmap(roadmap: dict, ressources: dict) -> dict:
    """
    Remplace les IDs de ressources par les objets complets (titre + url + langue).
    Les IDs inconnus sont ignorés silencieusement.

    Args:
        roadmap: roadmap JSON brute du LLM (avec IDs)
        ressources: base de ressources chargée

    Returns:
        dict: roadmap enrichie avec les vraies données de ressources
    """
    for etape in roadmap.get("etapes", []):
        ids = etape.get("ressources", [])
        etape["ressources_enrichies"] = []
        for rid in ids:
            if rid in ressources:
                etape["ressources_enrichies"].append({
                    "id": rid,
                    "titre": ressources[rid]["titre"],
                    "url": ressources[rid]["url"],
                    "langue": ressources[rid].get("langue", "?"),
                })
            # Si l'ID n'existe pas, on l'ignore (pas de lien inventé)

    return roadmap


# ──────────────────────────────────────────────
# Fonction principale
# ──────────────────────────────────────────────
def generer_roadmap(profil: dict) -> dict:
    """
    Génère une roadmap personnalisée à partir du profil utilisateur.

    Workflow :
    1. Charge la base de ressources
    2. Construit le prompt
    3. Appelle le LLM (jusqu'à MAX_RETRIES tentatives en cas d'échec)
    4. Valide le JSON retourné
    5. Enrichit la roadmap avec les vraies URLs
    6. Retourne la roadmap finale

    Args:
        profil: dict avec les clés :
            - objectif (str)
            - niveau (str)
            - competences_acquises (str)
            - temps_semaine (str)
            - contraintes (str)
            - langue (str)

    Returns:
        dict: roadmap enrichie

    Raises:
        EnvironmentError: si la clé API Groq est absente
        RuntimeError: si le LLM échoue après toutes les tentatives
    """
    # Vérification de la clé API
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "Variable d'environnement GROQ_API_KEY manquante. "
            "Créez un fichier .env avec GROQ_API_KEY=votre_clé."
        )

    # Chargement des ressources
    ressources = charger_ressources()

    # Initialisation du client Groq
    client = Groq(api_key=api_key)

    # Construction des messages
    prompt_utilisateur = construire_prompt_utilisateur(profil, ressources)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt_utilisateur},
    ]

    # Tentatives d'appel au LLM
    derniere_erreur = None
    derniere_reponse = ""

    for tentative in range(1, MAX_RETRIES + 2):  # +2 car range est exclusif et 1ère tentative compte
        try:
            reponse_brute = _appeler_llm(client, messages)
            derniere_reponse = reponse_brute
            roadmap = _extraire_json(reponse_brute)
            _valider_roadmap(roadmap)

            # Succès : enrichir et retourner
            return enrichir_roadmap(roadmap, ressources)

        except (ValueError, json.JSONDecodeError) as e:
            derniere_erreur = str(e)

            if tentative <= MAX_RETRIES:
                # Ajouter la réponse du LLM et demander une correction
                messages.append({"role": "assistant", "content": derniere_reponse})
                messages.append({
                    "role": "user",
                    "content": construire_prompt_correction(derniere_reponse, derniere_erreur)
                })

        except Exception as e:
            raise RuntimeError(f"Erreur lors de l'appel à l'API Groq : {e}") from e

    raise RuntimeError(
        f"Le LLM n'a pas réussi à générer un JSON valide après {MAX_RETRIES + 1} tentatives. "
        f"Dernière erreur : {derniere_erreur}"
    )
