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
from core.planets import Planet
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

    def calculate_for_month(self, month, date1, date2):
        """
        Calculates aspects present for 2 persons during given [month].

        :param date1: date of birth of the first person.
        :param date2: date of birth of the second person.
        """
        ...

    def calculate_for_day(self, day, date1, date2):
        """
        Calculates aspects present for 2 persons during given [day].

        :param date1: date of birth of the first person.
        :param date2: date of birth of the second person.
        """
        ...

    def collect_for_planet(self, planet: Planet, date1: str, date2: str):
        """Collects pairs of a planet with all transit planets."""

    def calculate_angels(self, date1: str, date2: str):
        ...

    def present_conflicts(
        self,
        planet_pairs: list[tuple[Planet]],
        aspects_good: npt.NDArray[int],
    ):
        # TODO: highlight conflictedness?
        # TODO: convert planet_pairs into np.array
        #  filter only bad aspects with planet_pairs[aspects_good == 0]
        ...
