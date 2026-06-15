# Copyright (C) 2016 -- Louis Paternault (spalax@gresille.org)
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

"""Generic stuff for pyromaths command line interface"""

import argparse

class PyromathsException(Exception):
    """Generic exception for this module."""
    pass

def exercise_argument(string=""):
    """Return the exercises matching ``string``.

    :param str string: a string, option of one of `testexo` commands.
    :rtype: dict
    :return: A dictionary with exercises as keys, and sets of integers (seeds)
    as values.
    """
    splitted = string.split(":")
    if len(splitted) == 1:
        name = string
        seeds = []
    elif len(splitted) == 2:
        name, raw = string.split(":")
        try:
            seeds = []
            for seed in raw.split(","):
                if seed.count("-") == 0:
                    seeds.append(int(seed))
                elif seed.count("-") == 1:
                    mini, maxi = seed.split("-")
                    seeds.extend(range(int(mini), int(maxi)+1))
                else:
                    raise ValueError
        except ValueError:
            raise argparse.ArgumentTypeError("Seeds must be a comma separated list of integers or ranges (e.g. 3,5-10).")
    else:
        raise argparse.ArgumentTypeError("Seeds must be a comma separated list of integer or ranges (e.g. 3,5-10)s.")

    return (name, seeds)

