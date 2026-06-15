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
import math
from pyromaths.ex import LegacyExercise


def nodesep(ligne):
    """
    Défini les valeurs nodesep : 0 pour une extrémité, 1 pour une continuité
    @param ligne: droite, demi-droite, segment
    @type ligne: string
    """

    if ligne == 'une droite':
        retour = ['1', '1']
    elif ligne == 'une demi-droite':
        retour = ['0', '1']
    else:
        retour = ['0', '0']
    return retour


def choix_points(n):
    """
    choisit n points parmi A, B, C, ..., Z
    @param n: nombre de points à choisir
    @type n: integer
    """

    points = [chr(i + 65) for i in range(26)]
    liste = []
    for i in range(n):
        liste.append(points.pop(random.randrange(len(points))))
    return liste


def choix_ligne(n):
    """
    Retourne n propositions parmi droite, segment et demi-droite
    @param n: nombre de propositions
    @type n: interger
    """

    lignes = ['une droite', 'une demi-droite', 'un segment']
    (liste_lignes, retour) = ([], [])
    for dummy in range((n - 1) // len(lignes) + 1):
        liste_lignes.extend(lignes)
    for dummy in range(n):
        retour.append(liste_lignes.pop(random.randrange(len(liste_lignes))))
    return retour


def symboles(ligne):
    """
    Retourne les couples (), [] ou [) correspondant au type de ligne
    @param ligne: droite, demi-droite ou segment
    @type ligne: string
    """

    if ligne == 'une droite':
        retour = [r'\left(', r'\right)']
    elif ligne == 'une demi-droite':
        retour = [r'\left[', r'\right)']
    else:
        retour = [r'\left[', r'\right]']
    return retour


def prepare_tuple(lpoints, ligne):
    """
    Prepare deux tuples pour permettre l'affichage de la question et
    de la solution
    @param lpoints: les points de la figure
    @type lpoints: liste de lettres
    @param ligne: droite, demi-droite ou segment
    @type ligne: string
    """

    (retour_exo, retour_sol) = ([], [])

    # choix des deux points permettant de tracer la ligne :

    templist = [i for i in range(len(lpoints))]
    deuxpoints = []
    for i in range(2):
        deuxpoints.append(lpoints[templist.pop(random.randrange(len(templist)))])

    # choix des symbole correspondant à la ligne :

    lsymboles = symboles(ligne)
    retour_sol.append(lsymboles[0])
    retour_sol.extend(deuxpoints)
    retour_sol.append(lsymboles[1])
    retour_sol.append(ligne)

    # choix des trous pour l'exercice :

    alea = random.randrange(3)
    if alea > 1:
        retour_exo = ['\\ldots', '\\ldots', '\\ldots', '\\ldots',
                      '\\dotfill']
    elif alea > 0:
        retour_exo = ['\\ldots']
        retour_exo.extend(retour_sol[1:3])
        retour_exo.extend(['\\ldots', retour_sol[4]])
    else:
        retour_exo = retour_sol[:4]
        retour_exo.append('\\dotfill')
    return (tuple(retour_exo), tuple(retour_sol))


def tex_figure(liste, lpoints, points_coord, nodesep=0):
    """
    Écrit dans un fichier tex la construction de 3 points et éventuellement
    une droite, une demi-droite ou un segment.
    @param liste: liste d'exos ou corrigés
    @type liste: liste
    @param lpoints: liste de 3 points
    @type lpoints: liste de 3 strings
    @param nodesep: liste des dépassements pour pstricks
    @type nodesep: liste de 2 strings
    """
    liste.append(r'\begin{tikzpicture}')
    liste.append(r"\clip (0, 0) rectangle (4, 2.5);")

    # Définition des coordonnées
    liste.append(fr"\coordinate ({points_coord[1]}) at (0.5, {points_coord[0]});")
    liste.append(fr"\coordinate ({points_coord[3]}) at (2.0, {points_coord[2]});")
    liste.append(fr"\coordinate ({points_coord[5]}) at (3.5, {points_coord[4]});")
    # Placement des points
    for lettre in lpoints:
        liste.append(fr"\draw ({lettre}) node[Maroon]{{$\times$}} node[above]{{${lettre}$}};")
    if nodesep:
        # Tracé du segment/droite/demie-droite AB
        a, b, A, B = nodesep
        liste.append(fr"\draw[Maroon] ($({A})+3*{a}*({A})-3*{a}*({B})$) -- ($({B})+3*{b}*({B})-3*{b}*({A})$);")
    liste.append(r'\end{tikzpicture}\tabularnewline')

def coord_points(lpoints):
    """Définit les ordonnées de trois points nommés dont les noms sont dans lpoints"""
    ordonnees = [random.randrange(5, 16) / 10 for i in range(3)]
    while abs(2 * ordonnees[1] - ordonnees[0] - ordonnees[2]) < .5:
        ordonnees = [random.randrange(5, 16) / 10 for i in range(3)]
    random.shuffle(ordonnees)
    for i in range(3):
        ordonnees.insert(2 * i + 1, lpoints[i])
    return tuple(ordonnees)

def tex_ligne_tableau(exo, cor, ligne):
    """
    Écrit une ligne de tableau dans un fichier tex
    @param exo: fichier d'exercices
    @type exo: file
    @param cor: fichier de corrections
    @type cor: file
    @param ligne: droite, demi-droite ou segment
    @type ligne: string
    """

    lpoints = choix_points(3)
    (exer, solution) = prepare_tuple(lpoints, ligne)
    exo.append('$%s %s%s %s$ est %s &' % 
             exer)
    cor.append('$%s %s%s %s$ est %s &' % 
             solution)
    lnodesep = nodesep(ligne)
    lnodesep.extend(solution[1:3])
    points_coord = coord_points(lpoints)
    if exer != ('\\ldots', '\\ldots', '\\ldots', '\\ldots', '\\dotfill'):
        tex_figure(exo, lpoints, points_coord)
    else:
        tex_figure(exo, lpoints, points_coord, lnodesep)
    tex_figure(cor, lpoints, points_coord, lnodesep)
    exo.append('\\hline')
    cor.append('\\hline')


def _Droites():
    """
    Écrit les 5 lignes du tableau
    @param exo: fichier d'exercices
    @type exo: file
    @param cor: fichier de corrections
    @type cor: file
    """
    exo = ["\\exercice", u"Compléter les pointillés et les figures :\\par",
            '\\renewcommand{\\tabularxcolumn}[1]{m{#1}}',
            '\\begin{tabularx}{\\linewidth}{|X|>{\\centering}m{5cm}|}',
            '\\hline',
            u'\\textbf{phrase} & \\textbf{Figure} \\tabularnewline \\hline']
    cor = ["\\exercice*", u"Compléter les pointillés et les figures :\\par",
            '\\renewcommand{\\tabularxcolumn}[1]{m{#1}}',
            '\\begin{tabularx}{\\linewidth}{|X|>{\\centering}m{5cm}|}',
            '\\hline',
            u'\\textbf{Phrase} & \\textbf{Figure} \\tabularnewline \\hline']

    line = choix_ligne(5)
    for i in range(5):
        tex_ligne_tableau(exo, cor, line[i])

    exo.append('\\end{tabularx}')
    cor.append('\\end{tabularx}')
    return (exo, cor)

class Droites(LegacyExercise):
    """Droites, demi-droites, segments"""

    tags = [
        "géométrie",
        "droites",
        "Cycle 3",
    ]
    function = _Droites


#------------------------------------------------------------------------------
# Parallèles et perpendiculaires
#------------------------------------------------------------------------------
# perp à (ac) passant par b => val2=('a', 'c', 'a', 'c', 'b', 'b', 'b', 'a'
# para à (ab) passant apr d => val2=('a', 'b', 'a', 'b', 'd', 'd')


def fig_perp(points, coor, solution=0, per=[], par=[]):
    val_enonce = (
        points[0], points[1], coor[0], coor[1], coor[2], coor[3],
        points[2], points[3], coor[4], coor[5], coor[6], coor[7],)
    text = fr"""\begin{{tikzpicture}}[
        very thick,
        scale=1,
        droite/.style={{shorten >=-8cm, shorten <=-8cm}},
        ]
    \clip (-4, -4) rectangle (4, 4);
    \draw[opacity=0] (-4, -4) rectangle (4, 4);
    \coordinate (A) at ({coor[1]}:{coor[0]});
    \coordinate (B) at ({coor[3]}:{coor[2]});
    \coordinate (C) at ({coor[5]}:{coor[4]});
    \coordinate (D) at ({coor[7]}:{coor[6]});
    \draw (A) node[Maroon]{{$\times$}} node[right]{{${points[0]}$}};
    \draw (B) node[Maroon]{{$\times$}} node[right]{{${points[1]}$}};
    \draw (C) node[Maroon]{{$\times$}} node[right]{{${points[2]}$}};
    \draw (D) node[Maroon]{{$\times$}} node[right]{{${points[3]}$}};
    """
    if solution:
        pts = ('A', 'B', 'C', 'D')
        per = ["ABCD"[item] for item in per]
        par = ["ABCD"[item] for item in par]

        text += fr"""
        % Perpendiculaire
        \draw[DarkBlue, droite] ({per[0]}) -- ({per[1]});
        \coordinate (K) at ($({per[0]})!({per[2]})!({per[1]})$);
        \draw[DarkBlue, droite] (K) -- ({per[2]});
        \draw pic[draw=DarkBlue]{{right angle={per[0]}--K--{per[2]}}};

        % Parallèle
        \draw[DarkRed, droite] ({par[0]}) -- ({par[1]});
        \draw[DarkRed, droite] ({par[2]}) -- ($({par[1]})+({par[2]})-({par[0]})$);
        """

    return text


def noms_sommets(nb):  # renvoie nb noms de sommets
    (listenb, listepts) = ([], [])
    for i in range(26):
        listenb.append(i + 65)
    for i in range(nb):
        listepts.append(chr(listenb.pop(random.randrange(26 - i))))
    listepts.sort()
    return tuple(listepts)


def cree_coordonnees(longueur=3):
    from math import floor
    alpha = random.randrange(180)
    k0 = random.randrange(50, 100) / 100
    a0 = alpha + random.randrange(30, 120)
    k1 = random.randrange(50, 100) / 100
    a1 = alpha + random.randrange(210, 300)
    return (longueur,alpha, longueur, alpha + 180, floor((k0* 10) * longueur) / 10, a0,
            floor((k1 * 10) * longueur) / 10, a1)


def enonce_perp(exo, cor):
    coor = cree_coordonnees(3)
    noms = noms_sommets(4)
    par, per = [], []
    lval = [0, 1, 2, 3]
    for dummy in range(3):
        par.append(lval.pop(random.randrange(len(lval))))
    while per == [] or (par[0], par[1]) == (per[0], per[1]) or \
            (par[0], par[1]) == (per[1], per[0]) :
        lval = [0, 1, 2, 3]
        per = []
        for dummy in range(3):
            per.append(lval.pop(random.randrange(len(lval))))
    exo.append(fig_perp(noms, coor))
    cor.append(fig_perp(noms, coor, 1, per, par))
    exo.append('\end{tikzpicture}\\par\n\\begin{enumerate}')
    cor.append('\end{tikzpicture}\\par\n\\begin{enumerate}')
    s_per = u"\\item Tracer la droite perpendiculaire à la droite $(%s%s)$ passant par $%s$"
    s_par = u"\\item Tracer la droite parallèle à la droite $(%s%s)$ passant par $%s$"
    s_per = s_per % (noms[per[0]], noms[per[1]], noms[per[2]])
    s_par = s_par % (noms[par[0]], noms[par[1]], noms[par[2]])
    if random.randrange(2):
        exo.append(s_par)
        cor.append(s_par)
        exo.append(s_per)
        cor.append(s_per)
    else:
        exo.append(s_per)
        cor.append(s_per)
        exo.append(s_par)
        cor.append(s_par)
    exo.append('\\end{enumerate}')
    cor.append('\\end{enumerate}')


def _Perpendiculaires():
    exo = ["\\exercice", u"Réaliser les figures suivantes :\\par", '\\begin{multicols}{2}']
    cor = ["\\exercice*", u"Réaliser les figures suivantes :\\par", '\\begin{multicols}{2}']

    enonce_perp(exo, cor)

    exo.append('\\columnbreak')
    cor.append('\\columnbreak')

    enonce_perp(exo, cor)

    exo.append('\\end{multicols}')
    cor.append('\\end{multicols}')
    return (exo, cor)

class Perpendiculaires(LegacyExercise):
    """Droites perpendiculaires et parallèles"""

    tags = [
        "droites",
        "géométrie",
        "tracé",
        "Cycle 3",
    ]
    function = _Perpendiculaires


#------------------------------------------------------------------------------
# Propriétés
#------------------------------------------------------------------------------


def PointInter(angle, xa, ya, dist=0):
    angle_rad = (angle * math.pi) / 180
    coef1 = math.floor(math.tan(angle_rad) * 1000) / 1000
    ord_or1 = math.floor((ya - xa * math.tan(angle_rad)) - dist / math.cos(angle_rad) * 1000) / 1000
    coef2 = math.floor(-1000 / math.tan(angle_rad)) / 1000
    x = ord_or1 // (coef2 - coef1)
    y = x * coef2
    return math.floor(x * 1000) / 1000, math.floor(y * 1000) / 1000


def Points(angle, xa, ya, dist=0):
    angle_rad = (angle * math.pi) / 180
    coef = math.floor(math.tan(angle_rad) * 1000) / 1000
    ord_or = math.floor((ya - xa * math.tan(angle_rad) - dist / math.cos(angle_rad)) * 1000) / 1000
    lpos = []
    if -1.5 < -2 * coef + ord_or < 1.5:
        x = -1.5
        y = math.floor((x * coef + ord_or) * 1000) / 1000
        lpos.append('(%s,%s)' % (x, y))
    if -1.5 < 2 * coef + ord_or < 1.5:
        x = 1.5
        y = math.floor((x * coef + ord_or) * 1000) / 1000
        lpos.append('(%s,%s)' % (x, y))
    if -2.1 < (1.5 - ya + dist / math.cos(angle_rad) + xa * math.tan(angle_rad)) / math.tan(angle_rad) < 2.1:
        y = 1.1
        x = math.floor(((y - ya + dist / math.cos(angle_rad) + xa * math.tan(angle_rad)) / math.tan(angle_rad)) * 1000) / 1000
        lpos.append('(%s,%s)' % (x, y))
    if -2.1 < (-1.5 - ya + dist / math.cos(angle_rad) + xa * math.tan(angle_rad)) / math.tan(angle_rad) < 2.1:
        y = -1.1
        x = math.floor(((y - ya + dist / math.cos(angle_rad) + xa * math.tan(angle_rad)) / math.tan(angle_rad)) * 1000) / 1000
        lpos.append('(%s,%s)' % (x, y))
    return lpos

def distance(A, B):
    return math.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)

def signe(x):
    if x < 0:
        return -1
    if x > 0:
        return 1
    raise ValueError()

def figure(angle, xa, ya, dist, lpoints, noms, par_per, dist2=0):
    """

    @param angle:
    @param xa:
    @param ya:
    @param dist:
    @param lpoints:
    @param noms: 1: nomme la droite (AB)
                 2: nomme la droite (d1)
    @param par_per: 1: parallèles + perpendiculaires
                    2: 2 parallèles
                    3: 2 perpendiculaires
    """

    ltxt = []
    ltxt.append(r"""\begin{tikzpicture}[
        very thick,
        droite/.style={{Maroon, shorten >=-8cm, shorten <=-8cm}},
        ]""")
    ltxt.append(r"\clip (-2, -1.5) rectangle (2, 1.5);")
    ltxt.append(r"\draw[opacity=0] (-2, -1.5) -- (2, 1.5);")
    # C'est très cracra, mais ça a été défini au départ pour pstricks avec des fonctions affines, puis converti en TiKZ avec de la géométrie cartésienne. C'était plus rapide pour moi de repartir de zéro que de comprendre ce qui a été fait.
    # Le principe est :
    # - on initialise le générateur aléatoire avec angle, xa, ya, dist, pour que la fonction soit déterministe
    # - les paramètres angle, xa, ya, dist ne sont pas utilisés (sauf pour le générateur aléatoire)
    # - on trace les droites horizontales ou verticales, puis on applique une rotation ensuite.
    random.seed(f"{angle}{xa}{ya}{dist}")
    if par_per == 2:
        while True:
            y1, y2, y3 = (
                random.randint(-1000, -500)/1000,
                random.randint(-500, 500)/1000,
                random.randint(500, 1000)/1000,
                )
            a1, a2 = sorted(random.randint(-1000, 1000)/1000 for _ in range(2))
            b1, b2 = sorted(random.randint(-1000, 1000)/1000 for _ in range(2))
            c1, c2 = sorted(random.randint(-1000, 1000)/1000 for _ in range(2))
            if min(abs(y1-y2), abs(y1-y3), abs(y2-y3)) <= .5:
                continue
            if min(abs(a1-a2), abs(b1-b2), abs(c1-c2)) <= .3:
                continue
            if max(
                    distance((a1, y1), (0, 0)),
                    distance((a2, y1), (0, 0)),
                    distance((b1, y2), (0, 0)),
                    distance((b2, y2), (0, 0)),
                    distance((c1, y3), (0, 0)),
                    distance((c2, y3), (0, 0)),
                    ) >= 1:
                continue
            break
        angle = random.randint(0, 359)
        ltxt.append(textwrap.dedent(fr"""
        \begin{{scope}}[rotate={angle}]
            \coordinate (A1) at ({a1}, {y1});
            \coordinate (A2) at ({a2}, {y1});
            \coordinate (B1) at ({b1}, {y2});
            \coordinate (B2) at ({b2}, {y2});
            \coordinate (C1) at ({c1}, {y3});
            \coordinate (C2) at ({c2}, {y3});
            \draw[droite] (A1) -- (A2);
            \draw[droite] (B1) -- (B2);
            \draw[droite] (C1) -- (C2);
        \end{{scope}}
        """))
        if len(lpoints) == 3:
            # (d1), (d2), (d3)
            d1, d2, d3 = random.sample(lpoints, 3)
            ltxt.append(textwrap.dedent(fr"""
            \path (A1) -- ++({angle-135}:.3) node{{${d1}$}};
            \path (B1) -- ++({angle+135}:.3) node{{${d2}$}};
            \path (C1) -- ++({angle+135}:.3) node{{${d3}$}};
            """))
        else:
            # (AB), (CD), (EF)
            A, B, C = random.sample((lpoints[0:2], lpoints[2:4], lpoints[4:6]), 3)
            ltxt.append(textwrap.dedent(fr"""
            \path (A1) node[Maroon]{{$\times$}} -- ++({angle-135}:.3) node{{${A[0]}$}};
            \path (A2) node[Maroon]{{$\times$}} -- ++({angle-45}:.3) node{{${A[1]}$}};
            \path (B1) node[Maroon]{{$\times$}} -- ++({angle+135}:.3) node{{${B[0]}$}};
            \path (B2) node[Maroon]{{$\times$}} -- ++({angle+45}:.3) node{{${B[1]}$}};
            \path (C1) node[Maroon]{{$\times$}} -- ++({angle+135}:.3) node{{${C[0]}$}};
            \path (C2) node[Maroon]{{$\times$}} -- ++({angle+45}:.3) node{{${C[1]}$}};
            """))
    else:
        # Deux parallèles et une perpendiculaire
        while True:
            y1 = random.randrange(-1000, 0) / 1000
            y2 = random.randrange(0, 1000) / 1000
            x = 0
            while x == 0:
                x = random.randrange(-1000, 1000)/1000
            x1 = -signe(x) * random.randrange(0, 1000) / 1000
            x2 = -signe(x) * random.randrange(0, 1000) / 1000

            if max(
                    distance((x, y1), (0, 0)),
                    distance((x, y2), (0, 0)),
                    distance((x1, y1), (0, 0)),
                    distance((x2, y2), (0, 0)),
                    ) > 1:
                continue
            if abs(y1-y2) <= .5:
                continue
            if min(abs(x-x1), abs(x-x2)) <= .5:
                continue
            break

        angle = random.randint(0, 359)
        ltxt.append(textwrap.dedent(fr"""
        \begin{{scope}}[rotate={angle}]
            \coordinate (I) at ({x}, {y1});
            \coordinate (J) at ({x}, {y2});
            \coordinate (A) at ({x1}, {y1});
            \coordinate (B) at ({x2}, {y2});
            \draw[droite] (I) -- (A);
            \draw[droite] (J) -- (B);
            \draw[droite] (I) -- (J);

            % Symétrique de B par rapport à J
            \coordinate (K) at ($2*(J)-(B)$);
            \draw pic[draw=Maroon, angle radius=3mm]{{right angle=A--I--J}};
            \draw pic[draw=Maroon, angle radius=3mm]{{right angle=K--J--I}};
        \end{{scope}}
        """))
        if len(lpoints) == 3:
            # (d1), (d2), (d3)
            ltxt.append(textwrap.dedent(fr"""
            \path (A) -- ++({angle-90}:.3) node{{${lpoints[0]}$}};
            \path (B) -- ++({angle+90}:.3) node{{${lpoints[1]}$}};
            \path ($.5*(I)+.5*(J)$) -- ++({angle}:.3) node{{${lpoints[2]}$}};
            """))
        else:
            # (AB), (CD), (EF)
            ltxt.append(textwrap.dedent(fr"""
            \path (A) node[Maroon]{{$\times$}} -- ++({angle-90}:.3) node{{${lpoints[1]}$}};
            \path (B) node[Maroon]{{$\times$}} -- ++({angle+90}:.3) node{{${lpoints[3]}$}};
            \path (I) -- ++({angle-135}:.3) node{{${lpoints[0]}$}};
            \path (J) -- ++({angle+45}:.3) node{{${lpoints[2]}$}};
            """))

    ltxt.append(r"\end{tikzpicture}")
    return ltxt


def valeurs_figures(par_per):
    noms = random.randrange(2)
    if noms:
        lpoints = noms_sommets(6)
    else:
        lindices = [1, 2, 3]
        lpoints = []
        for dummy in range(3):
            lpoints.append('(d_%s)' % lindices.pop(random.randrange(len(lindices))))
    angle = random.randrange(1, 90) + 90 * random.randrange(2)
    xa = random.randrange(-5, 5) / 10
    ya = random.randrange(-3, 3) / 10
    if random.randrange(2):
        dist = random.randrange(4, 9) / 10
    else:
        dist = -random.randrange(4, 9) / 10
    if par_per == 2:
        if dist > 0:
            dist2 = -random.randrange(4, 9) / 10
        else:
            dist2 = random.randrange(4, 9) / 10
        return (angle, xa, ya, dist, lpoints, noms, dist2)
    else:
        return (angle, xa, ya, dist, lpoints, noms)


def enonce_prop(exo, cor):
    exo.append('\\renewcommand{\\tabularxcolumn}[1]{m{#1}}')
    exo.append('\\begin{tabularx}{\\textwidth}[t]{|m{3cm}|m{4cm}|X|m{3cm}|}')
    exo.append('\\hline')
    exo.append(u'\\multicolumn{1}{|c|}{\\bf Données} & \\multicolumn{1}{|c|}{\\bf Figure codée}')
    exo.append(u'& \\multicolumn{1}{|c|}{\\bf Propriété} & \\multicolumn{1}{|c|}{\\bf Conclusion}\\\\')
    cor.append('\\renewcommand{\\tabularxcolumn}[1]{m{#1}}')
    cor.append('\\begin{tabularx}{\\textwidth}[t]{|m{3cm}|m{4cm}|X|m{3cm}|}')
    cor.append('\\hline')
    cor.append(u'\\multicolumn{1}{|c|}{\\bf Données} & \\multicolumn{1}{|c|}{\\bf Figure codée}')
    cor.append(u'& \\multicolumn{1}{|c|}{\\bf Propriété} & \\multicolumn{1}{|c|}{\\bf Conclusion}\\\\')
    ltypes = [1, 2, 3]
    lexos = []
    for i in range(3):
        lexos.append(ltypes.pop(random.randrange(len(ltypes))))
    for i in range(3):
        exo.append('\\hline')
        cor.append('\\hline')
        v = valeurs_figures(lexos[i])
        if lexos[i] == 2:
            if v[5]:  # noms de la forme (AB), on ajoute des parenthèses
                exo.append('''$(%s%s)//(%s%s)$\\par et\\par $(%s%s)//(%s%s)$ &
\\begin{tikzpicture}
\\draw[opacity=0] (-2.1,-1.6) -- (2.1,1.6);
\\end{tikzpicture}
& & \\\\''' % 
                         (v[4][0], v[4][1], v[4][2], v[4][3], v[4][0], v[4][1],
                         v[4][4], v[4][5]))
                cor.append('$(%s%s)//(%s%s)$\\par et\\par $(%s%s)//(%s%s)$ & ' % 
                         (v[4][0], v[4][1], v[4][2], v[4][3], v[4][0], v[4][1],
                         v[4][4], v[4][5]))
            else:
                exo.append('''$%s//%s$\\par et\\par $%s//%s$ &
\\begin{tikzpicture}
\\draw[opacity=0] (-2.1,-1.6) -- (2.1,1.6);
\\end{tikzpicture}
& & \\\\''' % 
                         (v[4][0], v[4][1], v[4][0], v[4][2]))
                cor.append('$%s//%s$\\par et\\par $%s//%s$ & ' % (v[4][0],
                         v[4][1], v[4][0], v[4][2]))
            cor.append('%s & ' % ('\n').join(figure(v[0], v[1], v[2],
                     v[3], v[4], v[5], lexos[i], v[6])))  # eror out of range in figure
            cor.append(u'Si deux droites sont parallèles, alors toute parallèle à l\'une est parallèle à l\'autre. &')
            if v[5]:
                cor.append('$(%s%s)//(%s%s)$ \\\\\n  \\hline' % (v[4][2],
                         v[4][3], v[4][4], v[4][5]))
            else:
                cor.append('$%s//%s$ \\\\\n  \\hline' % (v[4][1], v[4][2]))
        else:

            fig = random.randrange(2)
            if lexos[i] == 1:
                if v[5]:
                    if not fig:
                        exo.append('''$(%s%s)//(%s%s)$\\par et\\par $(%s%s)\\perp(%s%s)$ &
\\begin{tikzpicture}
\\draw[opacity=0] (-2.1,-1.6) -- (2.1,1.6);
\\end{tikzpicture}
& & \\\\''' % 
                                 (v[4][0], v[4][1], v[4][2], v[4][3], v[4][0],
                                 v[4][1], v[4][0], v[4][2]))
                    cor.append('$(%s%s)//(%s%s)$\\par et\\par $(%s%s)\\perp(%s%s)$ &' % 
                             (v[4][0], v[4][1], v[4][2], v[4][3], v[4][0],
                             v[4][1], v[4][0], v[4][2]))
                else:
                    if not fig:
                        exo.append('''$%s//%s$\\par et\\par $%s\perp%s$ &
\\begin{tikzpicture}
\\draw[opacity=0] (-2.1,-1.6) -- (2.1,1.6);
\\end{tikzpicture}
& & \\\\''' % 
                                 (v[4][0], v[4][1], v[4][0], v[4][2]))
                    cor.append('$%s//%s$\\par et\\par $%s\perp%s$ &' % 
                             (v[4][0], v[4][1], v[4][0], v[4][2]))
                if fig:
                    exo.append('& %s & & \\\\' % ('\n').join(figure(v[0],
                             v[1], v[2], v[3], v[4], v[5], lexos[i])))
                cor.append('%s & ' % ('\n').join(figure(v[0], v[1], v[2],
                         v[3], v[4], v[5], lexos[i])))
                cor.append(u'Si deux droites sont parallèles, alors toute perpendiculaire à l\'une est perpendiculaire à l\'autre. &')
                if v[5]:
                    cor.append('$(%s%s)\\perp(%s%s)$ \\\\\n  \\hline' % 
                             (v[4][2], v[4][3], v[4][0], v[4][2]))
                else:
                    cor.append('$%s\perp%s$ \\\\\n  \\hline' % (v[4][1],
                             v[4][2]))
            else:
                if v[5]:
                    if not fig:
                        exo.append('''$(%s%s)\\perp(%s%s)$\\par et\\par $(%s%s)\\perp(%s%s)$ &
\\begin{tikzpicture}
\\draw[opacity=0] (-2.1,-1.6) -- (2.1,1.6);
\\end{tikzpicture}
& & \\\\''' % 
                                 (v[4][0], v[4][1], v[4][0], v[4][2], v[4][2],
                                 v[4][3], v[4][0], v[4][2]))
                    cor.append('$(%s%s)\\perp(%s%s)$\\par et\\par $(%s%s)\\perp(%s%s)$ &' % 
                             (v[4][0], v[4][1], v[4][0], v[4][2], v[4][2],
                             v[4][3], v[4][0], v[4][2]))
                else:
                    if not fig:
                        exo.append('''$%s\\perp%s$\\par et\\par $%s\perp%s$ &
\\begin{tikzpicture}
\\draw[opacity=0] (-2.1,-1.6) -- (2.1,1.6);
\\end{tikzpicture}
& & \\\\''' % 
                                 (v[4][0], v[4][2], v[4][1], v[4][2]))
                    cor.append('$%s\\perp%s$\\par et\\par $%s\perp%s$ &' % 
                             (v[4][0], v[4][2], v[4][1], v[4][2]))
                if fig:
                    exo.append('& %s & & \\\\' % ('\n').join(figure(v[0],
                             v[1], v[2], v[3], v[4], v[5], lexos[i])))
                cor.append('%s &' % ('\n').join(figure(v[0], v[1], v[2],
                         v[3], v[4], v[5], lexos[i])))
                cor.append(u'Si deux droites sont perpendiculaires à une même troisième alors elles sont parallèles entre elles. &')
                if v[5]:
                    cor.append('$(%s%s)//(%s%s)$ \\\\\n  \\hline' % (v[4][0],
                             v[4][1], v[4][2], v[4][3]))
                else:
                    cor.append('$%s//%s$ \\\\\n  \\hline' % (v[4][0],
                             v[4][1]))
    exo.append('''\\hline
\\end{tabularx}
''')
    cor.append('\\end{tabularx}')


def _Proprietes():
    exo = ["\\exercice", u"Compléter le tableau suivant :\\par Les droites en gras sont parallèles.\\par """]
    cor = ["\\exercice*", u"Compléter le tableau suivant :\\par Les droites en gras sont parallèles.\\par """]

    enonce_prop(exo, cor)
    return (exo, cor)

class Proprietes(LegacyExercise):
    """Propriétés sur les droites"""

    tags = [
        "droites",
        "géométrie",
        "Cycle 3",
    ]
    function = _Proprietes
