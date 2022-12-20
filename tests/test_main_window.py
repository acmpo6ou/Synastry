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
import numpy.typing as npt
from astropy.coordinates import SkyCoord

from core.main_window import MainWindow, RED, GREEN, DARK_GREEN

DATE = "2022-08-04 12:00"
DATE2 = "2022-08-06 12:00"
BART = "1993-12-03 12:00"
NYNKE = "1997-11-03 12:00"
MARK = "1990-01-25 12:00"
MARJOLEIN = "1991-10-21 12:00"
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


def test_maybe(check):
    window = MainWindow()
    window.date1.date_time = BART
    window.date2.date_time = "1997-11-01 12:00"
    window.on_calculate()

    # the headers should be correct
    assert "maybe (6%)" in window.conflicts_header.markup
    assert RED in window.conflicts_header.markup

    assert "maybe (35%)" in window.love_header.markup
    assert DARK_GREEN in window.love_header.markup

    assert "maybe (47%)" in window.friendship_header.markup
    assert DARK_GREEN in window.friendship_header.markup

    assert "maybe (75%)" in window.unhappiness2_header.markup
    assert RED in window.unhappiness2_header.markup

    # the time buttons should be correct as well
    times = [button.label for button in window.conflict_times.children]
    assert times == ["16:00/00:00", "00:00/00:00"]

    times = [button.label for button in window.love_times.children]
    assert times == ["15:00/00:00", "00:00/00:00"]

    times = [button.label for button in window.frienship_times.children]
    assert times == ["14:00/18:00", "00:00/16:00", "00:00/03:00", "00:00/00:00"]

    times = [button.label for button in window.happiness1_times.children]
    assert times == ["00:00/00:00"]

    times = [button.label for button in window.happiness2_times.children]
    assert times == ["00:00/00:00"]

    times = [button.label for button in window.unhappiness1_times.children]
    assert times == ["00:00/00:00"]

    times = [button.label for button in window.unhappiness2_times.children]
    assert times == ["00:00/06:00", "00:00/00:00"]


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


def test_present_love_header():
    window = MainWindow()
    _, __, good = get_data(window, lambda: window.collect_love(DATE, DATE2))
    good = add_padding(good, 28, 32)
    window.present_love_header(good)
    assert "definitely yes" in window.love_header.markup
    assert GREEN in window.love_header.markup

    _, __, good = get_data(
        window, lambda: window.collect_love(BART, "1997-11-07 12:00")
    )
    good = add_padding(good, 28, 32)
    window.present_love_header(good)
    assert "definitely no" in window.love_header.markup
    assert RED in window.love_header.markup
    # TODO: test "maybe"


def test_present_love():
    window = MainWindow()
    data = get_data(window, lambda: window.collect_love(DATE, DATE2))
    window.present_love(*data)

    label = window.love.get_child_at(2, 2)
    assert label.text == "59.6°"
    assert GREEN in label.markup

    no_color = [label for label in window.love.children if NO_COLOR in label.markup]
    assert len(no_color) == 3


def test_present_friendship_header():
    window = MainWindow()
    _, __, good = get_data(window, lambda: window.collect_friendship(DATE, DATE2))
    good = add_padding(good, 32, 41)
    window.present_friendship_header(good)
    assert "definitely yes" in window.friendship_header.markup
    assert GREEN in window.friendship_header.markup

    _, __, good = get_data(
        window, lambda: window.collect_friendship(DATE, "2022-08-15 12:00")
    )
    good = add_padding(good, 32, 41)
    window.present_friendship_header(good)
    assert "definitely no" in window.friendship_header.markup
    assert RED in window.friendship_header.markup
    # TODO: test "maybe"


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


def test_present_happiness_header():
    window = MainWindow()
    _, __, good = get_data(window, lambda: window.collect_happiness(DATE2, DATE))
    good = add_padding(good, 41, 45)
    window.present_happiness_header(
        window.happiness1_header, 1, 41, 43, good,
    )
    assert "definitely yes" in window.happiness1_header.markup
    assert GREEN in window.happiness1_header.markup

    date = "2000-01-01 12:00"
    _, __, good = get_data(
        window, lambda: window.collect_happiness(date, date)
    )
    good = add_padding(good, 45, 49)
    window.present_happiness_header(
        window.happiness2_header, 2, 45, 47, good,
    )
    assert "definitely no" in window.happiness2_header.markup
    # TODO: test "maybe"


def test_present_unhappiness_header():
    window = MainWindow()
    _, __, good = get_data(window, lambda: window.collect_happiness(MARK, MARJOLEIN))
    good = add_padding(good, 41, 45)
    window.present_unhappiness_header(
        window.unhappiness1_header, 1, 43, 45, good,
    )
    assert "definitely yes" in window.unhappiness1_header.markup
    assert "red" in window.unhappiness1_header.markup

    _, __, good = get_data(
        window, lambda: window.collect_happiness(DATE, DATE2)
    )
    good = add_padding(good, 45, 49)
    window.present_unhappiness_header(
        window.unhappiness2_header, 2, 47, 49, good,
    )
    assert "definitely no" in window.unhappiness2_header.markup
    assert GREEN in window.unhappiness2_header.markup
    # TODO: test "maybe"


def test_present_happiness():
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
