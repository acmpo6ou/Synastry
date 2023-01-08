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
from calendar import monthrange

import numpy as np
from astropy.coordinates import SkyCoord
from gi.repository import Gtk

from core.gtk_utils import GladeTemplate
from core.main_window import MainWindow
from core.utils import ArrayIter, get_aspects_good
from core.planets import Planet, get_planet
import numpy.typing as npt


class PeriodsWindow(Gtk.Window, GladeTemplate):
    PLANETS = ("sun", "moon", "mercury", "venus", "mars",
               "jupiter", "saturn", "uranus", "neptune", "pluto")

    def __init__(
        self,
        conflict_pairs: list[tuple[Planet]],
        love_pairs: list[tuple[Planet]],
        friendship_pairs: list[tuple[Planet]],
        happiness_pairs: list[tuple[Planet]],
        unhappiness_pairs: list[tuple[Planet]],
    ):
        Gtk.Window.__init__(self)
        GladeTemplate.__init__(self, "periods")
        self.conflict_pairs = conflict_pairs
        self.love_pairs = love_pairs
        self.friendship_pairs = friendship_pairs
        self.happiness_pairs = happiness_pairs
        self.unhappiness_pairs = unhappiness_pairs
        self.all_pairs = (*conflict_pairs, *love_pairs, *friendship_pairs,
                          *happiness_pairs, *unhappiness_pairs)

    def on_calculate(self):
        # TODO: get actual selected date
        month, year = 1, 2023

        planet_pairs, angles = self.calculate_angles(month, year)
        good = get_aspects_good(angles, planet_pairs)

        # reshaping 1d arrays of all planets/angles/aspects into 4d arrays
        # each array will be an array of days, X axis (days_in_month)
        # each day will be an array of aspect arrays during that day, Y axis
        #     (the number of aspects is different per person pair, that's why I use -1 here)
        # each aspect array is an array of pairs since each aspect consists of 2 planets, Z axis (2)
        # each pair is an array of aspects of planet with all transit planets, A axis (num_planets)
        days_in_month = monthrange(year, month)[1]
        num_planets = len(self.PLANETS)
        self.planet_pairs = planet_pairs.reshape(days_in_month, -1, 2, num_planets)
        self.angles = angles.reshape(days_in_month, -1, 2, num_planets)
        self.good = good.reshape(days_in_month, -1, 2, num_planets)

        for day in range(days_in_month):
            self.present_day(day)

    def calculate_angles(self, month, year):
        planet_pairs_all = []
        ra1_all = []
        dec1_all = []
        ra2_all = []
        dec2_all = []

        days_in_month = monthrange(year, month)[1]
        for day in range(days_in_month):
            # TODO: adjust time
            date = f"{year}-{month:02}-{day:02} 08:00"
            planet_pairs, ra1, dec1, ra2, dec2 = self.collect_for_day(date)
            planet_pairs_all += planet_pairs
            ra1_all += ra1
            dec1_all += dec1
            ra2_all += ra2
            dec2_all += dec2

        coords1 = SkyCoord(ra1_all, dec1_all)
        coords2 = SkyCoord(ra2_all, dec2_all)
        angles = coords1.separation(coords2)
        planet_pairs_all = np.array(planet_pairs_all).flatten()
        return planet_pairs_all, angles.deg.round(decimals=1)

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

    def present_day(self, day):
        planet_pairs = ArrayIter(self.planet_pairs[day])
        angles = ArrayIter(self.angles[day])
        good = ArrayIter(self.good[day])

        def data(n):
            return planet_pairs[n], angles[n], good[n]

        n = len(self.conflict_pairs) * len(self.PLANETS)
        self.present_conflicts(*data(n))

    def present_conflicts(
        self,
        planet_pairs: npt.NDArray[Planet],
        aspects_good: npt.NDArray[int],
    ):
        # TODO: highlight conflictedness?
        for i, (p1, p2) in enumerate(planet_pairs):
            aspects1, aspects2 = aspects_good[i]
            aspects1[aspects1 == -1] = 1
            aspects2[aspects2 == -1] = 1

            for i, (a1, a2) in enumerate(zip(aspects1, aspects2)):
                if a1 == a2 == 0:
                    transit_planet = self.PLANETS[i]
                    print(f"{p1.name} - {transit_planet} - {p2.name}")
