# Création d'un paquet python (sources, wheel)

Lancer :

    # Paquet sources
    python3 setup.py sdist
    # Paquet wheel
    python3 setup.py bdist_wheel

Ceci est fait automatiquement avec :

    make src wheel

# Téléversement sur pypi

En utilisant twine :

    twine upload -s dist/PAQUET

# Création d'un paquet Debian

TODO
