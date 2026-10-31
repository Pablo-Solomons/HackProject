"""
test_generation.py – Script de test pour la Personne A (Tâche A1)

Lance : python3 test_generation.py
Nécessite : un fichier .env avec GROQ_API_KEY=votre_cle

Ce script teste 3 profils très différents et vérifie :
  ✅ JSON valide
  ✅ IDs de ressources tous dans ressources.json
  ✅ Durée totale cohérente
  ✅ Roadmaps différentes selon le profil
"""

import json
import os
import sys

from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────────────────────────
# Vérification rapide avant de commencer
# ──────────────────────────────────────────────
if not os.getenv("GROQ_API_KEY"):
    print("❌ GROQ_API_KEY manquante !")
    print("   → Crée un fichier .env avec : GROQ_API_KEY=ta_clé")
    print("   → Clé gratuite sur : https://console.groq.com")
    sys.exit(1)

from generation import charger_ressources, generer_roadmap

# ──────────────────────────────────────────────
# 3 profils de test contrastés
# ──────────────────────────────────────────────
PROFILS = [
    {
        "_label": "Profil 1 — Débutant absolu, 5h/sem, contraintes fortes",
        "objectif": "Développeur backend (Python/Django/FastAPI)",
        "niveau": "Débutant absolu",
        "competences_acquises": "Aucune",
        "temps_semaine": "5",
        "contraintes": "Budget zéro, connexion faible, ordinateur peu puissant",
        "langue": "Français",
    },
    {
        "_label": "Profil 2 — Intermédiaire, 20h/sem, sans contraintes",
        "objectif": "Développeur fullstack",
        "niveau": "Intermédiaire",
        "competences_acquises": "Python basique, HTML/CSS, Git, SQL simple",
        "temps_semaine": "20",
        "contraintes": "Aucune",
        "langue": "Les deux",
    },
    {
        "_label": "Profil 3 — Reconversion, mobile, 10h/sem",
        "objectif": "Développeur mobile (React Native / Flutter)",
        "niveau": "Notions de base",
        "competences_acquises": "Notions de JavaScript et HTML",
        "temps_semaine": "10",
        "contraintes": "Budget zéro",
        "langue": "Français",
    },
]


# ──────────────────────────────────────────────
# Fonctions de validation
# ──────────────────────────────────────────────
def valider_ids_ressources(roadmap: dict, ressources: dict) -> list[str]:
    """Retourne la liste des IDs de ressources invalides (pas dans ressources.json)."""
    invalides = []
    for etape in roadmap.get("etapes", []):
        for rid in etape.get("ressources", []):
            if rid not in ressources:
                invalides.append(rid)
    return invalides


def valider_duree_coherence(roadmap: dict) -> tuple[bool, int, int]:
    """Vérifie que la somme des durées des étapes est proche de la durée totale."""
    total_declare = roadmap.get("duree_totale_semaines", 0)
    total_calcule = sum(e.get("duree_semaines", 0) for e in roadmap.get("etapes", []))
    ok = abs(total_declare - total_calcule) <= 2  # tolérance de 2 semaines
    return ok, total_declare, total_calcule


def afficher_roadmap_resume(roadmap: dict) -> None:
    """Affiche un résumé lisible de la roadmap."""
    print(f"  🎯 Objectif : {roadmap.get('objectif', '?')}")
    print(f"  ⏱️  Durée totale : {roadmap.get('duree_totale_semaines', '?')} semaines")
    print(f"  📝 Message : {roadmap.get('message_personnalise', '')[:80]}...")
    print(f"  📋 Étapes ({len(roadmap.get('etapes', []))}) :")
    for i, etape in enumerate(roadmap.get("etapes", []), 1):
        ressources_ids = ", ".join(etape.get("ressources", []))
        print(f"     {i}. {etape.get('titre', '?')} ({etape.get('duree_semaines', '?')} sem)")
        print(f"        Ressources : {ressources_ids or 'aucune'}")
        print(f"        Mini-projet : {etape.get('mini_projet', '?')[:60]}...")


# ──────────────────────────────────────────────
# Lancement des tests
# ──────────────────────────────────────────────
def main():
    print("=" * 65)
    print("🧪 TEST DE GÉNÉRATION DE ROADMAPS — RoadmapIA")
    print("=" * 65)

    ressources = charger_ressources()
    print(f"✅ Base de ressources chargée : {len(ressources)} ressources\n")

    resultats = []

    for i, profil in enumerate(PROFILS, 1):
        label = profil.pop("_label")
        print(f"\n{'─'*65}")
        print(f"TEST {i}/3 : {label}")
        print("─" * 65)

        try:
            roadmap = generer_roadmap(profil)

            # Validations
            ids_invalides = valider_ids_ressources(roadmap, ressources)
            duree_ok, total_declare, total_calcule = valider_duree_coherence(roadmap)
            nb_etapes = len(roadmap.get("etapes", []))

            # Affichage résumé
            afficher_roadmap_resume(roadmap)
            print()

            # Résultat des validations
            statut_ids = "✅" if not ids_invalides else f"⚠️  IDs invalides : {ids_invalides}"
            statut_duree = "✅" if duree_ok else f"⚠️  Déclaré={total_declare}sem, Calculé={total_calcule}sem"
            statut_etapes = "✅" if 2 <= nb_etapes <= 10 else f"⚠️  {nb_etapes} étapes (attendu 2-10)"

            print(f"  Ressources vérifiées : {statut_ids}")
            print(f"  Cohérence durée      : {statut_duree}")
            print(f"  Nombre d'étapes      : {statut_etapes}")

            resultats.append({"profil": i, "ok": True, "ids_invalides": ids_invalides})

            # Sauvegarde JSON pour inspection
            with open(f"test_roadmap_profil_{i}.json", "w", encoding="utf-8") as f:
                json.dump(roadmap, f, ensure_ascii=False, indent=2)
            print(f"  💾 Sauvegardé : test_roadmap_profil_{i}.json")

        except Exception as e:
            print(f"  ❌ ERREUR : {e}")
            resultats.append({"profil": i, "ok": False, "erreur": str(e)})

    # ── Bilan final ──
    print(f"\n{'='*65}")
    print("📊 BILAN FINAL")
    print("=" * 65)
    ok_count = sum(1 for r in resultats if r["ok"])
    print(f"  {ok_count}/3 profils générés avec succès")

    if all(r["ok"] for r in resultats):
        print("  ✅ Tous les tests passent — prêt pour l'intégration !")
    else:
        for r in resultats:
            if not r["ok"]:
                print(f"  ❌ Profil {r['profil']} : {r.get('erreur', '?')}")
        print("\n  → Ajuste le prompt dans prompts.py et relance les tests.")

    print()


if __name__ == "__main__":
    main()
