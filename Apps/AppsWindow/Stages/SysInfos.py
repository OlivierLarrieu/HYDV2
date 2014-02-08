#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "Olivier LARRIEU"
__version__ = "0.1"

import os
import psutil
import threading
from gi.repository import GLib

from HydvCore import Hydv_Listner
from HydvCore import HydvWidgets
HydvWidgets = HydvWidgets()

GLib.threads_init()

class Stage_Actions():
    """ ================================== """
    """ All Stage actions goes here only """
    """ ================================== """
    def show_category(self, category):
        pass

    def slide_up(self):
        print self.stage_2.id
        try:
            self.test.stop()
            del self.test
        except:
            pass
        self.javascript('$("#' + self.stage_2.id + '").animate({"top": "-270px"}, 250);')

    def slide_down(self):
        self.test = Infos(self.javascript)
        self.test.start()
        print self.stage_2.id
        self.javascript('$("#' + self.stage_2.id + '").animate({"top": "10px"}, 250);')

class Stage(object, Stage_Actions):
    def __init__(self, caller):
        caller.Window.view.connect("title-changed", Hydv_Listner.Actions, self)
        self.javascript = caller.javascript
        # Stage principal
        self.stage_2 = caller.HydvWidgets.Hydv_Stage(self.javascript, caller.width, 300, 800, "info_stage")
        print psutil.disk_partitions()
        self.stage_principal = caller.HydvWidgets.Hydv_Stage(self.javascript, caller.width, caller.height, 800, "stage")
        cpu_percentage_by_cpu = psutil.cpu_percent(interval=0.7, percpu=True)
        
        #self.stage_2.add(div)
        for cpu in cpu_percentage_by_cpu:
            progress = caller.HydvWidgets.Hydv_ProgressBar(self.javascript, caller.width, 20)
            self.stage_2.add(progress)
        # Display categories icons
        self.stage_category = caller.HydvWidgets.Hydv_Stage(self.javascript, caller.width, 30, 1000, "black_stage")
        
        
        # Display list off applications
        self.stage_principal.add(self.stage_category )
        self.stage_principal.add(self.stage_2 )
        button = caller.HydvWidgets.Hydv_Button(self.javascript , "return", 50, 20, "btn")
        button.onclick("slide_init")
        self.stage_category.add(button)
        button = caller.HydvWidgets.Hydv_Button(self.javascript , "up", 50, 20, "btn")
        button.onclick("slide_up")

        self.stage_category.add(button)
        button = caller.HydvWidgets.Hydv_Button(self.javascript , "down", 50, 20, "btn")
        button.onclick("slide_down")

        self.stage_category.add(button)
        
class Infos(threading.Thread):
    '''Return system informations like:
        -cpu
        -memorie
        -partitions
    '''
    def __init__(self, javascript):
        threading.Thread.__init__(self)
        self.running = True
        
        self.javascript = javascript

    def stop(self):
        self.running = False
        
    def run(self):
        """Start the thread."""
        self.running = True
        print "ENTER THREAD"
        #get partitions
        partitions = psutil.disk_partitions() 
        chaine = ""
        for elem in partitions:
            chaine=chaine+"<br>"+elem.device+" \
            "+elem.mountpoint+" "+elem.fstype+" \
            "+str(psutil.disk_usage(elem.mountpoint).percent)+"%"
        memorie_total = os.popen('mem=$(free -m);echo $mem|cut -d ":" -f2|cut -d " " -f2').readline()
        print memorie_total
        """GLib.idle_add(self.info_window.web.execute_script,
                      'a='+str(memorie_total))
        GLib.idle_add(self.info_window.web.execute_script,
                      'cpu_div = document.getElementById("cpu");\
                       cpu_info_div = document.getElementById("cpu_info");')"""

        while self.running:
            print "tttt"
            # Use os module and bash to recup informations
            memorie_use = os.popen('mem=$(free -m);echo $mem|tail -2|cut -d ":" -f3|cut -d " " -f2').readline()
            memorie_cached = os.popen('mem=$(free -m);echo $mem|tail -2|cut -d ":" -f3|cut -d " " -f3').readline()
            memorie_rest = int(memorie_total)-int(memorie_use)
            pourcent_memorie_use = float(memorie_use)/float(memorie_total)*100
            print pourcent_memorie_use
            #memorie_use = float(memorie_use)-float(memorie_cached)
            """GLib.idle_add(self.info_window.web.execute_script, 'b='+str(memorie_use))
            GLib.idle_add(self.info_window.web.execute_script, 'c='+str(memorie_cached))
            GLib.idle_add(self.info_window.web.execute_script, 'd='+str(memorie_rest))
            GLib.idle_add(self.info_window.web.execute_script, 'e='+str("%.2f" % pourcent_memorie_use))
            GLib.idle_add(self.info_window.web.execute_script, 'f='+'"'+str(chaine)+'"')
            GLib.idle_add(self.info_window.web.execute_script,
                         'info_sys(a,b,c,d,e,f)')"""
            # Use psutil module to recup cpu information, this module is optimized for this.
            cpu_percentage_by_cpu = psutil.cpu_percent(interval=0.7, percpu=True)
            count_cpu = 1
            for cpu in cpu_percentage_by_cpu:
                GLib.idle_add(self.javascript, '$("#progress_'+str(count_cpu)+' meter").attr("value",'+str(cpu)+')')
                print cpu, count_cpu, cpu_percentage_by_cpu
                """GLib.idle_add(self.info_window.web.execute_script, 
                             'cpu_bar_construct("'+str(cpu)+'", "'+str(count_cpu)+'", "'+str(len(cpu_percentage_by_cpu))+'")')"""
                count_cpu += 1
       
