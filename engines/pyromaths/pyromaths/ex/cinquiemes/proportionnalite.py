# Pyromaths
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
# Copyright (C) 2006 -- Jérôme Ortais (jerome.ortais@pyromaths.org)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
#
from random import randint, randrange
import textwrap

from pyromaths.outils.decimaux import decimaux
from pyromaths.ex import LegacyExercise

def _exo_echelles():
    """À partir d'un plan tracé, déterminer l'échelle et des longueurs déterminées."""

    # Échelle
    echelle = [ 100, 250, 400, 500, 750, 1000][randrange(6)]

    # figure : un plan d'appartement dessiné en TikZ
    a, d = randint(40, 60), randint(36, 45)
    b, c = randint(8, d - 27), randint(9, a - 25)
    xF = a - c
    xE = xF - 6
    yK = b + 9
    yF = b - 6
#     yH = b
    # Calculs des grandeurs réelles en mm !
    reels = [echelle * a, echelle * b, echelle * c, echelle * d]

    plan = [a, b, c, d]
    # choix permet de choisir si on donne a, b, c ou d en énoncé
    choix = randrange(4)
    reponses = ["a", "b", "c", "d"]
    enonce = reponses.pop(choix)

    # sur la deuxième ligne du tableau, on écrit en cm, en gras, les nombres calculés
    tab_reels = [ "\\bf"*(i != choix) + decimaux(reels[i] / 10) for i in range(4)]

    # Pour placer les quatre lettres sur le plan
    cotation_couleur = [["a", ""],
                        ["b", ""],
                        ["c", ""],
                        ["d", ""]]
        # la longueur donnée est tracée en bleu
    cotation_couleur[choix][1] = "enonce"

    figure = textwrap.dedent(fr"""\
            \definecolor{{enonce}}{{rgb}}{{0.11,0.56,0.98}}
            \begin{{center}}
            \begin{{tikzpicture}}[Maroon, line width=.5pt, y=.1cm, x=.1cm]
            % Le rectangle ABCD
            \coordinate (A) at (0, 0);
            \coordinate (B) at ({a}, 0);
            \coordinate (C) at ({a}, {d});
            \coordinate (D) at (0, {d});
            \draw[line width=1pt] (A) rectangle (C);
            % Les points permettant de placer les cloisons
            \coordinate (E1) at ({xE}, 0);
            \coordinate (E2) at ({xE}, {yF});
            \coordinate (F1) at ({xF}, 0);
            \coordinate (F2) at ({xF}, {yF});
            \coordinate (G1) at ({a}, {b});
            \coordinate (G2) at ({xF}, {b});
            \coordinate (G3) at ({xF}, {25});
            \coordinate (H1) at ({xE}, {b});
            \coordinate (H2) at ({xE}, {25});
            \coordinate (H3) at ({xE}, {yK});
            \coordinate (H4) at ({15}, {yK});
            \coordinate (K2) at (0, {yK});
            \coordinate (K1) at (7, {yK});
            \coordinate (J1) at ({xE}, {d-7});
            \coordinate (J2) at ({xE}, {d});
            \coordinate (J3) at ({xF}, {d-7});
            \coordinate (J4) at ({xF}, {d});
            % Trace les cloisons, limitées par des tirets
            \draw (G1) -- (G2);
            \draw[-|] (E1) -- (E2);
            \draw[-|] (F1) -- (F2);
            \draw[|-] (J1) -- (J2);
            \draw[|-] (J3) -- (J4);
            \draw[|-] (K1) -- (K2);
            \draw[|-|] (G3) -- ($(G2)-(0, .2)$);
            \draw[|-|] (H1) -- (H2);
            \draw[-|] (H3) -- (H4);
            % # place les cotations sr la figure, l'énoncé en bleu
            \draw[Stealth-Stealth, dashed, {cotation_couleur[0][1]}] ([yshift=5]D) -- ([yshift=5]C) node[midway, above, black]{{ {cotation_couleur[0][0]} }};
            \draw[Stealth-Stealth, dashed, {cotation_couleur[1][1]}] ([xshift=5]B) -- ([xshift=5]G1) node[midway, right, black]{{ {cotation_couleur[1][0]} }};
            \draw[Stealth-Stealth, dashed, {cotation_couleur[2][1]}] ([yshift=-5]B) -- ([yshift=-5]F1) node[midway, below, black]{{ {cotation_couleur[2][0]} }};
            \draw[Stealth-Stealth, dashed, {cotation_couleur[3][1]}] ([xshift=-5]A) -- ([xshift=-5]D) node[midway, left, black]{{ {cotation_couleur[3][0]} }};
            \end{{tikzpicture}}
            \end{{center}}
            """)


    exo = [_(u"\\exercice Sur ce plan, la longueur $%s$ mesure en réalité \\SI{%s}{m} :\n") % (enonce, decimaux(reels[choix] / 1000))] \
           + [figure] \
           + ["\\begin{enumerate}",
           _(u"\\item Déterminer l'échelle de ce plan."),
           _(u"\\item Déterminer les longueurs réelles $%s$, $%s$ et $%s$.") % (reponses[0], reponses[1], reponses[2]),
            "\\end{enumerate}"]
    cor = [_(u"\\exercice* Sur ce plan, la longueur $%s$ mesure en réalité \\SI{%s}{m} : \n") % (enonce, decimaux(reels[choix] / 1000))] \
           + [figure] \
           + ["\\begin{enumerate}",
           _(u"\\item Déterminer l'échelle de ce plan.\\par"),
           _(u"Sur le plan, je mesure que $%s=\\SI{%s}{cm}$.\\par") % (enonce, decimaux(plan[choix] / 10)),
           _(u"Or on sait que en réalité $%s = \\SI{%s}{m} = \\SI{%s}{cm}$") % (enonce, decimaux(reels[choix] / 1000), decimaux(reels[choix] / 10)),
           _(u" et  $%s \\div %s = %s$.\\par") % (decimaux(reels[choix]), decimaux(plan[choix]), decimaux(echelle)),
           _(u"L'échelle de ce plan est donc $1/%s^e$.") % echelle,
           _(u"\\item Déterminer les longueurs réelles $%s$, $%s$ et $%s$.\n") % (reponses[0], reponses[1], reponses[2]),
           _(u"Grâce à la question précédente, je peux compléter le tableau :\n"),
           "\\begin{tabular}{|l|c|c|c|c|c}",
           ("\\multicolumn{1}{c}{}" + "&\\multicolumn{1}{c}{$%s$}"*4 + "\\\\") % ("a", "b", "c", "d"),
           "\\cline{1-5}",
           _("Sur le plan (en cm)  & %s & %s & %s & %s &\stepcounter{tikzmark}\\tikzmark{plan1}\\\\") % tuple([decimaux(n / 10) for n in plan]),
           "\\cline{1-5}",
           _(u"En réalité (en cm)  & %s & %s & %s & %s &\\tikzmark{plan2}%%") % tuple(tab_reels),
           fr"\tikz[overlay, Maroon, remember picture, line width=1pt, -Stealth, rounded corners=.5em] \draw (pic cs:plan1) -- ++(.5, 0) -- node[right]{{$\times {echelle}$}} ++(0, -.5) -- (pic cs:plan2); %",
           "\\\\",
           "\\cline{1-5}",
           "\\end{tabular}\n",
           _(u"Pour conclure, on convertit ses longueurs en m :\\par"),
           "$$a = \\SI{%s}{m} \\quad ; \\quad b = \\SI{%s}{m} \\quad ; \\quad c  = \\SI{%s}{m} \\quad ; \\quad d =\\SI{%s}{m}$$"\
                   % tuple([decimaux(n / 1000) for n in reels]),
           "\\end{enumerate}"]

    return exo, cor

class exo_echelles(LegacyExercise):
    """Échelles"""

    tags = [
        "Cinquième",
        "proportionnalité",
        "échelle",
    ]
    function = _exo_echelles


def exo_fruits():
    fruit = [_("Cerises"), _("Tomates"), _("Pommes"), _("Poires"), _("Raisin"), _("Oranges")][randrange(6)]
    while 1:
        a, b, c = randint(10, 50) / 10, randint(10, 50) / 10, randint(10, 50) / 10
        if a != b and a != c and b != c:
            break
    tarif = randint(20, 50) / 10
    fruits_c = (fruit, a, b, c)
    fruits_e = (fruit, decimaux(a), decimaux(b), "")
    prix_c = (_("prix"), decimaux(fruits_c[1] * tarif), decimaux(fruits_c[2] * tarif), decimaux(fruits_c[3] * tarif))
    prix_e = (_("prix"), decimaux(fruits_c[1] * tarif), "", decimaux(fruits_c[3] * tarif))

    fruits_c = (fruit, decimaux(a), decimaux(b), decimaux(c))
    tableau_exo = ["\\begin{tabular}{|l|c|c|c|}",
               "\hline",
               _(u"%s (en kg) & %s & %s &  %s  \\\\") % fruits_e,
               "\hline",
               _(u"%s (en \\euro)  & %s &  %s  & %s \\\\") % prix_e,
               "\hline",
               "\\end{tabular}"]
    tableau_cor = ["\\begin{tabular}{|l|c|c|c|}",
               "\hline",
               _(u"%s (en kg) & %s & %s &  \\bf %s  \\\\") % fruits_c,
               "\hline",
               _(u"%s (en \\euro)  & %s &  \\bf %s  & %s \\\\") % prix_c,
               "\hline",
               "\\end{tabular}"]
    exo = [_(u"\\exercice Le prix à payer est proportionnel à la masse de fruits achetés.\\par"),
           _(u"Détermine la valeur des cases vides")]
    cor = [_(u"\\exercice Le prix à payer est proportionnel à la masse de fruits achetés.\\par"),
           _(u"Détermine la valeur des cases vides")]
    exo += ["\n"] + tableau_exo
    cor += ["\n"] + tableau_cor
    cor.append("$$\\frac{%s \\times %s}{%s} = %s \\quad;\\qquad" % (prix_e[1], fruits_e[2], fruits_e[1], prix_c[2]))
    cor.append("\\frac{%s \\times %s}{%s} = %s $$" % (fruits_c[1], prix_c[3], prix_e[1], fruits_c[3]))

    return (exo, cor)
