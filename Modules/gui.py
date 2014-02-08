#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import cairo
from gi.repository import Gtk 
from gi.repository import Gdk 
from gi.repository import WebKit
from gi.repository import GLib

GLib.threads_init()
screen_x , screen_y = Gdk.Screen.width(), Gdk.Screen.height()
screen = Gdk.Screen()

class View(WebKit.WebView):
    def __init__(self, x, y, url, connected_function, caller_instance):
        super(View, self).__init__()
        self.url = url
        self.set_transparent(True)
        self.set_app_paintable(True)
        self.set_size_request(x,y)
        self._is_initialized = False
        browser_settings = self.get_settings()
        settings_list_true = ('enable-frame-flattening',
                              'enable-page-cache',
                              'tab-key-cycles-through-elements',
                              'enable-universal-access-from-file-uris',
                              'enable-offline-web-application-cache',
                              'enable-caret-browsing',
                              'enable-plugins',
                              'enable-scripts',
                              'auto-shrink-images',
                              'auto-load-images',
                              'enforce-96-dpi',
                              'enable-private-browsing',
                              'enable-spell-checking',
                              'enable-caret-browsing',
                              'enable-html5-database',
                              'enable-html5-local-storage',
                              'enable-xss-auditor',
                              'enable-spatial-navigation',
                              'enable-frame-flattening',
                              'javascript-can-access-clipboard',
                              'enable-offline-web-application-cache',
                              'enable-universal-access-from-file-uris',
                              'enable-file-access-from-file-uris',
                              'enable-site-specific-quirks',
                              'enable-page-cache',
                              'auto-resize-window',
                              'enable-java-applet',
                              'enable-hyperlink-auditing',
                              'enable-fullscreen',
                              #'enable-accelerated-compositing',
                              'enable_webgl')

        settings_list_false = (#'enable-default-context-menu',
                               #'enable-developer-extras',
                               'javascript-can-open-windows-automatically',
                               #'editing-behavior',
                               #'enable-dom-paste',
                               'tab-key-cycles-through-elements',
                               'enable-default-context-menu',
                               'enable-dns-prefetching',)
        for sets in settings_list_true:
             browser_settings.set_property(sets, True)

        for sets in settings_list_false:
             browser_settings.set_property(sets, False)
           
        self.set_settings(browser_settings)


        
        self.connect("title-changed", connected_function, caller_instance)
        self.connect("navigation-policy-decision-requested",
                                          self._disable_drop)
        self.open("file://" + url)
        self.connect("draw", self.area_draw)

    def area_draw(self, widget, cr):
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

    def _disable_drop(self, widget,widget1,request,widget2,widget3, data=None):
        #hack to disable drop in webview
        uri = request.get_uri()
        if uri != "file://" + self.url:
            self.stop_loading()

class HyWindow(Gtk.Window):
    def __init__(self, caller_instance, x, y, url, connected_function, type_int, above_value, title):
        super(HyWindow, self).__init__()
        self.caller_instance = caller_instance
        self.view = View(x, y, url, connected_function, self.caller_instance)
        self.view.is_init = False
        self.add(self.view)
        self.set_title(title)
        self.set_decorated(False)
        self.set_keep_above(above_value)
        self.set_type_hint(Gdk.WindowTypeHint(type_int))
        self.set_size_request(x,y)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_resizable(False)
        self.stick()

        self.set_app_paintable(True)
        self.screen = self.get_screen()
        self.visual = self.screen.get_rgba_visual()
        
        if self.visual != None and self.screen.is_composited():
            self.set_visual(self.visual)

        self.connect("destroy", self.leave)       
        self.connect("draw", self.area_draw)
        self.realize()
        self.show_all()

    def area_draw(self, widget, cr):
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

    def leave(self, ARG):
        Gtk.main_quit()
    

