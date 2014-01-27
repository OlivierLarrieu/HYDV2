#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from gi.repository import Gtk
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop


realpath = GLib.get_current_dir()
sys.path.append(realpath + '/Modules/')
sys.path.append(realpath + '/Apps/')
sys.path.append(realpath + '/Plugins/')

from Apps.MenuBar import MenuBar
from Apps.AppsWindow import AppsWindow
win = AppsWindow()

core = MenuBar()

Gtk.main()
