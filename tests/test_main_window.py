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

from core.main_window import MainWindow

DATE = "2022-08-04 12:00"
DATE2 = "2022-08-06 12:00"


def test_calculate_conflictedness():
    window = MainWindow()
    grid = window.conflicts1
    conflictedness = window.calculate_conflictedness(grid, DATE)

    assert grid.get_child_at(2, 1).text == "87.6°"
    assert conflictedness == ["mars", "saturn"]


def test_calculate_conflicts():
    window = MainWindow()
    conf1 = window.calculate_conflictedness(window.conflicts1, DATE)
    conf2 = window.calculate_conflictedness(window.conflicts2, DATE2)
    window.calculate_conflicts(DATE, DATE2, conf1, conf2)

    for i in range(1, 5):
        degrees = window.conflicts.get_child_at(i, i).text
        assert degrees in ("1.3°", "0.1°", "0.0°")

    assert window.conflicts.get_child_at(3, 1).text == "87.8°"
    assert window.conflicts.get_child_at(1, 3).text == "88.9°"


def test_calculate_love():
    window = MainWindow()
    window.calculate_love(DATE, DATE2)
    assert window.love.get_child_at(2, 2).text == "59.6°"


def test_calculate_friendship():
    window = MainWindow()
    window.calculate_friendship(DATE, DATE2)

    assert window.friendship.get_child_at(1, 1).text == "1.9°"
    assert window.friendship.get_child_at(3, 3).text == "2.4°"
    assert window.friendship.get_child_at(2, 3).text == "126.9°"


def test_calculate_happiness():
    window = MainWindow()
    window.calculate_happiness(window.happiness2, DATE2, DATE)

    assert window.happiness2.get_child_at(1, 1).text == "125.4°"
    assert window.happiness2.get_child_at(2, 2).text == "84.6°"
