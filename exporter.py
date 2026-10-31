"""
exporter.py – Export de la roadmap en Markdown et PDF (Personne C)

Ce module fournit la fonction exporter_markdown() et, en bonus,
une conversion PDF via la librairie fpdf2 (optionnelle).
"""

from datetime import datetime
from typing import Optional


# ──────────────────────────────────────────────
# Export Markdown
# ──────────────────────────────────────────────
def exporter_markdown(roadmap: dict) -> str:
    """
    Transforme la roadmap dict en texte Markdown téléchargeable.

    Args:
        roadmap: dict complet de la roadmap (enrichie ou non)

    Returns:
        str: contenu Markdown prêt à être téléchargé
    """
    lignes = []
    date_export = datetime.now().strftime("%d/%m/%Y à %H:%M")

    # ── En-tête ──
    lignes.append(f"# 🗺️ Roadmap personnalisée — {roadmap.get('objectif', 'Mon objectif')}")
    lignes.append("")
    lignes.append(f"> Générée le {date_export} par **RoadmapIA**")
    lignes.append("")

    # ── Résumé ──
    duree = roadmap.get("duree_totale_semaines", "?")
    lignes.append(f"**Durée totale estimée :** {duree} semaines")
    lignes.append("")

    message = roadmap.get("message_personnalise", "")
    if message:
        lignes.append(f"> 💬 {message}")
        lignes.append("")

    # ── Étapes ──
    lignes.append("---")
    lignes.append("")

    etapes = roadmap.get("etapes", [])
    for i, etape in enumerate(etapes, start=1):
        titre = etape.get("titre", f"Étape {i}")
        duree_etape = etape.get("duree_semaines", "?")
        competences = etape.get("competences", [])
        mini_projet = etape.get("mini_projet", "")

        # Titre de l'étape
        lignes.append(f"## Étape {i} — {titre}")
        lignes.append(f"**Durée :** {duree_etape} semaine(s)")
        lignes.append("")

        # Compétences
        if competences:
            lignes.append("**Compétences acquises :**")
            for comp in competences:
                lignes.append(f"- {comp}")
            lignes.append("")

        # Ressources enrichies (avec URLs réelles)
        ressources_enrichies = etape.get("ressources_enrichies", [])
        ressources_ids = etape.get("ressources", [])

        if ressources_enrichies:
            lignes.append("**📚 Ressources :**")
            for r in ressources_enrichies:
                langue = r.get("langue", "")
                flag = "🇫🇷" if langue == "fr" else "🇬🇧" if langue == "en" else ""
                lignes.append(f"- {flag} [{r['titre']}]({r['url']})")
            lignes.append("")
        elif ressources_ids:
            lignes.append("**📚 Ressources :**")
            for rid in ressources_ids:
                lignes.append(f"- `{rid}`")
            lignes.append("")

        # Mini-projet
        if mini_projet:
            lignes.append(f"**🛠️ Mini-projet :** {mini_projet}")
            lignes.append("")

        # Case de suivi de progression
        lignes.append("- [ ] Étape complétée")
        lignes.append("")
        lignes.append("---")
        lignes.append("")

    # ── Pied de page ──
    lignes.append("*Roadmap générée par RoadmapIA — IA pour tous 🌍*")
    lignes.append("*Ressources 100% gratuites et vérifiées.*")

    return "\n".join(lignes)


# ──────────────────────────────────────────────
# Export PDF (bonus, nécessite fpdf2)
# ──────────────────────────────────────────────
def exporter_pdf(roadmap: dict) -> Optional[bytes]:
    """
    Génère un PDF de la roadmap. Nécessite fpdf2 (pip install fpdf2).

    Args:
        roadmap: dict complet de la roadmap

    Returns:
        bytes: contenu du PDF, ou None si fpdf2 n'est pas disponible
    """
    try:
        from fpdf import FPDF
    except ImportError:
        return None

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Police par défaut (Helvetica = intégré, gère l'UTF-8 basique)
    pdf.set_font("Helvetica", "B", 18)
    titre = f"Roadmap - {roadmap.get('objectif', 'Mon objectif')}"
    pdf.cell(0, 12, txt=titre, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 11)
    duree = roadmap.get("duree_totale_semaines", "?")
    pdf.cell(0, 8, txt=f"Duree totale : {duree} semaines", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # Message personnalisé
    message = roadmap.get("message_personnalise", "")
    if message:
        pdf.set_font("Helvetica", "I", 10)
        pdf.multi_cell(0, 6, txt=message)
        pdf.ln(4)

    # Étapes
    for i, etape in enumerate(roadmap.get("etapes", []), start=1):
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, txt=f"Etape {i} - {etape.get('titre', '')}", new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 6, txt=f"Duree : {etape.get('duree_semaines', '?')} semaine(s)", new_x="LMARGIN", new_y="NEXT")

        # Compétences
        competences = etape.get("competences", [])
        if competences:
            pdf.cell(0, 6, txt="Competences : " + ", ".join(competences), new_x="LMARGIN", new_y="NEXT")

        # Ressources
        for r in etape.get("ressources_enrichies", []):
            pdf.cell(0, 6, txt=f"  - {r.get('titre', '')} : {r.get('url', '')}", new_x="LMARGIN", new_y="NEXT")

        # Mini-projet
        mini_projet = etape.get("mini_projet", "")
        if mini_projet:
            pdf.set_font("Helvetica", "I", 10)
            pdf.multi_cell(0, 6, txt=f"Mini-projet : {mini_projet}")

        pdf.ln(4)

    return bytes(pdf.output())
