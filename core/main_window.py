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

from core.date_time import DateTime
from core.gtk_utils import GladeTemplate, clear_table
from core.planets import Planet, Aspect


class MainWindow(Gtk.ApplicationWindow, GladeTemplate):
    # <editor-fold>
    parent_widget: Gtk.Box
    conflicts1: Gtk.Grid
    love: Gtk.Grid
    friendship: Gtk.Grid
    happiness1: Gtk.Grid
    happiness2: Gtk.Grid
    conflicts2: Gtk.Grid
    conflicts: Gtk.Grid

    # </editor-fold>
    def __init__(self, *args, **kwargs):
        Gtk.ApplicationWindow.__init__(self, *args, **kwargs)
        GladeTemplate.__init__(self, "main_window")

        self.set_default_size(1280, 720)
        # self.set_icon_from_file("img/icon.svg")

        self.date1 = DateTime(self)
        self.date2 = DateTime(self)

        hbox = Gtk.HBox()
        hbox.pack_start(self.date1, False, True, 0)
        hbox.pack_end(self.date2, False, True, 0)
        self.parent_widget.pack_start(hbox, False, True, 0)

    def on_date_changed(self):
        date1 = self.date1.date_time
        date2 = self.date2.date_time

        conf1 = self.calculate_conflictedness(self.conflicts1, date1)
        conf2 = self.calculate_conflictedness(self.conflicts2, date2)
        self.calculate_conflicts(date1, date2, conf1, conf2)

        self.calculate_love()
        self.calculate_friendship()

        self.calculate_happiness(self.happiness1, date1, date2)
        self.calculate_happiness(self.happiness2, date2, date1)

    @staticmethod
    def calculate_conflictedness(table: Gtk.Grid, date_time: str) -> list[str]:
        """
        Calculates conflictedness of a person.
        :returns: a list of conflicting planets of this person.
        """

        conflictedness = []
        mars = Planet("mars", date_time)
        jupiter = Planet("jupiter", date_time)
        saturn = Planet("saturn", date_time)
        pluto = Planet("pluto", date_time)

        clear_table(table)
        PLANETS = (mars, jupiter, saturn, pluto)
        planets = [mars, jupiter, saturn, pluto]

        for p1 in PLANETS:
            planets.remove(p1)
            for p2 in planets:
                aspect = Aspect(p1, p2)
                if aspect.angle is None or aspect.good:
                    continue

                conflictedness.extend((p1.name, p2.name))
                row = PLANETS.index(p1) + 1
                column = PLANETS.index(p2)

                label = Gtk.Label()
                label.xalign = 0
                label.markup = f'<span foreground="#f04b51">{aspect.angle}°</span>'
                table.attach(label, column, row, 1, 1)
                label.show()

                header1 = table.get_child_at(0, row)
                header2 = table.get_child_at(column, 0)
                header1.markup = f'<span foreground="#f04b51">{header1.text}</span>'
                header2.markup = f'<span foreground="#f04b51">{header2.text}</span>'
        return conflictedness

    def calculate_conflicts(
            self,
            date1: str,
            date2: str,
            conflictedness1: list[str],
            conflictedness2: list[str],
    ):
        mars1 = Planet("mars", date1)
        jupiter1 = Planet("jupiter", date1)
        saturn1 = Planet("saturn", date1)
        pluto1 = Planet("pluto", date1)

        mars2 = Planet("mars", date2)
        jupiter2 = Planet("jupiter", date2)
        saturn2 = Planet("saturn", date2)
        pluto2 = Planet("pluto", date2)

        clear_table(self.conflicts)

        planets1 = (mars1, jupiter1, saturn1, pluto1)
        planets2 = (mars2, jupiter2, saturn2, pluto2)

        planet_names1 = [planet.name for planet in planets1]
        planet_names2 = [planet.name for planet in planets2]

        for planet in conflictedness1:
            i = planet_names1.index(planet) + 1
            header = self.conflicts.get_child_at(0, i)
            header.markup = f'<span foreground="red">{header.text}</span>'

        for planet in conflictedness2:
            i = planet_names2.index(planet) + 1
            header = self.conflicts.get_child_at(i, 0)
            header.markup = f'<span foreground="red">{header.text}</span>'

        for p1 in planets1:
            for p2 in planets2:
                aspect = Aspect(p1, p2)
                if aspect.angle is None or aspect.good:
                    continue

                row = planets1.index(p1) + 1
                column = planets2.index(p2) + 1

                color = "#f04b51"
                if p1.name in conflictedness1 or p2.name in conflictedness2:
                    color = "red"

                label = Gtk.Label()
                label.xalign = 0
                label.markup = f'<span foreground="{color}">{aspect.angle}°</span>'
                self.conflicts.attach(label, column, row, 1, 1)
                label.show()

    def calculate_love(self):
        ...

    def calculate_friendship(self):
        ...

    def calculate_happiness(self, table: Gtk.Grid, date1: str, date2: str):
        """
        Calculates how happy/unhappy person with date2
        makes person with date1.
        """
