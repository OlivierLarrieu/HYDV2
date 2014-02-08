#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
from gi.repository import GLib

realpath = GLib.get_current_dir()
sys.path.append(realpath + '/Modules/')
sys.path.append(realpath + '/Apps/')

from Apps.MenuBar import MenuBar
from Apps.AppsWindow import AppsWindow

os.system('python MenuBar_main.py &')
os.system('python AppsWindow_main.py &')


