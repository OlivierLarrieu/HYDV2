#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "Olivier LARRIEU"
__version__ = "0.1"

import os, time
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
        #self.div.animate(direction="top", px="60", speed=10, delay=0)
        self.stage_principal.animate(direction="left", px=0, speed=150, delay=200)
        self.stage_menu.animate(direction="top", px="30", speed=150, delay=650)
        

    def _close(self):
        self.slide_up()
        self.stage_menu.animate(direction="top", px="-10", speed=150, delay=0)
        self.stage_principal.animate(direction="left", px="-350", speed=150, delay=300)
        self.stage_cpu.animate(direction="top", px="-290", speed=250, delay=0)
        #self.div.animate(direction="top", px="600", speed=250, delay=0)
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
            self.test = Infos(self.javascript,  self.moveup)
            self.test.start()
            self.thread = True        
        self.stage_cpu.animate(direction="top", px="50", speed=250, delay=0)
        

    def moveup(self, pourcent_memorie_use):
        self.counter += 1
        if self.counter == 3:
            ##self.div.animate(direction="left", px=self.stage_principal.width-#self.div.width*3, speed=300, delay=0)
            #self.div.animate(direction="top", px="-%d.2"%pourcent_memorie_use, speed=800, delay=0)
            self.c = False
        if self.counter == 6:
            ##self.div.animate(direction="left", px=0, speed=500, delay=0)
            #self.div.animate(direction="top", px=0, speed=800, delay=100)

            self.counter = 0

class Stage(object, Stage_Actions):
    def __init__(self, caller):
        self.state = "close"
        self.c = True
        self.counter = 0
        caller.Window.view.connect("title-changed", Hydv_Listner.Actions, self)
        self.javascript = caller.javascript
        # Stage principal
        self.stage_principal = caller.HydvWidgets_instance.Hydv_MasterStage(context=self,width=caller.width,
                                                                   height=caller.height,
                                                                   zindex=800,
                                                                   classname="stage")
        self.stage_cpu = caller.HydvWidgets_instance.Hydv_Stage(width=caller.width, height=170, zindex=800, classname="black_stage")

        cpu_percentage_by_cpu = psutil.cpu_percent(interval=0.7, percpu=True)
        counter = 1
        for cpu in cpu_percentage_by_cpu:
            title = caller.HydvWidgets_instance.Hydv_Div(width=80, height=20, text="cpu:"+str(counter), classname="progressbar")
            self.stage_cpu.add(title)
            progress_bar = caller.HydvWidgets_instance.Hydv_ProgressBar(width=caller.width-80, height=20)
            self.stage_cpu.add(progress_bar)
            counter += 1
        self.stage_menu = caller.HydvWidgets_instance.Hydv_Stage(width=caller.width, height=30, zindex=1000, classname="black_stage")
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
        
        caller.header.add(info_button)
        self._close()
        
class Infos(threading.Thread):
    '''Return system informations like:
        -cpu
        -memorie
        -partitions
    '''
    def __init__(self, javascript, div):
        threading.Thread.__init__(self)        
        self.javascript = javascript
        #self.div = div
    def stop(self):
        self.running = False

    def run(self):
        """Start the thread."""
        self.running = True
        #get partitions
        partitions = psutil.disk_partitions() 
        chaine = ""
        for elem in partitions:
            chaine=chaine+"<br>"+elem.device+" \
            "+elem.mountpoint+" "+elem.fstype+" \
            "+str(psutil.disk_usage(elem.mountpoint).percent)+"%"
        memorie_total = os.popen('mem=$(free -m);echo $mem|cut -d ":" -f2|cut -d " " -f2').readline()

        while self.running:
            # Use os module and bash to get informations
            memorie_use = os.popen('mem=$(free -m);echo $mem|tail -2|cut -d ":" -f3|cut -d " " -f2').readline()
            memorie_cached = os.popen('mem=$(free -m);echo $mem|tail -2|cut -d ":" -f3|cut -d " " -f3').readline()
            memorie_rest = int(memorie_total)-int(memorie_use)
            pourcent_memorie_use = float(memorie_use)/float(memorie_total)*100
            cpu_percentage_by_cpu = psutil.cpu_percent(interval=0.7, percpu=True)
            count_cpu = 1
            time.sleep(0.5)
            #GLib.idle_add(#self.div, pourcent_memorie_use)
            #GLib.timeout_add(800, self.movedown)
            for cpu in cpu_percentage_by_cpu:
                GLib.idle_add(self.javascript, '$("#progress_'+str(count_cpu)+' meter").attr("value",'+str(cpu)+')')
                count_cpu += 1
       
