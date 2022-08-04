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
from gi.repository import Gtk

from core.gtk_utils import GladeTemplate


class DateTime(GladeTemplate):
    # <editor-fold>
    parent_widget: Gtk.Box
    hours: Gtk.SpinButton
    minutes: Gtk.SpinButton
    day: Gtk.SpinButton
    month: Gtk.SpinButton
    year: Gtk.SpinButton

    # </editor-fold>
    def __init__(self):
        GladeTemplate.__init__(self, "date_time")

    @property
    def date_time(self) -> str:
        ...