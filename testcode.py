'''
Created on Nov 6, 2018

@author: david
'''
'''
Created on Sep 30, 2018

@author: david
'''
import os
import pathlib
import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from tkinter import font
import PIL
from PIL import Image, ImageTk

class splashScreen():
     
    def __init__(self):
        '''
        Splash constructor
        '''
        
        self.splash()
        
        
        
        
        #self.splashfrm.mainloop()
     
    def splash(self):
        '''
        '''
        root = tk.Tk()
        #root.title('Splash')
        #root.wm_attributes('-fullscreen','true')
        #eliminate the titlebar
        root.overrideredirect(1)
    
        image = Image.open("medmatix_tilt.png")
        canvas=Canvas(root, height=500, width=500, background='SteelBlue3')
        basewidth = 220
        wpercent = (basewidth / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(wpercent)))
        image = image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(250,250, image=photo)
        canvas.create_text(250,161, text='Welcome to', font=('Helvetica', '18', 'italic'))
        canvas.create_text(250,200, text='Open Accounting', font=('Helvetica', '32', 'bold italic' ))
        canvas.create_text(250,239, text='by Medmatix Analytics', font=('Helvetica', '18', 'italic'))
         
        canvas.grid() #.pack(side = tk.TOP, expand=True, fill=tk.BOTH)
        
        root.mainloop()
        
         
if __name__ == '__main__':
    spl = splashScreen()

     

#===============================================================================
# root=tk.Tk()
# image = Image.open("medmatix_tilt.png")
# canvas=Canvas(root, height=200, width=200)
# basewidth = 150
# wpercent = (basewidth / float(image.size[0]))
# hsize = int((float(image.size[1]) * float(wpercent)))
# image = image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
# photo = ImageTk.PhotoImage(image)
# item4 = canvas.create_image(100, 80, image=photo)
# 
# canvas.pack(side = tk.TOP, expand=True, fill=tk.BOTH)
# root.mainloop()
#===============================================================================