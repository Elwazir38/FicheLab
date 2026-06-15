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
import math
import textwrap

from pyromaths.ex import LegacyExercise

#===============================================================================
# Fractions partage
#===============================================================================


def dimensions_rectangle():
    taille_max = 8
    while True:
        (l, h) = (random.randrange(4, taille_max), random.randrange(4,
                  taille_max))
        div_t = diviseurs(l * h)
        if len(div_t) > 3:
            break
    if l < h:
        (l, h) = (h, l)
    return (l, h)


def numerateur_denominateur(l, h, cas):
    """

    @param l: largeur
    @param h: longueur
    @param cas:
        - nid: numerateur < denominateur
        - un: numerateur = denominateur
        - nsd: numerateur > denominateur
    @type cas: string
    """

    ldiv = diviseurs(l * h)
    if cas == "un":
        d = random.randrange(3, l * h)
    else:
        while True:
            d = ldiv[random.randrange(len(ldiv) - 1)]
            if d > 2:
                break
    if cas == "un":
        n = d
    elif cas == "nid":
        n = random.randrange(1, d)
    else:
        n = random.randrange(d + 1, d * 2)
    return (n, d)


def trace_rectangle(exo, cor, l, h, cas):
    exo.append(fr"\draw[thick, Olive] (0, 0) grid (16, {h});")
    cor.append(fr"\draw[thick, Olive] (0, 0) grid (16, {h});")
    exo.append(fr"\draw[very thick, Maroon] (0,0) rectangle ({l}, {h});")
    cor.append(fr"\draw[very thick, Maroon] (0,0) rectangle ({l}, {h});")
    if cas == "nsd":
        cor.append(fr"\draw[very thick, Maroon] ({l+1}, 0) rectangle ({2*l+1}, {h});")

def fractions_partage_corrige(l, h, n, d):
    div_l = diviseurs(l)
    div_h = diviseurs(h)
    div_d = diviseurs(d)
    (lc, hc) = (l, h)
    if n == d:
        (lc, hc) = (l, h)
    elif div_l.count(d):
        lc = l // d
    elif div_h.count(d):
        hc = h // d
    else:
        for i in range(len(div_d) - 1):
            if div_l.count(div_d[i + 1]) and div_h.count(d // div_d[i + 1]):
                (lc, hc) = (l // div_d[i + 1], (h * div_d[i + 1]) // d)
                break
    return (lc, hc)


def trace_partage(cor, l, h, lc, hc, cas):
    if lc < l:
        cor.append(fr"\foreach \x in {{1, ..., {l // lc} }} {{ \draw[thick, Maroon] ({{\x * {lc} }}, 0) -- ++(0,{h});}}")
        if cas == "nsd":
            cor.append(fr"\foreach \x in {{0, ..., {l // lc} }} {{ \draw[thick, Maroon] ({{\x * {lc} + {l+1} }}, 0) -- ++(0,{h});}}")
    if hc < h:
        cor.append(fr"\foreach \y in {{1, ..., {h // hc} }} {{ \draw[thick, Maroon] (0, {{\y * {hc} }}) -- ++({l}, 0);}}")
        if cas == "nsd":
            cor.append(fr"\foreach \y in {{1, ..., {h // hc} }} {{ \draw[thick, Maroon] ({l+1}, {{\y * {hc} }}) -- ++({l}, 0);}}")


def coloriage(cor, n, d, l, h, lc, hc):
    if n == d:
        cor.append(r"\fill[Peru] (0, 0) rectangle (%s, %s);" % 
                 (l, h))
    else:
        (x, y, nfig) = (0, 0, 0)
        for dummy in range(n):
            if nfig:
                cor.append(fr"\fill[Peru] ({x+nfig}, {y}) rectangle ++({lc}, {hc});")
            else:
                cor.append(fr"\fill[Peru] ({x}, {y}) rectangle ++({lc}, {hc});")
            if x + lc < l:
                x = x + lc
            elif y + hc < h:
                (x, y) = (0, y + hc)
            else:
                (x, y, nfig) = (0, 0, l + 1)


def diviseurs(n):
    l = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if not n % i:
            l.append(i)
            if i != n // i:
                l.append(n // i)
    l.sort()
    return l


def _FractionPartage():
    exo = ["\\exercice", '\\begin{multicols}{2}', '\\begin{enumerate}']
    cor = ["\\exercice*", '\\begin{multicols}{2}', '\\begin{enumerate}']

    lcas = ["nid", "un", "nsd", "nid", "nsd"]
    for i in range(4):
        cas = lcas.pop(random.randrange(len(lcas)))
        if cas == "nsd":
            while True:
                (l, h) = dimensions_rectangle()
                if l < 8:
                    break
        else:
            (l, h) = dimensions_rectangle()
        (n, d) = numerateur_denominateur(l, h, cas)
        (lc, hc) = fractions_partage_corrige(l, h, n, d)

        exo.append("\\item Colorer $\\frac{%s}{%s}$ de ce rectangle.\\par" % 
                 (n, d))
        cor.append("\\item Colorer $\\frac{%s}{%s}$ de ce rectangle.\\par" % 
                 (n, d))
        exo.append("\\begin{tikzpicture}[scale=.4]")
        cor.append("\\begin{tikzpicture}[scale=.4]")
        (lc, hc) = fractions_partage_corrige(l, h, n, d)
        coloriage(cor, n, d, l, h, lc, hc)
        trace_rectangle(exo, cor, l, h, cas)
        trace_partage(cor, l, h, lc, hc, cas)
        exo.append("\\end{tikzpicture}")
        cor.append("\\end{tikzpicture}")
        if i == 1:
            exo.append("\\columnbreak")
            cor.append("\\columnbreak")

    exo.append('\\end{enumerate}')
    exo.append('\\end{multicols}')
    cor.append('\\end{enumerate}')
    cor.append('\\end{multicols}')
    return (exo, cor)

class FractionPartage(LegacyExercise):
    """Fractions partage"""

    tags = [
        "fractions",
        "géométrie",
        "Cycle 3",
    ]
    function = _FractionPartage


#===============================================================================
# Fractions et abscisses
#===============================================================================


def valeurs_abscisses():
    origine = random.randrange(3, 11)
    nb_divisions = (
        6,
        8,
        9,
        10,
        12,
        14,
        15,
        16,
        18,
        20,
        )
    div = nb_divisions[random.randrange(len(nb_divisions))]
    nb_subd = diviseurs(div)
    subd = nb_subd[random.randrange(len(nb_subd) - 2) + 1]
    while subd < 3:
        subd = nb_subd[random.randrange(len(nb_subd) - 2) + 1]
    nb_grad = 58  # nb de graduations sur la demi-droite graduée
    lpts = [0 for i in range(7)]  # liste des places des points à trouver/placer sur la 1/2 droite graduée
    lpts[4] = random.randrange(1, nb_grad // div + 1) * div
    for i in range(2):
        a = random.randrange(1, nb_grad)
        while lpts.count(a):
            a = random.randrange(1, nb_grad)
        lpts[i] = a
    for i in range(2):
        a = random.randrange(1, (nb_grad * subd) // div)
        while lpts.count((a * div) // subd):
            a = random.randrange(1, (nb_grad * subd) // div)
        lpts[i + 2] = (a * div) // subd
    for i in range(2):
        a = random.randrange(1, (nb_grad * subd) // div)
        while lpts.count((a * div) // subd):
            a = random.randrange(1, (nb_grad * subd) // div)
        lpts[i + 5] = (a * div) // subd

    # npts=noms_pts(7)

    npts = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    lnum = list(range(7))  # liste des numérateurs
    lnum[0] = origine * div + lpts[0]
    lnum[1] = origine * div + lpts[1]
    lnum[2] = origine * subd + (lpts[2] * subd) // div
    lnum[3] = origine * subd + (lpts[3] * subd) // div
    lnum[4] = random.randrange(3, div)
    while diviseurs(div).count(lnum[4]):
        lnum[4] = random.randrange(3, div)
    lnum[5] = origine * div + lpts[5]
    lnum[6] = origine * div + lpts[6]
    return (origine, div, subd, lpts, npts, lnum)


def noms_pts(nb):  # renvoie nb noms de points
    (listenb, listepts) = ([], [])
    for i in range(26):
        listenb.append(i + 65)
    for i in range(nb):
        listepts.append(chr(listenb.pop(random.randrange(26 - i))))
    listepts.sort()
    return listepts


def unites_fractions(exo, cor, origine, div, subd):
    postf = u'ièmes'
    lch = [
        'cinqu',
        'six',
        'sept',
        'huit',
        'neuv',
        'dix',
        'onz',
        'douz',
        'treiz',
        'quatorz',
        'quinz',
        'seiz',
        'dix-sept',
        'dix-huit',
        'dix-neuv',
        'vingt',
        ]
    lfr = dict([(i + 5, lch[i] + postf) for i in range(len(lch))])
    lfr[2] = 'demis'
    lfr[3] = 'tiers'
    lfr[4] = 'quarts'
    exo.append(u'\\item 1 unité = \\ldots %s' % lfr[div])
    exo.append(u'\\item 1 unité = \\ldots~%s' % lfr[subd])
    exo.append(u'\\item %s unités = \\ldots~%s' % (origine,
             lfr[div]))
    exo.append(u'\\item %s unités = \\ldots~%s' % (origine,
             lfr[subd]))
    cor.append(u'\\item 1 unité = %s %s' % (div, lfr[div]))
    cor.append(u'\\item 1 unité = %s %s' % (subd, lfr[subd]))
    cor.append(u'\\item %s unités = %s %s' % (origine,
             origine * div, lfr[div]))
    cor.append(u'\\item %s unités = %s %s' % (origine,
             origine * subd, lfr[subd]))


def trace_demi_droite(exo, cor, origine, div, subd, lpts, npts, lnum):
    droite_des_reels = textwrap.dedent(fr"""
        \draw[-Stealth, Maroon] (-.2, 0) -- (20, 0);
        \foreach \x in {{ 0, ..., 58 }} {{
            \draw[Maroon] ({{\x / 3}}, -.1) -- ({{\x / 3}}, .1);
        }}
        \foreach \x in {{ 0, ..., {58 // div} }} {{
            \draw[Maroon] ({{ {div} * \x / 3}}, -.2) -- ({{ {div} * \x / 3}}, .2);
        }}
    """)
    for i in range(58 // div + 1):
        droite_des_reels += fr"\draw ({(i * div) / 3}, -.2) node[below]{{ {origine + i} }};" + "\n"
    exo.append(droite_des_reels)
    cor.append(droite_des_reels)
    for i in range(2):
        exo.append(fr"\draw ( {lpts[i + 5] / 3}, 0) node[above]{{${npts[i + 5]}$}};" + "\n")
    for i in range(7):
        cor.append(fr"\draw ( {lpts[i] / 3}, 0) node[above]{{${npts[i]}$}};" + "\n")


def ecrit_abscisses(exo, cor, origine, div, subd, lpts, lnum):
    exo.append("\\item $\\left(\\cfrac{%s}{%s}\\right)$" % (lnum[0], div))
    exo.append("\\item $\\left(\\cfrac{%s}{%s}\\right)$" % (lnum[1], div))
    exo.append("\\item $\\left(\\cfrac{%s}{%s}\\right)$" % (lnum[2], subd))
    exo.append("\\item $\\left(\\cfrac{%s}{%s}\\right)$" % (lnum[3], subd))
    exo.append("\\item $\\left(\\cfrac{%s}{%s}\\right)$" % (origine * 
             lnum[4] + (lpts[4] // div) * lnum[4], lnum[4]))
    cor.append("\\item $\\left(\\cfrac{%s}{%s}\\right)$" % (lnum[0], div))
    cor.append("\\item $\\left(\\cfrac{%s}{%s}\\right)$" % (lnum[1], div))
    cor.append("\\item $\\left(\\cfrac{%s}{%s}\\right)$" % (lnum[2], subd))
    cor.append("\\item $\\left(\\cfrac{%s}{%s}\\right)$" % (lnum[3], subd))
    cor.append("\\item $\\left(\\cfrac{%s}{%s}\\right)$" % (origine * 
             lnum[4] + (lpts[4] // div) * lnum[4], lnum[4]))


def trouve_abscisses(exo, cor, div, subd, lnum):
    exo.append("\\item $F~\\left(\\cfrac{\\ldots}{%s}\\right)$" % div)
    exo.append("\\item $F~\\left(\\cfrac{\\ldots}{%s}\\right)$" % subd)
    exo.append("\\item $G~\\left(\\cfrac{\\ldots}{%s}\\right)$" % div)
    exo.append("\\item $G~\\left(\\cfrac{\\ldots}{%s}\\right)$" % subd)
    cor.append("\\item $F~\\left(\\cfrac{%s}{%s}\\right)$" % (lnum[5], div))
    cor.append("\\item $F~\\left(\\cfrac{%s}{%s}\\right)$" % ((lnum[5] * 
             subd) // div, subd))
    cor.append("\\item $G~\\left(\\cfrac{%s}{%s}\\right)$" % (lnum[6], div))
    cor.append("\\item $G~\\left(\\cfrac{%s}{%s}\\right)$" % ((lnum[6] * 
             subd) // div, subd))


def _QuestionsAbscisses():
    exo = ["\\exercice"]
    cor = ["\\exercice*"]
    (origine, div, subd, lpts, npts, lnum) = valeurs_abscisses()
    exo.append("\\begin{enumerate}")
    exo.append(u"\\item Compléter :")
    exo.append("\\begin{multicols}{2}")
    exo.append("\\begin{enumerate}")
    cor.append("\\begin{enumerate}")
    cor.append(u"\\item Compléter :")
    cor.append("\\begin{multicols}{2}")
    cor.append("\\begin{enumerate}")
    unites_fractions(exo, cor, origine, div, subd)
    exo.append("\\end{enumerate}")
    exo.append("\\end{multicols}")
    exo.append(u"\\item Sur la demi-droite ci-dessous, placer les points d'abscisse donnée :")
    exo.append("\\begin{multicols}{5}")
    exo.append("\\begin{enumerate}")
    exo.append("\\renewcommand{\\theenumii}{\\Alph{enumii}}")
    exo.append("\\renewcommand{\\labelenumii}{$\\theenumii$}")
    cor.append("\\end{enumerate}")
    cor.append("\\end{multicols}")
    cor.append(u"\\item Sur la demi-droite ci-dessous, placer les points d'abscisse donnée :")
    cor.append("\\begin{multicols}{5}")
    cor.append("\\begin{enumerate}")
    cor.append("\\renewcommand{\\theenumii}{\\Alph{enumii}}")
    cor.append("\\renewcommand{\\labelenumii}{$\\theenumii$}")
    ecrit_abscisses(exo, cor, origine, div, subd, lpts, lnum)
    exo.append("\\end{enumerate}")
    exo.append("\\end{multicols}")
    exo.append(u"\\item Compléter les abscisses des points suivants :")
    exo.append("\\begin{multicols}{4}")
    exo.append("\\begin{enumerate}")
    cor.append("\\end{enumerate}")
    cor.append("\\end{multicols}")
    cor.append(u"\\item Compléter les abscisses des points suivants :")
    cor.append("\\begin{multicols}{4}")
    cor.append("\\begin{enumerate}")
    trouve_abscisses(exo, cor, div, subd, lnum)
    exo.append("\\end{enumerate}")
    exo.append("\\end{multicols}")
    exo.append("\\end{enumerate}")
    exo.append("\\begin{center}\\begin{tikzpicture}[very thick, scale=.8]")
    cor.append("\\end{enumerate}")
    cor.append("\\end{multicols}")
    cor.append("\\end{enumerate}")
    cor.append("\\begin{center}\\begin{tikzpicture}[very thick, scale=.8]")
    trace_demi_droite(exo, cor, origine, div, subd, lpts, npts, lnum)
    exo.append("\\end{tikzpicture}\\end{center}")
    cor.append("\\end{tikzpicture}\\end{center}")
    return (exo, cor)

class QuestionsAbscisses(LegacyExercise):
    """Fractions et abscisses"""

    tags = [
        "fractions",
        "Cycle 3",
    ]
    function = _QuestionsAbscisses
