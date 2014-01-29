#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "Olivier LARRIEU"
__version__ = "0.1"

import os
from gi.repository import Gtk
from gi.repository import GLib

from HydvCore import Hydv_Listner, Hydv_Screen_Utils
from HydvCore import HydvWidgets
HydvWidgets = HydvWidgets()
from Apps.MenuBar import MenuBarBus
import gui
import dbus
import time
realpath = GLib.get_current_dir()

class MenuBar_Actions():
    """ ================================== """
    """ All MenuBar actions goes here only """
    """ ================================== """
        
    def leave(self):
        self.BusService.stop()
        Gtk.main_quit()

    def open_appswindow(self):
        bus = dbus.SessionBus()
        bus_service = bus.get_object('org.hydv2.appswindow', '/org/hydv2/appswindow')
        print self.appswindowstate
        if not self.appswindowstate:
            show = bus_service.get_dbus_method('show', 'org.hydv2.appswindow')
            self.appswindowstate = True
        else:
            show = bus_service.get_dbus_method('hide', 'org.hydv2.appswindow')
            self.appswindowstate = False

        screen_height = self.Hydv_Screen_Utils.get_screen_height()
        y_position = screen_height - self.height
        show(0, y_position)
        
    def bottom_position(self):
        screen_height = self.Hydv_Screen_Utils.get_screen_height()
        y_position = screen_height - self.height
        self.Window.move(0, y_position)
        self.screen_position = "bottom"

    def top_position(self):
        self.Window.move(0, 0)
        self.screen_position = "top"

    def open_shutdow(self):       
        self.stage6.slide(2000, 1, 0)

    def close_shutdow(self):
        self.stage6.slide(2000, 1, -500)

    def openall(self):
        self.stage2.slide(2000, 1, -0)

    def closeall(self):
        
        self.stage2.slide(2000, 1, -330)

    def open_nautilus(self):
        os.system('nautilus &')
        return True

    def slide_init(self):
        self.closeall()
        self.stage3.slide(2000, 1, -330)
        self.stage4.slide(2000, 1, -300)

    def slide_next(self):
        self.closeall()
        self.stage3.slide(2000, 1, -self.width)
        self.stage4.slide(2000, 1, -self.width)
        
        
class MenuBar(object, Hydv_Listner, MenuBar_Actions):
    """ =========================== """
    """ MenuBar Element Constructor """
    """ =========================== """
    def __init__(self):
        
        """ initialise the Window with the embeded webview """
        self.is_init = False
        self.root_container = False
        self.appswindowstate = False
        self.Hydv_Screen_Utils = Hydv_Screen_Utils()
        self.width = self.Hydv_Screen_Utils.get_screen_width()
        self.height = 30
        html_file = realpath + "/Apps/MenuBar/index.html"
        self.type_hint = 6
        self.is_above = True
        self.window_title = 'MenuBar'
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

        #=== self.javascript is an alias to : self.Window.view.execute_script ===#
        #=== self.javascript execute javascript code evaluate by the view =======#
        self.javascript = getattr(self.Window.view, "execute_script")

        #=== Each Hydv Window has its own communication bus
        #GLib.timeout_add(400, MenuBarBus.BusService, self.Window)
        self.BusService = MenuBarBus.Service(self.Window)
        self.BusService.start()
        #=== Start the AppsWindow
    def on_view_init(self, action):
        """ Override from Hydv_Listner.on_view_init """
        """ Action here are executed on the View initialisation only """
        # Create the Root container
        self.create_root_container(self.width, self.height)

        self.create_menu_buttons()
        self.create_option_buttons()
        self.create_principal_bar()
        self.create_second_bar()
        self.slide_init()

#======================================= TESTING FUNCTIONS ===================#        
    def create_root_container(self, width, height):
        """ Each hydv window need a root container """
        self.javascript('Tools.Create_root_container("'+str(width)+'","'+str(height)+'");')
        self.root_container = True

    def create_principal_bar(self):
        self.stage3 = HydvWidgets.Hydv_Stage(self.javascript, self.width-self.stage1.width-20, self.height, 800, "stage")
        self.button_test = HydvWidgets.Hydv_Button(self.javascript , "apps", 100, 20, "btn")
        self.button_test.onclick('self.slide_next()')
        self.stage3.add(self.button_test)

    def create_second_bar(self):
        self.stage4 = HydvWidgets.Hydv_Stage(self.javascript, self.width-self.stage1.width, self.height, 800, "stage")
        for i in range(10):
            button_test2 = HydvWidgets.Hydv_Button(self.javascript , "apps"+str(i), 50, 20, "btn")
            button_test2.onclick('self.slide_init()')
            self.stage4.add(button_test2)

    def create_menu_buttons(self):
        self.stage1 = HydvWidgets.Hydv_Stage(self.javascript, 330, self.height, 1000, "left_stage")
        self.button_application = HydvWidgets.Hydv_Button(self.javascript , "apps", 100, 20, "btn")
        self.button_application.onclick('self.open_appswindow()')

        self.button_magic = HydvWidgets.Hydv_Button(self.javascript, "magic", 100, 20, "btn")
        self.button_magic.onclick('self.slide_next()')
        #self.button_magic.onmouseover('self.openall()')
        #self.button_magic.onmouseout('self.closeall()')
        self.button_hybryde = HydvWidgets.Hydv_Button(self.javascript, "hybryde", 100, 20, "btn")
        self.button_hybryde.onclick('self.openall()')

        self.stage1.add(self.button_application)
        self.stage1.add(self.button_magic)
        self.stage1.add(self.button_hybryde)

    def create_option_buttons(self):
        self.stage2 = HydvWidgets.Hydv_Stage(self.javascript, 350, self.height, 900, "left_stage")

        self.button_logout = HydvWidgets.Hydv_Button(self.javascript, "logout", 50, 20, "btn")
        self.button_logout.onclick('self.leave()')

        self.button_shutdown = HydvWidgets.Hydv_Button(self.javascript, "shutdown", 50, 20, "btn")
        self.button_shutdown.onclick('self.leave()')

        self.button_reboot = HydvWidgets.Hydv_Button(self.javascript, "reboot", 50, 20, "btn")
        self.button_reboot.onclick('self.leave()')

        self.button_sleep = HydvWidgets.Hydv_Button(self.javascript, "sleep", 50, 20, "btn")
        self.button_sleep.onclick('self.leave()')

        self.button_close = HydvWidgets.Hydv_Button(self.javascript, "sleep", 50, 20, "btn")
        self.button_close.onclick('self.leave()')

        self.stage2.add(self.button_logout)
        self.stage2.add(self.button_shutdown)
        self.stage2.add(self.button_reboot)        
        self.stage2.add(self.button_sleep)
        self.stage2.add(self.button_close)
        

