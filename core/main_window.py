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
import itertools
from time import perf_counter

import numpy as np
import numpy.typing as npt
from astropy.coordinates import SkyCoord, Angle
from gi.repository import Gtk

from core.date_db import DateDb
from core.date_time import DateTime
from core.gtk_utils import GladeTemplate, clear_table, insert_label
from core.planets import Planet, get_planet
from core.utils import ArrayIter, get_aspects_good

RED = "#f04b51"
GREEN = "#6db442"
DARK_GREEN = "#568F34"
CONFLICT_PLANETS = ("mars", "jupiter", "saturn", "pluto")


class MainWindow(Gtk.ApplicationWindow, GladeTemplate):
    # <editor-fold>
    parent_widget: Gtk.Box
    date_picker1: Gtk.ComboBoxText
    save1_button: Gtk.Button
    remove1_button: Gtk.Button
    date_picker2: Gtk.ComboBoxText
    remove2_button: Gtk.Button
    conflicts_header: Gtk.Label
    love_header: Gtk.Label
    conflicts1: Gtk.Grid
    friendship_header: Gtk.Label
    conflicts2: Gtk.Grid
    conflicts: Gtk.Grid
    conflict_times: Gtk.Grid
    happiness1: Gtk.Grid
    happiness1_header: Gtk.Label
    unhappiness1_header: Gtk.Label
    love: Gtk.Grid
    happiness2: Gtk.Grid
    unhappiness2_header: Gtk.Label
    happiness2_header: Gtk.Label
    friendship: Gtk.Grid
    love_times: Gtk.Grid
    frienship_times: Gtk.Grid
    happiness1_times: Gtk.Grid
    happiness2_times: Gtk.Grid
    unhappiness2_times: Gtk.Grid
    unhappiness1_times: Gtk.Grid
    # </editor-fold>

    def __init__(self, db_file="database.json", *args, **kwargs):
        Gtk.ApplicationWindow.__init__(self, *args, **kwargs)
        GladeTemplate.__init__(self, "main_window")

        self.maximize()
        # self.set_icon_from_file("img/icon.svg")
        self.date_db = DateDb(self, db_file)

        self.date1 = DateTime(self)
        self.date2 = DateTime(self)

        calculate = Gtk.Button("Calculate")
        calculate.connect("clicked", self.on_calculate)
        calculate.style_context.add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

        hbox = Gtk.Box(Gtk.Orientation.HORIZONTAL, 100)
        hbox.pack_start(self.date1, False, True, 0)
        hbox.center_widget = calculate
        hbox.pack_end(self.date2, False, True, 0)
        self.parent_widget.pack_start(hbox, False, True, 0)

    def on_calculate(self, _=None):
        start = perf_counter()
        date1 = self.date1.date_time
        date2 = self.date2.date_time

        self.dates1 = [date1]
        if self.date1.possibilities.active:
            self.dates1 = self.date1.get_possibilities()

        self.dates2 = [date2]
        if self.date2.possibilities.active:
            self.dates2 = self.date2.get_possibilities()

        planet_pairs, angles = self.calculate_angles(self.dates1, self.dates2)
        good = get_aspects_good(angles, planet_pairs)

        planet_pairs = [planet_pairs[i:i + 49] for i in range(0, len(planet_pairs), 49)]
        angles = angles.reshape(-1, 49)
        good = good.reshape(-1, 49)

        self.planet_pairs = planet_pairs
        self.angles = angles
        self.good = good

        self.present_conflicts_header(good)
        self.present_love_header(good)
        self.present_friendship_header(good)

        self.present_happiness_header(
            self.happiness1_header, 1, 41, 43, good, self.happiness1_times
        )
        self.present_happiness_header(
            self.happiness2_header, 2, 45, 47, good, self.happiness2_times
        )

        self.present_unhappiness_header(
            self.unhappiness1_header, 1, 43, 45, good, self.unhappiness1_times
        )
        self.present_unhappiness_header(
            self.unhappiness2_header, 2, 47, 49, good, self.unhappiness2_times
        )

        self.present_all_tables(0)
        print(perf_counter() - start)

    def present_all_tables(self, index):
        planet_pairs = ArrayIter(self.planet_pairs[index])
        angles = ArrayIter(self.angles[index])
        good = ArrayIter(self.good[index])

        def data(n):
            return planet_pairs[n], angles[n], good[n]

        conf1 = self.present_conflictedness(self.conflicts1, *data(6))
        conf2 = self.present_conflictedness(self.conflicts2, *data(6))
        self.present_conflicts(conf1, conf2, *data(16))

        self.present_love(*data(4))
        self.present_friendship(*data(9))

        self.present_happiness(self.happiness1, angles[4], good[4])
        self.present_happiness(self.happiness2, angles[4], good[4])

    def calculate_angles(self, dates1: list[str], dates2: list[str]):
        """
        Collects pairs of planets and their coordinates,
        and calculates angles between them.
        """

        planet_pairs_all = []
        ra1_all = []
        dec1_all = []
        ra2_all = []
        dec2_all = []

        for date1, date2 in itertools.product(dates1, dates2):
            planet_pairs, ra1, dec1, ra2, dec2 = self.collect_all_coords(date1, date2)
            planet_pairs_all += planet_pairs
            ra1_all += ra1
            dec1_all += dec1
            ra2_all += ra2
            dec2_all += dec2

        coords1 = SkyCoord(ra1_all, dec1_all)
        coords2 = SkyCoord(ra2_all, dec2_all)
        angles = coords1.separation(coords2)
        return planet_pairs_all, angles.deg.round(decimals=1)

    def collect_all_coords(self, date1: str, date2: str):
        conf1 = self.collect_conflictedness(date1)
        conf2 = self.collect_conflictedness(date2)
        confs = self.collect_conflicts(date1, date2)
        love = self.collect_love(date1, date2)
        friendship = self.collect_friendship(date1, date2)
        happiness1 = self.collect_happiness(date1, date2)
        happiness2 = self.collect_happiness(date2, date1)
        coords = (conf1, conf2, confs, love, friendship, happiness1, happiness2)

        planet_pairs_all = []
        ra1_all = []
        dec1_all = []
        ra2_all = []
        dec2_all = []

        for planet_pairs, ra1, dec1, ra2, dec2 in coords:
            planet_pairs_all += planet_pairs
            ra1_all += ra1
            dec1_all += dec1
            ra2_all += ra2
            dec2_all += dec2
        return planet_pairs_all, ra1_all, dec1_all, ra2_all, dec2_all

    @staticmethod
    def collect_coords(planets1: tuple[Planet], planets2: tuple[Planet]):
        planet_pairs = []
        ra1 = []
        dec1 = []
        ra2 = []
        dec2 = []

        for p1, p2 in itertools.product(planets1, planets2):
            planet_pairs.append((p1, p2))
            ra1.append(p1.body.ra)
            dec1.append(p1.body.dec)
            ra2.append(p2.body.ra)
            dec2.append(p2.body.dec)
        return planet_pairs, ra1, dec1, ra2, dec2

    @staticmethod
    def collect_conflictedness(date_time: str):
        mars = get_planet("mars", date_time)
        jupiter = get_planet("jupiter", date_time)
        saturn = get_planet("saturn", date_time)
        pluto = get_planet("pluto", date_time)

        PLANETS = (mars, jupiter, saturn, pluto)
        planets = [mars, jupiter, saturn, pluto]

        planet_pairs = []
        ra1 = []
        dec1 = []
        ra2 = []
        dec2 = []

        for p1 in PLANETS:
            planets.remove(p1)
            for p2 in planets:
                planet_pairs.append((p1, p2))
                ra1.append(p1.body.ra)
                dec1.append(p1.body.dec)
                ra2.append(p2.body.ra)
                dec2.append(p2.body.dec)
        return planet_pairs, ra1, dec1, ra2, dec2

    def present_conflictedness(
        self,
        table: Gtk.Grid,
        planet_pairs: list[tuple[Planet]],
        angles: Angle,
        aspects_good: npt.NDArray[int],
    ) -> list[str]:
        """
        Calculates conflictedness of a person.
        :returns: a list of conflicting planets of this person.
        """

        conflictedness = []
        clear_table(table)

        for (p1, p2), angle, good in zip(planet_pairs, angles, aspects_good):
            row = CONFLICT_PLANETS.index(p1.name) + 1
            column = CONFLICT_PLANETS.index(p2.name)

            if good == -1 or good:
                color = ""
            else:
                conflictedness.extend((p1.name, p2.name))
                color = f'foreground="{RED}"'

                header1 = table.get_child_at(0, row)
                header2 = table.get_child_at(column, 0)
                header1.markup = f'<span foreground="{RED}">{header1.text}</span>'
                header2.markup = f'<span foreground="{RED}">{header2.text}</span>'

            insert_label(color, angle, table, column, row)
        return conflictedness

    def collect_conflicts(self, date1: str, date2: str):
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
        return self.collect_coords(planets1, planets2)

    def present_conflicts_header(self, aspects_good: npt.NDArray[int]):
        conflicts = aspects_good[:, 12:28]
        conflicts[conflicts == 1] = -1
        self.present_times(conflicts, self.conflict_times)
        conflicts = (conflicts == 0).any(1)

        header = "Conflicts: <span foreground='{}'>{}</span>"
        if conflicts.all():
            color, text = "red", "definitely yes"
        elif (num := np.count_nonzero(conflicts)) > 0:
            percentage = num * 100 / len(conflicts)
            color, text = RED, f"maybe ({int(percentage)}%)"
        else:
            color, text = GREEN, "definitely no"
        self.conflicts_header.markup = header.format(color, text)

    def present_times(self, good: npt.NDArray[int], table: Gtk.Grid):
        table.foreach(lambda x: x.destroy())
        data = zip(itertools.product(self.dates1, self.dates2), good)
        column, row = 0, -1
        column_value = ""
        presented = []

        for (date1, date2), conflict in data:
            # show only times that have different aspects
            conflict = list(conflict)
            if conflict in presented:
                continue
            presented.append(conflict)

            time1 = date1.split()[1]
            time2 = date2.split()[1]

            # align items such that each column has the same time1
            # so we'll have a separate column where time1 is 00:00,
            # a separate one for time1 01:00, etc.
            if time1 != column_value:
                column_value = time1
                row = 0
                column += 1

            button = Gtk.Button(f"{time1}/{time2}")
            button.show_all()

            date1_i = self.dates1.index(date1)
            date2_i = self.dates2.index(date2)
            time_i = date1_i * 24 + date2_i
            button.connect(
                "clicked",
                lambda _, i=time_i, date1=date1, date2=date2: self.set_time(i, date1, date2),
            )

            table.attach(button, column, row, 1, 1)
            row += 1

    def set_time(self, i, date1, date2):
        self.date1.date_time = date1
        self.date2.date_time = date2
        self.present_all_tables(i)

    def present_conflicts(
        self,
        conflictedness1: list[str],
        conflictedness2: list[str],
        planet_pairs: list[tuple[Planet]],
        angles: Angle,
        aspects_good: npt.NDArray[int],
    ):
        clear_table(self.conflicts)

        for planet in conflictedness1:
            i = CONFLICT_PLANETS.index(planet) + 1
            header = self.conflicts.get_child_at(0, i)
            header.markup = f'<span foreground="red">{header.text}</span>'

        for planet in conflictedness2:
            i = CONFLICT_PLANETS.index(planet) + 1
            header = self.conflicts.get_child_at(i, 0)
            header.markup = f'<span foreground="red">{header.text}</span>'

        for (p1, p2), angle, good in zip(planet_pairs, angles, aspects_good):
            row = CONFLICT_PLANETS.index(p1.name) + 1
            column = CONFLICT_PLANETS.index(p2.name) + 1

            if good == -1 or good:
                color = ""
            else:
                color = f'foreground="{RED}"'
                if p1.name in conflictedness1 or p2.name in conflictedness2:
                    color = 'foreground="red"'

            insert_label(color, angle, self.conflicts, column, row)

    def collect_love(self, date1: str, date2: str):
        moon = get_planet("moon", date1)
        venus = get_planet("venus", date1)
        sun = get_planet("sun", date2)
        mars = get_planet("mars", date2)

        planets1 = (moon, venus)
        planets2 = (sun, mars)
        return self.collect_coords(planets1, planets2)

    def present_love_header(self, aspects_good: npt.NDArray[int]):
        love = aspects_good[:, 28:32]
        self.present_times(love, self.love_times)
        love = (love != -1).any(1)

        header = "Love: <span foreground='{}'>{}</span>"
        if love.all():
            color, text = GREEN, "definitely yes"
        elif (num := np.count_nonzero(love)) > 0:
            percentage = num * 100 / len(love)
            color, text = DARK_GREEN, f"maybe ({int(percentage)}%)"
        else:
            color, text = RED, "definitely no"
        self.love_header.markup = header.format(color, text)

    def present_love(
        self,
        planet_pairs: list[tuple[Planet]],
        angles: Angle,
        aspects_good: npt.NDArray[int],
    ):
        clear_table(self.love)
        planets1 = ("moon", "venus")
        planets2 = ("sun", "mars")

        for (p1, p2), angle, good in zip(planet_pairs, angles, aspects_good):
            row = planets1.index(p1.name) + 1
            column = planets2.index(p2.name) + 1

            if good == -1:
                color = ""
            elif good:
                color = f'foreground="{GREEN}"'
            else:
                color = f'foreground="{RED}"'

            insert_label(color, angle, self.love, column, row)

    def collect_friendship(self, date1: str, date2: str):
        sun1 = get_planet("sun", date1)
        moon1 = get_planet("moon", date1)
        venus1 = get_planet("venus", date1)

        sun2 = get_planet("sun", date2)
        moon2 = get_planet("moon", date2)
        venus2 = get_planet("venus", date2)

        planets1 = (sun1, moon1, venus1)
        planets2 = (sun2, moon2, venus2)
        return self.collect_coords(planets1, planets2)

    def present_friendship_header(self, aspects_good: npt.NDArray[int]):
        friendship = aspects_good[:, 32:41]
        friendship[:, 1:4] = -1  # don't count aspects of Sun and Moon/Venus
        friendship[:, 6] = -1
        friendship[friendship == 0] = -1
        self.present_times(friendship, self.frienship_times)
        friendship = (friendship == 1).any(1)

        header = "Friendship: <span foreground='{}'>{}</span>"
        if friendship.all():
            color, text = GREEN, "definitely yes"
        elif (num := np.count_nonzero(friendship)) > 0:
            percentage = num * 100 / len(friendship)
            color, text = DARK_GREEN, f"maybe ({int(percentage)}%)"
        else:
            color, text = RED, "definitely no"
        self.friendship_header.markup = header.format(color, text)

    def present_friendship(
        self,
        planet_pairs: list[tuple[Planet]],
        angles: Angle,
        aspects_good: npt.NDArray[int],
    ):
        clear_table(self.friendship)
        PLANETS = ("sun", "moon", "venus")

        for (p1, p2), angle, good in zip(planet_pairs, angles, aspects_good):
            row = PLANETS.index(p1.name) + 1
            column = PLANETS.index(p2.name) + 1

            # in the context of friendship we care only about
            # aspects between Suns, other aspects of Sun
            # (with Venus or Moon) are sexual and shouldn't
            # be highlighted
            if (p1.name == "sun" or p2.name == "sun") and p1.name != p2.name:
                good = -1

            if good == -1 or not good:
                color = ""
            else:
                color = f'foreground="{GREEN}"'

            insert_label(color, angle, self.friendship, column, row)

    def collect_happiness(self, date1: str, date2: str):
        sun1 = get_planet("sun", date1)
        moon1 = get_planet("moon", date1)
        jupiter2 = get_planet("jupiter", date2)
        saturn2 = get_planet("saturn", date2)

        planets1 = (jupiter2, saturn2)
        planets2 = (sun1, moon1)
        return self.collect_coords(planets1, planets2)

    def present_happiness_header(
        self,
        header: Gtk.Label,
        number: int,
        start: int,
        end: int,
        aspects_good: npt.NDArray[int],
        happiness_times: Gtk.Grid,
    ):
        happiness = aspects_good[:, start:end]
        happiness[happiness == 0] = -1
        self.present_times(happiness, happiness_times)
        happiness = (happiness == 1).any(1)

        header_text = "Happiness {}: <span foreground='{}'>{}</span>"
        if happiness.all():
            color, text = GREEN, "definitely yes"
        elif (num := np.count_nonzero(happiness)) > 0:
            percentage = num * 100 / len(happiness)
            color, text = DARK_GREEN, f"maybe ({int(percentage)}%)"
        else:
            header.markup = f"Happiness {number}: definitely no"
            return
        header.markup = header_text.format(number, color, text)

    def present_unhappiness_header(
        self,
        header: Gtk.Label,
        number: int,
        start: int,
        end: int,
        aspects_good: npt.NDArray[int],
        unhappiness_times: Gtk.Grid,
    ):
        unhappiness = aspects_good[:, start:end]
        unhappiness[unhappiness == 1] = -1
        self.present_times(unhappiness, unhappiness_times)
        unhappiness = (unhappiness == 0).any(1)

        header_text = "Unhappiness {}: <span foreground='{}'>{}</span>"
        if unhappiness.all():
            color, text = "red", "definitely yes"
        elif (num := np.count_nonzero(unhappiness)) > 0:
            percentage = num * 100 / len(unhappiness)
            color, text = RED, f"maybe ({int(percentage)}%)"
        else:
            color, text = GREEN, "definitely no"
        header.markup = header_text.format(number, color, text)

    @staticmethod
    def present_happiness(
        table: Gtk.Grid,
        angles: Angle,
        aspects_good: npt.NDArray[int],
    ):
        """
        Calculates how happy/unhappy person with date2
        makes person with date1.
        """
        clear_table(table)

        data = zip(angles[:2], aspects_good[:2], range(2))
        for angle, good, i in data:
            if good == -1 or not good:
                color = ""
            else:
                color = f'foreground="{GREEN}"'

            insert_label(color, angle, table, 1, i+1)

        data = zip(angles[2:], aspects_good[2:], range(2))
        for angle, good, i in data:
            if good == -1 or good:
                color = ""
            else:
                color = f'foreground="{RED}"'

            insert_label(color, angle, table, 2, i+1)

    def on_date_selected1(self, picker: Gtk.ComboBoxText):
        self.date_db.on_date_selected(picker, self.save1_button, self.remove1_button, self.date1)

    def on_date_selected2(self, picker: Gtk.ComboBoxText):
        self.date_db.on_date_selected(picker, self.save2_button, self.remove2_button, self.date2)

    def on_save1(self, picker: Gtk.ComboBoxText):
        self.date_db.on_save(picker, self.date1)

    def on_save2(self, picker: Gtk.ComboBoxText):
        self.date_db.on_save(picker, self.date2)

    def on_remove1(self, picker: Gtk.ComboBoxText):
        self.date_db.on_remove(picker)

    def on_remove2(self, picker: Gtk.ComboBoxText):
        self.date_db.on_remove(picker)
