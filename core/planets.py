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
from astropy.coordinates import EarthLocation, solar_system_ephemeris, get_body, SkyCoord
from astropy.time import Time

solar_system_ephemeris.set('de430')


class Planet:
    loc = EarthLocation.of_site('greenwich')

    def __init__(self, name: str, date_time: str):
        self.name = name
        time = Time(date_time)
        self.body = get_body(name, time, self.loc)

    @property
    def good(self) -> bool:
        return self.name in ("sun", "venus", "moon", "jupiter")


class Aspect:
    def __init__(self, planet1: "Planet", planet2: "Planet"):
        body1 = SkyCoord(planet1.body.ra, planet1.body.dec)
        body2 = SkyCoord(planet2.body.ra, planet2.body.dec)
        offsets = body1.spherical_offsets_to(body2)
        angle = offsets[0].degree
        self.angle = round(abs(angle), 1)

        if 112 < self.angle < 128 or 52 < self.angle < 68:
            self.good = True
        elif 174 < self.angle < 186 or 84 < self.angle < 96:
            self.good = False
        elif 0 <= self.angle < 8 and planet1.good and planet2.good:
            # in the context of conflicts Jupiter is a bad planet
            if planet1.name == planet2.name and planet1.name == "jupiter":
                if 0 <= self.angle < 6:
                    self.good = False
            else:
                self.good = True
        elif 0 <= self.angle < 6:
            self.good = False
        else:
            self.good = None
