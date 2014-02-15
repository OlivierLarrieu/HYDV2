#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "Olivier LARRIEU"
__version__ = "0.1"

import os
from HydvCore import Hydv_Listner

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

