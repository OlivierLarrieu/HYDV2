#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from gi.repository import Gtk
from gi.repository import GLib

realpath = GLib.get_current_dir()
sys.path.append(realpath + '/Modules/')
sys.path.append(realpath + '/Apps/')
sys.path.append(realpath + '/Plugins/')

from Apps.AppsWindow import AppsWindow
win = AppsWindow()

Gtk.main()
