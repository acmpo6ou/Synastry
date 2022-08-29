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
from time import perf_counter

from gi.repository import Gtk

from core.date_time import DateTime
from core.gtk_utils import GladeTemplate, clear_table
from core.planets import Planet, get_planet, Aspect

RED = "#f04b51"
GREEN = "#6db442"


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

        self.maximize()
        # self.set_icon_from_file("img/icon.svg")

        self.date1 = DateTime(self)
        self.date2 = DateTime(self)

        calculate = Gtk.Button("Calculate")
        calculate.connect("clicked", self.on_date_changed)
        calculate.style_context.add_class("suggested-action")

        hbox = Gtk.Box(Gtk.Orientation.HORIZONTAL, 100)
        hbox.pack_start(self.date1, False, True, 0)
        hbox.center_widget = calculate
        hbox.pack_end(self.date2, False, True, 0)
        self.parent_widget.pack_start(hbox, False, True, 0)

    def on_date_changed(self, _):
        start = perf_counter()
        date1 = self.date1.date_time
        date2 = self.date2.date_time

        conf1 = self.calculate_conflictedness(self.conflicts1, date1)
        conf2 = self.calculate_conflictedness(self.conflicts2, date2)
        self.calculate_conflicts(date1, date2, conf1, conf2)

        self.calculate_love(date1, date2)
        self.calculate_friendship(date1, date2)

        self.calculate_happiness(self.happiness1, date1, date2)
        self.calculate_happiness(self.happiness2, date2, date1)
        print(perf_counter() - start)

    @staticmethod
    def collect_conflictedness(date_time: str) -> tuple[list[float]]:
        mars = get_planet("mars", date_time)
        jupiter = get_planet("jupiter", date_time)
        saturn = get_planet("saturn", date_time)
        pluto = get_planet("pluto", date_time)

        PLANETS = (mars, jupiter, saturn, pluto)
        planets = [mars, jupiter, saturn, pluto]

        ra1 = []
        dec1 = []
        ra2 = []
        dec2 = []

        for p1 in PLANETS:
            planets.remove(p1)
            for p2 in planets:
                ra1.append(p1.body.ra)
                dec1.append(p1.body.dec)
                ra2.append(p2.body.ra)
                dec2.append(p2.body.dec)
        return ra1, dec1, ra2, dec2

    @staticmethod
    def calculate_conflictedness(table: Gtk.Grid, date_time: str) -> list[str]:
        """
        Calculates conflictedness of a person.
        :returns: a list of conflicting planets of this person.
        """

        conflictedness = []
        clear_table(table)

        """
        for p1 in PLANETS:
            planets.remove(p1)
            for p2 in planets:
                aspect = Aspect(p1, p2)
                row = PLANETS.index(p1) + 1
                column = PLANETS.index(p2)

                if aspect.good is None or aspect.good:
                    color = ""
                else:
                    conflictedness.extend((p1.name, p2.name))
                    color = f'foreground="{RED}"'

                    header1 = table.get_child_at(0, row)
                    header2 = table.get_child_at(column, 0)
                    header1.markup = f'<span foreground="{RED}">{header1.text}</span>'
                    header2.markup = f'<span foreground="{RED}">{header2.text}</span>'

                label = Gtk.Label()
                label.xalign = 0
                label.markup = f'<span {color}>{aspect.angle}°</span>'
                table.attach(label, column, row, 1, 1)
                label.show()
                """
        return conflictedness

    @staticmethod
    def collect_conflicts(date1: str, date2: str) -> tuple[list[float]]:
        mars1 = get_planet("mars", date1)
        jupiter1 = get_planet("jupiter", date1)
        saturn1 = get_planet("saturn", date1)
        pluto1 = get_planet("pluto", date1)

        mars2 = get_planet("mars", date2)
        jupiter2 = get_planet("jupiter", date2)
        saturn2 = get_planet("saturn", date2)
        pluto2 = get_planet("pluto", date2)

        planets1 = (mars1, jupiter1, saturn1, pluto1)
        planets2 = (mars2, jupiter2, saturn2, pluto2)

        ra1 = []
        dec1 = []
        ra2 = []
        dec2 = []

        for p1 in planets1:
            for p2 in planets2:
                ra1.append(p1.body.ra)
                dec1.append(p1.body.dec)
                ra2.append(p2.body.ra)
                dec2.append(p2.body.dec)
        return ra1, dec1, ra2, dec2

    def calculate_conflicts(
        self,
        date1: str,
        date2: str,
        conflictedness1: list[str],
        conflictedness2: list[str],
    ):
        mars1 = get_planet("mars", date1)
        jupiter1 = get_planet("jupiter", date1)
        saturn1 = get_planet("saturn", date1)
        pluto1 = get_planet("pluto", date1)

        mars2 = get_planet("mars", date2)
        jupiter2 = get_planet("jupiter", date2)
        saturn2 = get_planet("saturn", date2)
        pluto2 = get_planet("pluto", date2)

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
                row = planets1.index(p1) + 1
                column = planets2.index(p2) + 1

                if aspect.good is None or aspect.good:
                    color = ""
                else:
                    color = f'foreground="{RED}"'
                    if p1.name in conflictedness1 or p2.name in conflictedness2:
                        color = 'foreground="red"'

                label = Gtk.Label()
                label.xalign = 0
                label.markup = f'<span {color}>{aspect.angle}°</span>'
                self.conflicts.attach(label, column, row, 1, 1)
                label.show()

    def calculate_love(self, date1: str, date2: str):
        moon = get_planet("moon", date1)
        venus = get_planet("venus", date1)
        sun = get_planet("sun", date2)
        mars = get_planet("mars", date2)

        clear_table(self.love)
        planets1 = (moon, venus)
        planets2 = (sun, mars)

        for p1 in planets1:
            for p2 in planets2:
                aspect = Aspect(p1, p2)
                row = planets1.index(p1) + 1
                column = planets2.index(p2) + 1

                if aspect.good is None:
                    color = ""
                elif aspect.good:
                    color = f'foreground="{GREEN}"'
                else:
                    color = f'foreground="{RED}"'

                label = Gtk.Label()
                label.xalign = 0
                label.markup = f'<span {color}>{aspect.angle}°</span>'
                self.love.attach(label, column, row, 1, 1)
                label.show()

    def calculate_friendship(self, date1: str, date2: str):
        sun1 = get_planet("sun", date1)
        moon1 = get_planet("moon", date1)
        venus1 = get_planet("venus", date1)

        sun2 = get_planet("sun", date2)
        moon2 = get_planet("moon", date2)
        venus2 = get_planet("venus", date2)

        clear_table(self.friendship)
        planets1 = (sun1, moon1, venus1)
        planets2 = (sun2, moon2, venus2)

        for p1 in planets1:
            for p2 in planets2:
                aspect = Aspect(p1, p2)
                row = planets1.index(p1) + 1
                column = planets2.index(p2) + 1

                # in the context of friendship we care only about
                # aspects between Suns, other aspects of Sun
                # (with Venus or Moon) are sexual and shouldn't
                # be highlighted
                if (p1.name == "sun" or p2.name == "sun") and p1.name != p2.name:
                    aspect.good = None

                if aspect.good is None or not aspect.good:
                    color = ""
                else:
                    color = f'foreground="{GREEN}"'

                label = Gtk.Label()
                label.xalign = 0
                label.markup = f'<span {color}>{aspect.angle}°</span>'
                self.friendship.attach(label, column, row, 1, 1)
                label.show()

    @staticmethod
    def calculate_happiness(table: Gtk.Grid, date1: str, date2: str):
        """
        Calculates how happy/unhappy person with date2
        makes person with date1.
        """

        sun1 = get_planet("sun", date1)
        moon1 = get_planet("moon", date1)
        jupiter2 = get_planet("jupiter", date2)
        saturn2 = get_planet("saturn", date2)

        clear_table(table)

        for i, planet in enumerate((sun1, moon1)):
            aspect = Aspect(jupiter2, planet)
            if aspect.good is None or not aspect.good:
                color = ""
            else:
                color = f'foreground="{GREEN}"'

            label = Gtk.Label()
            label.xalign = 0
            label.markup = f'<span {color}>{aspect.angle}°</span>'
            table.attach(label, 1, i + 1, 1, 1)
            label.show()

        for i, planet in enumerate((sun1, moon1)):
            aspect = Aspect(saturn2, planet)
            if aspect.good is None or aspect.good:
                color = ""
            else:
                color = f'foreground="{RED}"'

            label = Gtk.Label()
            label.xalign = 0
            label.markup = f'<span {color}>{aspect.angle}°</span>'
            table.attach(label, 2, i + 1, 1, 1)
            label.show()
