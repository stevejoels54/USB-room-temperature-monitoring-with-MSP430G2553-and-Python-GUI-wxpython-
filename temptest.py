# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 12:31:23 2020

@author: STEVE JOELS
"""
"""

 The code below has two major functions that are threaded since they run at the same time 
 FUNCTIONS : >> my_app() updates values at the GUI side while check_device() gets the temperature values from the USB device
 
"""

import wx
import threading
import serial
import time

def my_app():
    global data
    global display_value
    global status
    global display_error
    global app
    global window
    global pnl
    app = wx.App()
    window = wx.Frame(None, title = "Temperature monitor 1.0", size = (700,500),style=wx.MINIMIZE_BOX|wx.RESIZE_BORDER| wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
    ico = wx.Icon('chip.ico', wx.BITMAP_TYPE_ICO)
    window.SetIcon(ico)
    window.SetBackgroundColour("gray")
    pnl = wx.Panel(window)
    global font    
    font = wx.Font(80, wx.DEFAULT, wx.NORMAL, wx.DEFAULT)
    global font1
    font1 = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.DEFAULT)
    textfont1 = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.DEFAULT)
    textfont2= wx.Font(65, wx.DEFAULT, wx.NORMAL, wx.DEFAULT)
    text1=wx.StaticText(pnl, label="TEMP SENSOR STATUS : ", pos=(50, 300))
    text1.SetFont(textfont1)
    text2=wx.StaticText(pnl, label="TEMP : ", pos=(10, 100))
    text2.SetFont(textfont2)
    closeButton = wx.Button(pnl, label='CLOSE', pos=(600,420))
    closeButton.Bind(wx.EVT_BUTTON, onclose)
    closeButton.SetBackgroundColour("red")
    display_error=wx.TextCtrl(pnl,-1,pos=(300,300),value ='',size=(270,28),style=wx.TE_READONLY|wx.TE_CENTER)
    display_value=wx.TextCtrl(pnl,-1,pos=(350,100),value ='',size=(300,120),style=wx.TE_READONLY|wx.TE_CENTER)
    display_value.SetBackgroundColour("black")
    display_value.SetForegroundColour("green")
    display_error.SetBackgroundColour("black")
    display_error.SetForegroundColour("red")
    status = "DEVICE NOT CONNECTED"
    display_value.SetValue(str('00'))# display 00 if no data coming in
    display_value.SetFont(font)
    display_error.SetValue(str(status))# display device connected or not depending on device connection state
    display_error.SetFont(font1)
    window.Bind(wx.EVT_CLOSE, onclose)
    window.Show(True)
    app.MainLoop()

def onclose(event):   # GUI close function
    global windowstatus
    dial = wx.MessageDialog(None,'Are sure you want to quit?','Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) # ask user if they really want to quit app
    ret=dial.ShowModal()
    if ret == wx.ID_YES:
        window.Destroy()
        

def check_device():
    while True:
        try:
            ser = serial.Serial('COM3',9600, timeout=1)# specify the serial port where the device is connected depending on the OS you are using then specify the baud rate same as the device so that data is not lost
            
        except serial.SerialException:
                status="DEVICE NOT CONNECTED"
                data ='00'
                time.sleep(1)
                pass
            
        else: 
              status="DEVICE CONNECTED"
              data = ser.readline().decode('ascii')# decode in coming data to ASCII
              time.sleep(1)
              ser.close()
              
        finally:
            try:
                p='C'
                display_value.SetValue(str(data+p))# display temp value coming in with 'C' representing celsius
                display_value.SetFont(font)
                display_error.SetValue(str(status))
                display_error.SetFont(font1)
                
            except:
                break
        
def main():
       t2 = threading.Thread(target=check_device)
       t2.start()
       t3 = threading.Thread(target=my_app())# my_app() must run as a main threading to prevent the blocking of some wxpython functions when app is closed
       t3.start()
       t2.join()
       t3.join()
           
main()

