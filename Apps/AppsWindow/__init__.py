#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "Olivier LARRIEU"
__version__ = "0.1"

import os
import HydvWindow
from gi.repository import Gtk
from gi.repository import GLib
from HydvCore import HydvWidgets
from Apps.AppsWindow import AppsWindowBus
from HydvCore import Hydv_Listner, Hydv_Screen_Utils

GLib.threads_init()
realpath = GLib.get_current_dir()

class AppsWindow_Actions():
    """ ================================== """
    """ All AppsWindow actions goes here only """
    """ ================================== """
    def leave(self):
        Gtk.main_quit()

    def open_stage(self, stage_id):
        print "open", stage_id
        self.HydvWidgets_instance.open_stage(stage_id)
    
    def close_stage(self):
        print "close"
        self.HydvWidgets_instance.close_current_stage()
    
    def bottom_position(self):
        screen_height = Hydv_Screen_Utils.get_screen_height()
        y_position = screen_height - self.height - 60
        self.Window.move(0, y_position)
        self.screen_position = "bottom"""

    def top_position(self):
        self.Window.move(0, 0)
        self.screen_position = "top"

class AppsWindow(object, AppsWindow_Actions):
    """ =========================== """
    """ AppsWindow Element Constructor """
    """ =========================== """
    def __init__(self):        
        """ initialise the Window with the embeded webview """
        self.is_init = False
        self.root_container = False
        self.width = 330
        self.height = 400

        self.Window = HydvWindow.HyWindow(caller_instance=self,
                                          width=self.width,
                                          height=self.height,
                                          type_hint=6,
                                          is_above=True,
                                          title='AppsWindow')
        # Move the window
        self.bottom_position()
        self.Window.hide()

        self.javascript = self.Window.javascript
        self.HydvWidgets_instance = self.Window.HydvWidgets_instance

        #=== Each Hydv Window has its own communication bus
        self.BusService = AppsWindowBus.Service(self.Window)
        self.BusService.start()
       
    def on_view_init(self, action):
        """ Override from Hydv_Listner.on_view_init """
        """ Action here are executed on the View initialisation only """
        # Create the Root container
        self.Window.view.create_root_container()   
        #self.create_root_container(self.width, self.height)
        # Header
        self.header = self.HydvWidgets_instance.Hydv_Header()
        # Footer
        #self.footer = self.HydvWidgets_instance.Hydv_Footer()
        # Activate specific applications/stage embeded in applications window
        # TODO: use importlib for this with specifics controls
        from Stages import Applications
        self.application_stage = Applications.Stage(self)
        from Stages import SysInfos
        self.sysinfo_stage = SysInfos.Stage(self)


