#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "Olivier LARRIEU"
__version__ = "0.1"

import os
from gi.repository import Gdk

class Stage(object):
    def __init__(self, caller):
        self.state = "open"
        self.caller = caller
        self.javascript = caller.javascript
        # Stage principal
        self.stage_principal = caller \
                              .HydvWidgets_instance \
                              .Hydv_MasterStage(context=self,
                                                width=caller.width,
                                                height=caller.height,
                                                zindex=800,
                                                classname="stage")
        self._open()
        caller.Window.view.connect("title-changed", Hydv_Listner.Actions, self)
        
    def launch_command(self, command):
        os.system(command+" &")

    def _open(self):  
        pass
        
    def _close(self):
        pass

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
    """ listen for javascript event and evaluate the action            """
    """ Each view is connected to its own Hydv_Listner.Actions         """
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
        if action != "_":
            # First initialisation of the view
            if not widget.is_init:
                Hydv_Listner.view_init(action, widget)
            else:
                Hydv_Listner.evaluate_action(action, widget, caller)                

class HydvWidgets(object):
    def __init__(self, javascript_context):
        """
        HydvWidgets must be instanciate in the principal window.
        HydvWidgets get traces of all embed objects, and manage
        the different open/close stage in the window.
        """
        self._stage_counter = 0
        self._div_counter = 0
        self._button_counter = 0
        self._icon_counter = 0
        self._header_counter = 0
        self._footer_counter = 0
        self._progressbar_counter = 0
        self.javascript_context = javascript_context
        self.master_stage_collection = []

    def get_stage_collection(self):
        return self.master_stage_collection

    def open_stage(self, stage_id):
        for stage in self.get_stage_collection():
            print stage.state
            print stage.stage_principal.id, stage_id
            if stage.stage_principal.id == stage_id:
                if stage.state != "open":
                    self.close_current_stage()
                    stage._open()
                    stage.state = "open"

    def close_current_stage(self):
        for stage in self.get_stage_collection():
            print stage.state
            print "open"
            stage._close()
            stage.state = "close"
 
    def Hydv_MasterStage(self, **kwargs):
        width = kwargs['width']
        height = kwargs['height']
        zindex = kwargs['zindex']
        classname = kwargs['classname']
        self._stage_counter += 1
        self.master_stage_collection.append(kwargs['context'])
        return Hydv_MasterStage(self.javascript_context, width, height, self._stage_counter, zindex, classname)

    def Hydv_Stage(self, **kwargs):                
        width = kwargs['width']
        height = kwargs['height']
        zindex = kwargs['zindex']
        classname = kwargs['classname']
        self._stage_counter += 1 
        return Hydv_Stage(self.javascript_context, width, height, self._stage_counter, zindex, classname)

    def Hydv_Div(self, **kwargs):
        width = kwargs['width']
        height = kwargs['height']
        text = kwargs['text']
        classname = kwargs['classname']
        self._div_counter += 1
        return Hydv_Div(self.javascript_context, text, width, height, self._div_counter, classname)

    def Hydv_Button(self, **kwargs):
        width = kwargs['width']
        height = kwargs['height']
        text = kwargs['text']
        classname = kwargs['classname']
        self._button_counter += 1
        return Hydv_Button(self.javascript_context, text, width, height, self._button_counter, classname)

    def Hydv_Icon(self, **kwargs):
        width = kwargs['width']
        height = kwargs['height']
        path = kwargs['path']
        classname = kwargs['classname']
        self._icon_counter += 1
        return Hydv_Icon(self.javascript_context, width, height, self._icon_counter, path, classname)

    def Hydv_Header(self):
        self._header_counter += 1
        return Hydv_Header(self.javascript_context)
    
    def Hydv_Footer(self):
        self._footer_counter += 1
        return Hydv_Footer(self.javascript_context)

    def Hydv_ProgressBar(self, **kwargs):
        width = kwargs['width']
        height = kwargs['height']
        self._progressbar_counter += 1
        return Hydv_ProgressBar(self.javascript_context, width, height, self._progressbar_counter)

class Hydv_MasterStage(object):
    """ ============================================================== """
    """ A MasterStage the principal container for embed application in HydvWindow     """
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
        self.javascript('Tools.Create_MasterStage("' + str(self.width)
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

    def animate(self, **kwargs):
        direction = kwargs['direction']
        px = kwargs['px']
        speed = kwargs['speed']
        delay = kwargs['delay']
        self.javascript('$("#%s").delay(%s).animate({"%s": "%spx"}, %s);'%(self.id, delay, direction, px, speed))

    def slide(self, speed, direction, position):
        self.javascript('Tools.slide_stage("'+ self.id +'","'+ str(speed) +'","' + str(direction) +'","' + str(position) + '");')

    def fadeIn(self):
        self.javascript('$("#%s").delay(0).fadeIn(200)'%self.id)

    def fadeOut(self):
        self.javascript('$("#%s").delay(100).fadeOut(200)'%self.id)

    def hide(self):
        self.javascript('Tools.hide_stage("'+ self.id +'");')
    
    def show(self):
        self.javascript('Tools.show_stage("'+ self.id +'");')        

class Hydv_Stage(object):
    """ ============================================================== """
    """ A stage is a container for embed MasterStage    """
    """ A MasterStage may have more than one stage.                         """
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

    def animate(self, **kwargs):
        direction = kwargs['direction']
        px = kwargs['px']
        speed = kwargs['speed']
        delay = kwargs['delay']
        self.javascript('$("#%s").delay(%s).animate({"%s": "%spx"}, %s);'%(self.id, delay, direction, px, speed))

    def slide(self, speed, direction, position):
        self.javascript('Tools.slide_stage("'+ self.id +'","'+ str(speed) +'","' + str(direction) +'","' + str(position) + '");')

    def fadeIn(self):
        self.javascript('$("#%s").delay(0).fadeIn(200)'%self.id)

    def fadeOut(self):
        self.javascript('$("#%s").delay(100).fadeOut(200)'%self.id)

    def hide(self):
        self.javascript('$("#'+ self.id +'").hide();')
    
    def show(self):
        self.javascript('$("#'+ self.id +'").show();')        

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
    def animate(self, **kwargs):
        direction = kwargs['direction']
        px = kwargs['px']
        speed = kwargs['speed']
        delay = kwargs['delay']
        self.javascript('$("#%s").delay(%s).animate({"%s": "%spx"}, %s);'%(self.id, delay, direction, px, speed))

    def add(self, element):
        self.javascript('Tools.Div_add("'+self.id+'","'+str(element.id)+'");')

    def onclick(self, action):
        self.javascript('Tools.Connect_Onclick("'+action+'","'+self.id+'");')

    def onmouseover(self, action):
        self.javascript('Tools.Connect_Onmouseover("'+action+'","'+self.id+'");')

    def onmouseout(self, action):
        self.javascript('Tools.Connect_Onmouseout("'+action+'","'+self.id+'");')

    def innerText(self, text):
        self.javascript('$("#%s")[0].innerText = "%s"'%text)

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

    def onclick(self, action):
        self.javascript('Tools.Connect_Onclick("'+action+'","'+self.id+'");')

    def onmouseover(self, action):
        self.javascript('Tools.Connect_Onmouseover("'+action+'","'+self.id+'");')

    def onmouseout(self, action):
        self.javascript('Tools.Connect_Onmouseout("'+action+'","'+self.id+'");')

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
