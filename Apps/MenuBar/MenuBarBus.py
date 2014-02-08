#!/usr/bin/env python
# -*- coding:utf-8 -*-

from gi.repository import GLib
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

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
    def test(self):
        self.MenuBarWindow.view.execute_script('Tools.Send("self.closeall()");')

    @dbus.service.method('org.hydv2.menubar')
    def add_favorite_app(self, app):
        self.MenuBarWindow.view.execute_script('Tools.add_fav_app("%s");'%app)

class Service(object):
    def __init__(self, MenuBarWindow):
        DBusGMainLoop(set_as_default=True)
        myservice = BusService(MenuBarWindow)

    def start(self):
        self.main_loop = GLib.MainLoop()
        self.main_loop.run()

    def stop(self):
        self.main_loop.quit()
        return True
