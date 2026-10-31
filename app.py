"""
app.py – Interface Streamlit de RoadmapIA (Personne B)

Flux :
  Formulaire → génération de la roadmap → affichage par étapes → export
"""

import json
import os

import streamlit as st
from dotenv import load_dotenv

from generation import generer_roadmap
from exporter import exporter_markdown, exporter_pdf

# ──────────────────────────────────────────────
# Configuration initiale
# ──────────────────────────────────────────────
load_dotenv()  # Charge .env en local (GROQ_API_KEY)

st.set_page_config(
    page_title="RoadmapIA – Votre parcours tech personnalisé",
    page_icon="🗺️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
# CSS personnalisé (apparence premium)
# ──────────────────────────────────────────────
st.markdown("""
<style>
  /* Police Google Fonts */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  /* Fond sombre */
  .stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: #e0e0e0;
  }

  /* Titre principal */
  .hero-title {
    text-align: center;
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
  }

  .hero-subtitle {
    text-align: center;
    color: #9ca3af;
    font-size: 1.05rem;
    margin-bottom: 2rem;
  }

  /* Cartes d'étapes */
  .step-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(167,139,250,0.25);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(6px);
  }

  .step-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin-bottom: 0.6rem;
  }

  .step-badge {
    background: linear-gradient(135deg, #7c3aed, #3b82f6);
    color: white;
    border-radius: 50%;
    width: 2rem;
    height: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.85rem;
    flex-shrink: 0;
  }

  .step-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #e2e8f0;
  }

  .step-duration {
    font-size: 0.82rem;
    color: #a78bfa;
    font-weight: 500;
    margin-bottom: 0.7rem;
  }

  .tag {
    display: inline-block;
    background: rgba(99,102,241,0.2);
    border: 1px solid rgba(99,102,241,0.4);
    color: #c4b5fd;
    border-radius: 20px;
    padding: 0.15rem 0.65rem;
    font-size: 0.78rem;
    margin: 0.2rem 0.15rem 0.2rem 0;
  }

  .resource-link {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    color: #60a5fa;
    font-size: 0.88rem;
    text-decoration: none;
    margin: 0.2rem 0;
  }

  .mini-projet {
    background: rgba(52,211,153,0.1);
    border-left: 3px solid #34d399;
    border-radius: 0 8px 8px 0;
    padding: 0.5rem 0.8rem;
    font-size: 0.9rem;
    color: #6ee7b7;
    margin-top: 0.7rem;
  }

  /* Boutons */
  .stButton > button {
    background: linear-gradient(135deg, #7c3aed, #3b82f6);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 2rem;
    font-weight: 600;
    font-size: 1rem;
    transition: opacity 0.2s;
  }
  .stButton > button:hover { opacity: 0.88; }

  /* Formulaire */
  .stSelectbox label, .stTextInput label, .stTextArea label,
  .stSlider label, .stRadio label {
    color: #c4b5fd !important;
    font-weight: 500;
  }

  /* Séparateur */
  hr { border-color: rgba(167,139,250,0.2); }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# En-tête héro
# ──────────────────────────────────────────────
st.markdown('<p class="hero-title">🗺️ RoadmapIA</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-subtitle">Votre parcours tech 100 % personnalisé · Ressources gratuites · IA pour tous 🌍</p>',
    unsafe_allow_html=True,
)
st.divider()


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

with st.form(key="profil_form"):
    st.subheader("📋 Décrivez votre profil")

    col1, col2 = st.columns(2)

    with col1:
        objectif = st.selectbox(
            "🎯 Votre objectif",
            options=[
                "Développeur backend (Python/Django/FastAPI)",
                "Développeur frontend (HTML, CSS, JavaScript, React)",
                "Développeur fullstack",
                "Développeur mobile (React Native / Flutter)",
                "Data Scientist / Analyste data",
                "DevOps / Cloud",
                "Développeur IA / Machine Learning",
                "Bases de l'informatique (débutant absolu)",
            ],
            help="Choisissez la spécialité vers laquelle vous voulez progresser.",
        )

        niveau = st.selectbox(
            "📊 Votre niveau actuel",
            options=["Débutant absolu", "Notions de base", "Intermédiaire", "Confirmé"],
        )

        langue = st.radio(
            "🌐 Langue préférée pour les ressources",
            options=["Français", "Anglais", "Les deux"],
            horizontal=True,
        )

    with col2:
        temps_semaine = st.slider(
            "⏱️ Heures disponibles par semaine",
            min_value=2,
            max_value=40,
            value=8,
            step=1,
            help="Soyez réaliste — mieux vaut sous-estimer.",
        )

        contraintes = st.multiselect(
            "⚡ Contraintes spécifiques",
            options=[
                "Connexion internet faible ou instable",
                "Ordinateur peu puissant (< 4 Go RAM)",
                "Budget zéro (tout doit être gratuit)",
                "Pas de compte bancaire / carte de crédit",
                "Préférence pour les ressources hors ligne",
            ],
            default=["Budget zéro (tout doit être gratuit)"],
            help="Cochez tout ce qui s'applique à votre situation.",
        )

    competences_acquises = st.text_area(
        "✅ Compétences déjà acquises (laissez vide si débutant)",
        placeholder="Ex : bases de Python, HTML/CSS, Git basique, SQL simple...",
        height=90,
    )

    submitted = st.form_submit_button("✨ Générer ma roadmap personnalisée", use_container_width=True)


# ──────────────────────────────────────────────
# Roadmap de démonstration (exemple statique)
# pour permettre à Personne B de travailler sans l'API
# ──────────────────────────────────────────────
ROADMAP_DEMO = {
    "objectif": "Développeur backend",
    "duree_totale_semaines": 22,
    "message_personnalise": "Avec 8 h par semaine, tu peux atteindre un niveau employable en backend Python en moins de 6 mois. Sois régulier et construis chaque mini-projet !",
    "etapes": [
        {
            "titre": "Bases de Python",
            "duree_semaines": 3,
            "competences": ["variables et types", "boucles et conditions", "fonctions", "fichiers"],
            "ressources": ["py_basics_fr"],
            "mini_projet": "Gestionnaire de dépenses en ligne de commande",
            "ressources_enrichies": [
                {
                    "id": "py_basics_fr",
                    "titre": "Python pour débutants – OpenClassrooms",
                    "url": "https://openclassrooms.com/fr/courses/7168871-apprenez-les-bases-du-langage-python",
                    "langue": "fr",
                }
            ],
        },
        {
            "titre": "Programmation orientée objet",
            "duree_semaines": 2,
            "competences": ["classes", "héritage", "encapsulation"],
            "ressources": ["py_poo_fr"],
            "mini_projet": "Simulateur de bibliothèque (livres, emprunts, retours)",
            "ressources_enrichies": [
                {
                    "id": "py_poo_fr",
                    "titre": "POO en Python – OpenClassrooms",
                    "url": "https://openclassrooms.com/fr/courses/7150616-apprenez-la-programmation-orientee-objet-avec-python",
                    "langue": "fr",
                }
            ],
        },
        {
            "titre": "Git & travail en équipe",
            "duree_semaines": 1,
            "competences": ["commits", "branches", "pull requests"],
            "ressources": ["git_fr"],
            "mini_projet": "Contribuer à un projet open source simple (corriger un README)",
            "ressources_enrichies": [
                {
                    "id": "git_fr",
                    "titre": "Git et GitHub – OpenClassrooms",
                    "url": "https://openclassrooms.com/fr/courses/7162856-gerez-du-code-avec-git-et-github",
                    "langue": "fr",
                }
            ],
        },
        {
            "titre": "Bases de données SQL",
            "duree_semaines": 3,
            "competences": ["SELECT", "JOIN", "INDEX", "transactions"],
            "ressources": ["sql_fr", "sql_en"],
            "mini_projet": "Base de données d'un système de gestion d'étudiants",
            "ressources_enrichies": [
                {
                    "id": "sql_fr",
                    "titre": "SQL – OpenClassrooms",
                    "url": "https://openclassrooms.com/fr/courses/6971126-implementez-vos-bases-de-donnees-relationnelles-avec-sql",
                    "langue": "fr",
                },
                {
                    "id": "sql_en",
                    "titre": "SQLZoo – Interactive SQL",
                    "url": "https://sqlzoo.net/",
                    "langue": "en",
                },
            ],
        },
        {
            "titre": "API REST avec FastAPI",
            "duree_semaines": 4,
            "competences": ["routage", "Pydantic", "authentification JWT", "documentation Swagger"],
            "ressources": ["fastapi_en", "api_rest_fr"],
            "mini_projet": "API de gestion de tâches (CRUD complet) avec documentation",
            "ressources_enrichies": [
                {
                    "id": "fastapi_en",
                    "titre": "FastAPI – Documentation officielle",
                    "url": "https://fastapi.tiangolo.com/tutorial/",
                    "langue": "en",
                },
                {
                    "id": "api_rest_fr",
                    "titre": "Construire une API REST – OpenClassrooms",
                    "url": "https://openclassrooms.com/fr/courses/6573181-adoptez-les-api-rest-pour-vos-projets-web",
                    "langue": "fr",
                },
            ],
        },
        {
            "titre": "Déploiement avec Docker",
            "duree_semaines": 2,
            "competences": ["Dockerfile", "docker-compose", "déploiement cloud basique"],
            "ressources": ["docker_fr"],
            "mini_projet": "Conteneuriser et déployer ton API FastAPI sur Render.com (gratuit)",
            "ressources_enrichies": [
                {
                    "id": "docker_fr",
                    "titre": "Docker – OpenClassrooms",
                    "url": "https://openclassrooms.com/fr/courses/2035766-optimisez-votre-deploiement-en-creant-des-conteneurs-avec-docker",
                    "langue": "fr",
                }
            ],
        },
    ],
}


# ──────────────────────────────────────────────
# Affichage de la roadmap
# ──────────────────────────────────────────────
def afficher_roadmap(roadmap: dict) -> None:
    """Affiche la roadmap complète en cartes stylisées."""

    st.divider()
    st.markdown(f"### 🎯 Roadmap : {roadmap.get('objectif', '')}")

    duree = roadmap.get("duree_totale_semaines", "?")
    st.markdown(f"**Durée totale estimée :** `{duree} semaines`")

    message = roadmap.get("message_personnalise", "")
    if message:
        st.info(f"💬 {message}")

    st.divider()

    etapes = roadmap.get("etapes", [])
    nb_etapes = len(etapes)
# Timeline visuelle en haut

    # Barre de progression globale
    if "progression" not in st.session_state:
        st.session_state.progression = [False] * nb_etapes

    nb_validees = sum(st.session_state.progression)
    pct = int(nb_validees / nb_etapes * 100) if nb_etapes else 0
    st.progress(pct / 100, text=f"Progression : {nb_validees}/{nb_etapes} étapes complétées ({pct}%)")
    st.markdown("")

    for i, etape in enumerate(etapes):
        titre = etape.get("titre", f"Étape {i+1}")
        duree_etape = etape.get("duree_semaines", "?")
        competences = etape.get("competences", [])
        mini_projet = etape.get("mini_projet", "")
        ressources_enrichies = etape.get("ressources_enrichies", [])
        ressources_ids = etape.get("ressources", [])

        # Construire la carte HTML
        tags_html = "".join(f'<span class="tag">{c}</span>' for c in competences)

        ressources_html = ""
        if ressources_enrichies:
            for r in ressources_enrichies:
                flag = "🇫🇷" if r.get("langue") == "fr" else "🇬🇧" if r.get("langue") == "en" else "🌐"
                ressources_html += (
                    f'<a class="resource-link" href="{r["url"]}" target="_blank">'
                    f'{flag} {r["titre"]}</a>'
                )
        elif ressources_ids:
            for rid in ressources_ids:
                ressources_html += f'<span class="tag">{rid}</span>'

        mini_projet_html = ""
        if mini_projet:
            mini_projet_html = f'<div class="mini-projet">🛠️ <strong>Mini-projet :</strong> {mini_projet}</div>'

        st.markdown(f"""
<div class="step-card">
  <div class="step-header">
    <div class="step-badge">{i+1}</div>
    <div class="step-title">{titre}</div>
  </div>
  <div class="step-duration">⏱️ {duree_etape} semaine(s)</div>
  <div>{tags_html}</div>
  <br/>
  <div><strong>📚 Ressources :</strong><br/>{ressources_html}</div>
  {mini_projet_html}
</div>
""", unsafe_allow_html=True)

        # Case à cocher de progression
        checked = st.checkbox(
            f"✅ Marquer « {titre} » comme terminée",
            value=st.session_state.progression[i] if i < len(st.session_state.progression) else False,
            key=f"etape_{i}",
        )
        st.session_state.progression[i] = checked

    # ── Boutons d'export ──
    st.divider()
    st.subheader("📥 Télécharger ma roadmap")

    col_md, col_pdf = st.columns(2)

    with col_md:
        contenu_md = exporter_markdown(roadmap)
        st.download_button(
            label="⬇️ Télécharger en Markdown (.md)",
            data=contenu_md,
            file_name=f"roadmap_{roadmap.get('objectif', 'tech').replace(' ', '_').lower()}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with col_pdf:
        contenu_pdf = exporter_pdf(roadmap)
        if contenu_pdf:
            st.download_button(
                label="⬇️ Télécharger en PDF",
                data=contenu_pdf,
                file_name=f"roadmap_{roadmap.get('objectif', 'tech').replace(' ', '_').lower()}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.button(
                "⬇️ PDF (installe fpdf2 pour activer)",
                disabled=True,
                use_container_width=True,
                help="pip install fpdf2",
            )


# ──────────────────────────────────────────────
# Logique principale
# ──────────────────────────────────────────────
if submitted:
    # Réinitialiser la progression
    st.session_state.progression = []

    profil = {
        "objectif": objectif,
        "niveau": niveau,
        "competences_acquises": competences_acquises.strip() or "Aucune",
        "temps_semaine": str(temps_semaine),
        "contraintes": ", ".join(contraintes) if contraintes else "Aucune",
        "langue": langue,
    }

    # Vérification de la clé API
    if not os.getenv("GROQ_API_KEY"):
        st.warning(
            "⚠️ **Clé API Groq non trouvée.** Affichage de la roadmap de démonstration.\n\n"
            "Pour utiliser l'IA, créez un fichier `.env` avec `GROQ_API_KEY=votre_clé`.",
            icon="⚠️",
        )
        st.session_state["roadmap"] = ROADMAP_DEMO

    else:
        with st.spinner("✨ L'IA génère votre roadmap personnalisée..."):
            try:
                roadmap = generer_roadmap(profil)
                st.session_state["roadmap"] = roadmap
                st.success("✅ Roadmap générée avec succès !")
            except Exception as e:
                st.error(f"❌ Erreur lors de la génération : {e}")
                st.info("Affichage de la roadmap de démonstration à la place.")
                st.session_state["roadmap"] = ROADMAP_DEMO

# Afficher la roadmap si elle est en session
if "roadmap" in st.session_state:
    afficher_roadmap(st.session_state["roadmap"])

# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.divider()
st.markdown(
    '<div style="text-align:center;color:#6b7280;font-size:0.82rem;">'
    "RoadmapIA — Hackathon IA pour tous 🌍 · Ressources 100% gratuites et vérifiées"
    "</div>",
    unsafe_allow_html=True,
)
