#!/usr/bin/env python
# -*- coding:utf-8 -*-

from gi.repository import Gtk, Gdk
from gi.repository import GLib
from HydvCore import *
import gui
import os
screen_x , screen_y = Gdk.Screen.width(), Gdk.Screen.height()
realpath = GLib.get_current_dir()

class MenuBar_Actions():
    """ ================================== """
    """ All MenuBar actions goes here only """
    """ ================================== """

    def open_dash(self):
        self.create_button(self.open_dash, str(self.button_counter))
        self.button_counter += 1   

    def open_nautilus(self):
        os.system('nautilus &')
        return True

class MenuBar(object, Hydv_Listner, MenuBar_Actions, Hydv_Javascript_Tools):
    """ =========================== """
    """ MenuBar Element Constructor """
    """ =========================== """
    def __init__(self):
        
        """ initialise the Window with the embeded webview """
        self.is_init = False
        self.root_container = False
        
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

    def on_view_init(self, action):
        """ Override from Hydv_Listner.on_view_init """
        """ Action here are executed on the View initialisation only """
        # Create the Root container
        self.create_root_container()
        #self.create_button('self.leave()', "Leave", "root_container")
        self.stage3 = Hydv_Stage(self.javascript, 110, self.height, "stage3", 1000, "stage_with_bg")
        self.stage4 = Hydv_Stage(self.javascript, 110, self.height, "stage4", 900, "stage_with_bg")
        self.stage5 = Hydv_Stage(self.javascript, 110, self.height, "stage5", 800, "left_stage")
        self.stage6 = Hydv_Stage(self.javascript, 550, self.height, "stage6", 700, "left_stage")
        self.stage1 = Hydv_Stage(self.javascript, self.width-380, self.height, "stage1", 500, "stage")
        self.stage2 = Hydv_Stage(self.javascript, self.width-380, self.height, "stage2", 500, "stage")

        
        self.create_button('self.openall()', "logout", self.stage6.stage_id)
        self.create_button('self.openall()', "<- reboot", self.stage6.stage_id)
        self.create_button('self.openall()', "<- shutdow", self.stage6.stage_id)
        self.create_button('self.close_shutdow()', "<- sleep", self.stage6.stage_id)
        self.create_button('self.open_shutdow()', "<- sleep", self.stage6.stage_id)
        self.create_menu_buttons()
        self.create_button('self.openall()', "<- Retour", self.stage2.stage_id)
        self.create_button('self.closeall()', "Applications", self.stage3.stage_id)
        self.create_button('self.closeall()', "Magic", self.stage4.stage_id)
        self.close_shutdow()
        self.stage1.slide(2000, 1, -500)

    def create_root_container(self):
        """ Each hydv window need a root container """
        self.javascript('Tools.Create_root_container();')
        self.root_container = True

    def create_menu_buttons(self):
        self.create_button('self.closeall()', "Options", self.stage5.stage_id)
        self.create_button('self.bottom_position()', "Bottom", self.stage2.stage_id)
        self.create_button('self.top_position()', "Top", self.stage2.stage_id)
        self.create_button('self.leave()', "Leave", self.stage2.stage_id)

    def leave(self):
        Gtk.main_quit()

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
        self.stage1.slide(2000, 1, -500)
        self.stage2.slide(2000, 1, self.width)

    def closeall(self):
        self.close_shutdow()
        
        self.stage1.slide(2000, 1, -830)
        self.stage2.slide(2000, 1, -self.width-120)
        

