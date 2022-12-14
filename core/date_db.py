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
import json
from pathlib import Path
from typing import TYPE_CHECKING
from gi.repository import Gtk

from core.date_time import DateTime
from core.widgets import WarningDialog

if TYPE_CHECKING:
    from core.main_window import MainWindow


class DateDb:
    def __init__(self, window: "MainWindow", db_file: str):
        self.window = window
        self.db_file = db_file
        self.database = {}

        self.fix_db_file()
        self.load_db()

    def fix_db_file(self):
        """ Creates database file if it's not present. """
        db_file = Path(self.db_file)
        if not db_file.exists():
            db_file.write_text("{}")

    def load_db(self):
        """ Loads database entries into main window's combo boxes. """
        with open(self.db_file) as file:
            self.database = json.load(file)
        self.load_date_picker(self.window.date_picker1)
        self.load_date_picker(self.window.date_picker2)

    def load_date_picker(self, picker: Gtk.ComboBoxText):
        picker.remove_all()
        for entry in sorted(self.database.keys()):
            picker.append(None, entry)

    def on_date_selected(
            self,
            picker: Gtk.ComboBoxText,
            save_button: Gtk.Button,
            remove_button: Gtk.Button,
            date_time: DateTime,
    ):
        """ Loads selected date into date_time. """
        selected = picker.active_text
        save_button.sensitive = bool(selected)
        remove_button.sensitive = bool(selected)
        date_time.time_data = self.database[selected]

    def on_save(self, picker: Gtk.ComboBoxText, date_time: DateTime):
        """ Saves current date to the database. """
        selected = picker.active_text
        if selected in self.database:
            result = WarningDialog(f"{selected} already exists, overwrite?").run()
            if result == Gtk.ResponseType.NO:
                return

        self.database[selected] = date_time.time_data
        with open(self.db_file, "w") as file:
            json.dump(self.database, file)

        self.load_date_picker(self.window.date_picker1)
        self.load_date_picker(self.window.date_picker2)

    def on_remove(self, picker: Gtk.ComboBoxText):
        """ Removes picked date from the database. """
        dialog = WarningDialog("Remove date?")
        if dialog.run() != Gtk.ResponseType.YES:
            return

        selected = picker.active_text
        if selected not in self.database:
            return

        del self.database[selected]
        with open(self.db_file, "w") as file:
            json.dump(self.database, file)

        self.load_date_picker(self.window.date_picker1)
        self.load_date_picker(self.window.date_picker2)
