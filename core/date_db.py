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
from pathlib import Path
from typing import TYPE_CHECKING
from gi.repository import Gtk

from core.date_time import DateTime

if TYPE_CHECKING:
    from core.main_window import MainWindow


class DateDb:
    def __init__(self, window: "MainWindow"):
        self.window = window
        self.fix_db_file()
        self.load_db()

    @staticmethod
    def fix_db_file():
        """ Creates database file if it's not present. """
        db_file = Path("database.json")
        if not db_file.exists():
            db_file.touch()

    def load_db(self):
        """ Loads database entries into main window's combo boxes. """

    def on_date_selected(self, picker: Gtk.ComboBoxText, date_time: DateTime):
        """ Loads selected date into date_time. """

    def on_save(self, picker: Gtk.ComboBoxText, date_time: DateTime):
        """ Saves current date to the database. """

    def on_remove(self, picker: Gtk.ComboBoxText, date_time: DateTime):
        """ Removes picked date from the database. """
