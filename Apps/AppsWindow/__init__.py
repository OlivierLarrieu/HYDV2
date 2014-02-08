#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "Olivier LARRIEU"
__version__ = "0.1"

import os
from gi.repository import Gtk
from gi.repository import GLib

import HydvWindow
from HydvCore import HydvWidgets
from HydvCore import Hydv_Listner, Hydv_Screen_Utils
from Apps.AppsWindow import AppsWindowBus

GLib.threads_init()
realpath = GLib.get_current_dir()

class AppsWindow_Actions():
    """ ================================== """
    """ All AppsWindow actions goes here only """
    """ ================================== """
    def leave(self):
        Gtk.main_quit()

    def bottom_position(self):
        screen_height = Hydv_Screen_Utils.get_screen_height()
        y_position = screen_height - self.height - 60
        self.Window.move(0, y_position)
        self.screen_position = "bottom"""

    def top_position(self):
        self.Window.move(0, 0)
        self.screen_position = "top"

    def slide_init(self):
        self.javascript('$("#stage_1").fadeIn(200)')

    def slide_next(self):
        self.javascript('$("#stage_1").fadeOut(200)')
    
class AppsWindow(object, AppsWindow_Actions):
    """ =========================== """
    """ AppsWindow Element Constructor """
    """ =========================== """
    def __init__(self):
        
        """ initialise the Window with the embeded webview """
        self.is_init = False
        self.root_container = False
        self.HydvWidgets = HydvWidgets()
        self.width = 330
        self.height = 400
        html_file = realpath + "/Apps/AppsWindow/index.html"
        self.type_hint = 6
        self.is_above = True
        self.window_title = 'AppsWindow'
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
        self.Window.hide()
        #=== self.javascript is an alias to : self.Window.view.execute_script ===#
        #=== self.javascript execute javascript code evaluate by the view =======#
        self.javascript = getattr(self.Window.view, "execute_script")

        #=== Each Hydv Window has its own communication bus
        self.BusService = AppsWindowBus.Service(self.Window)
        self.BusService.start()

        
    def on_view_init(self, action):
        """ Override from Hydv_Listner.on_view_init """
        """ Action here are executed on the View initialisation only """
        # Create the Root container        
        self.create_root_container(self.width, self.height)
        # Header
        self.header = self.HydvWidgets.Hydv_Header(self.javascript)
        # Footer
        self.footer = self.HydvWidgets.Hydv_Footer(self.javascript)
        from Stages import Applications
        stage = Applications.Stage(self)
        from Stages import SysInfos
        sysinfo = SysInfos.Stage(self)
        #self.Window.show_all()

    def create_root_container(self, width, height):
        """ Each hydv window need a root container """
        self.javascript('Tools.Create_root_container("'+str(width)+'","'+str(height)+'");')
        self.root_container = True
