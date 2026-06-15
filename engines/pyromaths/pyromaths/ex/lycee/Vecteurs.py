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


# #- additions / soustractions de vecteurs ( difficulté : ne pas sortir du cadre )
# #- multiplication d'un vecteur par un réel +  add + sous ( difficulté : ne pas sortir du cadre )
# #- lire les coordonnées d'un vecteur
# #- placer un point B connaissant A et les coordonnées de vec{AB} : avec coordonnées ou i et j ( difficulté : ne pas sortir du cadre )
# #- calcul de norme
# #- simplifier des sommes
# #- problèmes de colinéarité

from pyromaths.classes.Vecteurs import randvect, Vecteur
from pyromaths.classes.Racine import simplifie_racine
import math
from random import randint, shuffle
from pyromaths.ex import LegacyExercise

def dist_bords(a, b):
    '''Calcule les distances minimales d'un point de coordonnées (a,b) aux bords du cadre, selon l'axe x et y.'''
    x = min(a, 18 - a)  # la largeur vaut 18
    y = min(b, 10 - b)  # la hauteur vaut 10
    return (x, y)

def pair(n):
    '''Retourne le plus petit entier pair strictement plus grand que n'''
    if (n % 2 == 0):
        return n + 2
    else:
        return n + 1

def anchor_point(x, y):
    if x < 0:
        horizontal = "left"
    elif x == 0:
        horizontal = ""
    else:
        horizontal = "right"
    if y < 0:
        vertical = "below"
    elif y == 0:
        vertical = ""
    else:
        vertical = "above"
    return f"{vertical} {horizontal}"

def anchor_vecteur(u):
    '''Renvoie l'ancre pour l'affichage du nom du vecteur u.'''
    if math.fabs(u.x) > 2 and math.fabs(u.y) > 2:
        return "midway"

    if u.y == 0:
        return "midway, above=2pt"
    if u.x == 0:
        return "midway, right=2pt"

    horizontal = ""
    if u.x < 0:
        horizontal = "right"
    elif u.x > 0:
        horizontal = "left"

    vertical = ""
    if u.y < 0:
        vertical = "below"
    elif u.y > 0:
        vertical = "above"

    return f"midway, {vertical} {horizontal}"

def ChoixVecteur(u, v, w, x, y):
    listecoeff = [0.5, -0.5, -1, -2, 2, 3, -3]
    listevect = [(u, "u"), (v, "v"), (w, "w")]
    shuffle(listecoeff)
    shuffle(listevect)
    for vec in listevect:
        for coeff in listecoeff:
            if (0 <= x + coeff * vec[0].x <= 18) and (0 <= y + coeff * vec[0].y <= 10):
                return (coeff, coeff * vec[0], vec[1])



def repr_somme(u, v, u1, u2):
    """Représente la somme des vecteurs u + v."""

    if len(u2) > 1:
        signe = "-"
    else:
        signe = "+"

    return fr"""%
        \begin{{tikzpicture}}[scale=1, very thick, legende/.style={{fill=white, rectangle, inner sep=1pt, text=black}}]
        \draw[Olive, thick, step=.5]
            ({min(0, u.x, u.x+v.x)}-.4, {min(0, u.y, u.y+v.y)-.4})
            grid
            ({max(0, u.x, u.x+v.x)}+.4, {max(0, u.y, u.y+v.y)+.4})
            ;

        \draw[DarkGreen, |-Stealth] (0, 0) -- {u};
        \draw[DarkBlue, |-Stealth] {u} -- ++{v};
        \draw[dashed, Maroon, |-Stealth] (0, 0) -- (${u}+{v}$);

        \path (0, 0) -- {u} node[{anchor_vecteur(u)}, legende, text=DarkGreen]{{$\overrightarrow{{ {u1} }}$ }};
        \path {u} -- ++{v} node[{anchor_vecteur(v)}, legende, text=DarkBlue]{{$\overrightarrow{{ {u2} }}$ }};
        \path (0, 0) -- (${u}+{v}$) node[{anchor_vecteur(u+v)}, legende, text=Maroon]{{$\overrightarrow{{ {u1} }}{signe}\overrightarrow{{ {u2[-1]} }}$ }};
        \end{{tikzpicture}}%"""

def _vecteurs_add():
    '''Exercice sur la définition des vecteurs et leurs sommes.'''
    t = None
    while True:
    # Pour être sûr que l'exercice ait des solutions
        (u, posux, posuy) = randvect(0, 10)
        (v, posvx, posvy) = randvect(math.fabs(u.x) + 1, 10)
        (w, poswx, poswy) = randvect(math.fabs(v.x) + math.fabs(u.x) + 2, 10)

        # # Construction du point pour la question 2
        if 18 - poswx - max(w.x, 0) > 0:
            restes = (18 - poswx - max(w.x, 0), 10)
            pointy = randint(1, 19) // 2
        elif poswy + min(w.y, 0) > 10 - poswy - max(w.y, 0):
            restes = (poswx + min(w.x, 0), poswy + min(w.y, 0))
            pointy = randint(1, 2 * restes[1]) // 2
        else:
            restes = (poswx + min(w.x, 0), 10 - poswy - max(w.y, 0))
            pointy = randint(19 - restes[1], 19) // 2

        pointx = randint(2 * 18 - restes[0], 2 * 18 - 1) // 2

        t = ChoixVecteur(u, v, w, pointx, pointy)

        if t[1].x + pointx in (0, 18) or t[1].y + pointy in (0, 10):
            continue
        if pointx in (0, 18) or pointy in (0, 10):
            continue

        # Tout va bien
        break

    bx = pointx + t[1].x
    by = pointy + t[1].y

    exo = ["\\exercice"]
    cor = ["\\exercice*"]

    début = fr"""\begin{{center}}\begin{{tikzpicture}}[scale=.95, very thick, legende/.style={{fill=white, rectangle, inner sep=1pt, text=black}}]
        \draw[Olive, thick, step=.5] (0, 0) grid (18, 10);

        \draw ({pointx}, {pointy}) node[Maroon]{{$\times$}} node[{anchor_point(-t[1].x, -t[1].y)},legende]{{$A$}};
        """
    for vec in [(u, posux, posuy, "u"), (v, posvx, posvy, "v"), (w, poswx, poswy, "w")]:
        début += fr"""
            \draw[Maroon, |-Stealth] ({vec[1]}, {vec[2]}) -- ++({vec[0].x}, {vec[0].y});
        """

    exo.append(début)
    cor.append(début)

    cor.append(fr"\draw[DarkBlue,|-Stealth] ({pointx}, {pointy}) -- ({pointx+t[1].x}, {pointy+t[1].y});")
    cor.append(fr"\draw[DarkRed] ({pointx+t[1].x}, {pointy+t[1].y}) node[legende,{anchor_point(t[1].x, t[1].y)}]{{$B$}};")

    for vec in [(u, posux, posuy, "u"), (v, posvx, posvy, "v"), (w, poswx, poswy, "w")]:
        if vec[0].y > 0:
            plus = 1
        else:
            plus = 0
        exo.append(fr"\path[Maroon, |-Stealth] ({vec[1]}, {vec[2]}) -- ++({vec[0].x}, {vec[0].y}) node[{anchor_vecteur(vec[0])}, legende]{{$\overrightarrow{{ {vec[3]} }}$}};")
        cor.append(fr"\path[Maroon, |-Stealth] ({vec[1]}, {vec[2]}) -- ++({vec[0].x}, {vec[0].y}) node[{anchor_vecteur(vec[0])}, legende]{{$\overrightarrow{{ {vec[3]} }}\left({vec[0].x}; {vec[0].y}\right)$}};")
    cor.append(r"\end{tikzpicture}\end{center}")
    exo.append(r"\end{tikzpicture}\end{center}")

    exo.append("\\par")
    cor.append("\\par")
    exo.append(_(u"On se place dans un repère orthonormé et on considère les vecteurs $\\overrightarrow{u}$, $\\overrightarrow{v}$, et $\\overrightarrow{w}$ ci-dessous."))
    cor.append(_(u"On se place dans un repère orthonormé et on considère les vecteurs $\\overrightarrow{u}$, $\\overrightarrow{v}$, et $\\overrightarrow{w}$ ci-dessous."))

    exo.append("\\begin{enumerate}")
    cor.append("\\begin{enumerate}")

    exo.append(_(u"\\item Lire les coordonnées de chacun des vecteurs $\\overrightarrow{u}$, $\\overrightarrow{v}$, et $\\overrightarrow{w}$."))
    cor.append(_(u"\\item Lire les coordonnées de chacun des vecteurs $\\overrightarrow{u}$, $\\overrightarrow{v}$, et $\\overrightarrow{w}$."))

    cor.append("\\par")
    cor.append(_(u"Un petit rappel : l'abscisse d'un vecteur est la différence d'abscisse entre le fin et le début du vecteur. \
                 Concernant le vecteur $\\overrightarrow{u}$, son abscisse est $" + str(u.x) + u"$. \
                 On lit également son ordonnée : $") + str(u.x) + _(u"$. \
                 Donc les coordonnées de $\\overrightarrow{u}$ sont $(") + str(u.x) + ", " + str(u.y) + _(u" )$. \
                 Des pointillés ont été ajoutés sur la figure pour faciliter la lecture des coordonnées."))
    cor.append(_(u"De même, les coordonnées de $\\overrightarrow{v}$ sont $(") + str(v.x) + ", " + str(v.y) + _(u" )$ \
                 et les coordonnées de $\\overrightarrow{w}$ sont $(") + str(w.x) + ", " + str(w.y) + " )$.")

    exo.append(_(u"\\item Placer un point B de sorte que le vecteur $\\overrightarrow{AB}$ soit égal à $") + str(t[0]) + " \\times \\overrightarrow{" + t[2] + "}$.")
    cor.append(_(u"\\item Placer un point B de sorte que le vecteur $\\overrightarrow{AB}$ soit égal à $") + str(t[0]) + " \\times \\overrightarrow{" + t[2] + "}$.")

    cor.append(u"\\par")
    cor.append(_(u"Le plus simple pour répondre à cette question est de calculer les coordonnées du vecteur $") + str(t[0]) + " \\times \\overrightarrow{" + str(t[2]) + "}$.")
    cor.append(_(u"Cela se fait en multipliant les coordonnées de $\\overrightarrow{") + str(t[2]) + "}$ par $" + str(t[0]) + _(u"$, ce qui donne comme résultat $(") + str(t[1].x) + ";" + str(t[1].y) + ")$.")
    cor.append(_(u"En partant du point A et en respectant ces coordonnées, on dessine un vecteur (en bleu sur la figure ci-dessus) qui indique l'emplacement du point B."))

    exo.append(_(u"\\item Calculer les normes de chacun des vecteurs $\\overrightarrow{u}$, $\\overrightarrow{v}$, et $\\overrightarrow{w}$."))
    cor.append(_(u"\\item Calculer les normes de chacun des vecteurs $\\overrightarrow{u}$, $\\overrightarrow{v}$, et $\\overrightarrow{w}$."))

    if u.x ** 2 + u.y ** 2 == simplifie_racine(u.x ** 2 + u.y ** 2)[1]:  # Cas où la simplification est la même, donc inutile d'écrire deux fois la même chose.
        Norm_u = "$"
    else:
        Norm_u = "=" + str(u.normeTex()) + "$"

    if v.x ** 2 + v.y ** 2 == simplifie_racine(v.x ** 2 + v.y ** 2)[1]:
        Norm_v = "$"
    else:
        Norm_v = "=" + str(v.normeTex()) + "$"

    if w.x ** 2 + w.y ** 2 == simplifie_racine(w.x ** 2 + w.y ** 2)[1]:
        Norm_w = "$"
    else:
        Norm_w = "=" + str(w.normeTex()) + "$"

    cor.append("\\par")
    cor.append(u"$\|\\overrightarrow{u}\|=\\sqrt{(" + str(u.x) + ")^2+(" + str(u.y) + ")^2}=\\sqrt{" + str(u.x ** 2) + " + " + str(u.y ** 2) + "}= \
                 \\sqrt{" + str(u.x ** 2 + u.y ** 2) + "}" + Norm_u + ".\\par")
    cor.append(_(u"De la même manière, on obtient :"))

    cor.append(u"$\|\\overrightarrow{v}\|=\\sqrt{(" + str(v.x) + ")^2+(" + str(v.y) + ")^2}=\\sqrt{" + str(v.x ** 2) + " + " + str(v.y ** 2) + "}= \
                 \\sqrt{" + str(v.x ** 2 + v.y ** 2) + "}" + Norm_v + " et \\par")
    cor.append(u"$\|\\overrightarrow{w}\|=\\sqrt{(" + str(w.x) + ")^2+(" + str(w.y) + ")^2}=\\sqrt{" + str(w.x ** 2) + " + " + str(w.y ** 2) + "}= \
                 \\sqrt{" + str(w.x ** 2 + w.y ** 2) + "}" + Norm_w + ".\\par")

    exo.append(_(u"\\item Dessiner des représentants des vecteurs $\\overrightarrow{u}+\\overrightarrow{v}$, $\\overrightarrow{u}-\\overrightarrow{v}$, $\\overrightarrow{u}-\\overrightarrow{w}$ \
                 et $\\overrightarrow{v}+\\overrightarrow{w}$."))
    cor.append(_(u"\\item Dessiner des représentants des vecteurs $\\overrightarrow{u}+\\overrightarrow{v}$, $\\overrightarrow{u}-\\overrightarrow{v}$, $\\overrightarrow{u}-\\overrightarrow{w}$ \
                 et $\\overrightarrow{v}+\\overrightarrow{w}$."))

    cor.append("\\par")
    cor.append(_(u"Pour dessiner les sommes ou différences de vecteurs, il faut les mettre \"bouts à bouts\", \
                 comme sur les figures qui suivent :\\par"))

    cor.append(r"\hspace*{\stretch{1}}")
    cor.append(repr_somme(u, v, 'u', 'v'))
    cor.append(r"\hspace*{\stretch{1}}")
    cor.append(repr_somme(u, -v, 'u', '-v'))
    cor.append(r"\hspace*{\stretch{1}}")
    cor.append(repr_somme(u, -w, 'u', '-w'))
    cor.append(r"\hspace*{\stretch{1}}")
    cor.append(repr_somme(v, w, 'v', 'w'))
    cor.append(r"\hspace*{\stretch{1}}")

    exo.append("\\end{enumerate}")
    cor.append("\\end{enumerate}")

    return exo, cor

class vecteurs_add(LegacyExercise):
    """Vecteurs"""

    tags = [
        "Seconde",
        "lecture graphique",
        "vecteurs",
    ]
    function = _vecteurs_add
