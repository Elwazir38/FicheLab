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
import random, math
import textwrap

from pyromaths.outils import Geometrie as geo
from pyromaths.outils.Affichage import decimaux
from pyromaths.ex import LegacyExercise
from decimal import Decimal

# trigo en degré
tan = lambda z:math.tan(math.radians(z))
cos = lambda z:math.cos(math.radians(z))
sin = lambda z:math.sin(math.radians(z))
def shuffle_nom(polygone):
    """renvoie un nom aléatoire du polygone"""
    n = len(polygone)
    polygone = polygone + polygone + polygone
    debut = n + random.randrange(n)
    sens = [-1, 1][random.randrange(2)]
    nom = ""
    for i in range(debut, debut + n * sens, sens):
        nom += polygone[i]
    return nom

def _exo_triangle(test=False):
    questions = [
           quest_equilateral,
           quest_LAL,
           quest_ALA,
           quest_AAL,
           quest_isocele_angbase,
           quest_isocele_angprincipal,
           quest_rectangle_hypo_cote,
           quest_rectangle_hypo_angle,
           ]
    exo = ["\\exercice",
         "\\begin{enumerate}"]
    cor = ["\\exercice*",
         "\\begin{enumerate}"]
    cor.append("\\definecolor{enonce}{rgb}{0.11,0.56,0.98}")
    cor.append("\\definecolor{calcul}{rgb}{0.13,0.54,0.13}")
    for question in random.sample(questions, 4):
        question(exo, cor)

    exo.append("\\end{enumerate}")
    cor.append("\\end{enumerate}")
    return exo, cor

class exo_triangle(LegacyExercise):
    """Construction de triangles"""

    tags = [
        "Cinquième",
        "angles",
        "géométrie",
        "tracé",
        "triangle",
    ]
    function = _exo_triangle


def quest_equilateral(exo, cor):
    A, B, C = geo.choix_points(3)
    nom = shuffle_nom([A, B, C])
    c = Decimal(random.randint(40, 70))/10  # longueur AB
    angBAC = angABC = 60
    exo.append(_(u"\\item Trace un triangle $%s$ équilatéral de côté $\\SI{%s}{cm}$.\\par") % (nom, decimaux(c)))
    cor.append(_(u"\\item Trace un triangle $%s$ équilatéral de côté $\\SI{%s}{cm}$.\\par") % (nom, decimaux(c)))
    cor.append(textwrap.dedent(fr"""
    \begin{{tikzpicture}}[very thick, radius={c}cm]
        \coordinate (A) at (0, 0);
        \coordinate (B) at (0:{c}cm);
        \coordinate (C) at (60:{c}cm);
        \draw (A) node[below left] {{${A}$}};
        \draw (B) node[below right] {{${B}$}};
        \draw (C) node[above] {{${C}$}};
        \draw[Maroon] (A) -- (B) node[midway, below, color=enonce]{{\SI{{ {decimaux(c)} }}{{cm}}}} -- (C) -- cycle;
        \draw[color=enonce, draw,decoration={{markings, mark=at position .5  with {{\node[transform shape] {{$\parallel$}};}}}}]
            (A) edge[decorate] (B)
            (B) edge[decorate] (C)
            (C) edge[decorate] (A);
        \draw[calcul] (50:{c}cm) arc[start angle=50, delta angle=20];
        \draw[calcul] ($(0:{c}cm)+(110:{c}cm)$) arc[start angle=110, delta angle=20];
    \end{{tikzpicture}}
    """))

def quest_LAL(exo, cor):
    """on donne un angle et les longueurs de ses deux côtés"""
    """            angBAC et      AB=c et AC=b"""
    A, B, C = geo.choix_points(3)
    nom = shuffle_nom([A, B, C])
    c = Decimal(random.randint(40, 70))/10  # longueur AB
    b = Decimal(random.randint(20, 100))/10  # longueur BC
    angBAC = 3 * random.randint(7, 50)  # BAC mesure entre 21° et 150°

    exo.append(_(u"\\item Trace un triangle $%s$ tel que $%s%s=\\SI{%s}{cm}$, $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$")
               % (nom, A, B, decimaux(c), A, C, decimaux(b), B, A, C, angBAC))
    cor.append(_(u"\\item Trace un triangle $%s$ tel que $%s%s=\\SI{%s}{cm}$, $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, A, B, decimaux(c), A, C, decimaux(b), B, A, C, angBAC))
    cor.append(textwrap.dedent(fr"""
    \begin{{tikzpicture}}[very thick]
        \coordinate (A) at (0, 0);
        \coordinate (B) at (0:{c}cm);
        \coordinate (C) at ({angBAC}:{b}cm);
        \draw (A) node[left] {{${A}$}};
        \draw (B) node[below right] {{${B}$}};
        \draw (C) node[above] {{${C}$}};
        \draw[Maroon] (C) -- (B) -- (A) node[midway, below, color=enonce]{{\SI{{ {decimaux(b)} }}{{cm}}}} -- ({angBAC}:{1.1*float(b)}cm) node[midway, sloped, above, color=enonce]{{\SI{{ {decimaux(c)} }}{{cm}}}};
        \draw[calcul] ({angBAC-10}:{b}cm) arc[start angle={angBAC-10}, delta angle=20, radius={b}cm];
        \draw pic [draw,enonce,angle radius=20pt, angle eccentricity=2, "\ang{{ {angBAC} }}"] {{angle = B--A--C}};
    \end{{tikzpicture}}
    """))

def quest_ALA(exo, cor):
    """on donne deux angles et la longueur du côté commun"""
    """ angBAC et angABC et AB=c"""
    A, B, C = geo.choix_points(3)
    nom = shuffle_nom([A, B, C])
    c = Decimal(random.randint(40, 70))/10  # longueur AB
    angBAC = 5 * random.randint(4, 12)
    angABC = 5 * random.randint(4, 12)
    b = c * Decimal(sin(angABC)/sin(180 - angBAC - angABC)) # Longueur AC calculée avec la loi des sinus.
    exo.append(_(u"\\item Trace un triangle $%s$ tel que $%s%s=\\SI{%s}{cm}$,  $\\widehat{%s%s%s}=\\ang{%s}$ et $\\widehat{%s%s%s}=\\ang{%s}$")
               % (nom, A, B, decimaux(c), B, A, C, angBAC, A, B, C, angABC))
    cor.append(_(u"\\item Trace un triangle $%s$ tel que $%s%s=\\SI{%s}{cm}$,  $\\widehat{%s%s%s}=\\ang{%s}$ et $\\widehat{%s%s%s}=\\ang{%s}$\\par")
               % (nom, A, B, decimaux(c), B, A, C, angBAC, A, B, C, angABC))
    cor.append(textwrap.dedent(fr"""
    \begin{{tikzpicture}}[very thick]
        \coordinate (A) at (0, 0);
        \coordinate (B) at (0:{c}cm);
        \coordinate (C) at ({angBAC}:{b}cm);
        \draw (A) node[left] {{${A}$}};
        \draw (B) node[below right] {{${B}$}};
        \draw (C) node[above] {{${C}$}};
        \draw[Maroon] (A) -- (B) node[midway, below, color=enonce]{{\SI{{ {c} }}{{cm}}}};
        \draw[Maroon] (B) -- (C) -- ($(C)!-1cm!(B)$);
        \draw[Maroon] (A) -- (C) -- ($(C)!-1cm!(A)$);
        \draw pic [draw,enonce,angle radius=20pt, angle eccentricity=2, "\ang{{ {angBAC} }}"] {{angle = B--A--C}};
        \draw pic [draw,enonce,angle radius=20pt, angle eccentricity=2, "\ang{{ {angABC} }}"] {{angle = C--B--A}};
    \end{{tikzpicture}}
    """))

def quest_AAL(exo, cor):
    """on donne deux angles et la longueur d'un côté non commun aux deux angles"""
    """ angBAC et angACB et AB=c"""
    A, B, C = geo.choix_points(3)
    nom = shuffle_nom([A, B, C])
    angBAC = 3 * random.randint(10, 24)  # entre 30° et 72°
    angACB = 3 * random.randint(10, 24)  # entre 30° et 72°
    angABC = 180 - angBAC - angACB
    ABmax = int(35 * (tan(angABC) + tan(angBAC)) / (tan(angBAC) * tan(angABC)))  # donne une hauteur inférieur à 35*0.2=7 cm
    c = 2 * Decimal(random.randint(20, max(20, ABmax))) / 10  # longueur AB
    b = c * Decimal(sin(angABC)/sin(180 - angBAC - angABC)) # Longueur AC calculée avec la loi des sinus.

    exo.append(_(u"\\item Trace un triangle $%s$ tel que $%s%s=\\SI{%s}{cm}$,  $\\widehat{%s%s%s}=\\ang{%s}$ et $\\widehat{%s%s%s}=\\ang{%s}$")
               % (nom, A, B, decimaux(c), B, A, C, angBAC, A, C, B, angACB))
    cor.append(_(u"\\item Trace un triangle $%s$ tel que $%s%s=\\SI{%s}{cm}$,  $\\widehat{%s%s%s}=\\ang{%s}$ et $\\widehat{%s%s%s}=\\ang{%s}$\\par")
               % (nom, A, B, decimaux(c), B, A, C, angBAC, A, C, B, angACB))
    cor.append(_(u"On doit d'abord calculer la mesure de $\\widehat{%s%s%s}$.\\\\")
               % (A, B, C))
    cor.append(_(u"Or la somme des trois angles d'un triangle est égale à \\ang{180} donc $\\widehat{%s%s%s}=\\ang{180}-\\ang{%s}-\\ang{%s}=\\ang{%s}$.\\par")
               % (A, B, C, angBAC, angACB, angABC))
    cor.append(textwrap.dedent(fr"""
    \begin{{tikzpicture}}[very thick]
        \coordinate (A) at (0, 0);
        \coordinate (B) at (0:{c}cm);
        \coordinate (C) at ({angBAC}:{b}cm);
        \draw (A) node[left] {{${A}$}};
        \draw (B) node[below right] {{${B}$}};
        \draw (C) node[above] {{${C}$}};
        \draw[Maroon] (A) -- (B) node[midway, below, color=enonce]{{\SI{{ {c} }}{{cm}}}};
        \draw[Maroon] (B) -- (C) -- ($(C)!-1cm!(B)$);
        \draw[Maroon] (A) -- (C) -- ($(C)!-1cm!(A)$);
        \draw pic [draw,enonce,angle radius=20pt, angle eccentricity=2, "\ang{{ {angBAC} }}"] {{angle = B--A--C}};
        \draw pic [draw,calcul,angle radius=20pt, angle eccentricity=2, "\ang{{ {angABC} }}"] {{angle = C--B--A}};
        \draw pic [draw,enonce,angle radius=20pt, angle eccentricity=2, "\ang{{ {angACB} }}"] {{angle = A--C--B}};
    \end{{tikzpicture}}
    """))

def quest_isocele_angbase(exo, cor):
    """on donne ABC isocele en C, AB=c et angBAC"""
    A, B, C = geo.choix_points(3)
    nom = shuffle_nom([A, B, C])
    angABC = angBAC = random.randint(20, 70)
    maxc = max(20, int(35 / tan(angBAC)))  # longueur c maximale pour que la hauteur soit 7 cm =0.2*35
    minc = min(20, int(35 / tan(angBAC)))
    c = 2 * Decimal(random.randint(minc, min(maxc, 50))) / 10  # longueur AB
    b = c * Decimal(sin(angABC)/sin(180 - angBAC - angABC)) # Longueur AC calculée avec la loi des sinus.

    exo.append(_(u"\\item Tracer un triangle $%s$ isocèle en $%s$ tel que $%s%s=\\SI{%s}{cm}$,  $\\widehat{%s%s%s}=\\ang{%s}$.")
               % (nom, C, A, B, decimaux(c), B, A, C, angBAC))
    cor.append(_(u"\\item Tracer un triangle $%s$ isocèle en $%s$ tel que $%s%s=\\SI{%s}{cm}$,  $\\widehat{%s%s%s}=\\ang{%s}$. \\par")
               % (nom, C, A, B, decimaux(c), B, A, C, angBAC))
    cor.append(_(u"Comme $%s%s%s$ est un triangle isocèle en $%s$, on sait que les angles adjacents à la base sont de même mesure \
donc $\\widehat{%s%s%s}=\\widehat{%s%s%s}=\\ang{%s}$.\\par") % (A, B, C, C, A, B, C, B, A, C, angBAC))
    cor.append(textwrap.dedent(fr"""
    \begin{{tikzpicture}}[very thick]
        \coordinate (A) at (0, 0);
        \coordinate (B) at (0:{c}cm);
        \coordinate (C) at ({angBAC}:{b}cm);
        \draw (A) node[left] {{${A}$}};
        \draw (B) node[below right] {{${B}$}};
        \draw (C) node[above] {{${C}$}};
        \draw[Maroon] (A) -- (B) node[midway, below, color=enonce]{{\SI{{ {c} }}{{cm}}}};
        \draw[Maroon] (B) -- (C) -- ($(C)!-1cm!(B)$);
        \draw[Maroon] (A) -- (C) -- ($(C)!-1cm!(A)$);
        \draw pic [draw,enonce,angle radius=20pt, angle eccentricity=2, "\ang{{ {angBAC} }}"] {{angle = B--A--C}};
        \draw pic [draw,enonce,angle radius=20pt, angle eccentricity=2, "\ang{{ {angABC} }}"] {{angle = C--B--A}};
    \end{{tikzpicture}}
    """))

def quest_isocele_angprincipal(exo, cor):
    """on donne ABC isocele en C, AB=c et angACB"""
    A, B, C = geo.choix_points(3)
    nom = shuffle_nom([A, B, C])
    angACB = 2 * random.randint(20, 60)  # ACB est pair entre 40° et 120°
    angBAC = angABC = (180 - angACB) / 2
    maxc = max(20, int(35 / tan(angBAC)))  # longueur c maximale pour que la hauteur soit 7 cm =0.2*35
    c = 2 * Decimal(random.randint(20, min(maxc, 35))) / 10  # longueur AB
    b = c * Decimal(sin(angABC)/sin(180 - angBAC - angABC)) # Longueur AC calculée avec la loi des sinus.

    exo.append(_(u"\\item Tracer un triangle $%s$ isocèle en $%s$ tel que $%s%s=\\SI{%s}{cm}$,  $\\widehat{%s%s%s}=\\ang{%s}$.")
               % (nom, C, A, B, decimaux(c), A, C, B, angACB))
    cor.append(_(u"\\item Tracer un triangle $%s$ isocèle en $%s$ tel que $%s%s=\\SI{%s}{cm}$,  $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, C, A, B, decimaux(c), A, C, B, angACB))
    cor.append(_(u"Comme $%s%s%s$ est un triangle isocèle en $%s$, on sait que les angles adjacents à la base sont de même mesure \
donc $\\widehat{%s%s%s}=\\widehat{%s%s%s}$.\\par") % (A, B, C, C, A, B, C, B, A, C))
    cor.append(_(u"De plus, on sait que la somme des mesures des trois angles d'un triangle est égale à \\ang{180} \\\\ \
donc $\\widehat{%s%s%s}=\\widehat{%s%s%s}=(\\ang{180}-\\ang{%s})\\div 2=\\ang{%s}$. \\par")
               % (B, A, C, A, B, C, angACB, angBAC))
    cor.append(textwrap.dedent(fr"""
    \begin{{tikzpicture}}[very thick]
        \coordinate (A) at (0, 0);
        \coordinate (B) at (0:{c}cm);
        \coordinate (C) at ({angBAC}:{b}cm);
        \draw (A) node[left] {{${A}$}};
        \draw (B) node[below right] {{${B}$}};
        \draw (C) node[above] {{${C}$}};
        \draw[Maroon] (A) -- (B) node[midway, below, color=enonce]{{\SI{{ {c} }}{{cm}}}};
        \draw[Maroon] (B) -- (C) -- ($(C)!-1cm!(B)$);
        \draw[Maroon] (A) -- (C) -- ($(C)!-1cm!(A)$);
        \draw pic [draw,calcul,angle radius=20pt, angle eccentricity=2, "\ang{{ {decimaux(angBAC)} }}"] {{angle = B--A--C}};
        \draw pic [draw,calcul,angle radius=20pt, angle eccentricity=2, "\ang{{ {decimaux(angBAC)} }}"] {{angle = C--B--A}};
        \draw pic [draw,enonce,angle radius=20pt, angle eccentricity=2, "\ang{{ {angACB} }}"] {{angle = A--C--B}};
    \end{{tikzpicture}}
    """))

def quest_rectangle_hypo_angle(exo, cor):
    """on donne un triangle ABC rectangle en C et l'hypotenuse AB et l'angle BAC"""
    A, B, C = geo.choix_points(3)
    nom = shuffle_nom([A, B, C])
    c = 2 * Decimal(random.randint(20, 35)) / 10  # longueur AB
    angBAC = 3 * random.randint(7, 23)  # un angle mesurant entre 21° et 69°
    angABC = 90 - angBAC
    b = c * Decimal(cos(angBAC))

    exo.append(_(u"\\item Tracer un triangle $%s$ rectangle en $%s$ tel que $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, C, A, B, decimaux(c), B, A, C, angBAC))
    cor.append(_(u"\\item Tracer un triangle $%s$ rectangle en $%s$ tel que $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, C, A, B, decimaux(c), B, A, C, angBAC))
# #    cor.append("\\begin{multicols}{2}")
    cor.append(_(u"On sait que dans un triangle rectangle, les deux angles aigus sont complémentaires \\\\ \
donc $\widehat{%s%s%s}=\\ang{90}-\\ang{%s}=\\ang{%s}$.\\par") % (B, A, C, angBAC, angABC))

    cor.append("\\figureadroite{")
    cor.append(textwrap.dedent(fr"""
    \begin{{tikzpicture}}[very thick]
        \coordinate (A) at (0, 0);
        \coordinate (B) at (0:{c}cm);
        \coordinate (C) at ({angBAC}:{b}cm);
        \draw (A) node[left] {{${A}$}};
        \draw (B) node[below right] {{${B}$}};
        \draw (C) node[above] {{${C}$}};
        \draw[Maroon] (A) -- (B) node[midway, below, color=enonce]{{\SI{{ {c} }}{{cm}}}};
        \draw[Maroon] (B) -- (C) -- ($(C)!-1cm!(B)$);
        \draw[Maroon] (A) -- (C) -- ($(C)!-1cm!(A)$);
        \draw pic [draw,enonce,angle radius=20pt, angle eccentricity=2, "\ang{{ {decimaux(angBAC)} }}"] {{angle = B--A--C}};
        \draw pic [draw,calcul,angle radius=20pt, angle eccentricity=2, "\ang{{ {decimaux(angABC)} }}"] {{angle = C--B--A}};
        \draw pic [draw,enonce] {{right angle = A--C--B}};
    \end{{tikzpicture}}
    """))
    cor.append(u"}{")
    cor.append("\\begin{enumerate}")
    cor.append(_(u"\\item On trace le segment $[%s%s]$ mesurant $\\SI{%s}{cm}$ ;") % (A, B, decimaux(c)))
    cor.append(_(u"\\item puis la demi-droite $[%s%s)$ en traçant l'angle~$\widehat{%s%s%s}$ ;") % (A, C, B, A, C))
    cor.append(_(u"\\item puis la demi-droite $[%s%s)$ en traçant l'angle~$\widehat{%s%s%s}$ ;") % (B, C, A, B, C))
# #    cor.append(u"\\item enfin on vérifie les trois {\\color{enonce}conditions de l'énoncé}.")
    cor.append("\\end{enumerate}\n")
# #    cor.append("\\end{multicols}")
    cor.append("}")

def quest_rectangle_hypo_cote(exo, cor):
    """on donne un triangle ABC rectangle en B et l'hypotenuse AC et le coté AB"""
    A, B, C = geo.choix_points(3)
    nom = shuffle_nom([A, B, C])
    c = 2 * Decimal(random.randint(20, 35)) / 10  # longueur AB
    b = Decimal(random.randint(int(10 * (c)) + 1, 100)) / 10  # longueur AC
    angABC = 90
    # calcul pour tracer
    angBAC = math.degrees(math.acos(c / b))

    exo.append(_(u"\\item Tracer un triangle $%s$ rectangle en $%s$ tel que $%s%s=\\SI{%s}{cm}$,  $%s%s=\\SI{%s}{cm}$.\\par")
               % (nom, B, A, B, decimaux(c), A, C, decimaux(b)))
    cor.append(_(u"\\item Tracer un triangle $%s$ rectangle en $%s$ tel que $%s%s=\\SI{%s}{cm}$, $%s%s=\\SI{%s}{cm}$.\\par")
               % (nom, B, A, B, decimaux(c), A, C, decimaux(b)))
    cor.append("\\figureadroite{")
    cor.append(textwrap.dedent(fr"""
    \begin{{tikzpicture}}[very thick]
        \coordinate (A) at (0, 0);
        \coordinate (B) at (0:{c}cm);
        \coordinate (C) at ({angBAC}:{b}cm);
        \draw (A) node[below left] {{${A}$}};
        \draw (B) node[below right] {{${B}$}};
        \draw (C) node[above right] {{${C}$}};
        \draw[Maroon] (A) -- (B) node[midway, below, color=enonce]{{\SI{{ {c} }}{{cm}}}};
        \draw[Maroon] (A) -- (C) node[midway, sloped, above, color=enonce]{{\SI{{ {b} }}{{cm}}}};
        \draw[Maroon] (B) -- (C) -- ($(C)!-1cm!(B)$);
        \draw[calcul] ({angBAC-10}:{b}cm) arc[radius={b}cm, start angle={angBAC-10}, delta angle=20];
        \draw pic [draw,enonce] {{right angle = A--B--C}};
    \end{{tikzpicture}}
    """))
    cor.append(u"}{")
    cor.append(u"\\begin{enumerate}")
    cor.append(_(u"\\item On trace le segment $[%s%s]$ mesurant $\\SI{%s}{cm}$ ;") % (A, B, decimaux(c)))
    cor.append(_(u"\\item puis on trace l'angle droit $\\widehat{%s%s%s}$ ;") % (A, B, C))
    cor.append(_(u"\\item enfin, on reporte au compas la longueur \\mbox{$%s%s=\\SI{%s}{cm}$} à partir de $%s$.")
                % (A, C, decimaux(b), A))
    cor.append("\\end{enumerate}}")


#################################################################################################
#   Les construction sont faites avec [AB] horizontale (ou avec la diagonale [AC] horizontale)
#       D-------C
#      /       /
#     /       /
#    A-------B
#   A est toujours l'origine : A(0,0)
#
#   AB est la longueur AB : type(float) en cm
#   angBAC est la mesure de l'angle BAC : type(int) en degrés
#   x_C,y_C sont les coordonnées cartésiennes du point C
#  les coordonnées polaires sont notées (5 ; 60)
#
###################################################################################################

def _exo_quadrilatere():

    exo = ["\\exercice",
         "\\begin{enumerate}"]
    cor = ["\\exercice*",
         "\\begin{enumerate}"]
    cor.append("\\definecolor{enonce}{rgb}{0.11,0.56,0.98}")
    # couleur pour reporter les informations de la consigne
    cor.append("\\definecolor{calcul}{rgb}{0.13,0.54,0.13}")
    # couleur pour reporter des informations déduites par raisonnement ou calcul

    # liste des questions possibles
    q_rectangle = [
           quest_rectangle_diag,
           quest_rectangle_angle,
           quest_rectangle_angle_diag,
           quest_rectangle_diag_angle,
           ]
    q_parallelogramme = [
           quest_parallelogramme_CCA,
           quest_parallelogramme_CDA,
           quest_parallelogramme_DDA,
           ]
    q_losange = [
           quest_losange_DD,
           quest_losange_AC,
           quest_losange_ACbis,
           quest_losange_CC,
           ]
    q_carre = [
           carre_diag,
           ]

    # on choisit un parallélogramme, un losange et un rectangle
    random.choice(q_rectangle)(exo, cor)
    random.choice(q_parallelogramme)(exo, cor)
    random.choice(q_losange)(exo, cor)
    #random.choice(q_carre)(exo, cor) # le carré n'est jamais proposé

    exo.append("\\end{enumerate}")
    cor.append("\\end{enumerate}")
    return exo, cor

class exo_quadrilatere(LegacyExercise):
    """Construction de parallélogrammes"""

    tags = [
        "Cinquième",
        "angles",
        "géométrie",
        "tracé",
    ]
    function = _exo_quadrilatere

################################################################

####### RECTANGLES #############

def quest_rectangle_diag(exo, cor):
    """on donne un rectangle ABCD avec un côté AB et une diagonale AC"""
    A, B, C, D = geo.choix_points(4)
    nom = shuffle_nom([A, B, C, D])
    L = Decimal(random.randint(40, 60)) / 10  # AB mesure entre 4cm et 7cm, tracé horizontalement
    Diag = Decimal(random.randint(10 * L + 10, 70))/10
    # Calcul pour tracer
    angBAC = math.degrees(math.acos(L / Diag))
    l = Diag * Decimal(sin(angBAC))

    exo.append(_(u"\\item Tracer un rectangle $%s$ tel que $%s%s=\\SI{%s}{cm}$ et $%s%s=\\SI{%s}{cm}$.\\par")
               % (nom, A, B, decimaux(L), A, C, decimaux(Diag)))
    cor.append(_(u"\\item Tracer un rectangle $%s$ tel que $%s%s=\\SI{%s}{cm}$ et $%s%s=\\SI{%s}{cm}$.\\par")
               % (nom, A, B, decimaux(L), A, C, decimaux(Diag)))
    # figure
    cor.append("\\figureadroite{")
    cor.append(textwrap.dedent(fr"""
        \begin{{tikzpicture}}[very thick]
        \coordinate (A) at (0, 0);
        \coordinate (B) at (0:{L});
        \coordinate (C) at ({angBAC}:{Diag});
        \coordinate (D) at (90:{l});
        \draw[Maroon] (A) -- (B);
        \draw[Maroon] (B) -- ($(C)!-.5cm!(B)$);
        \draw[Maroon] (C) -- ($(D)!-.5cm!(C)$);
        \draw[Maroon] (A) -- ($(D)!-.5cm!(A)$);
        \draw (A) node[below left]{{${A}$}};
        \draw (B) node[below right]{{${B}$}};
        \draw (C) node[above right]{{${C}$}};
        \draw (D) node[above left]{{${D}$}};
        \draw[Maroon] (A) -- (C) node[midway, above, sloped, enonce]{{\SI{{ {decimaux(Diag)} }}{{cm}}}};
        \draw[Maroon] (A) -- (B) node[midway, below, enonce]{{\SI{{ {decimaux(L)} }}{{cm}}}};
        \draw pic [draw,enonce] {{right angle = D--A--B}};
        \draw pic [draw,enonce] {{right angle = A--B--C}};
        \draw pic [draw,enonce] {{right angle = B--C--D}};
        \draw[calcul] ($(A)+({angBAC-10}:{Diag}cm)$) arc[radius={Diag}, start angle={angBAC-10}, delta angle=20];
    \end{{tikzpicture}}
    """))
    cor.append(u"}{")
    # Programme de construction
    cor.append(u"\\begin{enumerate}")
    cor.append(_(u"\\item On trace le segment $[%s%s]$ mesurant $\\SI{%s}{cm}$ ;") % (A, B, decimaux(L)))
    cor.append(_(u"\\item puis on trace l'angle droit $\\widehat{%s%s%s}$ ;") % (A, B, C))
    cor.append(_(u"\\item On reporte au compas la longueur $%s%s=\\SI{%s}{cm}$ à partir de $%s$ ;") % (A, C, decimaux(Diag), A))
    cor.append(_(u"\\item On trace enfin les angles droits en $%s$ et en $%s$ pour placer le point $%s$.") % (A, C, D))
    cor.append("\\end{enumerate}}")


def quest_rectangle_angle(exo, cor):
    """On donne un rectangle ABCD avec le côté AB et l'angle BAC"""
    A, B, C, D = geo.choix_points(4)
    nom = shuffle_nom([A, B, C, D])
    L = Decimal(random.randint(40, 60)) / 10  # AB mesure entre 4cm et 7cm, tracé horizontalement
    angBAC = random.randint(25, 65)
    l = L * Decimal(tan(angBAC))

    exo.append(_(u"\\item Tracer un rectangle $%s$ tel que $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, A, B, decimaux(L), B, A, C, angBAC))
    cor.append(_(u"\\item Tracer un rectangle $%s$ tel que $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, A, B, decimaux(L), B, A, C, angBAC))

    cor.append("\\figureadroite{")
    cor.append(textwrap.dedent(fr"""
        \begin{{tikzpicture}}[very thick]
        \coordinate (A) at (0, 0);
        \coordinate (B) at ({L}, 0);
        \coordinate (C) at ({L}, {l});
        \coordinate (D) at (0, {l});
        \draw[Maroon] (A) -- (B);
        \draw[Maroon] (B) -- ($(C)!-.5cm!(B)$);
        \draw[Maroon] (C) -- ($(D)!-.5cm!(C)$);
        \draw[Maroon] (A) -- ($(D)!-.5cm!(A)$);
        \draw (A) node[below left]{{${A}$}};
        \draw (B) node[below right]{{${B}$}};
        \draw (C) node[below right]{{${C}$}};
        \draw (D) node[above left]{{${D}$}};
        \draw[Maroon] (A) -- (B) node[midway, below, enonce]{{\SI{{ {decimaux(L)} }}{{cm}}}};
        \draw[Maroon] (A) -- ($(C)!-1cm!(A)$);
        \draw pic [draw,enonce] {{right angle = D--A--B}};
        \draw pic [draw,enonce] {{right angle = A--B--C}};
        \draw pic [draw,enonce] {{right angle = B--C--D}};
        \draw pic [draw,enonce,angle radius=25pt, angle eccentricity=2, "\ang{{ {angBAC} }}"] {{angle = B--A--C}};
    \end{{tikzpicture}}
    """))
    cor.append(u"}{")
    # Programme de construction
    cor.append(u"\\begin{enumerate}")
    cor.append(_(u"\\item On trace le segment $[%s%s]$ mesurant $\\SI{%s}{cm}$ ;") % (A, B, decimaux(L)))
    cor.append(_(u"\\item puis on trace l'angle droit $\\widehat{%s%s%s}$ ;") % (A, B, C))
    cor.append(_(u"\\item la demi-droite $[%s%s)$ en mesurant $\\widehat{%s%s%s}=\\ang{%s}$.") % (A, C, B, A, C, angBAC))
    cor.append(_(u"\\item On trace enfin les angles droit en $%s$ et en $%s$ pour placer le point $%s$.") % (A, C, D))
    cor.append("\\end{enumerate}}")

def quest_rectangle_angle_diag(exo, cor):
    """On donne un rectangle ABCD de centre E, la diagonale AC et l'angle AEB"""
    A, B, C, D, E = geo.choix_points(5)
    nom = shuffle_nom([A, B, C, D])
    angAEB = 2 * random.randint(20, 70)
    Diag = 2 * Decimal(random.randint(25, 45)) / 10
    # calcul pour tracer
    angBAC = (180 - angAEB) // 2

    exo.append(_(u"\\item Tracer un rectangle $%s$ de centre $%s$ tel que $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, E, A, C, decimaux(Diag), A, E, B, angAEB))
    cor.append(_(u"\\item Tracer un rectangle $%s$ de centre $%s$ tel que $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, E, A, C, decimaux(Diag), A, E, B, angAEB))
# #    cor.append("\\begin{multicols}{2}")
    cor.append("\\figureadroite{")
    cor.append(textwrap.dedent(fr"""
        \begin{{tikzpicture}}[very thick]
        \coordinate (E) at (0, 0);
        \coordinate (A) at ({270-angAEB/2}:{Diag/2});
        \coordinate (B) at ({270+angAEB/2}:{Diag/2});
        \coordinate (C) at ({90-angAEB/2}:{Diag/2});
        \coordinate (D) at ({90+angAEB/2}:{Diag/2});
        \draw[Maroon] ($(B)!-5mm!(D)$) -- ($(D)!-5mm!(B)$);
        \draw[Maroon] (A) -- (B) -- (C) -- (D) -- cycle;
        \draw[Maroon] (A) -- (C) node[enonce, sloped, midway, above, inner sep=1pt,  text opacity=1, fill=white, opacity=.5]{{\SI{{{decimaux(Diag)}}}{{cm}}}};
        \draw[color=calcul, draw,decoration={{markings, mark=at position .5  with {{\node[transform shape] {{$\parallel$}};}}}}]
            (E) edge[decorate] (A)
            (E) edge[decorate] (B)
            (E) edge[decorate] (C)
            (E) edge[decorate] (D);
        \draw (A) node[below left]{{${A}$}};
        \draw (B) node[below]{{${B}$}};
        \draw (C) node[above right]{{${C}$}};
        \draw (D) node[left]{{${D}$}};
        \draw (E) node[right]{{${E}$}};
        \draw pic [draw,enonce,angle radius=20pt, angle eccentricity=1.5, "\ang{{ {angAEB} }}"] {{angle = A--E--B}};
        \draw[calcul] ($(E)+({260+angAEB/2}:{Diag/2}cm)$) arc[radius={Diag/2}cm, start angle={260+angAEB/2}, delta angle=20];
        \draw[calcul] ($(E)+({80+angAEB/2}:{Diag/2}cm)$) arc[radius={Diag/2}cm, start angle={80+angAEB/2}, delta angle=20];
    \end{{tikzpicture}}
    """))
    cor.append(u"}{")
    cor.append(u"\\begin{enumerate}")
    cor.append(_(u"\\item On trace le segment $[%s%s]$ mesurant $\\SI{%s}{cm}$ ;") % (A, C, decimaux(Diag)))
    cor.append(_(u"\\item le centre du rectangle est le milieu des diagonales donc $%s$ est le milieu de $[%s%s]$ ;") % (E, A, C))
    cor.append(_(u"\\item On trace la diagonale $(%s%s)$ passant par $%s$ en mesurant \\mbox{$\\widehat{%s%s%s}=\\ang{%s}$} ;")
               % (B, D, E, A, E, B, angAEB))
    cor.append(_(u"\\item Comme les diagonales du rectangle sont de même longueur, on reporte les longueurs $%s%s=%s%s=\\SI{%s}{cm}$.")
               % (E, D, E, B, decimaux(Diag / 2)))
# #    cor.append(_(u"\\item On trace enfin les angles droits en $%s$ et en $%s$ pour palcer le point $%s$.")%(A,C,D))
    cor.append("\\end{enumerate}}")
# #    cor.append("\\end{multicols}")

def quest_rectangle_diag_angle(exo, cor):
    """On donne un rectangle ABCD la diagonale AC et l'angle BAC"""
    A, B, C, D = geo.choix_points(4)
    nom = shuffle_nom([A, B, C, D])
    angBAC = random.randint(25, 65)
    Diag = Decimal(random.randint(50, 80)) / 10
    # Calcul
    L = Diag * Decimal(cos(angBAC))
    l = Diag * Decimal(sin(angBAC))

    exo.append(_(u"\\item Tracer un rectangle $%s$ tel que $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, A, C, decimaux(Diag), B, A, C, angBAC))
    cor.append(_(u"\\item Tracer un rectangle $%s$ tel que $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, A, C, decimaux(Diag), B, A, C, angBAC))

    cor.append("\\figureadroite{")
    cor.append(textwrap.dedent(fr"""
        \begin{{tikzpicture}}[very thick]
        \coordinate (A) at (0, 0);
        \coordinate (B) at (0:{L});
        \coordinate (C) at ({angBAC}:{Diag});
        \coordinate (D) at (90:{l});
        \draw[Maroon] (A) -- ($(B)!-.5cm!(A)$);
        \draw[Maroon] ($(B)!-.5cm!(C)$) -- ($(C)!-.5cm!(B)$);
        \draw[Maroon] (C) -- ($(D)!-.5cm!(C)$);
        \draw[Maroon] (A) -- ($(D)!-.5cm!(A)$);
        \draw (A) node[below left]{{${A}$}};
        \draw (B) node[below right]{{${B}$}};
        \draw (C) node[above right]{{${C}$}};
        \draw (D) node[above left]{{${D}$}};
        \draw[Maroon] (A) -- (C) node[midway, above, sloped, enonce]{{\SI{{ {decimaux(Diag)} }}{{cm}}}};
        \draw pic [draw,enonce] {{right angle = D--A--B}};
        \draw pic [draw,enonce] {{right angle = A--B--C}};
        \draw pic [draw,enonce] {{right angle = B--C--D}};
        \draw pic [draw,enonce,angle radius=25pt, angle eccentricity=2, "\ang{{ {angBAC} }}"] {{angle = B--A--C}};
    \end{{tikzpicture}}
    """))
    cor.append(u"}{")
    # Programme de construction
    cor.append(u"\\begin{enumerate}")
    cor.append(_(u"\\item On tracer le segment $[%s%s]$ mesurant $\\SI{%s}{cm}$ ;") % (A, C, decimaux(Diag)))
    cor.append(_(u"\\item la demi-droite $[%s%s)$ en mesurant \\mbox{$\\widehat{%s%s%s}=\\ang{%s}$} ;") % (A, B, B, A, C, angBAC))
    cor.append(_(u"\\item puis la perpendiculaire à $[%s%s)$ passant par~$%s$ ;") % (A, B, C))
    cor.append(_(u"\\item On tracer enfin les angles droits en $%s$ et en $%s$ pour placer le point~$%s$.") % (A, C, D))
    cor.append("\\end{enumerate}}")

################## PARALLÉLOGRAMMES QUELCONQUES ###########################

def quest_parallelogramme_CCA(exo, cor):
    """On donne un parallélogramme avec la longueur de deux côtés et un angle."""
    # 3 choix d'angle : CC ou un autre angle CC ou un angle Côté Diagonale
    A, B, C, D = geo.choix_points(4)
    nom = shuffle_nom([A, B, C, D])
    AB = Decimal(random.randint(40, 60)) / 10  # AB mesure entre 4cm et 7cm, tracé horizontalement
    AD = Decimal(random.randint(40, 60)) / 10  # AD mesure entre 4cm et 7cm, tracé horizontalement
    angBAD = random.randint(25, 65)

    exo.append(_(u"\\item Tracer un parallélogramme $%s$ tel que $%s%s=\\SI{%s}{cm}$, $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, A, B, decimaux(AB), D, A, decimaux(AD), B, A, D, angBAD))
    cor.append(_(u"\\item Tracer un parallélogramme $%s$ tel que $%s%s=\\SI{%s}{cm}$, $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, A, B, decimaux(AB), D, A, decimaux(AD), B, A, D, angBAD))
    cor.append(u"\\begin{enumerate}")
    cor.append(_(u"\\item On trace le segment $[%s%s]$ mesurant $\\SI{%s}{cm}$ ;") % (A, B, decimaux(AB)))
    cor.append(_(u"\\item On mesure l'angle  $\\widehat{%s%s%s}=\\ang{%s}$ puis on place le point~$%s$ ;") % (B, A, D, angBAD, D))
    cor.append(_(u"\\item enfin on reporte les longueurs $%s%s=%s%s$ et $%s%s=%s%s$ pour place le point~$%s$.")
               % (D, C, A, B, B, C, A, D, C))
    cor.append("\\end{enumerate}\n")
    cor.append(textwrap.dedent(fr"""
    \begin{{tikzpicture}}[very thick]
        \coordinate (A) at (0, 0);
        \coordinate (B) at (0:{AB}cm);
        \coordinate (D) at ({angBAD}:{AD}cm);
        \coordinate (C) at ($(B) + (D) - (A)$);
        \draw (A) node[below left] {{${A}$}};
        \draw (B) node[below right] {{${B}$}};
        \draw (C) node[above right] {{${C}$}};
        \draw (D) node[above left] {{${D}$}};
        \draw[Maroon] (D)
            -- (C)
            -- (B)
            -- (A) node[midway, below, color=enonce]{{\SI{{ {decimaux(AB)} }}{{cm}}}}
            -- (D) node[midway, above, sloped, color=enonce]{{\SI{{ {decimaux(AD)} }}{{cm}}}}
            -- ($(D)!-5mm!(A)$);
        \draw[color=enonce, draw,decoration={{markings, mark=at position .5  with {{\node[transform shape] {{$\parallel$}};}}}}]
            (A) edge[decorate] (B)
            (C) edge[decorate] (D);
        \draw[color=enonce, draw,decoration={{markings, mark=at position .5  with {{\node[transform shape] {{$\times$}};}}}}]
            (B) edge[decorate] (C)
            (D) edge[decorate] (A);
        \draw[calcul] ($(A)+({angBAD-10}:{AD}cm)$) arc[radius={AD}, start angle={angBAD-10}, delta angle=20];
        \draw[calcul] ($(D)+(-10:{AB}cm)$) arc[radius={AB}, start angle=-10, delta angle=20];
        \draw[calcul] ($(B)+({angBAD-10}:{AD}cm)$) arc[radius={AD}, start angle={angBAD-10}, delta angle=20];
        \draw pic [draw,enonce,angle radius=20pt, angle eccentricity=2, "\ang{{ {angBAD} }}"] {{angle = B--A--D}};
    \end{{tikzpicture}}
    """))

def quest_parallelogramme_CDA(exo, cor):
    """On donne un parallélogramme avec la longueur d'un côté et une diagonale et l'angle entre ces deux segments"""

    A, B, C, D = geo.choix_points(4)
    nom = shuffle_nom([A, B, C, D])
    AB = Decimal(random.randint(40, 60)) / 10  # AB mesure entre 4cm et 7cm, tracé horizontalement
    AC = Decimal(random.randint(40, 70)) / 10  # AC mesure entre 4cm et 7cm, tracé horizontalement
    angBAC = random.randint(25, 65)
    AD = Decimal(math.sqrt(AB**2+AC**2-2*AB*AC*Decimal(cos(angBAC)))) # Théorème d'Al-Kashi
    angACB = math.degrees(math.acos((AC**2+AD**2-AB**2)/(2*AD*AC))) # Théorème d'Al-Kashi

    exo.append(_(u"\\item Tracer un parallélogramme $%s$ tel que $%s%s=\\SI{%s}{cm}$, $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, A, B, decimaux(AB), C, A, decimaux(AC), B, A, C, angBAC))
    cor.append(_(u"\\item Tracer un parallélogramme $%s$ tel que $%s%s=\\SI{%s}{cm}$, $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, A, B, decimaux(AB), C, A, decimaux(AC), B, A, C, angBAC))
    # Programme de construction
    cor.append(u"\\begin{enumerate}")
    cor.append(_(u"\\item On trace le segment $[%s%s]$ mesurant $\\SI{%s}{cm}$ ;") % (A, B, decimaux(AB)))
    cor.append(_(u"\\item On trace la demi-droite $[%s%s)$ en mesurant $\\widehat{%s%s%s}=\\ang{%s}$ ;") % (A, C, B, A, C, angBAC))
    cor.append(_(u"\\item On place le point $%s$ en mesurant $%s%s=\\SI{%s}{cm}$ ;") % (C, A, C, decimaux(AC)))
    cor.append(_(u"\\item On construit le point $%s$ en reportant au compas $%s%s=%s%s$ et $%s%s=%s%s$.")
               % (D, C, D, B, A, A, D, B, C))
    cor.append("\\end{enumerate}\n")
    cor.append(textwrap.dedent(fr"""
    \begin{{tikzpicture}}[very thick]
        \coordinate (A) at (0, 0);
        \coordinate (B) at (0:{AB}cm);
        \coordinate (C) at ({angBAC}:{AC}cm);
        \coordinate (D) at ($(A)+(C)-(B)$);
        \draw (A) node[below left] {{${A}$}};
        \draw (B) node[below right] {{${B}$}};
        \draw (C) node[above right] {{${C}$}};
        \draw (D) node[above left] {{${D}$}};
        \draw[Maroon] (A)
            -- (B) node[midway, below, color=enonce]{{\SI{{ {decimaux(AB)} }}{{cm}}}}
            -- (C)
            -- (D)
            -- cycle;
        \draw[Maroon] (A) -- (C) node[midway, above, sloped, color=enonce]{{\SI{{ {decimaux(AC)} }}{{cm}}}} -- ($(C)!-5mm!(A)$);
        \draw[color=calcul, draw,decoration={{markings, mark=at position .5  with {{\node[transform shape] {{$\parallel$}};}}}}]
            (A) edge[decorate] (B)
            (C) edge[decorate] (D);
        \draw[color=calcul, draw,decoration={{markings, mark=at position .5  with {{\node[transform shape] {{$\times$}};}}}}]
            (B) edge[decorate] (C)
            (D) edge[decorate] (A);
        \draw pic [draw,enonce,angle radius=20pt, angle eccentricity=2, "\ang{{ {angBAC} }}"] {{angle = B--A--C}};
        \draw[calcul] ({angBAC-10}:{AC}) arc[radius={AC}, start angle={angBAC-10}, delta angle=20];
        \draw[calcul] ({angBAC + angACB - 10}:{AD}) arc[radius={AD}, start angle={angBAC + angACB - 10}, delta angle=20];
        \draw[calcul] ($(C)+(170:{AB}cm)$) arc[radius={AB}, start angle=170, delta angle=20];
    \end{{tikzpicture}}
    """))

def quest_parallelogramme_DDA(exo, cor):
    """On donne un parallélogramme avec la longueur des deux diagonales et l'angle entre les diagonales"""
    # choix d'angle : on pourrait donner l'angle BAC
    # diagonale ou demi-diagonale
    A, B, C, D, E = geo.choix_points(5)
    nom = shuffle_nom([A, B, C, D])
    BD = 2 * Decimal(random.randint(20, 40)) / 10  # AB mesure entre 4cm et 8cm, tracé horizontalement
    AC = 2 * Decimal(random.randint(20, 40)) / 10  # AC mesure entre 4cm et 8cm, tracé horizontalement
    angAEB = random.randint(35, 145)

    # calcul pour tracer
    AE = AC/2
    BE = BD/2
    AB = Decimal(math.sqrt(AE ** 2 + BE ** 2 - 2 * AE * BE * Decimal(cos(angAEB)))) # Théorème d'Al Kashi
    angBAC = math.degrees(math.asin(BE * Decimal(sin(angAEB)) / AB))

    exo.append(_(u"\\item Tracer un parallélogramme $%s$ de centre $%s$ tel que $%s%s=\\SI{%s}{cm}$, $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, E, A, C, decimaux(AC), B, D, decimaux(BD), A, E, B, angAEB))
    cor.append(_(u"\\item Tracer un parallélogramme $%s$ de centre $%s$ tel que $%s%s=\\SI{%s}{cm}$, $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, E, A, C, decimaux(AC), B, D, decimaux(BD), A, E, B, angAEB))
    cor.append(u"\\begin{enumerate}")
    cor.append(_(u"\\item On trace le segment $[%s%s]$ mesurant $\\SI{%s}{cm}$ ;") % (A, C, decimaux(AC)))
    cor.append(_(u"\\item Dans un parallélogramme les diagonales se coupent en leur milieu donc $%s%s=%s%s=\\SI{%s}{cm}$ et $%s%s=%s%s=\\SI{%s}{cm}$ ;")
               % (A, E, C, E, decimaux(AC / 2), B, E, E, D, decimaux(BD / 2)))
    cor.append("\\end{enumerate}\n")
    cor.append(textwrap.dedent(fr"""
    \begin{{tikzpicture}}[very thick]
        \coordinate (E) at (0, 0);
        \coordinate (A) at ({180+angBAC}:{AC/2}cm);
        \coordinate (B) at ({180+angBAC+angAEB}:{BD/2}cm);
        \coordinate (C) at ($2*(E)-(A)$);
        \coordinate (D) at ($2*(E)-(B)$);
        \draw (A) node[below left] {{${A}$}};
        \draw (B) node[right] {{${B}$}};
        \draw (C) node[above right] {{${C}$}};
        \draw (D) node[left] {{${D}$}};
        \draw (E) node[above] {{${E}$}};
        \draw[Maroon] (A) -- (B) -- (C) -- (D) -- cycle;
        \draw[Maroon] ($(B)!-5mm!(D)$) -- ($(D)!-5mm!(B)$);
        \path (B) -- (D) node[pos=.25, sloped, above, calcul]{{\SI{{{BE}}}{{cm}}}};
        \draw[Maroon] (A) -- (C) node[enonce, sloped, midway, above, inner sep=1pt,  text opacity=1, fill=white, opacity=.5]{{\SI{{{decimaux(AC)}}}{{cm}}}};

        \draw[color=calcul, draw,decoration={{markings, mark=at position .5  with {{\node[transform shape] {{$\parallel$}};}}}}]
            (E) edge[decorate] (B)
            (E) edge[decorate] (D);
        \draw[color=calcul, draw,decoration={{markings, mark=at position .5  with {{\node[transform shape] {{$\times$}};}}}}]
            (E) edge[decorate] (C)
            (E) edge[decorate] (A);
        \draw pic [draw,enonce,angle radius=20pt, angle eccentricity=2, "\ang{{ {angAEB} }}"] {{angle = A--E--B}};
        \draw[calcul] ($(E)+({angAEB+angBAC-10}:{BE}cm)$) arc[radius={BE}, start angle={angAEB+angBAC-10}, delta angle=20];
        \draw[calcul] ($(E)+({angAEB+angBAC+170}:{BE}cm)$) arc[radius={BE}, start angle={angAEB+angBAC+170}, delta angle=20];
    \end{{tikzpicture}}
    """))

###################### LOSANGES ########################

def quest_losange_DD(exo, cor):
    """On donne un losange avec la longueur des deux diagonales"""
    # diagonale ou demi-diagonale
    A, B, C, D, E = geo.choix_points(5)
    nom = shuffle_nom([A, B, C, D])
    BD = 2 * Decimal(random.randint(15, 25)) / 10 # AB mesure entre 4cm et 8cm, tracé horizontalement
    AC = 2 * Decimal(random.randint(20, 40)) / 10  # AC mesure entre 4cm et 8cm, tracé horizontalement

    exo.append(_(u"\\item Tracer un losange $%s$  tel que $%s%s=\\SI{%s}{cm}$ et $%s%s=\\SI{%s}{cm}$.\\par")
               % (nom, A, C, decimaux(AC), B, D, decimaux(BD)))
    cor.append(_(u"\\item Tracer un losange $%s$  tel que $%s%s=\\SI{%s}{cm}$ et $%s%s=\\SI{%s}{cm}$.\\par")
               % (nom, A, C, decimaux(AC), B, D, decimaux(BD)))

    cor.append(_(u"On note $%s$ le centre du losange.\\par") % E)

    cor.append("\\figureadroite{")
    cor.append(textwrap.dedent(fr"""
    \begin{{tikzpicture}}[very thick]
        \coordinate (E) at (0, 0);
        \coordinate (A) at (0:{AC/2}cm);
        \coordinate (C) at (0:{-AC/2}cm);
        \coordinate (B) at (90:{BD/2}cm);
        \coordinate (D) at (90:{-BD/2}cm);
        \draw[Maroon] (A) -- (B) -- (C) -- (D) -- cycle;
        \draw[Maroon] (A) -- (C) node[calcul, pos=.25, below]{{\SI{{{decimaux(AC/2)}}}{{cm}}}};
        \draw[Maroon] (B) -- (D) node[calcul, pos=.25, above, sloped]{{\SI{{{decimaux(BD/2)}}}{{cm}}}};
        \draw (A) node[right]{{${A}$}};
        \draw (B) node[above]{{${B}$}};
        \draw (C) node[left]{{${C}$}};
        \draw (D) node[below]{{${D}$}};
        \draw (E) node[below left]{{${E}$}};
        \draw[color=enonce, draw,decoration={{markings, mark=at position .5  with {{\node[transform shape] {{$\parallel$}};}}}}]
            (A) edge[decorate] (B)
            (B) edge[decorate] (C)
            (C) edge[decorate] (D)
            (D) edge[decorate] (A);
        \draw[color=enonce, draw,decoration={{markings, mark=at position .5  with {{\node[transform shape] {{$\times$}};}}}}]
            (A) edge[decorate] (E)
            (B) edge[decorate] (E)
            (C) edge[decorate] (E)
            (D) edge[decorate] (E);
        \draw pic [draw,enonce] {{right angle = A--E--B}};
        \draw[calcul] ($(E)+(-10:{AC/2}cm)$) arc[radius={AC/2}cm, start angle=-10, delta angle=20];
        \draw[calcul] ($(E)+(170:{AC/2}cm)$) arc[radius={AC/2}cm, start angle=170, delta angle=20];
        \draw[calcul] ($(E)+(80:{BD/2}cm)$) arc[radius={BD/2}cm, start angle=80, delta angle=20];
        \draw[calcul] ($(E)+(260:{BD/2}cm)$) arc[radius={BD/2}cm, start angle=260, delta angle=20];
    \end{{tikzpicture}}
    """))
    cor.append(u"}{")
    cor.append(_(u"Les diagonales du losange se coupent perpendiculairement en leur milieu~$%s$ ;  on a donc :") % E)
    cor.append(u"\\begin{enumerate}")
    cor.append(u"\\item $%s%s=%s%s=\\SI{%s}{cm}$ \\item $%s%s=%s%s=\\SI{%s}{cm}$ ;"
               % (A, E, C, E, decimaux(AC / 2), B, E, E, D, decimaux(BD / 2)))
    cor.append(u"\\item $(%s%s)\\perp(%s%s)$." % (A, C, B, D))
    cor.append("\\end{enumerate}}\n")

def quest_losange_CC(exo, cor):
    """On donne un losange avec la longueur d'un côté et un angle entre côtés"""
    # diagonale ou demi-diagonale
    A, B, C, D = geo.choix_points(4)
    nom = shuffle_nom([A, B, C, D])
    AB = 0.2 * random.randint(15, 25)  # AB mesure entre 4cm et 8cm, tracé horizontalement
    angBAD = random.randint(30, 150)
    # Calcul pour tracer

    exo.append(_(u"\\item Tracer un losange $%s$  tel que $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, A, B, decimaux(AB), B, A, D, angBAD))
    cor.append(_(u"\\item Tracer un losange $%s$  tel que $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, A, B, decimaux(AB), B, A, D, angBAD))

    cor.append(_(u"Les quatre côtés du losange sont de même longueur donc $%s%s=%s%s=%s%s=%s%s=\\SI{%s}{cm}$ ;") % (A, B, B, C, C, D, D, A, decimaux(AB)))
    cor.append(u"\\begin{enumerate}")
    cor.append(_(u"\\item On trace le côté $[%s%s]$ puis on mesure l'angle $\\widehat{%s%s%s}=\\ang{%s}$ ;") % (A, B, B, A, D, angBAD))
    cor.append(_(u"\\item ensuite on reporte au compas les longueurs $%s%s$ et $%s%s$ pour construire le point $%s$.") % (C, D, B, C, C))
    cor.append("\\end{enumerate}\n")
    cor.append(textwrap.dedent(fr"""
    \begin{{tikzpicture}}[very thick, radius={AB}cm]
        \coordinate (A) at (0, 0);
        \coordinate (B) at (0:{AB}cm);
        \coordinate (D) at ({angBAD}:{AB}cm);
        \coordinate (C) at ($(B)+(D)-(A)$);
        \draw[Maroon] (A) -- (B) node[enonce, midway, above]{{\SI{{{decimaux(AB)}}}{{cm}}}};
        \draw (A) node[below left]{{${A}$}};
        \draw (B) node[below right]{{${B}$}};
        \draw (C) node[above right]{{${C}$}};
        \draw (D) node[above left]{{${D}$}};
        \draw[Maroon] (D) -- (C) -- (B) -- (A) -- ($(D)!-5mm!(A)$);
        \draw[color=enonce, draw,decoration={{markings, mark=at position .5  with {{\node[transform shape] {{$\parallel$}};}}}}]
            (A) edge[decorate] (B)
            (B) edge[decorate] (C)
            (C) edge[decorate] (D)
            (D) edge[decorate] (A);
        \draw pic [draw,enonce,angle radius=20pt, angle eccentricity=1.5, "\ang{{{angBAD}}}"] {{angle = B--A--D}};
        \draw[calcul] ($(A)+({angBAD-10}:{AB}cm)$) arc[start angle={angBAD-10}, delta angle=20];
        \draw[calcul] ($(B)+({angBAD-10}:{AB}cm)$) arc[start angle={angBAD-10}, delta angle=20];
        \draw[calcul] ($(D)+(-10:{AB}cm)$) arc[start angle=-10, delta angle=20];
    \end{{tikzpicture}}
    """))

def quest_losange_AC(exo, cor):
    """On donne un losange avec la longueur d'une diagonale et la mesure d'un angle entre un côté et cette diagonale"""

    A, B, C, D = geo.choix_points(4)
    nom = shuffle_nom([A, B, C, D])
    AC = Decimal(random.randint(40, 60)) / 10  # AB mesure entre 4cm et 7cm, tracé horizontalement
    angBAC = random.randint(25, 75)
    AB = AC / (2 * Decimal(cos(angBAC)))

    exo.append(_(u"\\item Tracer un losange $%s$ tel que $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, A, C, decimaux(AC), B, A, C, angBAC))
    cor.append(_(u"\\item Tracer un losange $%s$ tel que $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, A, C, decimaux(AC), B, A, C, angBAC))
    # Rédaction
    cor.append(_(u" Comme $%s$ est un losange, on sait que $\\widehat{%s%s%s}=\\widehat{%s%s%s}=\\widehat{%s%s%s}=\\widehat{%s%s%s}=\\ang{%s}$.")
               % (nom, B, A, C, A, C, B, A, C, D, C, A, D, angBAC))
    # Programme de construction
    cor.append(u"\\begin{enumerate}")
    cor.append(_(u"\\item On trace le segment $[%s%s]$ mesurant $\\SI{%s}{cm}$ ;") % (A, C, decimaux(AC)))
    cor.append(_(u"\\item On trace $\\widehat{%s%s%s}$ et $\\widehat{%s%s%s}$ pour construire le point $%s$ ;") % (B, A, C, A, C, B, B))
    cor.append(_(u"\\item On trace $\\widehat{%s%s%s}$ et $\\widehat{%s%s%s}$ pour construire le point $%s$ ;") % (A, C, D, C, A, D, D))
    cor.append("\\end{enumerate}\n")
    cor.append(textwrap.dedent(fr"""
    \begin{{tikzpicture}}[very thick]
        \coordinate (A) at (0, 0);
        \coordinate (C) at (0:{AC}cm);
        \coordinate (B) at ({-angBAC}:{AB}cm);
        \coordinate (D) at ({angBAC}:{AB}cm);
        \draw[Maroon] (A) -- (C) node[enonce, midway, above]{{\SI{{{decimaux(AC)}}}{{cm}}}};
        \draw (A) node[left]{{${A}$}};
        \draw (B) node[below]{{${B}$}};
        \draw (C) node[right]{{${C}$}};
        \draw (D) node[above]{{${D}$}};
        \draw[Maroon] (A) -- ($(B)!-5mm!(A)$);
        \draw[Maroon] (A) -- ($(D)!-5mm!(A)$);
        \draw[Maroon] (C) -- ($(B)!-5mm!(C)$);
        \draw[Maroon] (C) -- ($(D)!-5mm!(C)$);
        \draw[color=enonce, draw,decoration={{markings, mark=at position .5  with {{\node[transform shape] {{$\parallel$}};}}}}]
            (A) edge[decorate] (B)
            (B) edge[decorate] (C)
            (C) edge[decorate] (D)
            (D) edge[decorate] (A);
        \draw pic [draw,enonce,angle radius=20pt, angle eccentricity=2, "\ang{{{angBAC}}}"] {{angle = B--A--C}};
        \draw pic [enonce,angle radius=20pt, angle eccentricity=1, "\times"] {{angle = B--A--C}};
        \draw pic [draw,calcul,angle radius=20pt, angle eccentricity=1, "\times"] {{angle = C--A--D}};
        \draw pic [draw,calcul,angle radius=20pt, angle eccentricity=1, "\times"] {{angle = A--C--B}};
        \draw pic [draw,calcul,angle radius=20pt, angle eccentricity=1, "\times"] {{angle = D--C--A}};
    \end{{tikzpicture}}
    """))

def quest_losange_ACbis(exo, cor):
    """On donne un losange avec la longueur d'une diagonale et la mesure d'un angle opposé à la diagonale."""

    A, B, C, D = geo.choix_points(4)
    nom = shuffle_nom([A, B, C, D])
    AC = Decimal(random.randint(40, 60)) / 10  # AC mesure entre 4cm et 7cm, tracé horizontalement
    angCDA = 2 * random.randint(15, 70)
    angCAD = (180 - angCDA) // 2
    AB = AC / (2 * Decimal(cos(angCAD)))

    exo.append(_(u"\\item Tracer un losange $%s$ tel que $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, A, C, decimaux(AC), C, D, A, angCDA))
    cor.append(_(u"\\item Tracer un losange $%s$ tel que $%s%s=\\SI{%s}{cm}$ et $\\widehat{%s%s%s}=\\ang{%s}$.\\par")
               % (nom, A, C, decimaux(AC), C, D, A, angCDA))

    # Rédaction des calculs
    cor.append(_(u"Les quatre côtés du losange sont de même longueur donc $%s%s=%s%s=%s%s=%s%s$.\\par") % (A, B, B, C, C, D, D, A))
    cor.append(_(u"Ainsi, le triangle $%s%s%s$ est isocèle en $%s$ et on peut calculer la mesure des angles $\\widehat{%s%s%s}=\\widehat{%s%s%s}$.\\par")
               % (A, C, D, A, A, C, D, C, A, D))
    cor.append(_(u"Dans un triangle, la somme des angles du triangle est égale à \\ang{180}\\\\"))
    cor.append(_(u"donc $\\widehat{%s%s%s}=\\widehat{%s%s%s}=(\\ang{180}-%s)\\div2=\\ang{%s}$") % (A, C, D, C, A, D, angCDA, angCAD))
    # Programme de construction
    cor.append(u"\\begin{enumerate}")
    cor.append(_(u"\\item On trace le segment $[%s%s]$ mesurant $\\SI{%s}{cm}$ ;") % (A, C, decimaux(AC)))
    cor.append(_(u"\\item On trace $\\widehat{%s%s%s}$ et $\\widehat{%s%s%s}$ pour construire le point $%s$ ;") % (B, A, C, A, C, B, B))
    cor.append(_(u"\\item On trace $\\widehat{%s%s%s}$ et $\\widehat{%s%s%s}$ pour construire le point $%s$ ;") % (A, C, D, C, A, D, D))
    cor.append("\\end{enumerate}\n")

    cor.append(textwrap.dedent(fr"""
    \begin{{tikzpicture}}[very thick]
        \coordinate (A) at (0, 0);
        \coordinate (C) at (0:{AC}cm);
        \coordinate (B) at ({-angCAD}:{AB}cm);
        \coordinate (D) at ({angCAD}:{AB}cm);
        \draw[Maroon] (A) -- (C) node[enonce, midway, above]{{\SI{{{decimaux(AC)}}}{{cm}}}};
        \draw (A) node[left]{{${A}$}};
        \draw (B) node[below]{{${B}$}};
        \draw (C) node[right]{{${C}$}};
        \draw (D) node[above]{{${D}$}};
        \draw[Maroon] (A) -- ($(B)!-5mm!(A)$);
        \draw[Maroon] (A) -- ($(D)!-5mm!(A)$);
        \draw[Maroon] (C) -- ($(B)!-5mm!(C)$);
        \draw[Maroon] (C) -- ($(D)!-5mm!(C)$);
        \draw[color=enonce, draw,decoration={{markings, mark=at position .5  with {{\node[transform shape] {{$\parallel$}};}}}}]
            (A) edge[decorate] (B)
            (B) edge[decorate] (C)
            (C) edge[decorate] (D)
            (D) edge[decorate] (A);
        \draw pic [draw,enonce,angle radius=20pt, angle eccentricity=1.5, "\ang{{{decimaux(angCDA)}}}"] {{angle = A--D--C}};
        \draw pic [draw,calcul,angle radius=20pt, angle eccentricity=1.5, "\ang{{{decimaux(angCAD)}}}"] {{angle = C--A--D}};
        \draw pic [draw,calcul,angle radius=20pt, angle eccentricity=1, "\times"] {{angle = B--A--C}};
        \draw pic [draw,calcul,angle radius=20pt, angle eccentricity=1, "\times"] {{angle = C--A--D}};
        \draw pic [draw,calcul,angle radius=20pt, angle eccentricity=1, "\times"] {{angle = A--C--B}};
        \draw pic [draw,calcul,angle radius=20pt, angle eccentricity=1, "\times"] {{angle = D--C--A}};
    \end{{tikzpicture}}
    """))

################### CARRÉ #######################

def carre_diag(exo, cor):
    """trace un carré dont on donne la longueur de la diagonale"""

    A, B, C, D, E = geo.choix_points(5)
    nom = shuffle_nom([A, B, C, D])
    BD = AC = 2 * Decimal(random.randint(20, 40)) / 10  # AC mesure entre 4cm et 8cm, tracé horizontalement
    AB = AC * Decimal(cos(45))

    exo.append(_(u"\\item Tracer un carré $%s$  tel que $%s%s=\\SI{%s}{cm}$.\\par")
               % (nom, A, C, decimaux(AC)))
    cor.append(_(u"\\item Tracer un carré $%s$  tel que $%s%s=\\SI{%s}{cm}$.\\par")
               % (nom, A, C, decimaux(AC)))

    cor.append(_(u"On note $%s$ le centre du carré.\\par") % (E))
    cor.append(_(u" Les diagonales du carré se coupent perpendiculairement en leur milieu $%s$ donc on a :") % E)
    cor.append("\\begin{enumerate}")
    cor.append(u"\\item $(%s%s)\\perp(%s%s)$." % (A, C, B, D))
    cor.append(u"\\item  $%s%s=%s%s=%s%s=%s%s=\\SI{%s}{cm}$ ;"
               % (A, E, C, E, B, E, D, E, decimaux(BD // 2)))
    cor.append("\\end{enumerate}\n")

    cor.append(textwrap.dedent(fr"""
    \begin{{tikzpicture}}[very thick, radius={AC/2}]
        \coordinate (A) at (0, 0);
        \coordinate (B) at (0:{AB});
        \coordinate (C) at (45:{AC});
        \coordinate (D) at (90:{AB});
        \coordinate (E) at (45:{AC/2});
        \draw[Maroon] (A) -- (B) -- (C) -- (D) -- cycle;
        \draw[Maroon] (A) -- ($(C)!-5mm!(A)$);
        \draw[Maroon] ($(B)!-5mm!(D)$) -- ($(D)!-5mm!(B)$);
        \draw[color=enonce, draw,decoration={{markings, mark=at position .5  with {{\node[transform shape] {{$\parallel$}};}}}}]
            (A) edge[decorate] (B)
            (B) edge[decorate] (C)
            (C) edge[decorate] (D)
            (D) edge[decorate] (A);
        \draw[color=enonce, draw,decoration={{markings, mark=at position .5  with {{\node[transform shape] {{$\times$}};}}}}]
            (A) edge[decorate] (E)
            (B) edge[decorate] (E)
            (C) edge[decorate] (E)
            (D) edge[decorate] (E);
        \draw pic [draw,calcul,angle radius=20pt, angle eccentricity=2, "\ang{{45}}"] {{angle = B--A--C}};
        \draw (A) node[below left] {{${A}$}};
        \draw (B) node[below] {{${B}$}};
        \draw (C) node[above] {{${C}$}};
        \draw (D) node[above] {{${D}$}};
        \draw (E) node[left] {{${E}$}};
        \draw pic [draw,enonce] {{right angle = A--E--B}};
        \draw[calcul] ($(E)+(-55:{AC/2})$) arc[start angle={-55}, delta angle=20];
        \draw[calcul] ($(E)+(35:{AC/2})$) arc[start angle={35}, delta angle=20];
        \draw[calcul] ($(E)+(125:{AC/2})$) arc[start angle={125}, delta angle=20];
    \end{{tikzpicture}}
    """))
