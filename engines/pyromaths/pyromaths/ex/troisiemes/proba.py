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
from pyromaths.classes.Fractions import Fraction
from pyromaths.ex import LegacyExercise

def proba(exo, cor):
    couleur = ['bleue', 'rouge', 'jaune', 'verte', 'marron', 'orange']
    initiale = ['B', 'R', 'J', 'V', 'M', 'O']
    # Choix des 3 couleurs et du nombre de boule
    rg = random.randrange(0, 4)
    c1, i1, n1 = couleur[rg], initiale[rg], random.randrange(1, 6)  # 1ere couleur, son initiale et le nombre
    # 2e couleur diférente de la première
    rg2 = (rg + random.randrange(1, 5)) % 6
    c2, i2, n2 = couleur[rg2], initiale[rg2], random.randrange(1, 6)
    # 3e couleur différente des précédentes
    c3, i3, n3 = couleur[(rg2 + 1) % 6], initiale[(rg2 + 1) % 6], random.randrange(1, 6)
    if n1 > 1:
        plur1 = "s"
    else :
        plur1 = ""
    if n2 > 1:
        plur2 = "s"
    else :
        plur2 = ""
    if n3 > 1:
        plur3 = "s"
    else :
        plur3 = ""
    exos = [u"Dans une urne, il y a %s boule%s %s%s (%s), %s boule%s %s%s (%s) et %s boule%s %s%s (%s), indiscernables au toucher. On tire successivement et sans remise deux boules." % (n1, plur1, c1, plur1, i1, n2, plur2, c2, plur2, i2, n3, plur3, c3, plur3, i3),
    "\\begin{enumerate}",
    u"\\item Quelle est la probabilité de tirer une boule %s au premier tirage ?" % c2,
    u"\\item Construire un arbre des probabilités décrivant l'expérience aléatoire.",
    u"\\item Quelle est la probabilité que la première boule soit %s et la deuxième soit %s ?" % (c3, c2),
    u"\\item Quelle est la probabilité que la deuxième boule soit %s ?" % c1,
    "\\end{enumerate}"]
    tot = n1 + n2 + n3
    # calculs intermédiaires pour la question 4
    p41 = "\\dfrac{%s}{%s}\\times \\dfrac{%s}{%s}+" % (n1, tot, n1 - 1, tot - 1)
    p42 = "\\dfrac{%s}{%s}\\times \\dfrac{%s}{%s}+" % (n2, tot, n1, tot - 1)
    p43 = "\\dfrac{%s}{%s}\\times \\dfrac{%s}{%s}=" % (n3, tot, n1, tot - 1)

    result4 = "\\dfrac{%s}{%s}" % (n1 * (n1 - 1 + n2 + n3), tot * (tot - 1))  # resultat non simplifié de la question 4
    cors = [u"Dans une urne, il y a %s boule%s %s%s (%s), %s boule%s %s%s (%s) et %s boule%s %s%s (%s), indiscernables au toucher. On tire successivement et sans remise deux boules." % (n1, plur1, c1, plur1, i1, n2, plur2, c2, plur2, i2, n3, plur3, c3, plur3, i3),

         "\\begin{enumerate}",
         u"\\item Quelle est la probabilité de tirer une boule %s au premier tirage ?\\par " % c2,
         "Il y a %s boules dans l'urne dont %s boule%s %s%s. \\par" % (tot, n2, plur2, c2, plur2),
         u" La probabilité de tirer une boule %s au premier tirage est donc $\\dfrac{%s}{%s}$." % (c2, n2, tot),
         u"\\item Construire un arbre des probabilités décrivant l'expérience aléatoire.\\\ [0,3cm] ",
         fr"""\begin{{center}}\begin{{tikzpicture}}[thick, edge from parent/.style={{draw=Maroon}}]
            \tikzstyle{{level 1}}=[level distance=23mm, sibling distance=35mm]
            \tikzstyle{{level 2}}=[level distance=23mm, sibling distance=13mm]
            \coordinate
            child {{
              node {{${i1}$}}
              child {{
                node {{${i1}$}}
                edge from parent node[midway, left]{{$\dfrac{{ {n1-1} }}{{ {tot-1} }}$}}
              }}
              child {{
                node {{${i2}$}}
                edge from parent node[midway, below left]{{$\dfrac{{ {n2} }}{{ {tot-1} }}$}}
              }}
              child {{
                node {{${i3}$}}
                edge from parent node[midway, right]{{$\dfrac{{ {n3} }}{{ {tot-1} }}$}}
              }}
              edge from parent node[midway, above left]{{$\dfrac{{ {n1} }}{{ {tot} }}$}}
            }}
            child {{
              node {{${i2}$}}
              child {{
                node {{${i1}$}}
                edge from parent node[midway, left]{{$\dfrac{{ {n1} }}{{ {tot-1} }}$}}
              }}
              child {{
                node {{${i2}$}}
                edge from parent node[midway, below left]{{$\dfrac{{ {n2-1} }}{{ {tot-1} }}$}}
              }}
              child {{
                node {{${i3}$}}
                edge from parent node[midway, right]{{$\dfrac{{ {n3} }}{{ {tot-1} }}$}}
              }}
              edge from parent node[midway, left]{{$\dfrac{{ {n2} }}{{ {tot} }}$}}
            }}
            child {{
              node {{${i3}$}}
              child {{
                node {{${i1}$}}
                edge from parent node[midway, left]{{$\dfrac{{ {n1} }}{{ {tot-1} }}$}}
              }}
              child {{
                node {{${i2}$}}
                edge from parent node[midway, below left]{{$\dfrac{{ {n2} }}{{ {tot-1} }}$}}
              }}
              child {{
                node {{${i3}$}}
                edge from parent node[midway, right]{{$\dfrac{{ {n3-1} }}{{ {tot-1} }}$}}
              }}
              edge from parent node[midway, above right]{{$\dfrac{{ {n3} }}{{ {tot} }}$}}
            }};
         \end{{tikzpicture}}\end{{center}}""",
         "\\vspace{0.3cm}",
         u"\\item Quelle est la probabilité que la première boule soit %s et la deuxième soit %s ?\\par" % (c3, c2),
         u"On note $(\\mathrm %s~,~\\mathrm %s)$ l'évènement: \\og{}la première boule tirée est %s et la deuxième tirée est %s\\fg{} et " % (i3,i2,c3,c2),
         u"on utilise l'arbre construit précédemment.\\par",
         "$p\\,(\\mathrm %s~,~\\mathrm %s)=%s \\times %s = %s$\\par" % \
                (i3, i2, str(Fraction(n3, tot)),
                 str(Fraction(n2, tot - 1)),
                 str(Fraction(n3 * n2, tot * (tot - 1)))),
         u"La probabilité que la première boule soit %s et la deuxième soit %s est égale à $\\dfrac{%s}{%s}$." % (c3, c2, n3 * n2, tot * (tot - 1)),
         u"\\item Quelle est la probabilité que la deuxième boule soit %s ?\\par" % c1,
         u"On note $(?~,~\\mathrm %s)$ l'évènement: \\og{}la deuxième boule tirée est %s\\fg{}. \\par" % (i1, c1),
         "$p\\,(?~,~\\mathrm %s)=p\\,(\\mathrm %s~,~\\mathrm %s)+p\\,(\\mathrm %s~,~\\mathrm %s)+p\\,(\\mathrm %s~,~\\mathrm %s)=" % (i1, i1, i1, i2, i1, i3, i1) + p41 + p42 + p43 + result4 + "$",
         "\\end{enumerate}"]
    for st in exos:
        exo.append(st)
    for st in cors:
        cor.append(st)

def _tex_proba():
    exo = ['\\exercice']
    cor = ['\\exercice*']
    proba(exo, cor)
    return (exo, cor)

class tex_proba(LegacyExercise):
    """Probabilités"""

    tags = [
        "probabilités",
        "Troisième",
    ]
    function = _tex_proba
