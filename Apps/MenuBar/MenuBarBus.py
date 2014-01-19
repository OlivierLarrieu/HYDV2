#!/usr/bin/env python
# -*- coding:utf-8 -*-

import dbus.service
import glib as GLib

class BusService(dbus.service.Object):
    # Dbus service to communicate with MenuBar
    def __init__(self, MenuBarWindow):
        #print "bar bus launched..."
        self.MenuBarWindow = MenuBarWindow
        try:
            bus_name = dbus.service.BusName('org.hydv2.menubar', bus=dbus.SessionBus())
            dbus.service.Object.__init__(self, bus_name, '/org/hydv2/menubar')
            print "Bus /org/hydv2/menubar listen..."
        except:
            pass 
        
    @dbus.service.method('org.hydv2.menubar')
    def test(self, position):
        self.MenuBarWindow.view.execute_script('Tools.Send("self.open_shutdow()");')
        print "here"

