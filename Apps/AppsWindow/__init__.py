#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "Olivier LARRIEU"
__version__ = "0.1"

import os
from gi.repository import Gtk
from gi.repository import GLib

from HydvCore import Hydv_Listner, Hydv_Screen_Utils, Hydv_Stage, Hydv_Button, Hydv_Div, Hydv_Icon
from Apps.AppsWindow import AppsWindowBus
import gui


realpath = GLib.get_current_dir()

class AppsWindow_Actions():
    """ ================================== """
    """ All AppsWindow actions goes here only """
    """ ================================== """
    def leave(self):
        Gtk.main_quit()

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
        self.stage.slide(2000, 1, 0)
        self.stage2.slide(2000, 1, 0)

    def slide_next(self):
        self.stage.slide(2000, 1, -self.width)
        self.stage2.slide(2000, 1, -self.width)
    
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
        cats = ['Accéssoires','Bureautiques','multimédia','internet','personnel','systeme','accés universel','Jeux','Autres']
        self.stage_principal = Hydv_Stage(self.javascript, self.width, self.height, 1, 800, "stage")
        counter = 0
        for cat in cats:
        
            button = Hydv_Button(self.javascript , cat, 100, 20, counter, "btn")
            button.onclick('self.slide_next()')
            self.stage_principal.add(button)
            counter += 1
        
        self.stage = Hydv_Stage(self.javascript, "95%", 230, 2, 800, "black_stage")
        for i in range(30):
            self.div = Hydv_Div(self.javascript , "div"+str(i), "45%", 50, i, "apps_button")
            icon = Hydv_Icon(self.javascript, 40, 40, i, "/usr/share/icons/oxygen/48x48/apps/accessories-calculator.png", "")
            self.div.add(icon)
            self.div.onclick('self.slide_next()')
            self.stage.add(self.div)
        self.stage_principal.add(self.stage)

        self.stage2 = Hydv_Stage(self.javascript, self.width, self.height, 3, 800, "stage")
        self.button_test2 = Hydv_Button(self.javascript , "apps", 100, 20, 10, "btn")
        self.button_test2.onclick('self.slide_init()')
        self.stage2.add(self.button_test2)
    def create_root_container(self, width, height):
        """ Each hydv window need a root container """
        self.javascript('Tools.Create_root_container("'+str(width)+'","'+str(height)+'");')
        self.root_container = True

