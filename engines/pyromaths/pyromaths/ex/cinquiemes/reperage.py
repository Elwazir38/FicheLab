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
# along with this program; if notPopen, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

import random
from pyromaths.outils.Affichage import decimaux
from pyromaths.ex import LegacyExercise

def noms_sommets(nb):
    """Renvoie nb noms de sommets"""
    (listenb, listepts) = ([], [])
    for i in range(26):
        listenb.append(i + 65)
    for i in range(nb):
        listepts.append(str(chr(listenb.pop(random.randrange(26 - i)))))
    listepts.sort()
    return tuple(listepts)

def valide(coord, liste_coord):
    """Évite deux points trop proches l'un de l'autre"""
    rep = True
    for c in liste_coord:
        if abs(coord[0] - c[0]) <= 0.5 and abs(coord[1] - c[1]) <= 0.5:
            rep = False
            break
    return rep

def quadrant(coord, liste_coord):
    """Évite 2 points dans le même quadrant"""
    rep = True
    for c in liste_coord:
        if coord[0] * c[0] >= 0 and coord[1] * c[1] >= 0:
            rep = False
            break
    return rep


def coordo_pts(nb):
    """Génère une liste de nb coordonnées. Je m'arrange pour avoir des points
    sur les 4 quadrants et sur les deux axes"""
    j = 0
    k = 0
    l = []
    i = 0
    while i < 4 and i < nb:
        j = j + 1
        if j == 600:
            # Correction d'un bug
            l, i, j = [], 0, 0
        a = random.randrange(-9, 10) / 2
        b = random.randrange(-9, 10) / 2
        if ((a, b) not in l) and valide((a, b), l)and quadrant((a, b), l):
            l.append((a, b))
            i = i + 1
    if nb >= 4:
        a = random.randrange(-9, 10) / 2
        while not valide((0, a), l):
            a = random.randrange(-9, 10) / 2
        rg = random.randrange(0, len(l) - 1)
        l[rg:rg] = [(0, a)]
        i = i + 1

    if nb >= 5:
        b = random.randrange(-9, 10) / 2
        while not valide((b, 0), l):
            b = random.randrange(-9, 10) / 2
        rg = random.randrange(0, len(l) - 1)
        l[rg:rg] = [(b, 0)]
        i = i + 1


    while i >= 6 and i < nb and i < 10:
        a = random.randrange(-9, 10) / 2
        b = random.randrange(-9, 10) / 2
        j = j + 1
        if j == 600:
            break
        if ((a, b) not in l) and valide((a, b), l)and quadrant((a, b), l[6:i]):
            l.append((a, b))
            i = i + 1
    if nb >= 11 and len(l) == 10:
        a = random.randrange(-9, 10) / 2
        while not valide((0, a), l):
            a = random.randrange(-9, 10) / 2
        rg = random.randrange(6, len(l) - 1)
        l[rg:rg] = [(0, a)]
        i = i + 1
    if nb >= 11 and len(l) == 11:
        b = random.randrange(-9, 10) / 2
        while not valide((b, 0), l):
            b = random.randrange(-9, 10) / 2
        rg = random.randrange(6, len(l) - 1)
        l[rg:rg] = [(b, 0)]
        i = i + 1

    while i >= 12 and i < nb :
        a = random.randrange(-9, 10) / 2
        b = random.randrange(-9, 10) / 2
        k = k + 1
        if k == 600:
            break
        if ((a, b) not in l) and valide((a, b), l):
            l.append((a, b))
            i = i + 1
    return l


def affiche_coord(coord):
    """Affiche les coordonnées des points au format LaTeX"""
    return '\\hbox{$(' + decimaux(str(coord[0]), 1) + '~;~' + \
                                             decimaux(str(coord[1]), 1) + ')$}'

def tex_liste_co(liste_coord):
    """prend une liste de coordonnées et renvoie la liste en string prête pour latex
    #\hbox évite que les coordonnées soient coupées à l'affichage"""
    i = 0
    tlc = []
    while i < len(liste_coord):
        tlc.append(affiche_coord(liste_coord[i]))
        i = i + 1
    return tlc

def _dessine_repere(coordonnées, noms):
    txt = r"""\begin{tikzpicture}[
        very thick,
        scale=.8,
        coord/.style={rectangle, inner sep=0pt, fill=white, text=black, text opacity=1, fill opacity=.5},
        ]
        \draw[thin, Olive, step=.5] (-5, -5) grid (5, 5);
        \draw[very thick, Olive, step=1] (-5, -5) grid (5, 5);
        \draw[Maroon, -Stealth] (-5, 0) -- (5.5, 0);
        \draw[Maroon, -Stealth] (0, -5) -- (0, 5.5);
        \foreach \i in {1, ..., 5} {
            \draw (\i, 0) node[coord, below]{$\i$};
            \draw ({-\i}, 0) node[coord, below]{$-\i$};
            \draw (0, \i) node[coord, left]{$\i$};
            \draw (0, {-\i}) node[coord, left]{$-\i$};
        }
        \draw (0, 0) node[coord, below left]{$O$};
        """
    for coord, nom in zip(coordonnées, noms):
        if coord[0] < 0:
            if coord[1] < 0:
                position = "below left"
            else:
                position = "above left"
        else:
            if coord[1] < 0:
                position = "below right"
            else:
                position = "above right"
        txt += fr"\draw {coord} node[Maroon]{{$\times$}} node[{position}, coord]{{${nom}$}};"
    txt += r"\end{tikzpicture}"

    return txt

def _reperage():
    nbpts = 13
    noms_pts = (noms_sommets(nbpts))
    coord_pts = coordo_pts(nbpts)
    voc = [_('abscisse'), _(u'ordonnée')]
    rg1 = random.randrange(0, 2)
    rg2 = abs(rg1 - 1)
    while len(coord_pts) < nbpts:
        coord_pts = coordo_pts(nbpts)
    exo = ["\\exercice",
         "\\parbox{0.4\\linewidth}{",
         "\\begin{enumerate}",
         _(u"\\item Donner les coordonnées des points %s, %s, %s, %s, %s et %s.") % tuple(noms_pts[0:6]),
         _(u"\\item Placer dans le repère les points %s, %s, %s, %s, %s et %s") % noms_pts[6:12] + _(u" de coordonnées respectives %s, %s, %s, %s, %s et %s. ") % tuple(tex_liste_co(coord_pts[6:12])),
         _(u"\\item Placer dans le repère le point %s d'%s %s et d'%s %s") % (noms_pts[12], voc[rg1], decimaux(str(coord_pts[12][rg1])), voc[rg2], decimaux(str(coord_pts[12][rg2]))),
         "\\end{enumerate}}\\hfill ",
         "\\parbox{0.55\\linewidth}{",
         _dessine_repere(coord_pts[0:6], noms_pts[0:6]),
         "}"]
    cor = ["\\exercice*",
         "\\parbox{0.4\\linewidth}{",
         _dessine_repere(coord_pts[0:13], noms_pts[0:13]),
         "}\\hfill",
         "\\parbox{0.5\\linewidth}{",
         "\\begin{enumerate}",
         _(u"\\item Donner les coordonnées des points %s, %s, %s, %s, %s et %s.") % tuple(noms_pts[0:6])]
    i = 0
    while i < 6:
        cor.append(_(u"Les coordonnées du point %s sont %s \n") % (noms_pts[i], affiche_coord(coord_pts[i])))
        i = i + 1
    cor[len(cor):len(cor)] = [_(u"\\item Placer dans le repère les points %s, %s, %s, %s, %s et %s") % noms_pts[6:12] +       _(u" de coordonnées respectives %s, %s, %s, %s, %s et %s. ") % tuple(tex_liste_co(coord_pts[6:12])),
         _(u"\\item Placer dans le repère le point %s d'%s %s et d'%s %s") % (noms_pts[12], voc[rg1], decimaux(str(coord_pts[12][rg1])), voc[rg2], decimaux(str(coord_pts[12][rg2]))),
         "\\end{enumerate}"]
    cor.append("}")
    return(exo, cor)

class reperage(LegacyExercise):
    """Repérage"""

    tags = [
        "Cinquième",
        "coordonnées",
    ]
    function = _reperage
