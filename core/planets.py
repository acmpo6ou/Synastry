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
from functools import cache

from astropy.coordinates import EarthLocation, solar_system_ephemeris, get_body
from astropy.time import Time
import numpy as np
import numpy.typing as npt

solar_system_ephemeris.set('de430')


class Planet:
    loc = EarthLocation(0, 0, 0)

    def __init__(self, name: str, date_time: str):
        self.name = name
        time = Time(date_time)
        self.body = get_body(name, time, self.loc)

    @property
    def good(self) -> bool:
        return self.name in ("sun", "venus", "moon", "jupiter")

    def __str__(self):
        return f"Planet({self.name}"

    def __repr__(self):
        return f"Planet({self.name})"


@cache
def get_planet(name: str, date_time: str):
    return Planet(name, date_time)


def aspects_good(
    angles: npt.ArrayLike,
    planets1_good: npt.ArrayLike,
    planets2_good: npt.ArrayLike,
) -> npt.NDArray[int]:
    """
    Decides if the angles represent good aspects.

    Note: this function was contributed by Mad Physicist. Thank you.
    https://stackoverflow.com/q/73672739/11004423

    :returns: an array with values as follows:
        1 – the angle is a good aspect
        0 – the angle is a bad aspect
       -1 – the angle doesn't represent an aspect
    """

    # sanitize data
    angles = np.asanyarray(angles)
    planets1_good = np.asanyarray(planets1_good, dtype=bool)
    planets2_good = np.asanyarray(planets2_good, dtype=bool)

    result = np.full_like(angles, -1, dtype=np.int8)

    bad_mask = np.abs(angles % 90) <= 6
    result[bad_mask] = 0

    good_mask = (np.abs(angles - 120) <= 8) |\
                (np.abs(angles - 60) <= 8) |\
                ((np.abs(angles - 4) <= 4) & planets1_good & planets2_good)
    result[good_mask] = 1

    return result
