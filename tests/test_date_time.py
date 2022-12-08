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
from core.date_time import DateTime
from core.main_window import MainWindow


def test_date_time():
    window = MainWindow()
    date_time = DateTime(window)
    assert date_time.date_time == "2000-01-01 12:00"


def test_gmt_plus():
    window = MainWindow()
    date_time = DateTime(window)
    date_time.gmt.value = +2
    assert date_time.date_time == "2000-01-01 10:00"


def test_gmt_minus():
    window = MainWindow()
    date_time = DateTime(window)
    date_time.gmt.value = -5
    assert date_time.date_time == "2000-01-01 17:00"
