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


class PeriodsWindow(Gtk.Window, GladeTemplate):
    def __init__(self, date1: str, date2: str):
        Gtk.Window.__init__(self)
        GladeTemplate.__init__(self, "periods")

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
