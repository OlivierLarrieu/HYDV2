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

    def slide_init(self):
        self.javascript('$("#%s").fadeIn(200)'%self.application_stage.stage_principal.id)
        self.javascript('$("#%s").fadeOut(200)'%self.sysinfo_stage.stage_principal.id)

    def slide_next(self):
        self.javascript('$("#%s").fadeOut(200)'%self.application_stage.stage_principal.id)
        self.javascript('$("#%s").fadeIn(200)'%self.sysinfo_stage.stage_principal.id)
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
        self.HydvWidgets_instance = HydvWidgets(self.javascript)
        #=== Each Hydv Window has its own communication bus
        self.BusService = AppsWindowBus.Service(self.Window)
        self.BusService.start()

        
    def on_view_init(self, action):
        """ Override from Hydv_Listner.on_view_init """
        """ Action here are executed on the View initialisation only """
        # Create the Root container        
        self.create_root_container(self.width, self.height)
        # Header
        self.header = self.HydvWidgets_instance.Hydv_Header()
        # Footer
        self.footer = self.HydvWidgets_instance.Hydv_Footer()
        from Stages import Applications
        self.application_stage = Applications.Stage(self)
        from Stages import SysInfos
        self.sysinfo_stage = SysInfos.Stage(self)
        #self.Window.show_all()

    def create_root_container(self, width, height):
        """ Each hydv window need a root container """
        self.javascript('Tools.Create_root_container("'+str(width)+'","'+str(height)+'");')
        self.root_container = True
