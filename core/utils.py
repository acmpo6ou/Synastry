#   Copyright (c) 2022. Bohdan Kolvakh
#   This file is part of Synastry.
#  #
#   Synastry is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#  #
#   Synastry is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#  #
#   You should have received a copy of the GNU General Public License
#   along with Synastry.  If not, see <https://www.gnu.org/licenses/>.
#
from core.planets import aspects_good


class ArrayIter:
    def __init__(self, array):
        self.array = array
        self.index = 0

    def __getitem__(self, n):
        res = self.array[self.index: self.index + n]
        self.index += n
        return res


def get_aspects_good(angles, planet_pairs):
    planets1_good = []
    planets2_good = []
    for p1, p2 in planet_pairs:
        planets1_good.append(p1.good)
        planets2_good.append(p2.good)
    good = aspects_good(angles, planets1_good, planets2_good)
    return good
