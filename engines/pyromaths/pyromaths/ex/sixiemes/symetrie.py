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
from math import atan, cos, pi, sin
from pyromaths.ex import LegacyExercise


# ===============================================================================
# Symétrique d'une figure par rapport à une droite avec quadrillage
# ===============================================================================


def valeurs_quad2(nb_pts):
    vals = []
    for i in range(nb_pts):
        angle = random.randrange(i * 360 // nb_pts, (i + 1) * 360 // nb_pts)
        vals.append((random.randrange(1, 7) * .5 * cos(angle * pi / 180),
                     random.randrange(1, 7) * .5 * sin(angle * pi / 180)))
    return vals


def valeurs_quad(nb_pts):
    vals = []
    for i in range(nb_pts):
        (alpha, beta) = ((i * 360) // nb_pts, ((i + 1) * 360) // nb_pts)
        (x, y, angle) = (0, 0, 0)
        while x == 0 or angle < alpha or angle > beta:
            (x, y) = (random.randrange(-6, 7) * .5, random.randrange(-6, 7) * .5)
            if x > 0:
                angle = int(atan(y / x) * 180 / pi + 360) % 360
            if x < 0:
                angle = int(atan(y / x) * 180 / pi + 180)
        vals.append((x, y))
    return vals


def place_pts(vals, angle):
    txt = r"\draw[Maroon] "
    for coord in vals:
        txt += f"{coord} -- "
    txt += "cycle;\n"
    txt += fr"\draw ({angle}:-4.5) -- ({angle}:4.5);"
    return txt


def _SymetrieQuadrillage():
    exo = ["\\exercice", u"Construire la symétrique de chacune des figures par rapport à la droite en",
           "utilisant le quadrillage :\\par"]
    cor = ["\\exercice*", u"Construire la symétrique de chacune des figures par rapport à la droite en",
           "utilisant le quadrillage :\\par"]

    nbpts = 5
    langles = [0, 90, 45, 135]
    for j in range(3):
        angle = langles.pop(random.randrange(len(langles)))
        vals = valeurs_quad(nbpts)
        txt = r"""\begin{tikzpicture}[scale=.9, very thick]
            \clip (-3.1, -3.1) rectangle (3.1, 3.1);
            \draw[Olive, step=.5] (-3, -3) grid (3, 3);
            """ + place_pts(vals, angle)
        exo.append(txt)
        cor.append(txt)
        for i, coord in enumerate(vals):
            cor.append(fr"\coordinate (K) at ($({angle}:-4.5)!{coord}!({angle}:4.5)$);")
            cor.append(fr"\coordinate (A{i}) at ($2*(K)-{coord}$);")
        cor.append(fr"\draw[black, dashed] ")
        for i in range(len(vals)):
            cor.append(fr"(A{i}) -- ")
        cor.append("cycle;")
        exo.append(r"\end{tikzpicture}")
        cor.append(r"\end{tikzpicture}")
        if j < 2:
            exo.append("\\hfill")
            cor.append("\\hfill")
    return exo, cor


class SymetrieQuadrillage(LegacyExercise):
    """Symétrie et quadrillages"""

    tags = [
        "géométrie",
        "symétrie",
        "tracé",
        "Cycle 3",
    ]
    function = _SymetrieQuadrillage
