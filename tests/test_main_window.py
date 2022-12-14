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
import numpy as np
from astropy.coordinates import SkyCoord

from core.main_window import MainWindow, RED, GREEN
import numpy.typing as npt

DATE = "2022-08-04 12:00"
DATE2 = "2022-08-06 12:00"
BART = "1993-11-03 12:00"
NYNKE = "1997-12-03 12:00"
NO_COLOR = "<span >"


def get_data(window, collect):
    planet_pairs, ra1, dec1, ra2, dec2 = collect()
    coords1 = SkyCoord(ra1, dec1)
    coords2 = SkyCoord(ra2, dec2)
    angles = coords1.separation(coords2).deg.round(decimals=1)
    good = window.aspects_good(angles, planet_pairs)
    return planet_pairs, angles, good


def add_padding(array: npt.NDArray[int], start, end):
    return np.hstack((np.zeros(start), array, np.zeros(49-end)))


def test_present_conflictedness():
    window = MainWindow()
    grid = window.conflicts1
    data = get_data(window, lambda: window.collect_conflictedness(DATE))
    confness = window.present_conflictedness(grid, *data)

    label = grid.get_child_at(2, 1)
    assert label.text == "87.6°"
    assert RED in label.markup
    assert confness == ["mars", "saturn"]

    no_color = [label for label in grid.children if NO_COLOR in label.markup]
    assert len(no_color) == 5


def test_present_conflicts_header():
    window = MainWindow()
    _, __, good = get_data(window, lambda: window.collect_conflicts(DATE, DATE2))
    good = add_padding(good, 12, 28)
    window.present_conflicts_header(good)
    assert "definitely yes" in window.conflicts_header.markup
    assert "red" in window.conflicts_header.markup

    _, __, good = get_data(window, lambda: window.collect_conflicts(BART, NYNKE))
    good = add_padding(good, 12, 28)
    window.present_conflicts_header(good)
    assert "definitely no" in window.conflicts_header.markup
    assert GREEN in window.conflicts_header.markup


def test_present_conflicts():
    window = MainWindow()
    data1 = get_data(window, lambda: window.collect_conflictedness(DATE))
    conf1 = window.present_conflictedness(window.conflicts1, *data1)
    data2 = get_data(window, lambda: window.collect_conflictedness(DATE2))
    conf2 = window.present_conflictedness(window.conflicts2, *data2)
    data = get_data(window, lambda: window.collect_conflicts(DATE, DATE2))
    window.present_conflicts(conf1, conf2, *data)

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

    no_color = [label for label in window.conflicts.children if NO_COLOR in label.markup]
    assert len(no_color) == 11


def test_present_love():
    window = MainWindow()
    data = get_data(window, lambda: window.collect_love(DATE, DATE2))
    window.present_love(*data)

    label = window.love.get_child_at(2, 2)
    assert label.text == "59.6°"
    assert GREEN in label.markup

    no_color = [label for label in window.love.children if NO_COLOR in label.markup]
    assert len(no_color) == 3


def test_present_friendship():
    window = MainWindow()
    data = get_data(window, lambda: window.collect_friendship(DATE, DATE2))
    window.present_friendship(*data)

    label = window.friendship.get_child_at(1, 1)
    assert label.text == "1.9°"
    assert GREEN in label.markup

    label = window.friendship.get_child_at(3, 3)
    assert label.text == "2.4°"
    assert GREEN in label.markup

    label = window.friendship.get_child_at(2, 3)
    assert label.text == "127.1°"
    assert GREEN in label.markup

    no_color = [label for label in window.friendship.children if NO_COLOR in label.markup]
    assert len(no_color) == 6


def test_calculate_happiness():
    window = MainWindow()
    data = get_data(window, lambda: window.collect_happiness(DATE2, DATE))
    window.present_happiness(window.happiness2, *data[1:])

    label = window.happiness2.get_child_at(1, 1)
    assert label.text == "125.4°"
    assert GREEN in label.markup

    label = window.happiness2.get_child_at(2, 2)
    assert label.text == "84.4°"
    assert RED in label.markup

    no_color = [label for label in window.happiness2.children if NO_COLOR in label.markup]
    assert len(no_color) == 2
