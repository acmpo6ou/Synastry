#  Copyright (c) 2022. Bohdan Kolvakh
#  This file is part of Synastry.
#
#  Synastry is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Synastry is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Synastry.  If not, see <https://www.gnu.org/licenses/>.

"""
Contains various utilities to simplify development with GTK.
"""

from __future__ import annotations

import contextlib
import itertools
import time
from typing import Callable

import pytest
from gi.repository import GObject, Gtk


# noinspection PyUnresolvedReferences
def _getattr(self, item: str):
    """
    A fluent API to get GTK object's attributes.

    Instead of writing:
    >>> label.get_text()
    >>> label.props.angle
    This method allows us to write:
    >>> label.text
    >>> label.angle
    Which is a more pythonic API.
    """
    try:
        return object.__getattribute__(self.props, item)
    except AttributeError:
        return object.__getattribute__(self, f"get_{item}")()


# noinspection PyUnresolvedReferences
def _setattr(self, item: str, value):
    """
    A fluent API to set GTK object's attributes.

    Instead of writing:
    >>> label.set_text("test")
    >>> label.props.angle = 90
    This method allows us to write:
    >>> label.text = "test"
    >>> label.angle = 90
    Which is a more pythonic API.
    """

    with contextlib.suppress(AttributeError):
        return setattr(self.props, item, value)
    try:
        getattr(self, f"set_{item}")(value)
    except AttributeError:
        original_setattr(self, item, value)


# save original __setattr__
original_setattr = GObject.Object.__setattr__

# replace __getattr__ and __setattr__ with our methods that provide fluent API
GObject.Object.__getattr__ = _getattr
GObject.Object.__setattr__ = _setattr


def _set_markup(self, value: str):
    self._html_text = value
    original_set_markup(self, value)


# replace set_markup with our version that saves the markup
# it's useful to get the markup later, e.g. in the tests
original_set_markup = Gtk.Label.set_markup
Gtk.Label.set_markup = _set_markup
Gtk.Label.get_markup = lambda self: self._html_text


class GladeTemplate(Gtk.Bin):
    """
    Simplifies loading of glade ui files.
    This class should be subclassed to automatically load needed ui file.
    """

    parent_widget: Gtk.Box

    def __init__(self, template: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.builder = Gtk.Builder.new_from_file(f"ui/{template}.glade")
        self.parent_widget = self.builder.get_object(template)
        self.add(self.parent_widget)
        self.builder.connect_signals(self)

    # noinspection PyUnresolvedReferences
    def __getattr__(self, item: str):
        """
        Simplifies widget access, instead of making builder.get_object() calls we can
        access widgets directly as attributes.

        Instead of writing this:
        >>> form.builder.get_object("mywidget")
        We can do this:
        >>> form.mywidget

        :param item: id of the widget.
        """
        # try to get widget from builder
        builder = object.__getattribute__(self, "builder")
        widget = builder.get_object(item)

        # if worked, return the widget
        if widget:
            attrs = object.__getattribute__(self, "__dict__")
            attrs[item] = widget  # cache it
            return widget

        # attribute we're trying to get is not a widget,
        # maybe it's a gtk property
        return _getattr(self, item)


def load_icon(icon_name: str, size: int) -> Gtk.Image:
    """
    Returns icon from default theme.
    """
    icon_theme = Gtk.IconTheme.get_default()
    icon = icon_theme.load_icon(icon_name, size, Gtk.IconLookupFlags.FORCE_SIZE)
    return Gtk.Image.new_from_pixbuf(icon)


def wait_until(callback: Callable[[], bool], timeout=5):
    """
    Waits until the return value from callback becomes True, or until timeout expires.
    """

    __tracebackhide__ = True
    start = time.time()

    while not callback():
        time_passed = time.time() - start
        if time_passed >= timeout:
            pytest.fail()

        while Gtk.events_pending():
            Gtk.main_iteration()


def clear_table(table: Gtk.Grid):
    for row, column in itertools.product(range(1, 5), range(1, 5)):
        child = table.get_child_at(column, row)
        if child:
            child.destroy()

    # clear colors from headers
    for i in range(1, 5):
        header1 = table.get_child_at(0, i)
        header2 = table.get_child_at(i, 0)

        if header1:
            header1.markup = header1.text
        if header2:
            header2.markup = header2.text


def insert_label(
    color: str,
    angle: float,
    table: Gtk.Grid,
    column: int,
    row: int,
):
    label = Gtk.Label()
    label.xalign = 0
    label.markup = f"<span {color}>{angle}°</span>"
    table.attach(label, column, row, 1, 1)
    label.show()
