# 🗺️ RoadmapIA — Hackathon IA pour tous

> **Prototype de hackathon (3h) — Équipe de 3 personnes**

Une application web qui génère des **roadmaps tech personnalisées** : ordonnées, adaptées au temps et aux contraintes de chaque apprenant, avec des ressources 100 % gratuites et vérifiées.

---

## ✨ Fonctionnalités du MVP

- 📋 **Formulaire de profil** : objectif, niveau, temps disponible, contraintes, langue
- 🤖 **Génération par IA** : Groq API (Llama 3.3 70B) → JSON structuré
- 🗂️ **Base de ressources vérifiées** : ~25 liens gratuits dans `ressources.json` (aucun lien inventé)
- 🃏 **Affichage par cartes** : une carte par étape avec compétences, ressources et mini-projet
- ✅ **Suivi de progression** : cases à cocher par étape
- ⬇️ **Export Markdown** (et PDF en bonus)

---

## 🏗️ Architecture

```
Formulaire → Prompt + ressources.json → LLM Groq → JSON → Affichage → Export
```

---

## 📁 Structure du projet

```
.
├── app.py            # Interface Streamlit       (Personne B)
├── generation.py     # Appel LLM + validation    (Personne A)
├── prompts.py        # Prompt système + builder  (Personne A)
├── exporter.py       # Export Markdown / PDF     (Personne C)
├── ressources.json   # Base de ressources        (Personne A)
├── requirements.txt  # Dépendances Python
├── .env.example      # Template de la clé API
└── .gitignore        # Exclut .env et __pycache__
```

---

## 🚀 Démarrage rapide

### 1. Cloner le dépôt

```bash
git clone https://github.com/<votre-org>/roadmapIA.git
cd roadmapIA
```

### 2. Créer l'environnement virtuel

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer la clé API Groq

```bash
cp .env.example .env
# Éditez .env et remplacez "votre_cle_api_ici" par votre vraie clé
# Obtenez-en une gratuitement sur https://console.groq.com
```

### 5. Lancer l'application

```bash
streamlit run app.py
```

L'application sera accessible sur **http://localhost:8501**

> **Sans clé API :** l'application fonctionne avec une roadmap de démonstration intégrée — pratique pour développer l'interface sans attendre l'API.

---

## 🤝 Répartition des tâches

| Personne | Rôle | Fichiers |
|---|---|---|
| **A** | IA & données | `generation.py`, `prompts.py`, `ressources.json` |
| **B** | Interface | `app.py` |
| **C** | Export & déploiement | `exporter.py`, `requirements.txt`, déploiement |

### Règles Git
- Une branche par personne : `git checkout -b personne-A`
- Fusion dans `main` aux points de synchro (0h30, 1h30, 2h30)
- **Ne jamais commiter `.env`** (il est dans `.gitignore`)

---

## ☁️ Déploiement sur Streamlit Community Cloud

1. Pousser le code sur GitHub (sans le `.env`)
2. Aller sur [share.streamlit.io](https://share.streamlit.io)
3. Connecter le dépôt GitHub
4. Dans **Secrets**, ajouter :
   ```toml
   GROQ_API_KEY = "votre_cle_api_ici"
   ```
5. Déployer → obtenir le lien public pour le jury

---

## 🔧 Variables d'environnement

| Variable | Description | Obligatoire |
|---|---|---|
| `GROQ_API_KEY` | Clé API Groq (gratuite sur console.groq.com) | Oui (pour l'IA réelle) |

---

## 📦 Dépendances

| Librairie | Rôle |
|---|---|
| `streamlit` | Interface web |
| `groq` | Client officiel Groq API |
| `python-dotenv` | Chargement du fichier `.env` |
| `fpdf2` | Export PDF (bonus) |

---

## ⚠️ Risques identifiés & solutions

| Risque | Solution |
|---|---|
| JSON invalide du LLM | `try/except` + retry automatique (`MAX_RETRIES = 2`) |
| Liens inventés | Seulement des IDs de `ressources.json` |
| Wifi instable au hackathon | Roadmap démo intégrée + vidéo de secours |

---

*Hackathon IA pour tous 🌍 — Ressources 100% gratuites et vérifiées*
