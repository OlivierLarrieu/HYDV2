#!/usr/bin/env python
# -*- coding:utf-8 -*-

import dbus.service
import glib as GLib
from dbus.mainloop.glib import DBusGMainLoop

class BusService(dbus.service.Object):
    # Dbus service to communicate with AppsWindow
    def __init__(self, AppsWindow):
        #print "bar bus launched..."
        self.AppsWindow = AppsWindow
        try:
            bus_name = dbus.service.BusName('org.hydv2.appswindow', bus=dbus.SessionBus())
            dbus.service.Object.__init__(self, bus_name, '/org/hydv2/appswindow')
            print "Bus /org/hydv2/appswindow listen..."
        except:
            pass 
        
    @dbus.service.method('org.hydv2.appswindow')
    def show(self, x, y):
        self.AppsWindow.show()
        self.AppsWindow.move(x, y-self.AppsWindow.get_size()[1])

    @dbus.service.method('org.hydv2.appswindow')
    def hide(self):
        self.AppsWindow.hide()

    @dbus.service.method('org.hydv2.appswindow')
    def move(self, x, y):
        self.AppsWindow.move(x, y)
        
class Service(object):
    def __init__(self, AppsWindow):
        DBusGMainLoop(set_as_default=True)
        myservice = BusService(AppsWindow)

    def start(self):
        self.main_loop = GLib.MainLoop()
        self.main_loop.run()

    def stop(self):
        self.main_loop.quit()
        return True
