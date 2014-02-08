#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import locale
from gi.repository import GLib
realpath = GLib.get_current_dir()

class HydvDesktopEntries(object):
    """
    Return a dictionnary with applications categories
    Is not based on XDG but stay soft and quick.
    """
    @classmethod
    def display_all(cls):
        tot_applications = 0
        apps = HydvDesktopEntries.get_applications()
        keys = apps.keys()
        for k in keys:
            tot_applications += len(apps[k])
            print "========================================================="
            print "Category :", k, str(len(apps[k]))
            for app in apps[k]:
                print "    -", app['name']
        print "========================================================="
        print "Total categories :", str(len(apps))
        print "Total applications :", str(tot_applications)

    @classmethod
    def get_applications(self):
        language = locale.getdefaultlocale()[0][0:2]
        CATEGORIES_DIC = {'AudioVideo': [],
                         'Network': ['X-GNOME-NetworkSettings',],
                         'Office':['Development',],
                         'Settings': [],
                         'System':['PackageManager','Security', 'Qt',],
                         'Application':['Emulator', 'Core', 'Utility',],
                         'Game': [],
                         'Graphics': [],
                         'Wine': ['Wine-Programs-Accessories',],
                         }

        dir_list = os.listdir('/usr/share/applications')
        dic = {}
        nodisplay = False
        command = False
        for desktop_file in dir_list:
            if desktop_file.split('.')[1] == "desktop":
                applications_dic = {}
                file_content = open('/usr/share/applications/'+desktop_file, 'r').readlines()
                for line in file_content:
                    # get application name
                    if "Name" in line and not "TypeName" in line and not "GenericName" in line :
                        if not 'name' in applications_dic:
                            applications_dic['name'] = line.split('=')[1].replace('\n','')
                    # get application command
                    if "Exec" in line:
                        command = True
                        applications_dic['command'] = line.split('=')[1].replace('\n','').split('%')[0]
                    # get application icon
                    if "Icon" in line:
                        icon = HydvDesktopEntries.findicon(line.split('=')[1].replace('\n',''))
                        applications_dic['icon'] = icon
                    # get application comment
                    if "Comment[%s]"%language in line:
                        applications_dic['comment'] = line.split('=')[1].replace('\n','')
                    if "Categories" in line:
                        category = line.replace('GNOME;','').replace('GTK;','').replace('\n','').split('=')[1].split(';')[0]
                        # get category directory                       
                    if "NoDisplay=true" in line:
                        nodisplay = True
                # Add application utils infos in category dic corresponding
                if command:
                    if not nodisplay:
                        applications_dic['desktopentry'] = desktop_file
                        for cat in CATEGORIES_DIC:
                            if category in CATEGORIES_DIC[cat]:
                                category = cat
                        if not category in dic:
                            dic[category] = []                        
                        dic[category].append({applications_dic['name']:applications_dic, })
                    else:
                        nodisplay = False
                    command = False
        return dic

    @classmethod
    def findicon(cls, icon_name):
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
                
