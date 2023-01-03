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

from gi.repository import Gtk

from core.gtk_utils import GladeTemplate
from core.main_window import ArrayIter
from core.planets import Planet, get_planet
import numpy.typing as npt


class PeriodsWindow(Gtk.Window, GladeTemplate):
    PLANETS = ("sun", "moon", "mercury", "venus", "mars",
               "jupiter", "saturn", "uranus", "neptune", "pluto")

    def __init__(
        self, date1: str, date2: str,
        conflict_pairs: list[tuple[Planet]],
        love_pairs: list[tuple[Planet]],
        friendship_pairs: list[tuple[Planet]],
        happiness_pairs: list[tuple[Planet]],
        unhappiness_pairs: list[tuple[Planet]],
    ):
        Gtk.Window.__init__(self)
        GladeTemplate.__init__(self, "periods")
        self.date1 = date1
        self.date2 = date2
        self.conflict_pairs = conflict_pairs
        self.love_pairs = love_pairs
        self.friendship_pairs = friendship_pairs
        self.happiness_pairs = happiness_pairs
        self.unhappiness_pairs = unhappiness_pairs
        self.all_pairs = (*conflict_pairs, *love_pairs, *friendship_pairs,
                          *happiness_pairs, *unhappiness_pairs)

        planet_pairs, angles = self.calculate_angles(self.dates1, self.dates2)
        good = self.aspects_good(angles, planet_pairs)

        planet_pairs = ArrayIter(planet_pairs)
        angles = ArrayIter(angles)
        good = ArrayIter(good)

    def calculate_for_month(self, month, date1, date2):
        """
        Calculates aspects present for 2 persons during given [month].

        :param date1: date of birth of the first person.
        :param date2: date of birth of the second person.
        """
        ...

    def collect_for_day(self, day):
        """
        Collects planet pairs of aspects present for 2 persons during given [day].
        """
        planet_pairs_all = []
        ra1_all = []
        dec1_all = []
        ra2_all = []
        dec2_all = []

        for pair in self.all_pairs:
            for planet in pair:
                planet_pairs, ra1, dec1, ra2, dec2 = self.collect_for_planet(planet, day)
                planet_pairs_all += planet_pairs
                ra1_all += ra1
                dec1_all += dec1
                ra2_all += ra2
                dec2_all += dec2
        return planet_pairs_all, ra1_all, dec1_all, ra2_all, dec2_all

    def collect_for_planet(self, planet: Planet, date: str):
        """Collects pairs of a planet with all transit planets."""
        planet_pairs = []
        ra1 = []
        dec1 = []
        ra2 = []
        dec2 = []

        for name in self.PLANETS:
            transit_planet = get_planet(name, date)
            planet_pairs.append(planet, transit_planet)
            ra1.append(planet.body.ra)
            dec1.append(planet.body.dec)
            ra2.append(transit_planet.body.ra)
            dec2.append(transit_planet.body.dec)
        return planet_pairs, ra1, dec1, ra2, dec2

    def calculate_angles(self, date1: str, date2: str):
        # TODO: combine, flatten, and set() all pairs
        #  (but order them because set is not ordered!!)
        ...

    def present_conflicts(
        self,
        planet_pairs: list[tuple[Planet]],
        aspects_good: npt.NDArray[int],
    ):
        # TODO: highlight conflictedness?

        # TODO: flatten, set() and order conflict_pairs
        #  create `aspects` dict:
        #      Planet to array of its aspects
        #      or planet.name + (1 or 2) to np.array

        # TODO: for p1, p2 in conflict_pairs
        #  get aspects1 and aspects2 from aspects dict
        #  filter both: set aspectsN[aspectsN == -1] = 1
        #  apply XOR to resulting np.arrays,
        #  this way we'll get transit planets that affect both natal planets
        #  for item in resulting array:
        #      if item is 0: present p1 - transit planet - p2
        ...
