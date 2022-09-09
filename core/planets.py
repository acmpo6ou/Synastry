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


def aspect_good(angle: float, planet1_good: bool, planet2_good: bool):
    """
    Decides if the angle represents a good aspect.
    NOTE: returns None if the angle doesn't represent an aspect.
    """
    # TODO: round all the angles at once in main_window
    angle = round(abs(angle), 1)

    if 112 <= angle <= 128 or 52 <= angle <= 68:
        return True
    elif 174 <= angle <= 186 or 84 <= angle <= 96:
        return False
    elif 0 <= angle <= 8 and planet1_good and planet2_good:
        return True
    elif 0 <= angle <= 6:
        return False
