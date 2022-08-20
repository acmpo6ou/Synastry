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

from core.main_window import MainWindow, RED, GREEN
from core.planets import Planet

DATE = "2022-08-04 12:00"
DATE2 = "2022-08-06 12:00"
NO_COLOR = "<span >"


def test_calculate_conflictedness():
    window = MainWindow()
    grid = window.conflicts1

    planets = window.conflicting_planets(DATE)
    conflictedness = window.calculate_conflictedness(grid, *planets)

    label = grid.get_child_at(2, 1)
    assert label.text == "87.6°"
    assert RED in label.markup
    assert conflictedness == ["mars", "saturn"]

    no_color = len([label for label in grid.children
                    if NO_COLOR in label.markup])
    assert no_color == 5


def test_calculate_conflicts():
    window = MainWindow()
    planets1 = window.conflicting_planets(DATE)
    planets2 = window.conflicting_planets(DATE2)

    conf1 = window.calculate_conflictedness(window.conflicts1, *planets1)
    conf2 = window.calculate_conflictedness(window.conflicts2, *planets2)
    window.calculate_conflicts(*planets1, *planets2, conf1, conf2)

    label = window.conflicts.get_child_at(1, 1)
    assert label.text == "1.3°"
    assert "red" in label.markup

    label = window.conflicts.get_child_at(2, 2)
    assert label.text == "0.1°"
    assert NO_COLOR in label.markup

    label = window.conflicts.get_child_at(3, 3)
    assert label.text == "0.1°"
    assert "red" in label.markup

    label = window.conflicts.get_child_at(4, 4)
    assert label.text == "0.0°"
    assert RED in label.markup

    label = window.conflicts.get_child_at(3, 1)
    assert label.text == "87.8°"
    assert "red" in label.markup

    label = window.conflicts.get_child_at(1, 3)
    assert label.text == "88.9°"
    assert "red" in label.markup

    no_color = len([label for label in window.conflicts.children
                    if NO_COLOR in label.markup])
    assert no_color == 11


def test_calculate_love():
    window = MainWindow()
    window.calculate_love(DATE, DATE2)

    label = window.love.get_child_at(2, 2)
    assert label.text == "59.6°"
    assert GREEN in label.markup

    no_color = len([label for label in window.love.children
                    if NO_COLOR in label.markup])
    assert no_color == 3


def test_calculate_friendship():
    window = MainWindow()
    window.calculate_friendship(DATE, DATE2)

    label = window.friendship.get_child_at(1, 1)
    assert label.text == "1.9°"
    assert GREEN in label.markup

    label = window.friendship.get_child_at(3, 3)
    assert label.text == "2.4°"
    assert GREEN in label.markup

    label = window.friendship.get_child_at(2, 3)
    assert label.text == "127.1°"
    assert GREEN in label.markup

    no_color = len([label for label in window.friendship.children
                    if NO_COLOR in label.markup])
    assert no_color == 6


def test_calculate_happiness():
    window = MainWindow()
    window.calculate_happiness(window.happiness2, DATE2, DATE)

    label = window.happiness2.get_child_at(1, 1)
    assert label.text == "125.4°"
    assert GREEN in label.markup

    label = window.happiness2.get_child_at(2, 2)
    assert label.text == "84.4°"
    assert RED in label.markup

    no_color = len([label for label in window.happiness2.children
                    if NO_COLOR in label.markup])
    assert no_color == 2
