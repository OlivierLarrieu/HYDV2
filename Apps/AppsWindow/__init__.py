#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "Olivier LARRIEU"
__version__ = "0.1"

import os
from gi.repository import Gtk
from gi.repository import GLib

from HydvCore import Hydv_Listner, Hydv_Screen_Utils, Hydv_Stage, Hydv_Button, Hydv_Div, Hydv_Icon
from Apps.AppsWindow import AppsWindowBus

import AppsManager
import gui


realpath = GLib.get_current_dir()

class AppsWindow_Actions():
    """ ================================== """
    """ All AppsWindow actions goes here only """
    """ ================================== """
    def leave(self):
        Gtk.main_quit()

    def show_category(self, category):
        print category
        self.javascript('$(".apps_button").hide()')
        self.javascript('$(".'+category+'").fadeIn()')
        
    def launch_command(self, command):
        print "here"
        os.system(command+" &")

    def bottom_position(self):
        screen_height = self.Hydv_Screen_Utils.get_screen_height()
        y_position = screen_height - 60
        self.Window.move(0, 600)
        self.screen_position = "bottom"""

    def top_position(self):
        self.Window.move(0, 0)
        self.screen_position = "top"


    def open_nautilus(self):
        os.system('nautilus &')
        return True

    def slide_init(self):
        self.javascript('$("#stage_1").fadeIn(200)')
        #self.stage_principal.slide(2000, 1, 0)
        #self.stage2.slide(2000, 1, 0)

    def slide_next(self):
        self.javascript('$("#stage_1").fadeOut(100)')
        #self.stage_principal.slide(2000, 1, -self.width)
        #self.stage2.slide(2000, 1, -self.width)
    
class AppsWindow(object, Hydv_Listner, AppsWindow_Actions):
    """ =========================== """
    """ AppsWindow Element Constructor """
    """ =========================== """
    def __init__(self):
        
        """ initialise the Window with the embeded webview """
        self.is_init = False
        self.root_container = False
        
        self.Hydv_Screen_Utils = Hydv_Screen_Utils()
        self.width = 330
        self.height = 400
        html_file = realpath + "/Apps/AppsWindow/index.html"
        self.type_hint = 6
        self.is_above = True
        self.window_title = 'AppsWindow'
        # Construct the window
        self.Window = gui.HyWindow(self.width,
                                   self.height,
                                   html_file,
                                   self.Actions, # Connecte the view signal to this Method
                                   self.type_hint,
                                   self.is_above,
                                   self.window_title)
        # Move the window
        self.bottom_position()
        self.Window.hide()
        #=== self.javascript is an alias to : self.Window.view.execute_script ===#
        #=== self.javascript execute javascript code evaluate by the view =======#
        self.javascript = getattr(self.Window.view, "execute_script")

        #=== Each Hydv Window has its own communication bus
        #GLib.timeout_add(400, AppsWindowBus.BusService, self.Window)
        self.BusService = AppsWindowBus.Service(self.Window)
        self.BusService.start()

    def on_view_init(self, action):
        """ Override from Hydv_Listner.on_view_init """
        """ Action here are executed on the View initialisation only """
        # Create the Root container

        
        self.create_root_container(self.width, self.height)
        self.javascript('Tools.Create_Header()')
        self.javascript('Tools.Create_Footer()')

        self.stage_principal = Hydv_Stage(self.javascript, self.width-11, self.height-40, 1, 800, "black_stage")
        self.stage = Hydv_Stage(self.javascript, "98%", 225, 2, 800, "stage")
        counter = 0
        for cat in self.load_categories():        
            button = Hydv_Button(self.javascript , cat[0], 100, 20, counter, "btn")
            button.onclick("self.show_category('cat_%s')"%counter)
            self.stage_principal.add(button)
            
        
            category_indice = counter
            for i in self.load_apps(cat[0]):
                print 'category_indice',"apps_button cat_%s"%category_indice
                self.div_1 = Hydv_Div(self.javascript , "", "96%", 30, counter, "apps_button cat_%s"%category_indice)
                self.div = Hydv_Div(self.javascript , "%s"%i['name'], "", "", counter+1*100, "")
                #print i['icon']
                find_icon = AppsManager.IconParser()
                icon = find_icon.findicon(i['icon'])

                icon = Hydv_Icon(self.javascript, 30, 30, counter, icon, "")
                self.div_1.add(icon)
                self.div_1.add(self.div)
                self.div_1.onclick("self.launch_command('%s')"%i['command'])
                self.stage.add(self.div_1)
                counter += 1

        self.stage_principal.add(self.stage)
        self.stage_down = Hydv_Stage(self.javascript, "34%", 35, 15, 800, "black_stage")
        self.stage_down2 = Hydv_Stage(self.javascript, "60%", 50, 16, 800, "stage")
        button = Hydv_Button(self.javascript , "next", 100, 24, counter+1, "btn")
        button.onclick("self.slide_next()")
        self.stage_down.add(button)
        self.stage_principal.add(self.stage_down2)
        self.stage_principal.add(self.stage_down)
        self.stage2 = Hydv_Stage(self.javascript, self.width, self.height, 3, 800, "black_stage")
        self.button_test2 = Hydv_Button(self.javascript , "apps", 100, 20, 10, "btn")
        self.button_test2.onclick('self.slide_init()')
        self.stage2.add(self.button_test2)
    def create_root_container(self, width, height):
        """ Each hydv window need a root container """
        self.javascript('Tools.Create_root_container("'+str(width)+'","'+str(height)+'");')
        self.root_container = True

    def load_categories(self):
        applications_instance = AppsManager.Apps()
        return applications_instance.get_category()

    def load_apps(self, category):
        applications_instance = AppsManager.Apps()
        return applications_instance.get_apps(category)
