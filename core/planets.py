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
from astropy.coordinates import EarthLocation, solar_system_ephemeris, get_body
from astropy.time import Time

solar_system_ephemeris.set('de430')


class Planet:
    loc = EarthLocation.of_site('greenwich')

    def __init__(self, name: str, date_time: str):
        self.name = name
        time = Time(date_time)
        self.body = get_body(name, time, self.loc)

    def __add__(self, other: "Planet") -> "Aspect":
        return Aspect(self, other)

    @property
    def good(self) -> bool:
        ...


class Aspect:
    def __init__(self, planet1: "Planet", planet2: "Planet"):
        offsets = planet1.body.spherical_offsets_to(planet2.body)
        angle = offsets[0].degree
        self.angle = round(abs(angle), 1)

        # TODO: handle Jupiter
        if 111.5 <= self.angle <= 128.5 or 51.5 <= self.angle <= 68.5:
            self.good = True
        elif 171.5 <= self.angle <= 188.5 or 81.5 <= self.angle <= 98.5:
            self.good = False
        elif 0 <= self.angle <= 8.5:
            self.good = planet1.good and planet2.good
        else:
            self.angle = None
