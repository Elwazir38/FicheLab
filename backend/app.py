"""Serveur local FicheLab : sert l'UI et expose l'API catalogue / fiches.

Lancer :  uvicorn backend.app:app --reload
Puis ouvrir http://localhost:8000
"""
from __future__ import annotations

import tempfile
import uuid as uuidlib
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import catalogue, fiches
from .mathalea import VUE_APERCU, VUES, build_url

WEB_DIR = Path(__file__).resolve().parent.parent / "web"

app = FastAPI(title="FicheLab", version="1.0")

# Utile si l'UI est ouverte depuis un autre port pendant le dev.
# Restreint aux origines locales : empêche un site tiers d'appeler l'API
# (écriture/suppression de fiches, déclenchement de la compilation LaTeX) via
# une requête cross-origin depuis le navigateur.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000", "http://127.0.0.1:8000",
        "http://localhost:5173", "http://127.0.0.1:5173",
    ],
    allow_methods=["*"], allow_headers=["*"],
)


# --------------------------------------------------------------------------- #
# Modèles (validation légère ; le manifeste reste un JSON ouvert).
# --------------------------------------------------------------------------- #
class FicheRequest(BaseModel):
    fiche: dict
    vue: str | None = Field(default=None)


# --------------------------------------------------------------------------- #
# API
# --------------------------------------------------------------------------- #
@app.get("/api/catalogue")
def get_catalogue():
    return catalogue.load_catalogue()


@app.post("/api/fiche/preview")
def preview(req: FicheRequest):
    """Manifeste -> URL MathALEA (aperçu ou export selon `vue`)."""
    vue = req.vue or VUE_APERCU
    if vue not in VUES:
        raise HTTPException(400, f"Vue inconnue : {vue}")
    try:
        url = build_url(req.fiche, vue)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    return {"url": url, "vue": vue}


@app.get("/api/catalogue/pyromaths")
def get_catalogue_pyromaths():
    """Catalogue Pyromaths (chargé paresseusement — import lourd au 1er appel)."""
    from . import pyromaths_engine
    return {"niveaux": pyromaths_engine.list_exercices()}


@app.post("/api/generate/pyromaths")
def generate_pyromaths(req: FicheRequest):
    """Génère localement le PDF d'une fiche Pyromaths et le renvoie."""
    from . import pyromaths_engine
    fiche = req.fiche
    selection = [
        {"name": ex.get("name") or ex.get("id"), "seed": ex.get("seed"), "nb": ex.get("nb", 1)}
        for ex in fiche.get("exercices", [])
        if ex.get("source") == "pyromaths" or ex.get("name")
    ]
    if not selection:
        raise HTTPException(400, "Aucun exercice Pyromaths dans la fiche.")
    mep = fiche.get("mise_en_page", {}) or {}
    entete = fiche.get("entete", {}) or {}
    out = Path(tempfile.gettempdir()) / f"fichelab-{uuidlib.uuid4().hex[:8]}.pdf"
    try:
        pdf = pyromaths_engine.generate(
            selection, out, enonce=True, corrige=mep.get("corrige", True),
            titre=fiche.get("titre", ""), niveau=fiche.get("niveau"),
            classe=entete.get("classe", ""), date_fiche=entete.get("date", ""),
        )
    except Exception as exc:  # compilation / sélection
        raise HTTPException(500, f"Génération échouée : {exc}") from exc
    filename = (fiches.slugify(fiche.get("titre", "fiche")) or "fiche") + ".pdf"
    return FileResponse(pdf, media_type="application/pdf", filename=filename)


@app.get("/api/fiches")
def api_list_fiches():
    return {"fiches": fiches.list_fiches()}


@app.get("/api/fiche/{slug}")
def api_get_fiche(slug: str):
    fiche = fiches.get_fiche(slug)
    if fiche is None:
        raise HTTPException(404, "Fiche introuvable")
    return fiche


@app.post("/api/fiche")
def api_save_fiche(fiche: dict):
    slug = fiches.save_fiche(fiche)
    return {"slug": slug}


@app.delete("/api/fiche/{slug}")
def api_delete_fiche(slug: str):
    if not fiches.delete_fiche(slug):
        raise HTTPException(404, "Fiche introuvable")
    return {"ok": True}


# --------------------------------------------------------------------------- #
# UI statique (montée en dernier pour ne pas masquer /api).
# --------------------------------------------------------------------------- #
app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="web")
