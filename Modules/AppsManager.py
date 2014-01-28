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
#get user home
USER_DIR = GLib.get_home_dir()
realpath = GLib.get_current_dir()

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

class ControlDatabase(object):
    """
    put in sql database applications which are on the system
    control if database exist, if not create one.
    """
    def test_and_create(self):
        #control if cache directory exist
        if not os.path.isdir(USER_DIR + "/.cache/hybryde"):
            os.mkdir(USER_DIR + "/.cache/hybryde")
        #control if database exist
        if not os.path.isfile(USER_DIR + "/.cache/hybryde/HyAppsDatabase.db"):
            connection = Sqlite3.connect(USER_DIR
                                         + "/.cache/hybryde/HyAppsDatabase.db")
            cursor = connection.cursor()
            # Create table applications
            cursor.execute('''CREATE TABLE applications
                          (name text, 
                           command text,
                           icon text,
                           comment text,
                           categorie text,
                           filename text,
                           dash int,
                           visible int)''')
            # Create table app_diff
            # this table is usefull to control applications table integrity
            # at the start of hy desktop, this table is record and a diff is done
            # with application table in the InitDatas Class.
            cursor.execute('''CREATE TABLE app_diff
                          (filename text)''') 

            connection.commit()
            connection.close()
            print "database created ..."
        else:
            print "database found ..."

class InitDatas(object):
    def init(self):
        Icon_Parser = IconParser()
        ICON_THEME = gtk.IconTheme.get_default()
        connection = Sqlite3.connect(USER_DIR + "/.cache/hybryde/HyAppsDatabase.db")
        cursor = connection.cursor()
        apps_lister = Apps()
        categories = apps_lister.get_category()
        for cat in categories:
            apps_liste_current_categorie = apps_lister.get_apps(cat[2])        
            for apps in apps_liste_current_categorie:
                #add apps in applications table
                record = cursor.execute('SELECT name FROM applications WHERE name=:name',
                                        {"name": apps['name']}).fetchall()
                if not record:
                    icon = Icon_Parser.findicon(apps['icon'])
                    if not icon:
                        icon = "/usr/share/icons/skype.png"
                    #print "New record created..."
                    try:
                       comment = apps['comment']
                    except:
                       comment = "no comment..."
                    cursor.execute('INSERT INTO applications VALUES (:name,\
                                                                     :command,\
                                                                     :icon,\
                                                                     :comment,\
                                                                     :categorie,\
                                                                     :filename,\
                                                                     :dash,\
                                                                     :visible)',{
                                                                     "name": apps['name'],
                                                                     "command": apps['command'], 
                                                                     "icon": icon, 
                                                                     "comment": comment,
                                                                     "categorie": cat[2].getName(),
                                                                     "filename": apps['filename'],
                                                                     "dash": "0",
                                                                     "visible": "0"})
                #put the record "filename" in app_diff table
                cursor.execute('INSERT INTO app_diff VALUES (:filename)',
                               {"filename": apps['filename']})
        #when the loop is finish, we do the diff between "application" and "app_diff" AND DELETE
        cursor.execute('DELETE FROM applications \
                               WHERE filename NOT IN \
                               (SELECT filename FROM applications \
                                INTERSECT \
                                SELECT filename FROM app_diff)')
        #delete the app_diff table
        cursor.execute('DELETE FROM app_diff')
        connection.commit()
        connection.close()

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
                if isinstance(entry, Menu.Menu) and entry == category:
                    for element in entry.getEntries():
                        try:
                            element_entry = element.DesktopEntry
                            apps_liste.append({'name': element_entry.getName(),
                                               'icon': element_entry.getIcon(),
                                               'command': element_entry.getExec(),
                                               'comment': element_entry.getComment(),
                                               'filename': element_entry.filename})
                        except:
                            pass
            return apps_liste

    def get_apps_sorted_by_category(self, visible):
        # get the apps list about a category
        # if the app is visible or not
        connection = Sqlite3.connect(USER_DIR + "/.cache/hybryde/HyAppsDatabase.db")
        cursor = connection.cursor()    
        apps_list =  cursor.execute('SELECT * FROM applications\
                                     WHERE visible=:visible ORDER BY categorie ',
                                     {"visible": visible}).fetchall()
        categorie_list = self.get_category()
        connection.close()
        if apps_list:
            return [categorie_list, apps_list]
        else:
            return None

    def get_apps_sorted_by_category_all(self):
        # get all the apps list order by category
        connection = Sqlite3.connect(USER_DIR + "/.cache/hybryde/HyAppsDatabase.db")
        cursor = connection.cursor()    
        apps_list =  cursor.execute('SELECT * FROM applications ORDER BY categorie ').fetchall()
        categorie_list = self.get_category()
        connection.close()
        if apps_list:
            return [categorie_list, apps_list]
        else:
            return None

    def find_dash_apps(self, theme_path, desktop_browser):
        #find apps which must go in the dash
        connection = Sqlite3.connect(USER_DIR + "/.cache/hybryde/HyAppsDatabase.db")
        cursor = connection.cursor()    
        apps_list =  cursor.execute('SELECT * FROM applications WHERE dash=1').fetchall()
        if apps_list:
            indice = 0
            for app in apps_list:
                script = 'add_dash_apps("'+ str(indice) +'","\
                                         '+ app[2] +'","\
                                         '+ app[1].split('%')[0].split('--caption')[0] +'","\
                                         '+ theme_path +'","'+ app[5] + '","'+ app[0] +'")'
                desktop_browser.execute_script(script)
                indice += 1
        connection.close()

    def del_dash_apps(self, filename, desktop_browser):
        #delete app in the dash
        script = 'delete_dash_app("/usr/share/applications/'+filename+'")'
        desktop_browser.execute_script(script)

class AppsBrowser(object):
    def __init__(self, need_init=True):
        control_instance = ControlDatabase()
        if need_init:
            self.data_instance = InitDatas()
            #control if database exist
            control_instance.test_and_create()
            #initialize applications database
            self.data_instance.init()

    def madeappsview(self, browser, browser2):
        cat_indice = 0
        app_indice = 0
        all_cat = []
        last_cat = ""
        applications_instance = Apps()
        applications_and_categories_list = applications_instance.get_apps_sorted_by_category(0)
        categorie_list = applications_and_categories_list[0]
        applications_list = applications_and_categories_list[1] 
        browser.execute_script('document.getElementById("loading").style.visibility = "visible";')   
        for cat in categorie_list:
            if not cat in all_cat:
                all_cat.append(cat)
                GLib.idle_add(browser.execute_script,
                              'categorie_name = "'
                              + unicode.encode(cat[0],'utf_8').replace(' ','_') +'";')
                GLib.idle_add(browser.execute_script,
                             'icon = "' + cat[1] + '";')
                GLib.idle_add(browser.execute_script,
                             'indice = "' + str(cat_indice) + '";')
                GLib.idle_add(browser.execute_script,
                             'make_categories_places(categorie_name, icon, indice);')
                if cat != last_cat:
                    for app in applications_list:
                        icon = app[2]
                        command_split = app[1].split('%')[0].split('--caption')[0]
                        command = command_split.split('"')[0]
                        name = app[0]
                        filename = app[5]
                        comment = app[3]
                        if not comment:
                            comment = "No comment..."
                        if app[4] == cat[0] and app[2] != None:
                            GLib.idle_add(browser.execute_script, 
                                          'categorie = "' + unicode.encode(cat[0],'utf_8').replace(' ','_') + '";')
                            GLib.idle_add(browser.execute_script,
                                          'app_indice = "' + str(app_indice) + '";')
                            GLib.idle_add(browser.execute_script,
                                          'icon = "' + icon + '";')
                            GLib.idle_add(browser.execute_script,
                                          'command = "' + command + '";')
                            GLib.idle_add(browser.execute_script,
                                          'name = "' + name + '";')
                            GLib.idle_add(browser.execute_script,
                                          'filename = "' + filename + '";')
                            GLib.idle_add(browser.execute_script,
                                          'comment = "' + comment + '";')
                            GLib.idle_add(browser.execute_script,
                                          'add_app_in_apps_table(categorie,\
                                                                 icon,\
                                                                 command,\
                                                                 name,\
                                                                 app_indice,\
                                                                 filename,\
                                                                 comment);')
                            app_indice += 1
                    last_cat = cat
                cat_indice += 1
        GLib.idle_add(browser.execute_script,
                      'document.getElementById("loading").style.visibility = "hidden";')
        GLib.idle_add(browser2.execute_script,
                      'document.getElementById("Magic_button").style.visibility = "visible";')

    def madeappsview_all(self, browser):
        #this function is use by AppsFilter
        cat_indice = 0
        app_indice = 0
        last_cat = ""
        applications_instance = Apps()
        applications_and_categories_list = applications_instance.get_apps_sorted_by_category_all()
        categorie_list = applications_and_categories_list[0]
        applications_list = applications_and_categories_list[1]    
        for cat in categorie_list:
            browser.execute_script('categorie_name = "' + unicode.encode(cat[0],'utf_8').replace(' ','_') +'";')
            browser.execute_script('icon = "' + cat[1] + '";')
            browser.execute_script('indice = "' + str(cat_indice) + '";')
            browser.execute_script('make_categories_places(categorie_name, icon, indice);')
            if cat != last_cat:
                for app in applications_list:
                    icon = app[2]
                    command = app[1].split('%')[0].split('--caption')[0]
                    name = app[0]
                    filename = app[5]
                    comment = app[3]
                    visible = app[7]
                    if app[4] == cat[0] and app[2] != None:
                        browser.execute_script('categorie = "' + unicode.encode(cat[0],'utf_8').replace(' ','_')  + '";')
                        browser.execute_script('app_indice = "' + str(app_indice) + '";')
                        browser.execute_script('icon = "' + icon + '";')
                        browser.execute_script('command = "' + command + '";')
                        browser.execute_script('name = "' + name + '";')
                        browser.execute_script('filename = "' + filename + '";')
                        browser.execute_script('comment = "' + comment + '";')
                        browser.execute_script('visible = "' + str(visible) + '";')
                        browser.execute_script('add_app_in_apps_table_appsfilter(categorie, icon, command, name, app_indice, filename, comment, visible);')
                        app_indice += 1
                last_cat = cat
            cat_indice += 1
