#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "Olivier LARRIEU"
__version__ = "0.1"

import os
import psutil
import threading
from gi.repository import GLib

from HydvCore import Hydv_Listner


GLib.threads_init()

class Stage_Actions():
    """ ================================== """
    """ All Stage actions goes here only """
    """ ================================== """
    def show_category(self, category):
        pass

    def _open(self):
        #1) animate category stage on top
        self.stage_principal.animate(direction="left", px=0, speed=150, delay=200)
        self.stage_menu.animate(direction="top", px="30", speed=150, delay=650)

    def _close(self):
        #1) animate category stage on top  
        print "close sysinfo"
        self.stage_menu.animate(direction="top", px="-10", speed=150, delay=0)
        self.stage_principal.animate(direction="left", px="-350", speed=150, delay=300)
        
    def slide_up(self):
        try:
            self.test.stop()
            del self.test
            
        except:
            pass
        self.thread = False
        self.stage_cpu.animate(direction="top", px="-290", speed=250, delay=0)
        
    def slide_down(self):
        if not self.thread:
            self.test = Infos(self.javascript)
            self.test.start()
            self.thread = True
        
        self.stage_cpu.animate(direction="top", px="10", speed=250, delay=0)

    
class Stage(object, Stage_Actions):
    def __init__(self, caller):
        self.state = "close"
        caller.Window.view.connect("title-changed", Hydv_Listner.Actions, self)
        self.javascript = caller.javascript
        # Stage principal
        self.stage_principal = caller.HydvWidgets_instance.Hydv_MasterStage(context=self,width=caller.width,
                                                                   height=caller.height,
                                                                   zindex=800,
                                                                   classname="stage")

        self.stage_cpu = caller.HydvWidgets_instance.Hydv_Stage(width=caller.width, height=300, zindex=800, classname="info_stage")


        cpu_percentage_by_cpu = psutil.cpu_percent(interval=0.7, percpu=True)
        for cpu in cpu_percentage_by_cpu:
            progress_bar = caller.HydvWidgets_instance.Hydv_ProgressBar(width=caller.width, height=20)
            self.stage_cpu.add(progress_bar)
        # Display categories icons
        self.stage_menu = caller.HydvWidgets_instance.Hydv_Stage(width=caller.width, height=30, zindex=1000, classname="black_stage")
        
        
        # Display list off applications
        self.stage_principal.add(self.stage_menu )
        self.stage_principal.add(self.stage_cpu )
        button = caller.HydvWidgets_instance.Hydv_Button(text="up", width=50, height=20, classname="btn")
        button.onclick("slide_up")
        self.stage_menu.add(button)
        button = caller.HydvWidgets_instance.Hydv_Button(text="down", width=50, height=20, classname="btn")
        button.onclick("slide_down")
        self.stage_menu.add(button)
        info_button = caller.HydvWidgets_instance.Hydv_Button(text="infos system", width=80, height=20, classname="btn")
        info_button.onclick("open_stage('%s')" %self.stage_principal.id)
        
        caller.footer.add(info_button)
        self.slide_up()

class Infos(threading.Thread):
    '''Return system informations like:
        -cpu
        -memorie
        -partitions
    '''
    def __init__(self, javascript):
        threading.Thread.__init__(self)        
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
       
