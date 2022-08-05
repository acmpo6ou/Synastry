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
from core.planets import Aspect, Planet

DATE = "2022-08-04 12:00"


def test_calculate_conflictedness():
    window = MainWindow()
    grid = Gtk.Grid()

    window.calculate_conflictedness(grid, DATE)
    for row, column in itertools.product(range(5), range(5)):
        if row == 0 or column == 0:
            continue
        if row == 1 and column == 3:
            assert grid.get_child_at(column, row).text == "87.5°"
            continue
        assert not grid.get_child_at(column, row), f"{row}, {column}"


def test_aspect_120():
    p1 = Planet("sun", DATE)
    p2 = Planet("jupiter", DATE)

    aspect = Aspect(p1, p2)
    assert aspect.angle == 124.3
    assert aspect.good


def test_aspect_60():
    p1 = Planet("moon", DATE)
    p2 = Planet("mercury", DATE)

    aspect = Aspect(p1, p2)
    assert aspect.angle == 58.8
    assert aspect.good


def test_aspect_180():
    p1 = Planet("venus", DATE)
    p2 = Planet("pluto", DATE)

    aspect = Aspect(p1, p2)
    assert aspect.angle == 173.9
    assert not aspect.good


def test_aspect_90():
    p1 = Planet("moon", DATE)
    p2 = Planet("pluto", DATE)

    aspect = Aspect(p1, p2)
    assert aspect.angle == 85.8
    assert not aspect.good


def test_aspect_0_good_good():
    p1 = Planet("moon", "2022-07-29 06:00")
    p2 = Planet("sun", "2022-07-29 06:00")

    aspect = Aspect(p1, p2)
    assert aspect.angle == 7.3
    assert aspect.good


def test_aspect_0_good_bad():
    p1 = Planet("moon", "2022-08-10 07:00")
    p2 = Planet("pluto", "2022-08-10 07:00")

    aspect = Aspect(p1, p2)
    assert aspect.angle == 4.3
    assert not aspect.good


def test_aspect_0_bad_bad():
    p1 = Planet("mars", DATE)
    p2 = Planet("uranus", DATE)

    aspect = Aspect(p1, p2)
    assert aspect.angle == 1.8
    assert not aspect.good


def test_aspect_0_jupiter_no_conflicts():
    p1 = Planet("jupiter", DATE)
    p2 = Planet("jupiter", DATE)

    aspect = Aspect(p1, p2)
    assert aspect.angle == 0
    assert aspect.good


def test_aspect_0_jupiter_conflicts():
    p1 = Planet("jupiter", DATE)
    p2 = Planet("jupiter", DATE)

    aspect = Aspect(p1, p2, conflicts=True)
    assert aspect.angle == 0
    assert not aspect.good


def test_no_aspect():
    p1 = Planet("moon", DATE)
    p2 = Planet("sun", DATE)

    aspect = Aspect(p1, p2)
    assert aspect.angle is None
