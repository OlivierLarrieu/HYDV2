#!/usr/bin/env python
# -*- coding:utf-8 -*-


from gi.repository import GLib, Gtk
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

GLib.threads_init()

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
        self.AppsWindow.show_all()
        self.AppsWindow.set_position(Gtk.WindowPosition.MOUSE)
        self.move(x, y)

    @dbus.service.method('org.hydv2.appswindow')
    def hide(self):
        self.AppsWindow.hide()

    @dbus.service.method('org.hydv2.appswindow')
    def move(self, x, y):
        self.AppsWindow.move(x, y)

    @dbus.service.method('org.hydv2.appswindow')
    def getWindow(self, arg):
        pass
        
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
