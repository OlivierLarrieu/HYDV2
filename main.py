#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from gi.repository import Gtk
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

DBusGMainLoop(set_as_default=True)
GLib.threads_init()

realpath = GLib.get_current_dir()
sys.path.append(realpath + '/Modules/')
sys.path.append(realpath + '/Apps/')
sys.path.append(realpath + '/Plugins/')

from Apps.MenuBar import MenuBar

core = MenuBar()
Gtk.main()
