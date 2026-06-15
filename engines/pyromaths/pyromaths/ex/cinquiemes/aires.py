#!/usr/bin/env python3
#
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

import random
import textwrap

from pyromaths.outils.decimaux import decimaux
from pyromaths.ex import LegacyExercise

#
# ------------------- Aire de disques -------------------
#


def arrondir(nombre):
    [partie_entiere, partie_decimale] = nombre.split(".")
    return int(partie_entiere) + (int(partie_decimale[0]) >= 5)


def _exo_aire_diques():
    exo = ["\\exercice"]
    cor = ["\\exercice*"]
    rayon1 = 2 * (random.randrange(33) + 1)
    rayon2 = int(1.5 * rayon1)
    i = random.randrange(2)
    if i == 0:
        donnees = (_('rayons'), rayon1, rayon2)
    else:
        donnees = (_(u'diamètres'), 2 * rayon1, 2 * rayon2)
    difference_des_carres = rayon2 ** 2 - rayon1 ** 2
    aire_arrondie = arrondir(str(3.14 * difference_des_carres))
    enonce = \
        textwrap.dedent(r"""
            \begin{minipage}{4cm}
            \begin{tikzpicture}[thick]
            \fill[Peru, draw=Maroon] (0,0) circle (1.5);
            \fill[White, draw=Maroon] (0,0) circle (1);
            \draw (0, 0) node{$\times$} node[above right]{$O$};
            \end{tikzpicture}
            \end{minipage}\hfill"""
            ) + _("""
\\begin{minipage}{13cm}
On considère deux cercles de centre $O$ et de %s respectifs $\\SI{%s}{cm}$ et $\\SI{%s}{cm}$.\\par
Calculer l'aire de la couronne circulaire (partie colorée) comprise entre les deux cercles en arrondissant le résultat au $\\si{cm^2}$ le plus proche.""") % donnees
    exo.append(enonce)
    cor.append(enonce)
    cor.append(_("\\par\\dotfill{}\\\\\n"))
    if i == 0:
        cor.append(_(u"On calcule l'aire du disque de rayon $\\SI{%s}{cm}$:") % rayon2)
        cor.append(_(u"\\[\\pi \\times %s^2 = \\pi \\times %s \\times %s = %s\\pi\\si{cm^2}\\]") % (rayon2, rayon2, rayon2, decimaux(rayon2 ** 2)))
        cor.append(_(u"On calcule l'aire du disque de rayon $\\SI{%s}{cm}$:") % rayon1)
        cor.append(_(u"\\[ \\pi \\times %s^2 = \\pi \\times %s \\times %s = %s \\pi\\si{cm^2}\]") % (rayon1, rayon1, rayon1, decimaux(rayon1 ** 2)))
    else:
        cor.append(_(u"Un disque de diamètre $\\SI{%s}{cm}$ a pour rayon $%s \div 2 = \\SI{%s}{cm}$. Calculons son aire:") % (2 * rayon2, 2 * rayon2, rayon2))
        cor.append(_(u"\\[\\pi \\times %s^2 = \\pi \\times %s \\times %s = %s \\pi\\si{cm^2}\\]") % (rayon2, rayon2, rayon2, decimaux(rayon2 ** 2)))
        cor.append(_(u"Un disque de diamètre $\\SI{%s}{cm}$ a pour rayon $%s \div 2 = \\SI{%s}{cm}$. Calculons son aire:") % (2 * rayon1, 2 * rayon1, rayon1))
        cor.append(_(u"\\[\\pi \\times %s^2 = \\pi \\times %s \\times %s = %s \\pi\\si{cm^2}\\]") % (rayon1, rayon1, rayon1, decimaux(rayon1 ** 2)))
    cor.append(_(u"L'aire $\\mathcal{A}$ de la couronne est obtenue en retranchant l'aire du disque de rayon  $\\SI{%s}{cm}$  à l'aire du disque de rayon  $\\SI{%s}{cm}$:") % (rayon1, rayon2))
    cor.append(u"\\[\\mathcal{A} = %s \\pi  - %s \\pi= (%s - %s)\\pi =%s \\pi\\si{cm^2}\\]" % (decimaux(rayon2 ** 2), decimaux(rayon1 ** 2), decimaux(rayon2 ** 2), decimaux(rayon1 ** 2), decimaux(difference_des_carres)))
    cor.append(_(u"L'aire exacte de la couronne est $%s \\pi\\si{cm^2}$.") % (decimaux(difference_des_carres)))
    cor.append(_(u"En prenant 3,14 comme valeur approchée du nombre $\\pi$, on obtient :"))
    cor.append(u"\\[\\mathcal{A}  \\simeq %s \\times 3,14\\]" % decimaux(difference_des_carres))
    cor.append(u"\\[\\boxed{\\mathcal{A} \\simeq  \\SI{%s}{cm^2}}\\]" % decimaux(aire_arrondie))
    exo.append("\\end{minipage}\n")
    cor.append("\\end{minipage}\n")
    return (exo, cor)

class exo_aire_diques(LegacyExercise):
    """Aire de disques"""

    tags = [
        "Cinquième",
        "aires",
        "géométrie",
    ]
    function = _exo_aire_diques
