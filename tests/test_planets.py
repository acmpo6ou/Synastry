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
from core.planets import Planet, Aspect
from tests.test_main_window import DATE


def test_aspect_120():
    p1 = Planet("sun", DATE)
    p2 = Planet("jupiter", DATE)

    aspect = Aspect(p1, p2)
    assert aspect.angle == 123.5
    assert aspect.good


def test_aspect_60():
    p1 = Planet("moon", DATE)
    p2 = Planet("mercury", DATE)

    aspect = Aspect(p1, p2)
    assert aspect.angle == 60.6
    assert aspect.good


def test_aspect_180():
    p1 = Planet("venus", "2022-08-06 12:00")
    p2 = Planet("pluto", "2022-08-06 12:00")

    aspect = Aspect(p1, p2)
    assert aspect.angle == 176.1
    assert not aspect.good


def test_aspect_90():
    p1 = Planet("moon", DATE)
    p2 = Planet("pluto", DATE)

    aspect = Aspect(p1, p2)
    assert aspect.angle == 86.1
    assert not aspect.good


def test_aspect_0_good_good():
    p1 = Planet("moon", "2022-07-29 00:00")
    p2 = Planet("sun", "2022-07-29 00:00")

    aspect = Aspect(p1, p2)
    assert aspect.angle == 5.4
    assert aspect.good


def test_aspect_0_good_bad():
    p1 = Planet("moon", "2022-08-10 07:00")
    p2 = Planet("pluto", "2022-08-10 07:00")

    aspect = Aspect(p1, p2)
    assert aspect.angle == 5.3
    assert not aspect.good


def test_aspect_0_bad_bad():
    p1 = Planet("mars", DATE)
    p2 = Planet("uranus", DATE)

    aspect = Aspect(p1, p2)
    assert aspect.angle == 2.0
    assert not aspect.good


def test_no_aspect():
    p1 = Planet("moon", DATE)
    p2 = Planet("sun", DATE)

    aspect = Aspect(p1, p2)
    assert aspect.good is None
