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
DATE2 = "2022-08-06 12:00"


def test_calculate_conflictedness():
    window = MainWindow()
    grid = window.conflicts1
    conflictedness = window.calculate_conflictedness(grid, DATE)

    for row, column in itertools.product(range(4), range(4)):
        if row == 0 or column == 0:
            continue
        if row == 1 and column == 2:
            assert grid.get_child_at(column, row).text == "87.5°"
            continue
        assert not grid.get_child_at(column, row), f"{row}, {column}"

    assert conflictedness == ["mars", "saturn"]


def test_calculate_conflicts():
    window = MainWindow()
    conf1 = window.calculate_conflictedness(window.conflicts1, DATE)
    conf2 = window.calculate_conflictedness(window.conflicts2, DATE2)
    window.calculate_conflicts(DATE, DATE2, conf1, conf2)

    for row, column in itertools.product(range(5), range(5)):
        if row == 0 or column == 0:
            continue
        if row == column:
            degrees = window.conflicts.get_child_at(column, row).text
            assert degrees in ("1.2°", "0.1°", "0.0°")
        elif row == 1 and column == 3:
            assert window.conflicts.get_child_at(column, row).text == "87.7°"
        elif row == 3 and column == 1:
            assert window.conflicts.get_child_at(column, row).text == "88.8°"
        else:
            assert not window.conflicts.get_child_at(column, row), f"{row}, {column}"
