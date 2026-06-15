#!/usr/bin/env python3

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

from math import atan, cos, pi, sin
from pyromaths.ex import LegacyExercise

#===============================================================================
# Symétrique d'une figure par rapport à une droite avec quadrillage
#===============================================================================


def valeurs_quad2(nb_pts):
    vals = []
    for i in range(nb_pts):
        angle = random.randrange(i * 360 // nb_pts, (i + 1) * 360 // nb_pts)
        vals.append(random.randrange(1, 7) / 2 * cos(angle * pi / 180), random.randrange(1, 7) / 2 * sin(angle * pi / 180))
    return vals


def valeurs_quad(nb_pts):
    vals = []
    for i in range(nb_pts):
        (alpha, beta) = ((i * 360) // nb_pts, ((i + 1) * 360) // nb_pts)
        (x, y, angle) = (0, 0, 0)
        while x == 0 or angle < alpha or angle > beta:
            (x, y) = (random.randrange(-6, 7) * .5, random.randrange(-6,
                      7) * .5)
            if x > 0:
                angle = int(atan(y / x) * 180 / pi + 360) % 360
            if x < 0:
                angle = int(atan(y / x) * 180 / pi + 180)
        vals.append((x, y))
    return vals


def centre_sym(vals):
    fin = 0
    while not fin:
        (fin, cpt) = (1, 0)
        (o1, o2) = (random.randrange(-6, 7) * .5, random.randrange(-6, 7) *
                    .5)
        while fin and cpt < len(vals):
            fin = fin and -3 <= 2 * o1 - vals[cpt][0] <= 3 and -3 <= 2 * \
                o2 - vals[cpt][1] <= 3
            cpt = cpt + 1
    return (o1, o2)


def place_pts(vals, O):
    txt = r"\draw[Maroon, line width=1pt] "
    for coord in vals:
        txt += f"{coord} -- "
    txt += "cycle;\n"
    txt += fr"\draw {O} node{{$\times$}} node[right]{{$O$}};"
    return txt


def place_pts_sym(vals, O):
    txt = r"\draw[black, line width=1pt, dashed] "
    for coord in vals:
        txt += f"($2*{O}-{coord}$) -- "
    txt += "cycle;\n"
    return txt


def exo_quadrillage(f0, f1):
    pass


def _symetrie():
    exo = ["\\exercice",
           _(u"Construire la symétrique de chacune des figures par rapport au point O en"),
           _("utilisant le quadrillage :\\par")]
    cor = ["\\exercice*",
           _(u"Construire la symétrique de chacune des figures par rapport au point O en"),
           _("utilisant le quadrillage :\\par")]
    nbpts = 5
    langles = [0, 90, 45, 135]
    for i in range(3):
        langles.pop(random.randrange(len(langles)))
        vals = valeurs_quad(nbpts)
        O = centre_sym(vals)
        txt = r"""\begin{tikzpicture}[scale=.9]
            \draw[thick, Olive, step=.5] (-3, -3) grid (3, 3);
        """ + place_pts(vals, O)
        exo.append(txt)
        cor.append(txt)
        cor.append(place_pts_sym(vals, O))
        cor.append(r"\end{tikzpicture}")
        exo.append(r"\end{tikzpicture}")
        if i < 2:
            exo.append("\\hfill")
            cor.append("\\hfill")
    return (exo, cor)

class symetrie(LegacyExercise):
    """Symétrie centrale"""

    tags = [
        "Cinquième",
        "géométrie",
        "symétrie",
        "tracé",
    ]
    function = _symetrie
