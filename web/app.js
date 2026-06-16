/* ===========================================================================
   FicheLab — logique de l'interface (vanilla JS, sans dépendance)
   État central = un manifeste de fiche, identique au format sauvegardé .json.
   =========================================================================== */
"use strict";

const $ = (sel) => document.querySelector(sel);
const api = (path, opts) => fetch(path, opts).then(async (r) => {
  if (!r.ok) throw new Error((await r.json().catch(() => ({}))).detail || r.statusText);
  return r.json();
});

// Petit jeton aléatoire (uuid / graine alea) — figé dans le manifeste.
const tok = (n = 5) =>
  Array.from(crypto.getRandomValues(new Uint8Array(Math.ceil(n / 2))))
    .map((b) => b.toString(16).padStart(2, "0")).join("").slice(0, n);

const DRAFT_KEY = "fichelab:draft";

// ---------------------------------------------------------------- état --- //
let CATALOGUE = { niveaux: [] };          // MathALEA
let PYROMATHS = null;                       // chargé paresseusement
let catalogueSource = "mathalea";           // "mathalea" | "pyromaths"
let activeLevel = null;
let currentVue = "eleve";
let previewTimer = null;

function newFiche() {
  return {
    version: 1,
    titre: "",
    entete: { classe: "", date: "", etablissement: "", consignes: "" },
    mise_en_page: { colonnes: 2, corrige: true, vue: "eleve" },
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
// Normalise les deux sources en : niveaux[{ niveau, label, themes:[{titre, exercices }] }]
// où chaque exercice = { source, key, code, titre } (key/code dépend de la source).
function normalizeCatalogue(source) {
  if (source === "mathalea") {
    return (CATALOGUE.niveaux || []).map((n) => ({
      niveau: n.niveau, label: n.label,
      themes: n.themes.map((t) => ({
        titre: t.titre,
        exercices: t.exercices.map((e) => ({ source: "mathalea", code: e.id, titre: e.titre })),
      })),
    }));
  }
  // pyromaths : un niveau = un seul groupe (pas de sous-thèmes)
  return (PYROMATHS?.niveaux || []).map((n) => ({
    niveau: n.niveau, label: n.niveau,
    themes: [{ titre: n.niveau, exercices: n.exercices.map((e) => ({ source: "pyromaths", code: e.name, titre: e.description })) }],
  }));
}

async function ensurePyromaths() {
  if (PYROMATHS === null) {
    PYROMATHS = { niveaux: [] };
    PYROMATHS = await api("/api/catalogue/pyromaths");
  }
}

async function loadCatalogue() {
  CATALOGUE = await api("/api/catalogue");
  activeLevel = CATALOGUE.niveaux[0]?.niveau || null;
  renderLevelTabs();
  renderCatalogue();
}

async function switchSource(src) {
  catalogueSource = src;
  $("#src-tabs").querySelectorAll("button").forEach((b) => b.classList.toggle("active", b.dataset.src === src));
  if (src === "pyromaths") {
    try { await ensurePyromaths(); } catch (e) { toast("Catalogue Pyromaths indisponible : " + e.message, true); }
  }
  const cat = normalizeCatalogue(src);
  activeLevel = cat[0]?.niveau || null;
  renderLevelTabs();
  renderCatalogue();
}

function renderLevelTabs() {
  const cat = normalizeCatalogue(catalogueSource);
  const box = $("#level-tabs");
  box.innerHTML = "";
  cat.forEach((n) => {
    const b = document.createElement("button");
    b.textContent = n.label;
    b.className = n.niveau === activeLevel ? "active" : "";
    b.onclick = () => { activeLevel = n.niveau; renderLevelTabs(); renderCatalogue(); };
    box.appendChild(b);
  });
}

function renderCatalogue() {
  const box = $("#catalogue");
  const q = $("#search").value.trim().toLowerCase();
  const cat = normalizeCatalogue(catalogueSource);
  const niveau = cat.find((n) => n.niveau === activeLevel);
  box.innerHTML = "";
  if (!niveau) return;

  niveau.themes.forEach((theme, ti) => {
    const exos = theme.exercices.filter((e) =>
      !q || e.titre.toLowerCase().includes(q) || e.code.toLowerCase().includes(q));
    if (!exos.length) return;

    const details = document.createElement("details");
    details.className = "theme";
    details.open = !!q || ti < 2 || catalogueSource === "pyromaths";
    const sum = document.createElement("summary");
    sum.innerHTML = `${escapeHtml(theme.titre)}<span class="count">${exos.length}</span>`;
    details.appendChild(sum);

    exos.forEach((e) => {
      const card = document.createElement("div");
      card.className = "exo-card";
      card.innerHTML = `<span class="code">${e.code}</span><span class="titre">${escapeHtml(e.titre)}</span>`;
      const add = document.createElement("button");
      add.className = "btn small icon add"; add.textContent = "＋"; add.title = "Ajouter à la fiche";
      add.onclick = () => addExercice(e);
      card.appendChild(add);
      details.appendChild(card);
    });
    box.appendChild(details);
  });
}

// ======================================================= FICHE (centre) === //
function addExercice(e) {
  if (e.source === "pyromaths") {
    fiche.exercices.push({
      source: "pyromaths", name: e.code, titre: e.titre,
      nb: 1, seed: Math.floor(Math.random() * 1e9), // graine figée -> reproductible
    });
  } else {
    fiche.exercices.push({
      source: "mathalea", id: e.code, titre: e.titre,
      n: 2, sup: {}, cd: null, uuid: tok(5), alea: tok(4),
    });
  }
  renderFiche(); schedulePreview(); saveDraft();
  toast(`Ajouté : ${e.code}`);
}

function renderFiche() {
  // méta
  $("#exo-count").textContent = fiche.exercices.length;
  $("#fiche-empty").style.display = fiche.exercices.length ? "none" : "block";

  const box = $("#fiche-exos");
  box.innerHTML = "";
  fiche.exercices.forEach((ex, i) => box.appendChild(renderExoRow(ex, i)));
}

function renderExoRow(ex, i) {
  const el = document.createElement("div");
  el.className = "fiche-exo"; el.draggable = true; el.dataset.i = i;
  const isPyro = ex.source === "pyromaths";
  const code = isPyro ? ex.name : ex.id;

  const ctrls = isPyro ? `
    <div class="ctrls">
      <span class="mini"><label>Nombre</label><input type="number" min="1" max="10" value="${ex.nb || 1}" data-f="nb"></span>
      <span class="mini"><label title="Graine = reproductibilité : même graine ⇒ exactement les mêmes énoncés à chaque génération.">Graine ⓘ</label><code title="Graine de tirage figée. Même graine ⇒ mêmes valeurs.">${ex.seed}</code>
        <button class="btn small icon" data-act="reseed" title="Nouveau tirage aléatoire (change les valeurs des énoncés).">🎲</button></span>
    </div>` : `
    <div class="ctrls">
      <span class="mini"><label>Questions</label><input type="number" min="1" max="30" value="${ex.n}" data-f="n"></span>
      <span class="mini"><label title="Graine = reproductibilité : même graine ⇒ exactement les mêmes énoncés à chaque génération.">Graine ⓘ</label><code title="Graine de tirage figée. Même graine ⇒ mêmes valeurs.">${ex.alea}</code>
        <button class="btn small icon" data-act="reseed" title="Nouveau tirage aléatoire (change les valeurs des énoncés).">🎲</button></span>
      <button class="btn small ghost" data-act="adv" title="Paramètres supplémentaires (s, s2, s3) propres à l'exercice MathALEA : variantes, niveaux de difficulté, options.">Réglages avancés ▾</button>
    </div>
    <div class="adv">
      <span class="mini"><label title="Paramètre « sup » MathALEA : type/variante de l'exercice (selon l'exercice).">s</label><input type="text" value="${ex.sup?.s ?? ""}" data-f="s"></span>
      <span class="mini"><label title="Paramètre « sup2 » MathALEA : 2ᵉ option (selon l'exercice).">s2</label><input type="text" value="${ex.sup?.s2 ?? ""}" data-f="s2"></span>
      <span class="mini"><label title="Paramètre « sup3 » MathALEA : 3ᵉ option (selon l'exercice).">s3</label><input type="text" value="${ex.sup?.s3 ?? ""}" data-f="s3"></span>
    </div>`;

  el.innerHTML = `
    <div class="row1">
      <span class="grip" title="Glisser pour réordonner">⠿</span>
      <span class="badge-src ${isPyro ? "pyromaths" : "mathalea"}">${isPyro ? "Pyromaths" : "MathALEA"}</span>
      <span class="code">${code}</span>
      <span class="titre">${escapeHtml(ex.titre || code)}</span>
      <button class="btn small icon" data-act="up" title="Monter">↑</button>
      <button class="btn small icon" data-act="down" title="Descendre">↓</button>
      <button class="btn small icon" data-act="del" title="Retirer">✕</button>
    </div>${ctrls}`;

  // actions communes
  el.querySelector('[data-act=del]').onclick = () => { fiche.exercices.splice(i, 1); commit(); };
  el.querySelector('[data-act=up]').onclick = () => move(i, -1);
  el.querySelector('[data-act=down]').onclick = () => move(i, +1);

  if (isPyro) {
    el.querySelector('[data-act=reseed]').onclick = () => { ex.seed = Math.floor(Math.random() * 1e9); commit(); };
    el.querySelector('[data-f=nb]').onchange = (e) => { ex.nb = parseInt(e.target.value) || 1; commit(false); };
  } else {
    el.querySelector('[data-act=reseed]').onclick = () => { ex.alea = tok(4); commit(); };
    el.querySelector('[data-act=adv]').onclick = (e) => {
      el.querySelector('.adv').classList.toggle('open');
      e.target.textContent = el.querySelector('.adv').classList.contains('open') ? "Réglages avancés ▴" : "Réglages avancés ▾";
    };
    el.querySelector('[data-f=n]').onchange = (e) => { ex.n = parseInt(e.target.value) || 1; commit(false); };
    ["s", "s2", "s3"].forEach((k) => {
      el.querySelector(`[data-f=${k}]`).onchange = (e) => {
        ex.sup = ex.sup || {};
        if (e.target.value.trim() === "") delete ex.sup[k];
        else ex.sup[k] = e.target.value.trim();
        commit(false);
      };
    });
  }

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

// rerender + preview + autosave
function commit(rerender = true) {
  if (rerender) renderFiche();
  schedulePreview(); saveDraft();
}

// méta -> fiche
function bindMeta() {
  $("#f-titre").oninput = (e) => { fiche.titre = e.target.value; saveDraft(); };
  $("#f-classe").oninput = (e) => { fiche.entete.classe = e.target.value; saveDraft(); };
  $("#f-date").onchange = (e) => { fiche.entete.date = e.target.value; saveDraft(); };
  $("#f-cols").onchange = (e) => { fiche.mise_en_page.colonnes = parseInt(e.target.value); schedulePreview(); saveDraft(); };
  $("#f-corrige").onchange = (e) => { fiche.mise_en_page.corrige = e.target.checked; schedulePreview(); saveDraft(); };
}

function syncMetaInputs() {
  $("#f-titre").value = fiche.titre || "";
  $("#f-classe").value = fiche.entete?.classe || "";
  $("#f-date").value = fiche.entete?.date || "";
  $("#f-cols").value = String(fiche.mise_en_page?.colonnes || 2);
  $("#f-corrige").checked = fiche.mise_en_page?.corrige !== false;
}

// ====================================================== APERÇU (droite) === //
function schedulePreview() {
  clearTimeout(previewTimer);
  previewTimer = setTimeout(refreshPreview, 500);
}

async function buildUrl(vue) {
  const { url } = await api("/api/fiche/preview", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ fiche, vue }),
  });
  return url;
}

function countBySource(src) {
  return fiche.exercices.filter((e) => (e.source || "mathalea") === src).length;
}

async function refreshPreview() {
  const hint = $("#preview-hint");
  if (!countBySource("mathalea")) {
    $("#preview").src = "about:blank";
    hint.style.display = "flex";
    hint.textContent = countBySource("pyromaths")
      ? "Aperçu live = MathALEA uniquement. Pour les exercices Pyromaths, utilise « PDF Pyromaths (local) »."
      : "L'aperçu apparaîtra ici dès qu'un exercice MathALEA est ajouté.";
    return;
  }
  try {
    const url = await buildUrl(currentVue);
    $("#preview").src = url;
    hint.style.display = "none";
  } catch (err) {
    hint.style.display = "flex"; hint.textContent = "Erreur d'aperçu : " + err.message;
  }
}

function bindViewTabs() {
  $("#view-tabs").querySelectorAll("button").forEach((b) => {
    b.onclick = () => {
      currentVue = b.dataset.vue;
      $("#view-tabs").querySelectorAll("button").forEach((x) => x.classList.toggle("active", x === b));
      refreshPreview();
    };
  });
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
  fiche = newFiche(); syncMetaInputs(); renderFiche(); refreshPreview(); saveDraft();
  toast("Nouvelle fiche");
}

function dupliquer() {
  fiche.titre = (fiche.titre || "Fiche") + " (copie)";
  // Nouvelles graines pour de vraies variantes : la graine qui détermine les
  // valeurs est `alea` (MathALEA) ou `seed` (Pyromaths) — régénérer le seul
  // `uuid` laissait des énoncés identiques.
  fiche.exercices.forEach((ex) => {
    ex.uuid = tok(5);
    if ((ex.source || "mathalea") === "pyromaths") {
      ex.seed = Math.floor(Math.random() * 1e9);
    } else {
      ex.alea = tok(4);
    }
  });
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
      syncMetaInputs(); renderFiche(); refreshPreview(); saveDraft();
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

async function genererPdf() {
  if (!countBySource("mathalea")) { toast("Aucun exercice MathALEA.", true); return; }
  const url = await buildUrl("latex");
  window.open(url, "_blank");
  toast("Page LaTeX ouverte — clique sur « Compiler / Télécharger PDF ».");
}

function simpleSlug(s) {
  return (s || "fiche").normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/[^\w\s-]/g, "").trim().toLowerCase().replace(/[\s_]+/g, "-") || "fiche";
}

async function genererPdfLocal() {
  if (!countBySource("pyromaths")) { toast("Aucun exercice Pyromaths dans la fiche.", true); return; }
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
    toast("PDF Pyromaths téléchargé.");
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
  bindMeta(); bindViewTabs();
  $("#search").oninput = renderCatalogue;
  $("#btn-enregistrer").onclick = enregistrer;
  $("#btn-nouvelle").onclick = nouvelle;
  $("#btn-dupliquer").onclick = dupliquer;
  $("#btn-charger").onclick = ouvrirCharger;
  $("#modal-close").onclick = () => $("#modal-charger").classList.remove("open");
  $("#btn-refresh").onclick = refreshPreview;
  $("#btn-onglet").onclick = async () => window.open(await buildUrl(currentVue), "_blank");
  $("#btn-pdf").onclick = genererPdf;
  $("#btn-pdf-local").onclick = genererPdfLocal;
  $("#src-tabs").querySelectorAll("button").forEach((b) => { b.onclick = () => switchSource(b.dataset.src); });

  syncMetaInputs(); renderFiche();
  try { await loadCatalogue(); } catch (e) { toast("Catalogue indisponible : " + e.message, true); }
  refreshPreview();
}

init();
