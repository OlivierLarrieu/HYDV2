#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Copyright (C) 2012 Josepe36
This is part of hy-d-v1 project.
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see www.gnu.org/licenses/.

Contact: olivier.hybryde.dev@gmail.com
"""

import os
import Menu
from gi.repository import GLib
from gi.repository import Gtk as gtk

USER_DIR = GLib.get_home_dir()
realpath = GLib.get_current_dir()

print "realpath", realpath
class IconParser(object):
    def findicon(self, icon_name):
        usr_share_icons = os.listdir('/usr/share/icons/')  
        usr_share_pixmaps = os.listdir('/usr/share/pixmaps/')      
        for elem in usr_share_icons:
            if os.path.isdir("/usr/share/icons/"+elem):
                if os.path.isdir("/usr/share/icons/"+elem+"/48x48/"):
                    icon_dir_list = os.listdir('/usr/share/icons/'+elem+"/48x48/")
                    for directory in icon_dir_list:
                        tmp_list = os.listdir('/usr/share/icons/'+elem+"/48x48/"+directory)
                        for icon in tmp_list:
                            if icon.split('.')[0] == icon_name:
                                del usr_share_icons
                                del usr_share_pixmaps
                                return "/usr/share/icons/"+elem+"/48x48/"+directory+"/"+icon
        for elem in usr_share_pixmaps:
            if  os.path.isfile('/usr/share/pixmaps/'+elem):
                if elem.split('.')[0] == icon_name:

                    return '/usr/share/pixmaps/'+elem
        for elem in usr_share_icons:
            if  os.path.isfile('/usr/share/icons/'+elem):
                if elem.split('.')[0] == icon_name:
                    return '/usr/share/icons/'+elem
        return realpath + "/base/categories/applications-system.png"

class Apps(object):
    def __init__(self, apps_browser="", desktop_browser=""):
        self.count_cat = 0
        self.ICON_THEME = gtk.IconTheme.get_default()
        self.count = 0
        self.count_cat = 0 

    def get_category(self):
        Icon_Parser = IconParser()
        # this function find categories whith help of module xdg
        liste = []
        ICON_THEME = gtk.IconTheme.get_default()
        try:
            xdgmenu = Menu.parse('hybryde.menu')
        except:
            xdgmenu = Menu.parse('applications.menu')
        for entry in xdgmenu.getEntries():
            if isinstance(entry, Menu.Menu):
                name = entry.getName()
                icon = Icon_Parser.findicon(entry.getIcon())
                if not icon:
                    icon = realpath + "/base/categories/applications-system.png"
                liste.append([name, icon, entry])
        return liste

    def get_apps(self, category):
        # this find apps associated on the category give on argument
        if category:
            try:
                xdgmenu = Menu.parse('hybryde.menu')
            except:
                xdgmenu = Menu.parse('applications.menu')
            apps_liste = []
            for entry in xdgmenu.getEntries():
                print entry
                print category
                
                if isinstance(entry, Menu.Menu) and entry == category:
                    for element in entry.getEntries():
                        try:
                            element_entry = element.DesktopEntry
                            command = element_entry.getExec().split('-caption')[0].split('%')[0]
                            apps_liste.append({'name': element_entry.getName(),
                                               'icon': element_entry.getIcon(),
                                               'command': command,
                                               'comment': element_entry.getComment(),
                                               'filename': element_entry.filename})
                        except:
                            pass
            return apps_liste
