#!/usr/bin/env python
# -*- coding:utf-8 -*-
from gi.repository import Gtk, Gdk

class Hydv_Screen_Utils(object):
    """ ============================================================== """
    """ Class generic                                                  """
    """ ============================================================== """

    @classmethod
    def get_screen_width(cls):
        screen = Gdk.Screen.get_default()
        screen_width = screen.get_width()
        return screen_width

    @classmethod
    def get_screen_height(cls):
        screen = Gdk.Screen.get_default()
        screen_height = screen.get_height()
        return screen_height

    @classmethod
    def get_n_monitors(cls):
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
    @classmethod
    def view_init(self, action, widget):
        """ Initialisation of the View """
        if action == "init":
            widget.is_init = True
            parent_window = widget.get_parent()
            parent_window.caller_instance.on_view_init(action)
            return True

    @classmethod
    def evaluate_action(self, action, widget, caller):
        # Interpret action from javascript
        try:
            fonction = action.split('(')[0]
            arg = action.replace(fonction, '')[1:-2].replace("'",'').replace('"','')
            call = getattr(caller, fonction)            
            if arg != "":
                call(arg)
            else:
                call()
        except:
            pass

    @classmethod
    def Actions(self, widget, frame, action, caller):
        """ Connector for a View to listen javascript events. """
        print caller
        if action != "_":
            print "action widget.is_init", widget.is_init
            # First initialisation of the view
            if not widget.is_init:
                Hydv_Listner.view_init(action, widget)
            else:
                Hydv_Listner.evaluate_action(action, widget, caller)                



class HydvWidgets(object):
    def __init__(self):
        self._stage_counter = 0
        self._div_counter = 0
        self._button_counter = 0
        self._icon_counter = 0
        self._header_counter = 0
        self._footer_counter = 0
        self._progressbar_counter = 0

    def Hydv_Stage(self, javascript_context, width, height, zindex, classname):
        self._stage_counter += 1
        return Hydv_Stage(javascript_context, width, height, self._stage_counter, zindex, classname)
        
    def Hydv_Div(self, javascript_context, text, width, height, classname):
        self._div_counter += 1
        return Hydv_Div(javascript_context, text, width, height, self._div_counter, classname)

    def Hydv_Button(self, javascript_context, text, width, height, classname):
        self._button_counter += 1
        return Hydv_Button(javascript_context, text, width, height, self._button_counter, classname)

    def Hydv_Icon(self, javascript_context, width, height, path, classname):
        self._icon_counter += 1
        return Hydv_Icon(javascript_context, width, height, self._icon_counter, path, classname)

    def Hydv_Header(self, javascript_context):
        self._header_counter += 1
        return Hydv_Header(javascript_context)
    
    def Hydv_Footer(self, javascript_context):
        self._footer_counter += 1
        return Hydv_Footer(javascript_context)

    def Hydv_ProgressBar(self, javascript_context, width, height):
        self._progressbar_counter += 1
        return Hydv_ProgressBar(javascript_context, width, height, self._progressbar_counter)

class Hydv_Stage(object):
    """ ============================================================== """
    """ A stage is a container for embed application in HydvWindow     """
    """ A window may have more than one stage.                         """
    """ ============================================================== """

    #print "__INIT stage__",self._stage_counter
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

    def add(self, element):
        self.javascript('Tools.Button_add("'+self.id+'","'+str(element.id)+'");')

    def onclick(self, action):
        self.javascript('Tools.Connect_Onclick("'+action+'","'+self.id+'");')

    def onmouseover(self, action):
        self.javascript('Tools.Connect_Onmouseover("'+action+'","'+self.id+'");')

    def onmouseout(self, action):
        self.javascript('Tools.Connect_Onmouseout("'+action+'","'+self.id+'");')

class Hydv_Icon(object):
    def __init__(self, javascript_context, width, height, number, path, classname):
        self.width = width
        self.height = height
        self.path = path
        self.classname = classname
        self.id = "icon_" + str(number)
        self.javascript = javascript_context
        self._create_icon()

    def _create_icon(self):
        self.javascript('Tools.Create_Icon("'+str(self.width)+'","'
                                               +str(self.height)+'","'
                                               +self.id+'","'
                                               +self.path+'","'
                                               +self.classname+'");')

class Hydv_ProgressBar(object):
    def __init__(self, javascript_context, width, height, number):
        self.width = width
        self.height = height
        self.id = "progress_" + str(number)
        self.javascript = javascript_context
        self._create_progressbar()

    def _create_progressbar(self):
        self.javascript('Tools.Create_ProgressBar("'+str(self.width)+'","'
                                                    +str(self.height)+'","'
                                                    +self.id+'");')

class Hydv_Header(object):
    def __init__(self, javascript_context):
        self.javascript = javascript_context
        self._create_header()

    def _create_header(self):
        self.javascript('Tools.Create_Header()')

    def add(self, element):
        self.javascript('Tools.Header_add("'+str(element.id)+'");')

class Hydv_Footer(object):
    def __init__(self, javascript_context):
        self.javascript = javascript_context
        self._create_footer()

    def _create_footer(self):
        self.javascript('Tools.Create_Footer()')

    def add(self, element):
        self.javascript('Tools.Footer_add("'+str(element.id)+'");')

