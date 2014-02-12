#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "Olivier LARRIEU"
__version__ = "0.1"

import os
import dbus
import time
import HydvWindow
from gi.repository import Gtk
from gi.repository import GLib

from HydvCore import Hydv_Listner, Hydv_Screen_Utils
from HydvCore import HydvWidgets
from Apps.MenuBar import MenuBarBus


realpath = GLib.get_current_dir()
print realpath
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
        
        self.logout_stage.slide(2000, 1, -330)

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
        
        
class MenuBar(object, MenuBar_Actions):
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
        self.Window = HydvWindow.HyWindow(self,
                                   self.width,
                                   self.height,
                                   html_file,
                                   Hydv_Listner.Actions, # Connecte the view signal to this Method
                                   self.type_hint,
                                   self.is_above,
                                   self.window_title)
        # Move the window
        self.bottom_position()

        #=== self.javascript is an alias to : self.Window.view.execute_script ===#
        #=== self.javascript execute javascript code evaluate by the view =======#
        self.javascript = getattr(self.Window.view, "execute_script")
        #=== self.HydvWidgets_instance = self.HydvWidgets_instance() is the widget controller
        #=== it is usefull to instanciate it with the javascript context
        self.HydvWidgets_instance = HydvWidgets(self.javascript)
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
        self.create_menu_stage()
        self.create_logout_stage()
        self.create_principal_bar()
        self.create_second_bar()
        self.slide_init()
        self.Window.show_all()
#======================================= TESTING FUNCTIONS ===================#        
    def create_root_container(self, width, height):
        """ Each hydv window need a root container """
        self.javascript('Tools.Create_root_container("'+str(width)+'","'+str(height)+'");')
        self.root_container = True

    def create_principal_bar(self):
        self.stage3 = self.HydvWidgets_instance.Hydv_Stage(width=self.width-self.button_stage.width-20,
                                                           height=self.height,
                                                           zindex=800,
                                                           classname="stage")
        self.button_test = self.HydvWidgets_instance.Hydv_Button(text="apps",
                                                                 width=100,
                                                                 height=20,
                                                                 classname="btn")
        self.button_test.onclick('slide_next')
        self.stage3.add(self.button_test)

    def create_second_bar(self):
        self.stage4 = self.HydvWidgets_instance.Hydv_Stage(width=self.width-self.button_stage.width,
                                                           height=self.height,
                                                           zindex=800,
                                                           classname="stage")
        for i in range(10):
            button_test2 = self.HydvWidgets_instance.Hydv_Button(text="apps"+str(i),
                                                                 width=50,
                                                                 height=20,
                                                                 classname="btn")
            button_test2.onclick('slide_init')
            self.stage4.add(button_test2)

    def create_menu_stage(self):
        self.button_stage = self.HydvWidgets_instance.Hydv_Stage(width=330,
                                                                 height=self.height,
                                                                 zindex=1000,
                                                                 classname="left_stage")
        self.button_application = self.HydvWidgets_instance.Hydv_Icon(width=self.height,
                                                                      height=self.height, 
                                                                      path=realpath + '/Apps/AppsWindow/medias/icons/add.png',
                                                                      classname="menu_button")

        self.button_application.onclick('open_appswindow')
        self.button_stage.add(self.button_application)

    def create_logout_stage(self):
        self.logout_stage = self.HydvWidgets_instance.Hydv_Stage(width=350, height=self.height, zindex=900, classname="left_stage")
        
        self.button_logout = self.HydvWidgets_instance.Hydv_Button(text="logout", width=50, height=20, classname="btn")
        self.button_logout.onclick('leave')

        self.button_shutdown = self.HydvWidgets_instance.Hydv_Button(text="shutdown", width=50, height=20, classname="btn")
        self.button_shutdown.onclick('leave')

        self.button_reboot = self.HydvWidgets_instance.Hydv_Button(text="reboot", width=50, height=20, classname="btn")
        self.button_reboot.onclick('leave')

        self.button_sleep = self.HydvWidgets_instance.Hydv_Button(text="sleep", width=50, height=20, classname="btn")
        self.button_sleep.onclick('leave')

        self.button_close = self.HydvWidgets_instance.Hydv_Button(text="sleep", width=50, height=20, classname="btn")
        self.button_close.onclick('leave')

        self.logout_stage.add(self.button_logout)
        self.logout_stage.add(self.button_shutdown)
        self.logout_stage.add(self.button_reboot)        
        self.logout_stage.add(self.button_sleep)
        self.logout_stage.add(self.button_close)
        

