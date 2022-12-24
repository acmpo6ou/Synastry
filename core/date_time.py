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
from datetime import datetime, timedelta

from gi.repository import Gtk

from core.gtk_utils import GladeTemplate


class DateTime(GladeTemplate):
    # <editor-fold>
    days: Gtk.Adjustment
    gmta: Gtk.Adjustment
    hour: Gtk.Adjustment
    minute: Gtk.Adjustment
    months: Gtk.Adjustment
    years: Gtk.Adjustment
    parent_widget: Gtk.Box
    hours: Gtk.SpinButton
    minutes: Gtk.SpinButton
    gmt: Gtk.SpinButton
    day: Gtk.SpinButton
    month: Gtk.SpinButton
    year: Gtk.SpinButton
    possibilities: Gtk.CheckButton
    # </editor-fold>

    def __init__(self, main_window):
        GladeTemplate.__init__(self, "date_time")
        self.main_window = main_window

    @staticmethod
    def show_leading_plus(gmt_field: Gtk.SpinButton):
        value = int(gmt_field.adjustment.value)
        gmt_field.text = f"+{value}" if value >= 0 else str(value)
        return True

    @staticmethod
    def show_leading_zero(field: Gtk.SpinButton):
        value = int(field.adjustment.value)
        field.text = f"{value:02}"
        return True

    def on_time_changed(self, _):
        hours = int(self.hours.value)
        minutes = int(self.minutes.value)
        gmt = int(self.gmt.value)
        self.possibilities.active = hours == 12 and minutes == 0 and gmt == 0

    def format_datetime(self, hours):
        minutes = int(self.minutes.value)
        day = int(self.day.value)
        month = int(self.month.value)
        year = int(self.year.value)

        date = datetime(year, month, day, hours, minutes)
        date -= timedelta(hours=int(self.gmt.value))
        return date.strftime("%Y-%m-%d %H:%M")

    @property
    def date_time(self) -> str:
        hours = int(self.hours.value)
        return self.format_datetime(hours)

    @date_time.setter
    def date_time(self, value: str):
        date = datetime.strptime(value, "%Y-%m-%d %H:%M")
        self.year.value = date.year
        self.month.value = date.month
        self.day.value = date.day
        self.hours.value = date.hour
        self.minutes.value = date.minute

    def get_possibilities(self) -> list[str]:
        return [self.format_datetime(hour) for hour in range(24)]
