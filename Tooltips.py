# -*- coding: utf-8 -*-
"""
Data Science Calculator Tool tips
Adapted on Wed Sep 29, 2018 based on a template from
Python GUI Programming Solutions, by Burkhardt Meyer Packt Publishing

@author: David York
@copyright: David York 2018
@license: MIT license
"""

#======================
# imports
#======================
import tkinter as tk

class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.col = self.row = 0                 # col = x value, row = y value

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        col, row, _ccol, crow = self.widget.bbox("insert")
        col = col + self.widget.winfo_rootx() + 27
        row = row + crow + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (col, row))

        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

#===================================================================
def createToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
