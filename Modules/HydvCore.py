#!/usr/bin/env python
# -*- coding:utf-8 -*-
from gi.repository import Gtk, Gdk

class Hydv_Screen_Utils(object):
    """ ============================================================== """
    """ Class generic                                                  """
    """ ============================================================== """
    def get_screen_width(self):
        screen = Gdk.Screen.get_default()
        screen_width = screen.get_width()
        return screen_width

    def get_screen_height(self):
        screen = Gdk.Screen.get_default()
        screen_height = screen.get_height()
        return screen_height

    def get_n_monitors(self):
        screen = Gdk.Screen.get_default()
        monitor_number = screen.get_n_monitors()
        return monitor_number

class Hydv_Listner():
    """ ============================================================== """
    """ Class generic                                                  """
    """ listen for javascript event and evaluate the action            """
    """ the action is a method or function existing in a module Action """
    """ Each view is connected to its own Hydv_Listner """
    """ ============================================================== """
    def view_init(self, action):
        """ Initialisation of the View """
        if action == "init" and self.is_init == False:
            self.is_init = True
            self.on_view_init(action)
            return True

    def evaluate_action(self, action):
        # Interpret action from javascript
        print action
        try:
            method = eval(action)
            method()
            return True
        except:
            return False

    def Actions(self, widget, frame, action):
        """ Connector for a View to listen javascript events. """
        if action != "_":
            # First initialisation of the view
            if not self.is_init:
                self.view_init(action)
            else:
                self.evaluate_action(action)                



class Hydv_Stage(object):
    """ ============================================================== """
    """ A stage is a container for embed application in HydvWindow     """
    """ A window may have more than one stage.                         """
    """ ============================================================== """
    def __init__(self, javascript_context, width, height, number, zindex, classname):
        self.width = width
        self.height = height
        self.zindex = str(zindex)
        self.classname = classname
        self.stage_id = "stage_" + str(number)
        self.javascript = javascript_context
        self._create_stage()

    def _create_stage(self):
        self.javascript('Tools.Create_stage("' + str(self.width)
                                               + '","' 
                                               + str(self.height)
                                               + '","'
                                               + self.stage_id
                                               + '","'
                                               + self.zindex
                                               + '","'
                                               + self.classname + '");')

    def slide(self, speed, direction, position):
        self.javascript('Tools.slide_stage("'+ self.stage_id +'","'+ str(speed) +'","' + str(direction) +'","' + str(position) + '");')

    def fadeIn(self):
        self.javascript('Tools.fadeIn_stage("'+ self.stage_id +'");')

    def fadeOut(self):
        self.javascript('Tools.fadeOut_stage("'+ self.stage_id +'");')
        
    def hide(self):
        self.javascript('Tools.hide_stage("'+ self.stage_id +'");')
    
    def show(self):
        self.javascript('Tools.show_stage("'+ self.stage_id +'");')        

class Hydv_Javascript_Tools():
    """ ============================================================== """
    """ Tools are shortcuts to create and embed widget in stage or     """
    """ root_container                                                 """
    """ ============================================================== """

    def create_button(self, function, text, destination_id):
        """
            Action is the direct reference to the function which will be call
            on the sending signal.
        """
        self.javascript('Tools.Create_Button("'+function+'","'+text+'","btn","'+destination_id+'");')

    def create_button_fixed(self, function, text, destination_id):
        """
            Action is the direct reference to the function which will be call
            on the sending signal.
        """
        self.javascript('Tools.Create_Button_Fixed("'+function+'","'+text+'","btn","'+destination_id+'");')


