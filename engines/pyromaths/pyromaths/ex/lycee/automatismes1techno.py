# Pyromaths
#
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
#
# Copyright (C) 2021 -- Louis Paternault (spalax@gresille.org)
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

"""Automatismes en classe de première technologique"""

import collections
import datetime
import itertools
import random
from decimal import Decimal

from pyromaths.ex import Jinja2Exercise
from pyromaths.outils.jinja2utils import facteur, signe


class CalculerAppliquerExprimerProportion(Jinja2Exercise):
    """Calculer, appliquer, exprimer une proportion sous différentes formes"""

    tags = [
        "1re technologique — Automatismes",
        "pourcentages",
        "proportions",
    ]

    filters = {"facteur": facteur}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        questions = dict()

        # Appliquer 1
        a = b = c = 0
        while a == b or a % b == 0:
            a = random.randint(1, 9)
            b = random.randint(2, 9)
            c = b * random.randint(2, 9) * random.choice((1, 2, 5, 10, 100))
            u = random.choice(("kg", "m", "km", "L"))

        questions["appliquer1"] = {
            "a": a,
            "b": b,
            "c": c,
            "u": u,
            "unite": {
                "kg": "kilogrammes",
                "m": "mètres",
                "km": "kilomètres",
                "L": "litres",
            }[u],
        }

        # Appliquer 2
        pourcent = 10 * random.randint(2, 9)
        questions["appliquer2"] = {
            "employes": random.randint(2, 9) * pourcent,
            "pourcent": pourcent,
        }

        # Calculer 1
        pgcd = random.randint(2, 9)
        femmes = employes = 0
        while femmes >= employes:
            employes = pgcd * random.randint(2, 9)
            femmes = pgcd * random.choice((2, 4, 5))
        questions["calculer1"] = {
            "employes": employes,
            "femmes": femmes,
            "pgcd": pgcd,
        }

        # Calculer 2
        notes = {0: 10}
        while max(notes.values()) >= 10 or len(notes) != 6:
            notes = dict(collections.Counter(random.choices(range(0, 6), k=20)))
        seuil = random.choice((2, 3, 4))
        questions["calculer2"] = {
            "seuil": seuil,
            "audessusduseuil": Decimal(
                sum(notes[n] for n in range(seuil, max(notes) + 1))
            ),
            "note": random.randint(1, 5),
            "notes": notes,
        }

        # Calculer 3
        a, b, c = random.sample(range(2, 9), k=3)
        questions["calculer3"] = {
            "a": a,
            "b": b,
            "c": c,
            "prix": c * random.choice((2, 3, 4, 10)),
        }

        # Inverse 1
        pourcent = random.randint(2, 9) * 10
        total = random.randint(2, 9) * 10
        questions["inverse1"] = {
            "lettre": random.choice("ABCDEFGHIJKLMNPQRSTUVWXYZ"),
            "pourcent": pourcent,
            "total": total,
            "partie": pourcent * total // 100,
        }

        self.context["questions"] = {
            question: questions[question]
            for question in random.sample(questions.keys(), 3)
        }


class ProportionDUneProportion(Jinja2Exercise):
    """Calculer la proportion d'une proportion"""

    tags = [
        "1re technologique — Automatismes",
        "pourcentages",
        "proportions",
    ]
    filters = {"facteur": facteur}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.context = {
            "p1": random.choice((2, 5, 10, 20, 40, 50)),
            "p2": random.randint(2, 9),
            "question": random.randint(1, 3),
        }

class CalculerAppliquerTauxDEvolution(Jinja2Exercise):
    """Calculer, appliquer un taux d'évolution.

    Cet exercice fait travailler les automatismes suivants :

    - calculer un taux d’évolution, l’exprimer en pourcentage ;
    - appliquer un taux d’évolution pour calculer une valeur finale ou initiale.
    """

    tags = ["1re technologique", "taux d'évolution", "pourcentages"]
    filters = {
        "facteur": facteur,
        "signe": signe,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Calcul des années
        annee0 = annee1 = annee2 = 0
        while min(abs(x - y) for x, y in itertools.combinations((annee0, annee1, annee2), 2)) < 3:
            annee0, annee1, annee2 = (
                    datetime.datetime.today().year - random.randint(2, 22)
                    for _ in range(3)
                    )

        # Calcul du taux d'évolution
        initiale0 = taux0 = 1000
        while initiale0 * (1+taux0/100) >= 1000:
            initiale0, taux0 = random.choice((
                ( # Augmentation ou diminution de 25%
                    random.randint(1, 4) * 100,
                    random.choice((25, -25)),
                    ),
                ( # Augmentation ou diminution de 5%
                    random.randint(1, 9)*100,
                    random.choice((5, -5)),
                    ),
                ( # Augmentation ou diminution de X0%
                    random.randint(1, 9)*100,
                    random.choice((1, -1)) * random.randint(1,9)*10,
                    )
                ))

        # Calcul de l'état final
        for i in range(100):
            initiale1 = taux1 = 1000
            while initiale1 * (1+taux1/100) >= 1000:
                if random.random() > .4:
                    initiale1 = random.randint(1, 9) * 100
                    taux1 = random.randint(1, 5) * 10
                elif random.random() > .5:
                    initiale1 = random.randint(1, 5) * 100
                    taux1 = -random.choice((50, 60, 65, 70, 75, 80, 85, 90))
                else:
                    initiale1 = random.choice(
                            tuple(range(100, 200, 10)) + tuple(range(200, 500, 50)) + tuple(range(500, 900, 100))
                            )
                    taux1 = random.choice((-80, -70, -60, -50))

        # Calcul de l'état initial
        initiale2, taux2, finale2 = random.choice(
            tuple(
                (100*i, 10*t, round(100*i*(1+10*t/100)))
                for i in range(2, 5)
                for t in range(1, 10)
                if 100*i*(1+10*t/100) < 1000
            ) + tuple(
                (100*i, -10*t, round(100*i*(1-10*t/100)))
                for i in range(2, 5)
                for t in range(1, 10)
                if 100*i*(1-10*t/100) < 1000
            ) + tuple(
                (100*i, -25, round(100*i*.75))
                for i in range(2, 10, 2)
                )
        )

        self.context = {
                # Contexte de l'exercice
                "contexte": random.randint(0, 4),
                # Ordre des questions
                "ordre": random.sample(range(3), k=3),
                # Année
                "annee0": annee0,
                "annee1": annee1,
                "annee2": annee2,
                # Calcul du taux d'évolution
                "initiale0": initiale0,
                "taux0": taux0,
                "finale0": round(initiale0*(1+taux0/100)),
                # Calcul de l'état final
                "initiale1": initiale1,
                "taux1": taux1,
                "mult1": round(1+taux1/100, 2),
                "finale1": round(initiale1 * (1+taux1/100)),
                # Calcul de l'état initial
                "initiale2": initiale2,
                "finale2": finale2,
                "taux2": taux2,
                "mult2": round(1+taux2/100, 2),
                }
