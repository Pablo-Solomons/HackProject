"""
test_sans_api.py – Tests qui ne nécessitent PAS la clé API Groq

Lance : python3 test_sans_api.py

Teste :
  ✅ Chargement et validation de ressources.json
  ✅ Construction des prompts (prompts.py)
  ✅ Export Markdown (exporter.py)
  ✅ Export PDF si fpdf2 est installé
  ✅ Enrichissement de roadmap (generation.py, sans appel réseau)
"""

import json
import sys
import os

PASS = "✅"
FAIL = "❌"
WARN = "⚠️ "
resultats = []

def ok(label):
    print(f"  {PASS} {label}")
    resultats.append((label, True))

def ko(label, detail=""):
    print(f"  {FAIL} {label}" + (f" — {detail}" if detail else ""))
    resultats.append((label, False))

def warn(label, detail=""):
    print(f"  {WARN}{label}" + (f" — {detail}" if detail else ""))

print("=" * 60)
print("🧪 TESTS SANS API — RoadmapIA (Personne A)")
print("=" * 60)

# ──────────────────────────────────────────────
# TEST 1 : ressources.json
# ──────────────────────────────────────────────
print("\n📦 [1/5] Validation de ressources.json")
try:
    with open("ressources.json", encoding="utf-8") as f:
        data = json.load(f)

    ressources = data.get("ressources", {})
    ok(f"{len(ressources)} ressources chargées")

    # Vérifier les champs obligatoires
    champs_requis = ["titre", "url", "langue", "gratuit", "hors_ligne", "niveau", "tags"]
    erreurs = []
    for rid, r in ressources.items():
        for champ in champs_requis:
            if champ not in r:
                erreurs.append(f"'{rid}' manque '{champ}'")
        if not r.get("url", "").startswith("http"):
            erreurs.append(f"'{rid}' URL invalide : {r.get('url')}")
        if not isinstance(r.get("tags"), list) or len(r.get("tags", [])) == 0:
            erreurs.append(f"'{rid}' tags vide ou absent")

    if erreurs:
        for e in erreurs[:5]:
            ko(e)
    else:
        ok("Tous les champs obligatoires présents")

    # Tags couverts
    tags = set()
    for r in ressources.values():
        tags.update(r.get("tags", []))
    ok(f"{len(tags)} tags uniques couverts")

    # Tous gratuits ?
    non_gratuits = [rid for rid, r in ressources.items() if not r.get("gratuit")]
    if non_gratuits:
        warn(f"{len(non_gratuits)} ressources non gratuites", str(non_gratuits))
    else:
        ok("Toutes les ressources sont gratuites")

except Exception as e:
    ko("Erreur lors du chargement de ressources.json", str(e))

# ──────────────────────────────────────────────
# TEST 2 : prompts.py
# ──────────────────────────────────────────────
print("\n📝 [2/5] Validation de prompts.py")
try:
    from prompts import SYSTEM_PROMPT, construire_prompt_utilisateur, construire_prompt_correction

    ok(f"SYSTEM_PROMPT chargé ({len(SYSTEM_PROMPT)} caractères)")

    # Vérifier que les règles clés sont dans le prompt
    regles_cles = ["JSON", "ressources", "acquises", "durée", "mini-projet"]
    for regle in regles_cles:
        if regle.lower() in SYSTEM_PROMPT.lower():
            ok(f"Règle présente : '{regle}'")
        else:
            warn(f"Règle absente du SYSTEM_PROMPT : '{regle}'")

    # Tester la construction du prompt utilisateur
    profil_test = {
        "objectif": "Développeur backend",
        "niveau": "Débutant",
        "competences_acquises": "Aucune",
        "temps_semaine": "5",
        "contraintes": "Budget zéro",
        "langue": "Français",
    }
    prompt = construire_prompt_utilisateur(profil_test, ressources)
    ok(f"Prompt utilisateur généré ({len(prompt)} caractères)")

    # Vérifier que le profil est bien injecté
    assert "Développeur backend" in prompt, "Objectif absent du prompt"
    assert "Budget zéro" in prompt, "Contraintes absentes du prompt"
    ok("Profil correctement injecté dans le prompt")

    # Vérifier que les IDs des ressources sont dans le prompt
    nb_ids_dans_prompt = sum(1 for rid in ressources if rid in prompt)
    ok(f"{nb_ids_dans_prompt}/{len(ressources)} IDs de ressources dans le prompt")

    # Tester le prompt de correction
    prompt_corr = construire_prompt_correction('{"mauvais": json}', "JSONDecodeError")
    ok(f"Prompt de correction généré ({len(prompt_corr)} caractères)")

except Exception as e:
    ko("Erreur dans prompts.py", str(e))

# ──────────────────────────────────────────────
# TEST 3 : generation.py (sans appel API)
# ──────────────────────────────────────────────
print("\n⚙️  [3/5] Validation de generation.py (sans appel API)")
try:
    from generation import charger_ressources, enrichir_roadmap

    r = charger_ressources()
    ok(f"charger_ressources() : {len(r)} ressources")

    # Tester enrichir_roadmap avec une roadmap fictive
    roadmap_fictive = {
        "objectif": "Test",
        "duree_totale_semaines": 4,
        "message_personnalise": "Bravo",
        "etapes": [
            {
                "titre": "Python",
                "duree_semaines": 2,
                "competences": ["variables"],
                "ressources": ["py_basics_fr", "id_inexistant_xyz"],
                "mini_projet": "Projet test",
            }
        ],
    }
    enrichie = enrichir_roadmap(roadmap_fictive, r)
    ressources_enrichies = enrichie["etapes"][0].get("ressources_enrichies", [])
    assert len(ressources_enrichies) == 1, "L'ID invalide aurait dû être ignoré"
    assert ressources_enrichies[0]["id"] == "py_basics_fr"
    ok("enrichir_roadmap() : ID valide conservé, ID invalide ignoré ✓")

    # Vérifier que l'URL est bien récupérée
    assert "openclassrooms" in ressources_enrichies[0]["url"]
    ok("URL correctement récupérée dans ressources_enrichies")

except Exception as e:
    ko("Erreur dans generation.py", str(e))

# ──────────────────────────────────────────────
# TEST 4 : exporter.py
# ──────────────────────────────────────────────
print("\n📄 [4/5] Validation de exporter.py")
try:
    from exporter import exporter_markdown, exporter_pdf

    roadmap_test = {
        "objectif": "Développeur backend",
        "duree_totale_semaines": 20,
        "message_personnalise": "Tu peux le faire !",
        "etapes": [
            {
                "titre": "Bases de Python",
                "duree_semaines": 3,
                "competences": ["variables", "fonctions", "POO"],
                "ressources": ["py_basics_fr"],
                "mini_projet": "Gestionnaire de dépenses CLI",
                "ressources_enrichies": [
                    {
                        "id": "py_basics_fr",
                        "titre": "Python pour débutants",
                        "url": "https://openclassrooms.com/fr/courses/7168871",
                        "langue": "fr",
                    }
                ],
            },
            {
                "titre": "Git",
                "duree_semaines": 1,
                "competences": ["commits", "branches"],
                "ressources": ["git_fr"],
                "mini_projet": "Dépôt GitHub personnel",
                "ressources_enrichies": [
                    {
                        "id": "git_fr",
                        "titre": "Git et GitHub",
                        "url": "https://openclassrooms.com/fr/courses/7162856",
                        "langue": "fr",
                    }
                ],
            },
        ],
    }

    # Markdown
    md = exporter_markdown(roadmap_test)
    assert len(md) > 200, "Markdown trop court"
    assert "Bases de Python" in md
    assert "openclassrooms.com" in md
    assert "[ ]" in md  # cases à cocher
    ok(f"exporter_markdown() : {len(md)} caractères générés")
    ok("Liens, titres et cases à cocher présents dans le Markdown")

    # Sauvegarder pour inspection
    with open("test_export.md", "w", encoding="utf-8") as f:
        f.write(md)
    ok("test_export.md sauvegardé (ouvre-le pour vérifier)")

    # PDF
    pdf = exporter_pdf(roadmap_test)
    if pdf:
        with open("test_export.pdf", "wb") as f:
            f.write(pdf)
        ok(f"exporter_pdf() : PDF généré ({len(pdf)} octets) → test_export.pdf")
    else:
        warn("exporter_pdf() : fpdf2 non installé, PDF ignoré")

except Exception as e:
    ko("Erreur dans exporter.py", str(e))

# ──────────────────────────────────────────────
# TEST 5 : Vérifier la clé API (sans l'utiliser)
# ──────────────────────────────────────────────
print("\n🔑 [5/5] Vérification de la clé API Groq")
try:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if api_key and api_key.startswith("gsk_") and len(api_key) > 20:
        ok(f"GROQ_API_KEY présente dans .env (gsk_...{api_key[-6:]})")
    elif api_key:
        warn("GROQ_API_KEY présente mais format inhabituel")
    else:
        ko("GROQ_API_KEY absente — crée un fichier .env")
except Exception as e:
    ko("Erreur lecture .env", str(e))

# ──────────────────────────────────────────────
# BILAN
# ──────────────────────────────────────────────
print(f"\n{'='*60}")
print("📊 BILAN")
print("=" * 60)
nb_ok = sum(1 for _, r in resultats if r)
nb_total = len(resultats)
print(f"  {nb_ok}/{nb_total} vérifications réussies")
if nb_ok == nb_total:
    print(f"\n  {PASS} TOUT EST OK — prêt pour les tests avec l'API !")
    print("  Lance maintenant : python3 test_generation.py")
else:
    echecs = [label for label, r in resultats if not r]
    print(f"\n  Échecs :")
    for e in echecs:
        print(f"    {FAIL} {e}")
print()
