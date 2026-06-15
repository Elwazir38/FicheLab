# Pyromaths
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
# Copyright (C) 2006-2021 -- Jérôme Ortais (jerome.ortais@pyromaths.org)
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

"""Un ensemble de fonctions pour générer du code TikZ.

Utiliser de préférence un template jinja2 que ces fonctions.
"""

import math
import textwrap

from ..classes.Vecteurs import Coordonnees2D


def grid(xmin, ymin, xmax, ymax, *, axes=True):
    text = ""
    text += rf"""
        \draw[Olive, step=.5] ({xmin}, {ymin}) grid ({xmax}, {ymax});
        \draw[Olive, step=1, line width=1pt] ({xmin}, {ymin}) grid ({xmax}, {ymax});
        """
    if axes:
        text += rf"""
            \draw[Maroon, line width=1.2pt, -{{Latex[length=7pt]}}] ({xmin}, 0) -> ({xmax}, 0);
            \draw[Maroon, line width=1.2pt, -{{Latex[length=7pt]}}] (0, {ymin}) -> (0, {ymax});
            \node[below left] (O) at (0, 0) {{$0$}};
            \foreach \x in {{{xmin}, ..., {xmax}}}{{
                \ifnum\x=0{{
                }}\else{{
                    \draw (\x, 0) node[below]{{ \x }};
                }}\fi
            }}
            \foreach \y in {{{ymin}, ..., {ymax}}}{{
                \ifnum\y=0{{
                }}\else{{
                    \draw (0, \y) node[left]{{ \y }};
                }}\fi
            }}
            """
    return text


def polygon(points):
    text = r"""\draw[pattern={north east lines}, pattern color=Maroon, draw=Maroon] """
    for p in points:
        text += f"{p} -- "
    text += "cycle;\n"
    return text


class axis:
    def __init__(self, x, y, *, options=None):
        self.x = x
        self.y = y
        self.options = {
            "axis lines": "center",
            "enlargelimits": "true",
            "axis line style": "{Maroon,-Stealth,line width=1.2pt}",
            "grid": "both",
            "minor tick num": "1",
            "minor grid style": "{draw=lightgray, line width=.4pt}",
            "major grid style": "{draw=Olive, line width=.6pt}",
            "xmin": self.x[0],
            "xmax": self.x[1],
            "xtick distance": "1",
            "xlabel": "{$x$}",
            "ymin": self.y[0],
            "ymax": self.y[1],
            "ytick distance": "1",
            "ylabel": "{$y$}",
            "ticklabel style": r"{font=\tiny,fill=white}",
            "after end axis/.code": r"{\path (axis cs:0,0) node [below left] {\tiny 0};}",
        }
        if options is not None:
            self.options.update(options)

    def begin(self):
        return (
            r"""\begin{tikzpicture}[very thick]
            \begin{axis}["""
            + "\n        ".join(
                f"{key}={value}," for key, value in self.options.items()
            )
            + "\n]\n"
        )

    def end(self):
        return textwrap.dedent(
            r"""
            \end{axis}
            \end{tikzpicture}"""
        )


def interpolation(coordonnees, *, systeme=None, tension=0.5):
    r"""Renvoit la chaîne à placer dans "\draw XXX;" pour tracer une droite interpolant les points donnés en argument.

    On aurait pu utiliser la construction "\addplot[smooth] coordinates {(0, 0) (1, 1)};", mais cette dernière ne respecte ni les extremums, ni les « plateaux » (parties localement constantes de la courbe).
    """
    # Liste des points par lesquels passer
    coordonnees = [Coordonnees2D(*coord) for coord in coordonnees]
    # Liste des points de contrôle (qui définissent la direction d'arrivée et de départ) :
    # En arrivant vers le point d'indice 4 :
    # - la courbe vient de la direction de controls[4][0],
    # - puis repart vers la direction de controls[4][1].
    controls = [[None, None] for _ in coordonnees]

    for i in range(len(coordonnees)):
        if 0 < i < len(coordonnees) - 1 and (  # Ni le premier ni le dernier point
            (
                coordonnees[i - 1].y > coordonnees[i].y
                and coordonnees[i + 1].y > coordonnees[i].y
            )  # C'est un minimum local
            or (
                coordonnees[i - 1].y < coordonnees[i].y
                and coordonnees[i + 1].y < coordonnees[i].y
            )  # C'est un maximum local
        ):
            pente = 0
        elif 0 < i < len(
            coordonnees
        ) - 1 and (  # Ni le premier ni le dernier point  # Le point fait partie d'un « plateau » de la courbe (localement constante)
            coordonnees[i - 1].y == coordonnees[i].y
            or coordonnees[i + 1].y == coordonnees[i].y
        ):
            pente = 0
        else:
            pente = (
                coordonnees[max(0, i - 1)].y
                - coordonnees[min(i + 1, len(coordonnees) - 1)].y
            ) / (
                coordonnees[max(0, i - 1)].x
                - coordonnees[min(i + 1, len(coordonnees) - 1)].x
            )
        controls[i][0] = coordonnees[i] - Coordonnees2D(tension, tension * pente)
        controls[i][1] = coordonnees[i] + Coordonnees2D(tension, tension * pente)

    txt = ""
    for i, coord in enumerate(coordonnees):
        txt += f"({systeme}{coordonnees[i].x}, {coordonnees[i].y}) "
        if i != len(coordonnees) - 1:
            txt += f".. controls ({systeme}{controls[i][1].x}, {controls[i][1].y}) and ({systeme}{controls[i+1][0].x}, {controls[i+1][0].y}) .."
        txt += "\n"

    return txt


def interpolation_avec_pente(coordonnees, *, systeme=None, tension=1):
    coordonnees = list(coordonnees)
    # Liste des points par lesquels passer, triées selon les abscisses
    points = [Coordonnees2D(x, y) for x, y, dy in coordonnees]
    # Liste des pentes
    dy = [coord[2] for coord in coordonnees]
    # Liste des points de contrôle (qui définissent la direction d'arrivée et de départ) :
    # En arrivant vers le point d'indice 4 :
    # - la courbe vient de la direction de controls[4][0],
    # - puis repart vers la direction de controls[4][1].
    controls = [[None, None] for _ in points]

    for i in range(len(points) - 1):
        deltax = points[i + 1].x - points[i].x
        controls[i][1] = points[i] + tension * Coordonnees2D(
            deltax / 3, float(dy[i]) * deltax / 3
        )
        controls[i + 1][0] = points[i + 1] - tension * Coordonnees2D(
            deltax / 3, float(dy[i + 1]) * deltax / 3
        )

    txt = ""
    for i, point in enumerate(points):
        txt += f"({systeme}{point.x}, {point.y}) "
        if i != len(points) - 1:
            txt += f".. controls ({systeme}{controls[i][1].x}, {controls[i][1].y}) and ({systeme}{controls[i+1][0].x}, {controls[i+1][0].y}) .."
        txt += "\n"
    return txt
