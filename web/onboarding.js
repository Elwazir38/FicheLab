/* ===========================================================================
   FicheLab — couche de prise en main (additive, réversible)
   Charge APRÈS app.js. Ne touche pas à l'état `fiche` ni à la logique métier.
   - Panneau de bienvenue (1re visite) réutilisant .modal / .modal-back
   - Bouton « ⓘ Guide » dans la topbar pour le rouvrir à tout moment
   - Fermeture clavier (Échap) + clic hors-modal, gérées localement
   100% offline : aucun CDN, aucune police distante. Vanilla.
   =========================================================================== */
"use strict";

(function onboarding() {
  const KEY = "fichelab:onboarded";

  // --- markup du panneau, injecté une seule fois -------------------------- //
  const back = document.createElement("div");
  back.className = "modal-back";
  back.id = "modal-guide";
  back.setAttribute("role", "dialog");
  back.setAttribute("aria-modal", "true");
  back.setAttribute("aria-labelledby", "guide-title");
  back.innerHTML = `
    <div class="modal guide-modal">
      <button class="guide-x btn ghost small" id="guide-close-x" aria-label="Fermer le guide" title="Fermer">✕</button>
      <h3 id="guide-title">Bienvenue dans FicheLab 👋</h3>
      <p class="guide-lead">Compose une fiche d'exercices de maths prête à imprimer en
        <strong>trois temps</strong>. Voici le parcours :</p>

      <ol class="guide-steps">
        <li>
          <span class="gs-num">1</span>
          <div class="gs-body">
            <strong>Choisis des exercices</strong> dans le <em>Catalogue</em> (colonne de gauche).
            Filtre par niveau ou par recherche, puis clique sur <span class="gs-kbd">＋</span> pour
            ajouter un exercice à ta fiche.
          </div>
        </li>
        <li>
          <span class="gs-num">2</span>
          <div class="gs-body">
            <strong>Règle ta fiche</strong> au centre : titre, classe, nombre de questions, corrigé,
            ordre des exercices (glisser-déposer). La <em>graine</em> rend la fiche reproductible —
            même graine, mêmes énoncés.
          </div>
        </li>
        <li>
          <span class="gs-num">3</span>
          <div class="gs-body">
            <strong>Génère le PDF</strong> depuis la colonne <em>Génération</em> (à droite). Le moteur
            <strong>Pyromaths</strong> produit énoncés + corrigés détaillés <strong>en local</strong>,
            avec ton style maison. <em>Nécessite une chaîne LaTeX</em> (MiKTeX ou TeX Live).
          </div>
        </li>
      </ol>

      <p class="guide-tip">Astuce : tu peux rouvrir ce guide à tout moment via le bouton
        <span class="gs-kbd">ⓘ Guide</span> en haut.</p>

      <div class="guide-foot">
        <button class="btn primary" id="guide-start">C'est parti</button>
      </div>
    </div>`;
  document.body.appendChild(back);

  // --- ouverture / fermeture ---------------------------------------------- //
  let lastFocus = null;

  function open() {
    lastFocus = document.activeElement;
    back.classList.add("open");
    document.addEventListener("keydown", onKey);
    // focus sur le bouton d'action principal (accessibilité clavier)
    const start = back.querySelector("#guide-start");
    if (start) start.focus();
  }

  function close() {
    back.classList.remove("open");
    document.removeEventListener("keydown", onKey);
    try { localStorage.setItem(KEY, "1"); } catch (e) {}
    if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
  }

  function onKey(e) {
    if (e.key === "Escape") { e.stopPropagation(); close(); }
  }

  // clic hors-modal (sur le fond) ferme — comme les autres modales du projet
  back.addEventListener("click", (e) => { if (e.target === back) close(); });
  back.querySelector("#guide-close-x").onclick = close;
  back.querySelector("#guide-start").onclick = close;

  // bouton persistant dans la topbar
  const btn = document.getElementById("btn-guide");
  if (btn) btn.onclick = open;

  // --- 1re visite : ouverture automatique --------------------------------- //
  // (échappatoire « ?guide=skip » : utile pour démos / captures, sans rien casser)
  const skip = new URLSearchParams(location.search).get("guide") === "skip";
  let seen = "1";
  try { seen = localStorage.getItem(KEY); } catch (e) { seen = "1"; }
  if (!seen && !skip) open();
})();
