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
from contextlib import contextmanager
from time import perf_counter

from gi.repository import Gtk

from core.gtk_utils import GladeTemplate


@contextmanager
def catch_time(name) -> float:
    start = perf_counter()
    yield
    print(name, perf_counter() - start)


class DateTime(GladeTemplate):
    # <editor-fold>
    days: Gtk.Adjustment
    hour: Gtk.Adjustment
    minute: Gtk.Adjustment
    months: Gtk.Adjustment
    years: Gtk.Adjustment
    parent_widget: Gtk.Box
    hours: Gtk.SpinButton
    minutes: Gtk.SpinButton
    day: Gtk.SpinButton
    month: Gtk.SpinButton
    year: Gtk.SpinButton

    # </editor-fold>
    def __init__(self, main_window):
        GladeTemplate.__init__(self, "date_time")
        self.main_window = main_window

    @property
    def date_time(self) -> str:
        hours = int(self.hours.value)
        minutes = int(self.minutes.value)
        day = int(self.day.value)
        month = int(self.month.value)
        year = int(self.year.value)
        return f"{year}-{month:02}-{day:02} {hours:02}:{minutes:02}"

    def on_value_changed(self, _):
        with catch_time("") as t:
            self.main_window.on_date_changed()
