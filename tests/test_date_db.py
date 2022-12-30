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
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

from gi.repository import Gtk
from core.main_window import MainWindow

DATE = "2022-08-04 12:00"


@pytest.fixture
def date_db():
    Path("database.json").unlink()
    return MainWindow().date_db


def test_fix_db_file(date_db):
    # database file should be created automatically
    assert Path("database.json").exists()


def test_on_save(date_db):
    window = date_db.window
    window.date1.date_time = DATE
    window.date1.gmt.value = +3
    window.date_picker1.child.text = "date1"

    window.save1_button.clicked()
    assert Path("database.json").read_text() == """{"date1": [12, 0, 3, 4, 8, 2022]}"""


def test_load_db(date_db):
    shutil.copyfile("tests/database.json", "./database.json")
    date_db.load_db()
    assert date_db.database == {"date1": [12, 0, 3, 4, 8, 2022], "date2": [12, 0, 3, 6, 8, 2022]}


@patch("core.date_db.WarningDialog", autospec=True)
def test_on_remove(dialog, date_db):
    shutil.copyfile("tests/database.json", "./database.json")
    date_db.load_db()
    window = date_db.window
    window.date_picker1.active = 0

    dialog.return_value.run.return_value = Gtk.ResponseType.YES
    window.remove1_button.clicked()

    assert "date1" not in date_db.database
    assert Path("database.json").read_text() == """{"date2": [12, 0, 3, 6, 8, 2022]}"""


def test_on_date_selected(date_db):
    shutil.copyfile("tests/database.json", "./database.json")
    date_db.load_db()

    window = date_db.window
    window.date_picker1.active = 0
    assert window.date1.time_data == [12, 0, 3, 4, 8, 2022]


def test_button_sensitivity(date_db):
    shutil.copyfile("tests/database.json", "./database.json")
    date_db.load_db()

    window = date_db.window
    assert not window.save1_button.sensitive
    assert not window.remove1_button.sensitive

    window.date_picker1.active = 0
    assert window.save1_button.sensitive
    assert window.remove1_button.sensitive
