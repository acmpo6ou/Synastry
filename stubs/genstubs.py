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
Generates type stubs for `core` package.

Adds stubs extracted from glade ui files.
This way, all classes that derive from GladeTemplate will have proper autocomplete.
"""

import os
import re

from xml.etree import ElementTree

CORE_DIR = "core/"
SKIP = ("__init__.py", "gtk_utils.py", "database_utils.py", "widgets.py", "__pycache__")


def gen_glade_stubs():
    out.write("    # <editor-fold>\n")
    ids = re.findall('id="([a-z_]*)"', glade_file)

    for _id in ids:
        widget = root.findall(f".//*[@id='{_id}']")[0]
        classname = widget.attrib["class"].replace("Gtk", "Gtk.")

        if _id == parent_widget_id:
            out.write(f"    parent_widget: {classname}\n")
            continue

        out.write(f"    {_id}: {classname}\n")
    out.write("    # </editor-fold>\n")


for file in os.listdir(CORE_DIR):
    if file in SKIP:
        continue

    _in = open(f"{CORE_DIR}/{file}", "r").readlines()
    out = open(f"{CORE_DIR}/{file}", "w")

    injected = False
    skip = False

    for line in _in:
        # skip previously generated stubs
        if "<editor-fold>" in line:
            skip = True
        elif "</editor-fold>" in line:
            skip = False
            continue

        if skip:
            continue

        out.write(line)

        if "class " in line and not injected:
            injected = True

            # fmt: off
            glade_filepath = f"ui/{file[:-2]}glade" \
                .replace("ui/create_", "ui/create_edit_") \
                .replace("ui/edit_", "ui/create_edit_")

            parent_widget_id = glade_filepath \
                .replace("ui/", "") \
                .replace(".glade", "")
            # fmt: on

            glade_file = open(glade_filepath, "r").read()
            root = ElementTree.parse(glade_filepath).getroot()

            gen_glade_stubs()
