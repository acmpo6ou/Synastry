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
from gi.repository import Gtk
from core.main_window import MainWindow

DATE = "2022-08-04 12:00"


def test_calculate_conflictedness():
    window = MainWindow()
    grid = Gtk.Grid()
    conflictedness = window.calculate_conflictedness(grid, DATE)

    for row, column in itertools.product(range(5), range(5)):
        if row == 0 or column == 0:
            continue
        if row == 1 and column == 3:
            assert grid.get_child_at(column, row).text == "87.5°"
            continue
        assert not grid.get_child_at(column, row), f"{row}, {column}"

    assert conflictedness[0].angle == 87.5
    assert len(conflictedness) == 1
