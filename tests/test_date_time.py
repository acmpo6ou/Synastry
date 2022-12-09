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
import pytest

from core.date_time import DateTime
from core.main_window import MainWindow


@pytest.fixture
def date_time():
    window = MainWindow()
    return DateTime(window)


def test_date_time(date_time):
    assert date_time.date_time == "2000-01-01 12:00"


def test_gmt(date_time):
    date_time.gmt.value = +2
    assert date_time.date_time == "2000-01-01 10:00"

    date_time.gmt.value = -5
    assert date_time.date_time == "2000-01-01 17:00"


def test_gmt_boundaries(date_time):
    date_time.hours.value = 0
    date_time.gmt.value = +2
    assert date_time.date_time == "1999-12-31 22:00"

    date_time.hours.value = 23
    date_time.gmt.value = -5
    assert date_time.date_time == "2000-01-02 04:00"


def test_calculate_possibilities_state(date_time):
    ...
