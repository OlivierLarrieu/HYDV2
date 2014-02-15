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
        show(0,self.height)

    def slide_next(self):
        self.Window.javascript('$("#%s").hide();alert()'%self.principal_bar.id)
        
    def open_logout_stage(self):
        print self.logout
        if self.logout:
            self.logout_stage.animate(direction="left", px=-1000, speed=400, delay=0)
            self.logout = False
        else:
            self.logout_stage.animate(direction="left", px=0, speed=400, delay=0)
            self.logout = True

    def launch_command(self, command):
        os.system(command+" &")

    def add_fav_app(self, app, command):
        apps_button = self.HydvWidgets_instance.Hydv_Button(text="",
                                                              width=25,
                                                              height=25,
                                                              classname="fav_app")
        apps_button.onclick("launch_command('%s')"%command)
        add_icon = self.HydvWidgets_instance.Hydv_Icon(width=25,
                                                     height=25,
                                                     path=app,
                                                     classname="")
        apps_button.add(add_icon)
        self.principal_bar.add(apps_button)
            
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

        self.Window = HydvWindow.HyWindow(caller_instance=self,
                                          width=self.width,
                                          height=self.height,
                                          type_hint=6,
                                          is_above=True,
                                          title='MenuBar')

        # Move the window
        #self.bottom_position()
        
        self.javascript = self.Window.javascript
        self.HydvWidgets_instance = self.Window.HydvWidgets_instance

        self.BusService = MenuBarBus.Service(self)
        self.BusService.start()
        #=== Start the AppsWindow

    def on_view_init(self, action):
        """ Override from Hydv_Listner.on_view_init """
        """ Action here are executed on the View initialisation only """
        # Create the Root container
        self.Window.view.create_root_container()
        self.menu_stage = self.create_menu_stage()
        self.logout_stage = self.create_logout_stage()
        self.principal_bar = self.create_principal_bar()
        self.second_bar = self.create_second_bar()       
        self.Window.show_all()
#======================================= TESTING FUNCTIONS ===================#        
    def create_menu_stage(self):
        stage = self.HydvWidgets_instance.Hydv_Stage(width=331,
                                                                 height=self.height,
                                                                 zindex=1000,
                                                                 classname="left_stage")
        button_application = self.HydvWidgets_instance.Hydv_Div(width=100, height=20, text="Menu", classname="btn")
        button_application.onclick('open_appswindow')
        stage.add(button_application)
        spacer = self.HydvWidgets_instance.Hydv_Div(width=190, height=20, text="", classname="")

        stage.add(spacer)
        button_logout = self.HydvWidgets_instance.Hydv_Button(text="",
                                                                 width=20,
                                                                 height=20,
                                                                 classname="btn")
        button_logout.onclick('open_logout_stage')
        stage.add(button_logout)
        return stage

    def create_logout_stage(self):
        self.logout = False
        stage = self.HydvWidgets_instance.Hydv_Stage(width=350, height=self.height, zindex=900, classname="left_stage")
        
        button_logout = self.HydvWidgets_instance.Hydv_Button(text="logout", width=70, height=20, classname="btn")
        button_logout.onclick('leave')

        button_shutdown = self.HydvWidgets_instance.Hydv_Button(text="shutdown", width=70, height=20, classname="btn")
        button_shutdown.onclick('leave')

        button_reboot = self.HydvWidgets_instance.Hydv_Button(text="reboot", width=70, height=20, classname="btn")
        button_reboot.onclick('leave')

        button_sleep = self.HydvWidgets_instance.Hydv_Button(text="sleep", width=70, height=20, classname="btn")
        button_sleep.onclick('leave')

        spacer = self.HydvWidgets_instance.Hydv_Div(width=10, height=20, text="", classname="")
        stage.add(spacer)
        stage.add(button_logout)
        stage.add(button_shutdown)
        stage.add(button_reboot)        
        stage.add(button_sleep)
        stage.animate(direction="left", px=-350, speed=200, delay=0)
        return stage

    def create_principal_bar(self):
        stage = self.HydvWidgets_instance.Hydv_Stage(width=self.width-self.menu_stage.width-20,
                                                           height=self.height,
                                                           zindex=800,
                                                           classname="stage")
        stage.animate(direction="left", px=-self.logout_stage.width, speed=200, delay=0)
        return stage
    def create_second_bar(self):
        stage = self.HydvWidgets_instance.Hydv_Stage(width=self.width-self.menu_stage.width,
                                                           height=self.height,
                                                           zindex=800,
                                                           classname="stage")
        for i in range(10):
            button= self.HydvWidgets_instance.Hydv_Button(text="apps"+str(i),
                                                                 width=50,
                                                                 height=20,
                                                                 classname="btn")
            button.onclick('slide_init')
            stage.add(button)
        return stage


        

