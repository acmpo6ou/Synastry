#!/usr/bin/env python3

#   Copyright (c) 2022. Bohdan Kolvakh
#   This file is part of Synastry.
#
#   Synastry is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Synastry is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Synastry.  If not, see <https://www.gnu.org/licenses/>.
#

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gio

import sys

from core.main_window import MainWindow


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id="com.acmpo6ou.Synastry",
            flags=Gio.ApplicationFlags.HANDLES_OPEN,
            **kwargs
        )
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = MainWindow(application=self, title="Synastry")
            self.window.show_all()


if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
