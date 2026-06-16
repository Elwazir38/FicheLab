# Programme de mathématiques — Seconde générale et technologique

> Référentiel officiel : **arrêté du 17 juillet 2018** (BO spécial n°1 du
> 22 juillet 2018), modifié par l'**arrêté du 17 janvier 2019** (BOEN spécial
> n°1 du 22 janvier 2019). Source secondaire utilisée pour cette synthèse :
> page Eduscol *Programmes et ressources en mathématiques voie GT*
> (`eduscol.education.fr/2068/`) — le PDF officiel n'a pu être récupéré
> automatiquement (certificat / 403), structure néanmoins canonique et stable.
> Ce document valide la cohérence du niveau "Seconde" exposé par Pyromaths
> dans FicheLab (11 exercices publics tagués "Seconde").

## Grands domaines

Le programme s'organise en **4 domaines de contenu** + un volet transversal
*Algorithmique et programmation*. Synthèse à grain compétence-clef.

### 1. Nombres et calculs
- **1.1 Ensembles de nombres** — ℕ, ℤ, 𝔻, ℚ, ℝ ; inclusions ; appartenance.
- **1.2 Intervalles de ℝ** — notations, réunion, intersection, valeur absolue
  comme distance ; encadrements, approximations.
- **1.3 Calcul numérique et littéral** — puissances (entières relatives),
  racines carrées, identités remarquables ; développer, factoriser, réduire ;
  fractions, opérations sur les puissances.
- **1.4 Équations et inéquations** — du **premier degré** à une inconnue ;
  inéquation produit / quotient avec **tableau de signes** ; résolution
  graphique d'équations f(x)=k et f(x)=g(x).
- **1.5 Proportions et pourcentages** — proportion, proportion d'une
  proportion, évolutions, taux d'évolution, coefficient multiplicateur,
  évolutions successives / réciproques.

### 2. Géométrie
- **2.1 Repérage dans le plan** — repère orthonormé, coordonnées d'un point,
  **distance entre deux points**, **coordonnées du milieu** d'un segment.
- **2.2 Vecteurs du plan** — définition (translation), égalité vectorielle,
  **somme**, produit par un réel, colinéarité ; coordonnées d'un vecteur
  dans un repère ; norme.
- **2.3 Droites du plan** — vecteur directeur, équation cartésienne, équation
  réduite y=mx+p, parallélisme, intersection.
- **2.4 Géométrie classique** — configurations du plan (triangles, cercles,
  Thalès, Pythagore consolidés), démonstration.
- **2.5 Trigonométrie** — **cercle trigonométrique**, enroulement de la
  droite réelle, cosinus et sinus d'un réel ; angles remarquables.

### 3. Fonctions
- **3.1 Généralités** — image, antécédent, ensemble de définition, **courbe
  représentative**, parité (paire/impaire, lecture graphique).
- **3.2 Variations et extrema** — **sens de variation**, **tableau de
  variations**, extremum local / global, **lecture graphique** des
  variations et des extrema.
- **3.3 Fonctions de référence** — affine, carré, inverse, racine carrée,
  cube ; variations, courbes, comparaison d'images via la monotonie.
- **3.4 Équations / inéquations associées** — résolution graphique et
  algébrique ; signe d'une fonction affine, du trinôme du second degré sous
  forme factorisée (le second degré général est en 1re Spé).

### 4. Statistiques et probabilités
- **4.1 Statistique descriptive** — séries univariées, indicateurs de
  position (moyenne, médiane, quartiles) et de dispersion (étendue,
  écart-interquartile, écart-type) ; **histogrammes** et diagrammes en boîte.
- **4.2 Probabilités** — vocabulaire (univers, événement, contraire,
  réunion, intersection), équiprobabilité, calculs ; modélisation d'une
  expérience aléatoire ; échantillonnage et fluctuation.

### 5. Algorithmique et programmation (transversal)
- Variables, affectations, instructions conditionnelles, boucles bornées et
  non bornées, fonctions ; mise en œuvre en **Python**.

## Audit des 11 exercices Pyromaths "Seconde"

Source : `engines/pyromaths/pyromaths/ex/lycee/` — classes publiques portant
`tags = [..., "Seconde", ...]`.

| # | Classe (fichier) | Description | Verdict | Justification |
|---|---|---|---|---|
| 1 | `cercle_trigonometrique` (CercleTrigo.py) | Cercle trigonométrique, radians, angles remarquables | ✓ Seconde | Trigonométrie / cercle trigo introduits en 2nde (§2.5). |
| 2 | `BilanTrinomeSansDiscriminant` (SecondDegre.py) | Bilan trinômes — formes, inéquation, tableau de signes, variations (**sans** discriminant) | ✓ Seconde | Le trinôme apparaît en 2nde via forme factorisée et tableau de signes ; le discriminant lui-même est 1re Spé (toutes les autres classes Sd*FormeCanonique, Racines… sont taguées "1re Spé math"). |
| 3 | `InequationPremierDegre` (inequations.py) | Résoudre une inéquation du 1er degré | ✓ Seconde | Inéquations 1er degré, intervalles (§1.4). |
| 4 | `CoupleInequationsPremierDegre` (inequations.py) | Résoudre un système / couple d'inéquations du 1er degré | ✓ Seconde | Idem §1.4, sous forme d'intersection d'intervalles. |
| 5 | `vecteurs_add` (Vecteurs.py) | Somme de vecteurs (lecture graphique) | ✓ Seconde | Vecteurs et somme : cœur du §2.2. |
| 6 | `BilanDistanceMilieu` (reperage.py) | Distances et coordonnées du milieu | ✓ Seconde | Repérage §2.1 exactement. |
| 7 | `Vf1SensEtTableau` (VariationsFonctions.py) | Sens et tableau de variations | ✓ Seconde | §3.2. |
| 8 | `Vf2ExtremaGraphiques` (VariationsFonctions.py) | Extrema et représentation graphique | ✓ Seconde | §3.2 (lecture graphique). |
| 9 | `Vf3VariationVersCourbe` (VariationsFonctions.py) | Tableau de variations → courbe | ✓ Seconde | §3.2. |
| 10 | `Vf4ComparerImages` (VariationsFonctions.py) | Comparer des images à partir du sens de variation | ✓ Seconde | §3.2-3.3, exploitation monotonie. |
| 11 | `Vf5Extrema_Tableau` (VariationsFonctions.py) | Extrema locaux à partir d'un tableau de variations | ✓ Seconde | §3.2. |

**Bilan : 11 ✓ / 0 ⚠ / 0 ✗.** Aucun faux Seconde détecté. Le tag est
cohérent ; les exercices "limites", trinôme avec discriminant, dérivation,
suites, matrices, polynômes degré ≥ 2 sont bien taguées "1re Spé math" ou
"Tle" dans le même dossier.

## Trous identifiés (compétences Seconde sans exercice Pyromaths)

Domaines du programme non couverts par les 11 exercices natifs :

- **Nombres & calculs** — ensembles de nombres (ℕ⊂ℤ⊂…), intervalles &
  valeur absolue, puissances, racines carrées, identités remarquables,
  développement/factorisation littérale.
- **Proportions et pourcentages** — taux d'évolution, évolutions
  successives, coefficient multiplicateur (présent côté Pyromaths mais
  tagué "1re technologique" dans `automatismes1techno.py`, pas "Seconde").
- **Géométrie / droites du plan** — équation de droite, vecteur directeur,
  colinéarité (le module Vecteurs ne couvre que la somme).
- **Fonctions de référence** — carré, inverse, racine, cube : pas
  d'exercice dédié aux courbes/variations de ces fonctions nommées.
- **Équations / inéquations produits ou quotients** — tableau de signes
  d'un produit de facteurs affines.
- **Statistiques descriptives** — indicateurs de position/dispersion ;
  l'unique exercice `_Histogramme` est privé (préfixe `_`) donc non exposé.
- **Probabilités** — totalement absent.
- **Algorithmique / Python** — totalement absent (cohérent : Pyromaths
  produit du PDF, pas du code).

## Recommandations pour FicheLab

1. **Garder les 11 exercices tels quels sous le label "Seconde"** : la
   classification Pyromaths est saine, aucun reclassement nécessaire.
2. **Prévenir Rachid sur les angles morts majeurs** : *probabilités*,
   *statistique descriptive*, *droites du plan*, *fonctions de référence*,
   *pourcentages/évolutions*. Ce sont les chapitres où Pyromaths seul ne
   suffit pas pour couvrir l'année.
3. **Réactiver `_Histogramme`** (le dégriffer en `Histogramme`) si on veut
   un point d'entrée stats en Seconde — c'est le seul levier interne
   immédiat. À vérifier côté qualité avant exposition.
4. **Tag de second degré sans discriminant** (`BilanTrinomeSansDiscriminant`)
   : OK en Seconde mais à surveiller — c'est la zone limite où certains
   profs préfèrent attendre la 1re. Pas un défaut, juste à connaître.
5. **Roadmap moteur** : si on veut compléter, la priorité côté FicheLab
   est soit (a) d'ajouter quelques générateurs Python maison dans le style
   Pyromaths pour les chapitres manquants ci-dessus (proba simple, stats,
   droites du plan : tout est faisable à coût raisonnable), soit (b) de
   pousser la phase 4 prévue (pipeline LM Studio + Gemma/Qwen-Coder pour
   les contextes d'énoncés textuels et le boilerplate). Probas et stats
   sont l'angle mort le plus urgent.
