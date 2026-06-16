/* ===========================================================================
   FicheLab — logique de l'interface (vanilla JS, sans dépendance)
   État central = un manifeste de fiche, identique au format sauvegardé .json.
   Moteur unique : Pyromaths (génération PDF locale via LaTeX).
   =========================================================================== */
"use strict";

const $ = (sel) => document.querySelector(sel);
const api = (path, opts) => fetch(path, opts).then(async (r) => {
  if (!r.ok) throw new Error((await r.json().catch(() => ({}))).detail || r.statusText);
  return r.json();
});

const DRAFT_KEY = "fichelab:draft";

// ---------------------------------------------------------------- état --- //
let CATALOGUE = { niveaux: [] };
let activeLevel = null;

function newFiche() {
  return {
    version: 1,
    titre: "",
    entete: { classe: "", date: "", etablissement: "", consignes: "" },
    mise_en_page: { corrige: true },
    exercices: [],
  };
}
let fiche = newFiche();

// --------------------------------------------------------------- toast --- //
function toast(msg, isErr = false) {
  const t = $("#toast");
  t.textContent = msg; t.className = "show" + (isErr ? " err" : "");
  setTimeout(() => (t.className = ""), 2200);
}

// ====================================================== CATALOGUE (gauche) //
// Le backend renvoie {niveaux: [{niveau, exercices: [{name, description}]}]}.
async function loadCatalogue() {
  CATALOGUE = await api("/api/catalogue");
  activeLevel = CATALOGUE.niveaux[0]?.niveau || null;
  renderLevelTabs();
  renderCatalogue();
}

function renderLevelTabs() {
  const box = $("#level-tabs");
  box.innerHTML = "";
  (CATALOGUE.niveaux || []).forEach((n) => {
    const b = document.createElement("button");
    b.textContent = n.niveau;
    b.className = n.niveau === activeLevel ? "active" : "";
    b.onclick = () => { activeLevel = n.niveau; renderLevelTabs(); renderCatalogue(); };
    box.appendChild(b);
  });
}

function renderCatalogue() {
  const box = $("#catalogue");
  const q = $("#search").value.trim().toLowerCase();
  const groupe = (CATALOGUE.niveaux || []).find((n) => n.niveau === activeLevel);
  box.innerHTML = "";
  if (!groupe) return;

  const exos = groupe.exercices.filter((e) =>
    !q || e.description.toLowerCase().includes(q) || e.name.toLowerCase().includes(q));
  if (!exos.length) {
    box.innerHTML = `<p class="empty-sub" style="padding:12px">Aucun exercice ne correspond à « ${escapeHtml(q)} » dans ${escapeHtml(groupe.niveau)}.</p>`;
    return;
  }

  const details = document.createElement("details");
  details.className = "theme";
  details.open = true;
  const sum = document.createElement("summary");
  sum.innerHTML = `${escapeHtml(groupe.niveau)}<span class="count">${exos.length}</span>`;
  details.appendChild(sum);

  exos.forEach((e) => {
    const card = document.createElement("div");
    card.className = "exo-card";
    card.innerHTML = `<span class="code">${escapeHtml(e.name)}</span><span class="titre">${escapeHtml(e.description)}</span>`;
    const add = document.createElement("button");
    add.className = "btn small icon add"; add.textContent = "＋"; add.title = "Ajouter à la fiche";
    add.onclick = () => addExercice(e);
    card.appendChild(add);
    details.appendChild(card);
  });
  box.appendChild(details);
}

// ======================================================= FICHE (centre) === //
function addExercice(e) {
  fiche.exercices.push({
    source: "pyromaths", name: e.name, titre: e.description,
    nb: 1, seed: Math.floor(Math.random() * 1e9), // graine figée -> reproductible
  });
  renderFiche(); saveDraft();
  toast(`Ajouté : ${e.name}`);
}

function renderFiche() {
  $("#exo-count").textContent = fiche.exercices.length;
  $("#fiche-empty").style.display = fiche.exercices.length ? "none" : "block";
  $("#gen-empty").style.display = fiche.exercices.length ? "none" : "block";

  const box = $("#fiche-exos");
  box.innerHTML = "";
  fiche.exercices.forEach((ex, i) => box.appendChild(renderExoRow(ex, i)));
}

function renderExoRow(ex, i) {
  const el = document.createElement("div");
  el.className = "fiche-exo"; el.draggable = true; el.dataset.i = i;
  const code = ex.name;

  el.innerHTML = `
    <div class="row1">
      <span class="grip" title="Glisser pour réordonner">⠿</span>
      <span class="badge-src pyromaths">Pyromaths</span>
      <span class="code">${escapeHtml(code)}</span>
      <span class="titre">${escapeHtml(ex.titre || code)}</span>
      <button class="btn small icon" data-act="up" title="Monter">↑</button>
      <button class="btn small icon" data-act="down" title="Descendre">↓</button>
      <button class="btn small icon" data-act="del" title="Retirer">✕</button>
    </div>
    <div class="ctrls">
      <span class="mini"><label>Nombre</label><input type="number" min="1" max="10" value="${ex.nb || 1}" data-f="nb"></span>
      <span class="mini"><label title="Graine = reproductibilité : même graine ⇒ exactement les mêmes énoncés à chaque génération.">Graine ⓘ</label><code title="Graine de tirage figée. Même graine ⇒ mêmes valeurs.">${ex.seed}</code>
        <button class="btn small icon" data-act="reseed" title="Nouveau tirage aléatoire (change les valeurs des énoncés).">🎲</button></span>
    </div>`;

  el.querySelector('[data-act=del]').onclick = () => { fiche.exercices.splice(i, 1); commit(); };
  el.querySelector('[data-act=up]').onclick = () => move(i, -1);
  el.querySelector('[data-act=down]').onclick = () => move(i, +1);
  el.querySelector('[data-act=reseed]').onclick = () => { ex.seed = Math.floor(Math.random() * 1e9); commit(); };
  el.querySelector('[data-f=nb]').onchange = (e) => { ex.nb = parseInt(e.target.value) || 1; commit(false); };

  // drag & drop
  el.addEventListener("dragstart", () => { el.classList.add("dragging"); el.dataset.drag = "1"; });
  el.addEventListener("dragend", () => { el.classList.remove("dragging"); delete el.dataset.drag; });
  el.addEventListener("dragover", (e) => e.preventDefault());
  el.addEventListener("drop", (e) => {
    e.preventDefault();
    const from = parseInt(document.querySelector('.fiche-exo[data-drag="1"]')?.dataset.i);
    const to = parseInt(el.dataset.i);
    if (!isNaN(from) && !isNaN(to) && from !== to) {
      const [m] = fiche.exercices.splice(from, 1);
      fiche.exercices.splice(to, 0, m);
      commit();
    }
  });
  return el;
}

function move(i, delta) {
  const j = i + delta;
  if (j < 0 || j >= fiche.exercices.length) return;
  [fiche.exercices[i], fiche.exercices[j]] = [fiche.exercices[j], fiche.exercices[i]];
  commit();
}

function commit(rerender = true) {
  if (rerender) renderFiche();
  saveDraft();
}

// méta -> fiche
function bindMeta() {
  $("#f-titre").oninput = (e) => { fiche.titre = e.target.value; saveDraft(); };
  $("#f-classe").oninput = (e) => { fiche.entete.classe = e.target.value; saveDraft(); };
  $("#f-date").onchange = (e) => { fiche.entete.date = e.target.value; saveDraft(); };
  $("#f-corrige").onchange = (e) => { fiche.mise_en_page.corrige = e.target.checked; saveDraft(); };
}

function syncMetaInputs() {
  $("#f-titre").value = fiche.titre || "";
  $("#f-classe").value = fiche.entete?.classe || "";
  $("#f-date").value = fiche.entete?.date || "";
  $("#f-corrige").checked = fiche.mise_en_page?.corrige !== false;
}

// ====================================================== ACTIONS FICHE ===== //
async function enregistrer() {
  if (!fiche.titre.trim()) { toast("Donne un titre à la fiche.", true); $("#f-titre").focus(); return; }
  if (!fiche.exercices.length) { toast("Ajoute au moins un exercice.", true); return; }
  try {
    const { slug } = await api("/api/fiche", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify(fiche),
    });
    toast(`Enregistré : ${slug}.json`);
  } catch (err) { toast("Échec : " + err.message, true); }
}

function nouvelle() {
  fiche = newFiche(); syncMetaInputs(); renderFiche(); saveDraft();
  toast("Nouvelle fiche");
}

function dupliquer() {
  fiche.titre = (fiche.titre || "Fiche") + " (copie)";
  // Nouvelles graines pour de vraies variantes — même fiche, valeurs renouvelées.
  fiche.exercices.forEach((ex) => { ex.seed = Math.floor(Math.random() * 1e9); });
  syncMetaInputs(); renderFiche(); toast("Fiche dupliquée — pense à enregistrer");
}

async function ouvrirCharger() {
  const { fiches } = await api("/api/fiches");
  const box = $("#fiche-list");
  box.innerHTML = fiches.length ? "" : "<p>Aucune fiche enregistrée pour l'instant.</p>";
  fiches.forEach((f) => {
    const it = document.createElement("div");
    it.className = "fiche-list-item";
    it.innerHTML = `<div class="meta"><strong>${escapeHtml(f.titre)}</strong><br>
      <small>${f.nb_exercices} exercice(s)${f.date ? " · " + f.date : ""}</small></div>`;
    const load = document.createElement("button"); load.className = "btn small primary"; load.textContent = "Ouvrir";
    load.onclick = async () => {
      fiche = await api("/api/fiche/" + f.slug);
      $("#modal-charger").classList.remove("open");
      syncMetaInputs(); renderFiche(); saveDraft();
      toast("Chargée : " + f.titre);
    };
    const del = document.createElement("button"); del.className = "btn small ghost"; del.textContent = "🗑";
    del.onclick = async () => {
      if (!confirm("Supprimer « " + f.titre + " » ?")) return;
      await api("/api/fiche/" + f.slug, { method: "DELETE" });
      ouvrirCharger();
    };
    it.append(load, del);
    box.appendChild(it);
  });
  $("#modal-charger").classList.add("open");
}

function simpleSlug(s) {
  return (s || "fiche").normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/[^\w\s-]/g, "").trim().toLowerCase().replace(/[\s_]+/g, "-") || "fiche";
}

async function genererPdfLocal() {
  if (!fiche.exercices.length) { toast("Aucun exercice dans la fiche.", true); return; }
  toast("Génération locale en cours…");
  try {
    const r = await fetch("/api/generate/pyromaths", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ fiche, vue: null }),
    });
    if (!r.ok) throw new Error((await r.json().catch(() => ({}))).detail || r.statusText);
    const blob = await r.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = simpleSlug(fiche.titre) + ".pdf";
    document.body.appendChild(a); a.click(); a.remove();
    URL.revokeObjectURL(url);
    toast("PDF téléchargé.");
  } catch (err) { toast("Échec : " + err.message, true); }
}

// ----------------------------------------------------------- brouillon --- //
function saveDraft() { try { localStorage.setItem(DRAFT_KEY, JSON.stringify(fiche)); } catch {} }
function loadDraft() {
  try {
    const d = JSON.parse(localStorage.getItem(DRAFT_KEY) || "null");
    if (d && d.exercices) fiche = d;
  } catch {}
}

// --------------------------------------------------------------- utils --- //
function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

// --------------------------------------------------------------- init ----- //
async function init() {
  loadDraft();
  bindMeta();
  $("#search").oninput = renderCatalogue;
  $("#btn-enregistrer").onclick = enregistrer;
  $("#btn-nouvelle").onclick = nouvelle;
  $("#btn-dupliquer").onclick = dupliquer;
  $("#btn-charger").onclick = ouvrirCharger;
  $("#modal-close").onclick = () => $("#modal-charger").classList.remove("open");
  $("#btn-pdf-local").onclick = genererPdfLocal;

  syncMetaInputs(); renderFiche();
  try { await loadCatalogue(); } catch (e) { toast("Catalogue indisponible : " + e.message, true); }
}

init();
