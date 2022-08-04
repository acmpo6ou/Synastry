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

from core.date_time import DateTime
from core.gtk_utils import GladeTemplate


class MainWindow(Gtk.ApplicationWindow, GladeTemplate):
    # <editor-fold>
    parent_widget: Gtk.Box
    conflicts1: Gtk.Grid
    love: Gtk.Grid
    friendship: Gtk.Grid
    happiness1: Gtk.Grid
    happiness2: Gtk.Grid
    conflicts2: Gtk.Grid
    conflicts: Gtk.Grid

    # </editor-fold>
    def __init__(self, *args, **kwargs):
        Gtk.ApplicationWindow.__init__(self, *args, **kwargs)
        GladeTemplate.__init__(self, "main_window")

        self.set_default_size(1280, 720)
        # self.set_icon_from_file("img/icon.svg")

        self.date1 = DateTime(self)
        self.date2 = DateTime(self)

        hbox = Gtk.HBox()
        hbox.pack_start(self.date1, False, True, 0)
        hbox.pack_end(self.date2, False, True, 0)
        self.parent_widget.pack_start(hbox, False, True, 0)

    def on_date_changed(self):
        date1 = ...
        date2 = ...
        self.calculate_conflictedness(self.conflicts1)

    def calculate_conflictedness(self, table: Gtk.Grid, date_time: str):
        """ Calculates conflictedness of a person. """

    def calculate_conflicts(self):
        ...

    def calculate_love(self):
        ...

    def calculate_friendship(self):
        ...

    def calculate_happiness(self, table: Gtk.Grid, date1: str, date2: str):
        """
        Calculates how happy/unhappy person with date2
        makes person with date1.
        """
