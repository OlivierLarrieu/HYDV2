#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "Olivier LARRIEU"
__version__ = "0.1"

import os
import time
from HydvCore import Hydv_Listner
from HydvMenu import HydvDesktopEntries


class Stage_Actions():
    """ ================================== """
    """ All Stage actions goes here only """
    """ ================================== """

    def show_category(self, category):
        self.javascript('$(".apps_button").hide();$(".add").hide()')
        self.javascript('$(".'+category+'").fadeIn()')        

    def launch_command(self, command):
        os.system(command+" &")

    def _open(self):  
        self.stage_principal.animate(direction="left", px="0", speed=150, delay=0)
        self.category_container.animate(direction="top", px="30", speed=150, delay=250)
        self.stage.animate(direction="top", px=30, speed=150, delay=550)
    def _close(self):
        self.stage.animate(direction="top", px=-self.stage.height-100, speed=250, delay=0)
        self.category_container.animate(direction="top", px="-80", speed=150, delay=200)
        
        self.stage_principal.animate(direction="left", px="-350", speed=150, delay=400)
        self.javascript('Tools.Send("open_sysinfo_stage")')

class Stage(object, Stage_Actions):
    def __init__(self, caller):
        self.state = "open"
        self.caller = caller
        print "_____________________________________________________"
        self.javascript = caller.javascript
        # Stage principal
        self.stage_principal = caller.HydvWidgets_instance.Hydv_MasterStage(context=self,
                                                                      width=caller.width,
                                                                      height=caller.height,
                                                                      zindex=800,
                                                                      classname="stage", toto="re")
        # Display categories icons
        self.category_container = caller.HydvWidgets_instance.Hydv_Stage(width=caller.width,
                                                                         height=80,
                                                                         zindex=800,
                                                                         classname="black_stage")
        # Display list off applications
        self.stage = caller.HydvWidgets_instance.Hydv_Stage(width="98%",
                                                            height=270,
                                                            zindex=700,
                                                            classname="apps_button_stage")
        category_indice = 0
        Apps = HydvDesktopEntries.get_applications()
        keylist = Apps.keys()
        keylist.sort()
        for cat in keylist:                  
            button = caller.HydvWidgets_instance.Hydv_Button(text="",
                                                             width=30,
                                                             height=30,
                                                             classname="btn")
            icon = caller.HydvWidgets_instance.Hydv_Icon(width=30,
                                                         height=30,
                                                         path=HydvDesktopEntries.findicon(cat),
                                                         classname="cat_icon")
            button.add(icon)
            button.onclick("show_category('cat_%s')"%category_indice)
            self.category_container.add(button)
            t = Apps[cat]
            t.sort()
            for i in t:
                div = caller.HydvWidgets_instance.Hydv_Div(text="",
                                                           width="85%",
                                                           height=30,
                                                           classname="apps_button cat_%s"%category_indice)
                apps_name = caller.HydvWidgets_instance.Hydv_Div(text="%s"%i[i.keys()[0]]['name'],
                                                                 width="85%",
                                                                 height="",
                                                                 classname="")
                add_button = caller.HydvWidgets_instance.Hydv_Div(text="",
                                                                  width="",
                                                                  height="",
                                                                  classname="add cat_%s"%category_indice)
                

                icon = caller.HydvWidgets_instance.Hydv_Icon(width=30,
                                                             height=30,
                                                             path=i[i.keys()[0]]['icon'],
                                                             classname="")
                div.add(icon)
                div.add(apps_name)
                div.onclick("launch_command('%s')"%i[i.keys()[0]]['command'])
                add_button.onclick("add_to_menubar('%s')"%i[i.keys()[0]]['icon'])
                self.stage.add(div)
                self.stage.add(add_button)
            category_indice += 1                
        self.stage_principal.add(self.category_container )
        self.stage_principal.add(self.stage)        
        apps_button = caller.HydvWidgets_instance.Hydv_Button(text="Applications",
                                                              width=100,
                                                              height=20,
                                                              classname="btn")
        apps_button.onclick("open_stage('%s')" %self.stage_principal.id)
        caller.footer.add(apps_button)
        self._open()
        caller.Window.view.connect("title-changed", Hydv_Listner.Actions, self)
