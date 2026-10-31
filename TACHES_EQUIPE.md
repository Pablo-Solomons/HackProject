# 🗺️ RoadmapIA — État du projet & Tâches finales par personne

> Hackathon IA pour tous · Équipe 3 personnes · Durée 3h
> **Projet pushé sur GitHub :** `github.com/Pablo-Solomons/HackProject`

---

## ✅ Ce qui est déjà fait (base commune pushée)

### Fichiers présents dans le dépôt

| Fichier | Statut | Ce qu'il fait |
|---|---|---|
| `app.py` | ✅ Complet | Interface Streamlit dark mode, formulaire, cartes, progression, export |
| `generation.py` | ✅ Complet | Appel API Groq + validation JSON + auto-retry (2 tentatives) |
| `prompts.py` | ✅ Complet | Prompt système (10 règles strictes) + builder de prompt + correction |
| `exporter.py` | ✅ Complet | Export Markdown complet + export PDF (bonus via fpdf2) |
| `ressources.json` | ✅ Base (26) | 26 ressources gratuites vérifiées FR + EN |
| `requirements.txt` | ✅ Complet | streamlit, groq, python-dotenv, fpdf2 |
| `.gitignore` | ✅ Complet | Exclut .env, venv, __pycache__, secrets Streamlit |
| `.env.example` | ✅ Complet | Template de la clé API Groq |
| `README.md` | ✅ Complet | Setup, architecture, déploiement |

### Ce qui fonctionne déjà sans clé API
L'app tourne **immédiatement** avec une roadmap de démonstration intégrée :
```bash
pip install -r requirements.txt
streamlit run app.py   # → http://localhost:8501
```

---

## 🚧 Ce qui reste à faire pour atteindre le MVP final

---

## 👤 Personne A — IA & Données
### Fichiers : `generation.py` · `prompts.py` · `ressources.json`

### Étape 0 — Setup (5 min)
```bash
git checkout -b personne-A
cp .env.example .env
# Éditer .env : remplacer "votre_cle_api_ici" par la vraie clé Groq
# Clé disponible sur : https://console.groq.com (gratuit)
pip install -r requirements.txt
```

### Tâche A1 — Tester le LLM en live (20 min)
Créer un fichier `test_generation.py` à la racine :
```python
from generation import generer_roadmap
import json

# Test profil 1 : débutant, peu de temps
profil1 = {
    "objectif": "Développeur backend (Python/Django/FastAPI)",
    "niveau": "Débutant absolu",
    "competences_acquises": "Aucune",
    "temps_semaine": "5",
    "contraintes": "Budget zéro, connexion faible",
    "langue": "Français"
}

# Test profil 2 : confirmé, beaucoup de temps
profil2 = {
    "objectif": "Développeur fullstack",
    "niveau": "Intermédiaire",
    "competences_acquises": "Python basique, HTML/CSS, Git",
    "temps_semaine": "20",
    "contraintes": "Aucune",
    "langue": "Les deux"
}

for i, profil in enumerate([profil1, profil2], 1):
    print(f"\n{'='*50}\nPROFIL {i}\n{'='*50}")
    try:
        r = generer_roadmap(profil)
        print(json.dumps(r, indent=2, ensure_ascii=False))
        print(f"✅ Profil {i} OK — {len(r['etapes'])} étapes, {r['duree_totale_semaines']} semaines")
    except Exception as e:
        print(f"❌ Erreur : {e}")
```
```bash
python3 test_generation.py
```

**Critères de succès :**
- [ ] Le JSON est valide (pas d'erreur de parsing)
- [ ] Les IDs de ressources dans `etapes[].ressources` existent tous dans `ressources.json`
- [ ] Les deux profils donnent des roadmaps différentes
- [ ] La durée totale est cohérente avec le temps disponible

### Tâche A2 — Enrichir `ressources.json` (20 min)
Ajouter au moins 10 ressources supplémentaires pour couvrir les tags manquants.
Ouvrir `ressources.json` et ajouter dans `"ressources": { ... }` :

**Tags manquants prioritaires :** `typescript`, `vue`, `devops`, `cloud`, `algorithmique avancé`

Exemples à ajouter :
```json
"freecodecamp_en": {
  "titre": "freeCodeCamp – Full curriculum",
  "url": "https://www.freecodecamp.org/learn",
  "langue": "en",
  "gratuit": true,
  "hors_ligne": false,
  "niveau": "debutant",
  "tags": ["html", "css", "javascript", "python", "backend", "data"]
},
"exercism_en": {
  "titre": "Exercism – Pratique guidée par langue",
  "url": "https://exercism.org/",
  "langue": "en",
  "gratuit": true,
  "hors_ligne": false,
  "niveau": "intermediaire",
  "tags": ["python", "javascript", "algorithmique", "pratique"]
},
"odin_project_en": {
  "titre": "The Odin Project – Web Development",
  "url": "https://www.theodinproject.com/",
  "langue": "en",
  "gratuit": true,
  "hors_ligne": false,
  "niveau": "debutant",
  "tags": ["html", "css", "javascript", "nodejs", "frontend", "backend"]
},
"kaggle_en": {
  "titre": "Kaggle – Data Science & ML Courses",
  "url": "https://www.kaggle.com/learn",
  "langue": "en",
  "gratuit": true,
  "hors_ligne": false,
  "niveau": "intermediaire",
  "tags": ["data", "machine-learning", "python", "pandas", "sql"]
}
```

### Tâche A3 — Ajuster le prompt si nécessaire (10 min)
Après les tests A1, si le LLM :
- Renvoie trop d'étapes → ajouter dans `SYSTEM_PROMPT` : *"Limite à 8 étapes maximum."*
- Oublie les contraintes connexion faible → ajouter : *"Si connexion faible, max 1 vidéo par étape."*
- Donne des durées irréalistes → ajouter : *"La somme de `duree_semaines` de toutes les étapes doit être égale à `duree_totale_semaines`."*

Fichier à modifier : `prompts.py` ligne 22 (`SYSTEM_PROMPT`)

### Tâche A4 — Commit & merge (5 min)
```bash
git add generation.py prompts.py ressources.json
git commit -m "feat(A): enrichir ressources (36+) et affiner prompt"
git checkout main
git pull origin main
git merge personne-A
git push origin main
```

> [!IMPORTANT]
> Ne jamais modifier `app.py` ni `exporter.py` — ce sont les fichiers de B et C.

---

## 👤 Personne B — Interface Streamlit
### Fichier : `app.py`

> **Aucune clé API nécessaire.** Tout le travail se fait avec la `ROADMAP_DEMO` déjà en dur dans `app.py`.

### Étape 0 — Setup (5 min)
```bash
git checkout -b personne-B
pip install -r requirements.txt
streamlit run app.py   # vérifier que ça tourne sur http://localhost:8501
```

### Tâche B1 — Ajouter les "Profils rapides" dans le formulaire (20 min)
Juste **avant** le `with st.form(key="profil_form"):` (vers ligne 110), ajouter :

```python
st.subheader("⚡ Profils rapides")
col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    if st.button("🚀 Débutant pressé", use_container_width=True,
                 help="5h/sem, budget zéro, connexion faible"):
        st.session_state["prefill"] = {
            "objectif_idx": 7,   # "Bases de l'informatique"
            "niveau_idx": 0,     # "Débutant absolu"
            "temps": 5,
            "contraintes": ["Connexion internet faible ou instable",
                            "Budget zéro (tout doit être gratuit)"],
            "langue_idx": 0,     # Français
        }
        st.rerun()
with col_p2:
    if st.button("🎓 Étudiant sérieux", use_container_width=True,
                 help="15h/sem, intermédiaire"):
        st.session_state["prefill"] = {
            "objectif_idx": 0,
            "niveau_idx": 2,
            "temps": 15,
            "contraintes": ["Budget zéro (tout doit être gratuit)"],
            "langue_idx": 2,
        }
        st.rerun()
with col_p3:
    if st.button("🔄 Reconversion pro", use_container_width=True,
                 help="20h/sem, quelques bases"):
        st.session_state["prefill"] = {
            "objectif_idx": 2,
            "niveau_idx": 1,
            "temps": 20,
            "contraintes": [],
            "langue_idx": 2,
        }
        st.rerun()
st.divider()
```

### Tâche B2 — Améliorer l'affichage des cartes (20 min)
Dans la fonction `afficher_roadmap()`, après la barre de progression, ajouter une **timeline visuelle** :

```python
# Timeline visuelle en haut
timeline_items = []
for i, e in enumerate(etapes):
    timeline_items.append(f"**{i+1}.** {e.get('titre','')} `{e.get('duree_semaines','?')}sem`")
st.markdown(" → ".join(timeline_items) + " → 🎯")
st.markdown("")
```

Et dans le CSS, ajouter une couleur de bordure par type d'étape :
```python
# Détecter la catégorie de l'étape par ses tags/titre
def couleur_etape(titre: str) -> str:
    titre_lower = titre.lower()
    if any(k in titre_lower for k in ["python", "base", "algorith"]):
        return "#f59e0b"  # orange = fondations
    if any(k in titre_lower for k in ["web", "html", "css", "js", "react"]):
        return "#3b82f6"  # bleu = frontend
    if any(k in titre_lower for k in ["api", "backend", "django", "fastapi"]):
        return "#10b981"  # vert = backend
    if any(k in titre_lower for k in ["docker", "deploy", "devops", "cloud"]):
        return "#8b5cf6"  # violet = devops
    return "#6366f1"  # indigo par défaut
```

### Tâche B3 — Message de félicitations à la fin (10 min)
À la fin de `afficher_roadmap()`, après les boutons d'export :

```python
if nb_validees == nb_etapes and nb_etapes > 0:
    st.balloons()
    st.success("🎉 Félicitations ! Tu as terminé toute ta roadmap. Tu es prêt(e) à postuler !")
```

### Tâche B4 — Brancher la vraie API (au point de synchro +1h30)
Au moment de l'intégration, **rien à changer** : la logique dans `app.py` autour de la ligne 265 gère déjà le vrai appel à `generer_roadmap()`. Il suffit que le `.env` soit présent.

Tester avec le formulaire rempli → cliquer "Générer" → vérifier que les vraies cartes s'affichent.

### Tâche B5 — Commit & merge (5 min)
```bash
git add app.py
git commit -m "feat(B): profils rapides, timeline visuelle, couleurs par catégorie"
git checkout main
git pull origin main
git merge personne-B
git push origin main
```

> [!IMPORTANT]
> Ne jamais modifier `generation.py`, `prompts.py`, `ressources.json`, ni `exporter.py`.

---

## 👤 Personne C — Export, Déploiement & Démo
### Fichiers : `exporter.py` · `requirements.txt` · GitHub · Streamlit Cloud

### Étape 0 — Setup (5 min)
```bash
git checkout -b personne-C
pip install -r requirements.txt   # installe aussi fpdf2
streamlit run app.py              # vérifier le bouton "Télécharger en Markdown"
```

### Tâche C1 — Améliorer l'export Markdown (15 min)
Dans `exporter.py`, dans la fonction `exporter_markdown()`, ajouter un **tableau de synthèse** juste après le message personnalisé :

```python
# Tableau de synthèse
lignes.append("## 📊 Vue d'ensemble")
lignes.append("")
lignes.append("| # | Étape | Durée | Mini-projet |")
lignes.append("|---|---|---|---|")
for i, etape in enumerate(etapes, start=1):
    titre_court = etape.get("titre", "")
    duree_e = etape.get("duree_semaines", "?")
    projet = etape.get("mini_projet", "")[:60]  # tronquer si trop long
    lignes.append(f"| {i} | {titre_court} | {duree_e} sem | {projet} |")
lignes.append("")
lignes.append("---")
lignes.append("")
```

Tester :
```python
# Dans un terminal Python
from exporter import exporter_markdown
# Coller la ROADMAP_DEMO depuis app.py et appeler exporter_markdown(ROADMAP_DEMO)
```

### Tâche C2 — Améliorer l'export PDF avec police Unicode (20 min)

Le PDF actuel ne gère pas bien les émojis et accents. Fix avec DejaVu :

```bash
# Télécharger la police DejaVu (dans le dossier du projet)
mkdir -p fonts
cd fonts
wget https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.tar.bz2
tar -xf dejavu-fonts-ttf-2.37.tar.bz2
cp dejavu-fonts-ttf-2.37/ttf/DejaVuSans.ttf .
cp dejavu-fonts-ttf-2.37/ttf/DejaVuSans-Bold.ttf .
cd ..
```

Dans `exporter.py`, modifier `exporter_pdf()` :
```python
# Remplacer les lignes de police par :
font_path = os.path.join(os.path.dirname(__file__), "fonts", "DejaVuSans.ttf")
font_bold_path = os.path.join(os.path.dirname(__file__), "fonts", "DejaVuSans-Bold.ttf")
if os.path.exists(font_path):
    pdf.add_font("DejaVu", "", font_path)
    pdf.add_font("DejaVu", "B", font_bold_path)
    pdf.set_font("DejaVu", "B", 18)
else:
    pdf.set_font("Helvetica", "B", 18)  # fallback sans émojis
```

Ajouter `fonts/` dans `.gitignore` (les polices sont volumineuses) :
```bash
echo "fonts/" >> .gitignore
```

### Tâche C3 — Déploiement sur Streamlit Community Cloud (15 min)

```bash
# 1. S'assurer que main est à jour avec tout le travail de l'équipe
git checkout main
git pull origin main
git push origin main   # vérifier que ça passe sans erreur
```

**Sur https://share.streamlit.io :**
1. Se connecter avec le compte GitHub `Pablo-Solomons`
2. Cliquer **"New app"**
3. Repository : `Pablo-Solomons/HackProject`
4. Branch : `main`
5. Main file path : `app.py`
6. Cliquer **"Advanced settings"** → **"Secrets"** → coller :
   ```toml
   GROQ_API_KEY = "la_vraie_clé_de_Personne_A"
   ```
7. Cliquer **"Deploy"**
8. Attendre 2–3 min → copier l'URL publique → la partager avec l'équipe et le jury

### Tâche C4 — Vidéo de secours (10 min)
Enregistrer une vidéo de 30–45 sec montrant :
1. Remplissage du formulaire (profil débutant)
2. Clic "Générer"
3. Affichage de la roadmap avec les cartes
4. Coche d'une étape (progression)
5. Téléchargement du Markdown

Outil recommandé : `kazam` ou `obs-studio` (Linux)

### Tâche C5 — Commit & merge (5 min)
```bash
git add exporter.py requirements.txt .gitignore
git commit -m "feat(C): export Markdown avec tableau de synthèse, PDF avec police Unicode"
git checkout main
git pull origin main
git merge personne-C
git push origin main
```

> [!IMPORTANT]
> Ne jamais modifier `app.py`, `generation.py`, `prompts.py`, ni `ressources.json`.

---

## 🔄 Planning des synchros

| Moment | Ce que chacun montre | Action Git |
|---|---|---|
| **+30 min** | A : premier `test_generation.py` OK · B : profils rapides affichés · C : déploiement lancé | Chacun commit sur sa branche |
| **+1h30** | A : 36+ ressources + prompt stable · B : UI complète · C : export Markdown OK + URL Streamlit | Merge dans `main` · B branche la vraie API |
| **+2h30** | **GEL DU CODE** — test bout en bout sur 2 profils opposés | Dernier push, aucun nouveau feature |
| **+3h00** | Démo au jury : 2 min démo + 1 min technique | — |

---

## 🚦 Workflow Git pour chaque personne

```bash
# ── Au démarrage ──
git checkout -b personne-X          # créer sa branche

# ── Pendant le développement ──
git add fichier.py
git commit -m "feat(X): description courte"

# ── Au point de synchro ──
git checkout main
git pull origin main --no-rebase    # récupérer le travail des autres
git merge personne-X                # intégrer son travail
git push origin main                # pousser

git checkout personne-X             # retourner sur sa branche
git merge main                      # récupérer les changements des autres
```

> [!CAUTION]
> Vérifier **avant chaque push** : `git status` ne doit PAS montrer `.env`

---

## 🏁 Définition du MVP "terminé"

- [ ] Formulaire rempli → roadmap affichée en cartes (sans erreur)
- [ ] Deux profils très différents → deux roadmaps différentes
- [ ] Toutes les ressources ont un vrai lien cliquable (aucun lien inventé)
- [ ] Bouton "Télécharger en Markdown" fonctionne
- [ ] L'app tourne sur une URL Streamlit publique
- [ ] La démo dure ≤ 3 min et montre clairement la personnalisation

**Bonus (si le temps le permet) :**
- [ ] Export PDF avec émojis corrects
- [ ] Diagramme Mermaid de la roadmap
- [ ] Profils rapides préremplis
- [ ] Message de félicitations quand toutes les étapes sont cochées

---

## ⚠️ Risques et plan B

| Risque | Solution déjà en place |
|---|---|
| JSON invalide du LLM | Auto-retry 2x dans `generation.py` |
| Liens inventés | Seulement des IDs de `ressources.json` |
| API Groq down | Mode démo intégré dans `app.py` |
| WiFi hackathon coupé | Vidéo de secours (Tâche C4) + mode démo |
| Conflit Git | Une branche par personne, un fichier par personne |

---

*RoadmapIA · Hackathon IA pour tous 🌍 · Ressources 100% gratuites et vérifiées*
