#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "Olivier LARRIEU"
__version__ = "0.1"
from HydvCore import Hydv_Listner
from HydvCore import HydvWidgets
HydvWidgets = HydvWidgets()
from AppsManager import Apps, IconParser
from xdg_test import HydvDesktopEntries
import os

class Stage_Actions():
    """ ================================== """
    """ All Stage actions goes here only """
    """ ================================== """
    def show_category(self, category):
        self.javascript('$(".apps_button").hide();$(".add").hide()')
        self.javascript('$(".'+category+'").fadeIn()')
        
    def launch_command(self, command):
        os.system(command+" &")


class Stage(object, Stage_Actions):
    def __init__(self, caller):
        print self
        self.javascript = caller.javascript
        # Stage principal
        self.stage_principal = caller.HydvWidgets.Hydv_Stage(self.javascript, caller.width, caller.height, 800, "stage")
        # Display categories icons
        self.stage_category = caller.HydvWidgets.Hydv_Stage(self.javascript, caller.width, 80, 800, "black_stage")
        # Display list off applications
        self.stage = caller.HydvWidgets.Hydv_Stage(self.javascript, "98%", 245, 700, "apps_button_stage")
        category_indice = 0
        Apps = HydvDesktopEntries.get_applications()
        keylist = Apps.keys()
        keylist.sort()
        for cat in keylist:        
            button = caller.HydvWidgets.Hydv_Button(self.javascript , "", 30, 30, "btn")
            icon = caller.HydvWidgets.Hydv_Icon(self.javascript, 30, 30, HydvDesktopEntries.findicon(Apps[cat]), "cat_icon")
            button.add(icon)
            button.onclick("show_category('cat_%s')"%category_indice)
            self.stage_category.add(button)
            t = Apps[cat]
            print t.sort()
            for i in t:
                self.div_1 = caller.HydvWidgets.Hydv_Div(self.javascript , "", "85%", 30, "apps_button cat_%s"%category_indice)
                self.div = caller.HydvWidgets.Hydv_Div(self.javascript , "%s"%i[i.keys()[0]]['name'], "85%", "", "")
                self.add = caller.HydvWidgets.Hydv_Div(self.javascript , "", "", "", "add cat_%s"%category_indice)
                

                icon = caller.HydvWidgets.Hydv_Icon(self.javascript, 30, 30, i[i.keys()[0]]['icon'], "")
                self.div_1.add(icon)
                self.div_1.add(self.div)
                self.div_1.onclick("launch_command('%s')"%i[i.keys()[0]]['command'])
                self.add.onclick("add_to_menubar('%s')"%i[i.keys()[0]]['icon'])
                self.stage.add(self.div_1)
                self.stage.add(self.add)
            category_indice += 1                
        self.stage_principal.add(self.stage_category )
        self.stage_principal.add(self.stage)        
        button = caller.HydvWidgets.Hydv_Button(self.javascript , "next", 50, 20, "btn")
        button.onclick("slide_next")
        caller.footer.add(button)
        
        caller.Window.view.connect("title-changed", Hydv_Listner.Actions, self)

    def load_categories(self):
        applications_instance = AppsManager.Apps()
        return applications_instance.get_category()

    def load_apps(self, category):
        applications_instance = AppsManager.Apps()
        return applications_instance.get_apps(category)


