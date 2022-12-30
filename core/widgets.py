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

from core.gtk_utils import load_icon


class IconDialog(Gtk.Dialog):
    """
    Dialog containing icon and message.
    """

    # DO NOT REMOVE THIS, this is needed because of strange issues with
    # _setattr from gtk_utils
    vbox = None

    def __init__(self, title: str, message: str, icon: str, *args, **kwargs):
        super().__init__(self, title=title, modal=True, *args, **kwargs)
        self.vbox = self.content_area
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.vbox.add(box)

        image = load_icon(icon, 64)
        image.margin = 10
        box.add(image)

        label = Gtk.Label(message, use_markup=True)
        label.margin = 10
        box.add(label)

    def run(self) -> Gtk.ResponseType:
        self.show_all()
        response = super().run()
        self.destroy()
        return response


class WarningDialog(IconDialog):
    """
    Dialog with warning icon and 2 buttons: `Yes` and `No`.
    """

    def __init__(self, message: str, buttons: tuple = None, *args, **kwargs):
        if not buttons:
            buttons = ("_No", Gtk.ResponseType.NO, "Yes", Gtk.ResponseType.YES)

        super().__init__(
            title="Warning!",
            message=message,
            icon="dialog-warning",
            buttons=buttons,
            *args,
            **kwargs,
        )


class ErrorDialog(IconDialog):
    """
    Dialog with error icon, error message and details.
    """

    def __init__(self, message: str, err: Exception, *args, **kwargs):
        super().__init__(
            title="Error!",
            message=message,
            icon="dialog-error",
            *args,
            **kwargs,
        )

        # fmt: off
        error_class = str(err.__class__) \
            .removeprefix("<class '") \
            .removesuffix("'>")
        # fmt: on
        details = f"{error_class}:\n{err}"

        details_label = Gtk.Label()
        details_label.markup = f"<span font_desc='Ubuntu Mono 20'>{details}</span>"
        details_label.selectable = True
        details_label.line_wrap = True
        details_label.xalign = 0
        details_label.margin_start = 5
        details_label.margin_end = 5

        expander = Gtk.Expander.new_with_mnemonic("_Details")
        expander.add(details_label)
        self.vbox.add(expander)
