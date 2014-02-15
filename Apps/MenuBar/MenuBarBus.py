#!/usr/bin/env python
# -*- coding:utf-8 -*-

from gi.repository import GLib
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

GLib.threads_init()

class BusService(dbus.service.Object):
    # Dbus service to communicate with MenuBar
    def __init__(self, MenuBar):
        #print "bar bus launched..."
        self.MenuBar = MenuBar
        try:
            bus_name = dbus.service.BusName('org.hydv2.menubar', bus=dbus.SessionBus())
            dbus.service.Object.__init__(self, bus_name, '/org/hydv2/menubar')
            print "Bus /org/hydv2/menubar listen..."
        except:
            pass 
        

    @dbus.service.method('org.hydv2.menubar')
    def add_favorite_app(self, arg):
        app = arg.split('#')[0]
        command = arg.split('#')[1]
        self.MenuBar.add_fav_app(app, command)

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
