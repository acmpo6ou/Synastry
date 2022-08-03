#!/usr/bin/env python3.9

#  Copyright (c) 2021-2022. Bohdan Kolvakh
#  This file is part of PyAccounts.
#
#  PyAccounts is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyAccounts is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with PyAccounts.  If not, see <https://www.gnu.org/licenses/>.

"""
Extends PyGObject-stubs to include our pythonic properties.
This way, we get autocompletion for them.
See _getattr and _setattr from gtk_utils module for more details.
"""


import re
import shutil

GTK_STUBS_PATH = "venv/lib/python3.9/site-packages/gi-stubs/repository/"

for module in ("Gtk", "Gdk", "Gio"):
    _in = open(f"{GTK_STUBS_PATH}/{module}.pyi")
    out = open(f"/tmp/{module}.pyi", "w")

    for line in _in.readlines():
        out.write(line)

        if line.startswith("    def get_"):
            prop = re.search("get_([a-z_]*)", line)[1]
            type_hint = "Any"

            if "->" in line:
                type_hint = re.search(r"->(.*?):", line)[1]
            out.write(f"    {prop}:{type_hint}\n")

    shutil.copyfile(f"/tmp/{module}.pyi", f"{GTK_STUBS_PATH}/{module}.pyi")
