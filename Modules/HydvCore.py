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
        self.id = "stage_" + str(number)
        self.javascript = javascript_context
        self._create_stage()

    def _create_stage(self):
        self.javascript('Tools.Create_stage("' + str(self.width)
                                               + '","' 
                                               + str(self.height)
                                               + '","'
                                               + self.id
                                               + '","'
                                               + self.zindex
                                               + '","'
                                               + self.classname + '");')

    def add(self, element):
        self.javascript('Tools.Stage_add("'+self.id+'","'+str(element.id)+'");')

    def slide(self, speed, direction, position):
        self.javascript('Tools.slide_stage("'+ self.id +'","'+ str(speed) +'","' + str(direction) +'","' + str(position) + '");')

    def fadeIn(self):
        self.javascript('Tools.fadeIn_stage("'+ self.id +'");')

    def fadeOut(self):
        self.javascript('Tools.fadeOut_stage("'+ self.id +'");')
        
    def hide(self):
        self.javascript('Tools.hide_stage("'+ self.id +'");')
    
    def show(self):
        self.javascript('Tools.show_stage("'+ self.id +'");')        

class Hydv_Div(object):
    def __init__(self, javascript_context, text, width, height, number, classname):
        self.text = text
        self.width = width
        self.height = height
        self.classname = classname
        self.id = "div_" + str(number)
        self.javascript = javascript_context
        self._create_div()

    def _create_div(self):
        self.javascript('Tools.Create_Div("'+self.text+'","'
                                               +str(self.width)+'","'
                                               +str(self.height)+'","'
                                               +self.id+'","'
                                               +self.classname+'");')
    def add(self, element):
        self.javascript('Tools.Div_add("'+self.id+'","'+str(element.id)+'");')

    def onclick(self, action):
        self.javascript('Tools.Connect_Onclick("'+action+'","'+self.id+'");')

    def onmouseover(self, action):
        self.javascript('Tools.Connect_Onmouseover("'+action+'","'+self.id+'");')

    def onmouseout(self, action):
        self.javascript('Tools.Connect_Onmouseout("'+action+'","'+self.id+'");')

class Hydv_Button(object):
    def __init__(self, javascript_context, text, width, height, number, classname):
        self.text = text
        self.width = width
        self.height = height
        self.classname = classname
        self.id = "button_" + str(number)
        self.javascript = javascript_context
        self._create_button()

    def _create_button(self):
        self.javascript('Tools.Create_Button("'+self.text+'","'
                                               +str(self.width)+'","'
                                               +str(self.height)+'","'
                                               +self.id+'","'
                                               +self.classname+'");')

    def onclick(self, action):
        self.javascript('Tools.Connect_Onclick("'+action+'","'+self.id+'");')

    def onmouseover(self, action):
        self.javascript('Tools.Connect_Onmouseover("'+action+'","'+self.id+'");')

    def onmouseout(self, action):
        self.javascript('Tools.Connect_Onmouseout("'+action+'","'+self.id+'");')

class Hydv_Icon(object):#self.javascript, 20, 20, i, "/usr/share/icons/oxygen/48x48/apps/accessories-calculator.png", ""
    def __init__(self, javascript_context, width, height, number, path, classname):
        self.width = width
        self.height = height
        self.path = path
        self.classname = classname
        self.id = "icon_" + str(number)
        self.javascript = javascript_context
        self._create_icon()

    def _create_icon(self):#width, height, id, path, classname
        self.javascript('Tools.Create_Icon("'+str(self.width)+'","'
                                               +str(self.height)+'","'
                                               +self.id+'","'
                                               +self.path+'","'
                                               +self.classname+'");')

