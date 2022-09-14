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
import numpy as np
from rich.pretty import pprint

from core.planets import aspects_good


def test_aspects_good():
    tests = np.array([
        [120, True, False, True],
        [60, True, False, True],
        [180, True, False, False],
        [90, True, False, False],

        [129, True, False, -1],
        [111, True, False, -1],
        [69, True, False, -1],
        [51, True, False, -1],
        [187, True, False, -1],
        [173, True, False, -1],
        [97, True, False, -1],
        [83, True, False, -1],

        [0, True, True, True],
        [0, True, False, False],
        [0, False, True, False],
        [0, False, False, False],

        [7, False, False, -1],
        [7, True, True, True],
        [9, True, True, -1],
    ])

    angles = tests[:, 0]
    planets1_good = tests[:, 1]
    planets2_good = tests[:, 2]
    expected = tests[:, 3]

    result = aspects_good(angles, planets1_good, planets2_good)

    # for debugging
    result = np.vstack(result)
    expected = np.vstack(expected)
    concat = np.concatenate((result, expected), axis=1)
    pprint(concat)

    assert np.array_equal(result, expected)
