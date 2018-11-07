'''
Created on Nov 6, 2018
@summary: The module contains the code needed to build and present the splash screen at start-up
@author: david york
'''

# #############################################
# imports for the splash code functionality
# #############################################
import os
import pathlib
import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from tkinter import font
import PIL
from PIL import Image, ImageTk
import time

class splashScreen():
    '''
    The splashScreen class
    '''
     
    def __init__(self):
        '''
        splashScreen constructor
        '''
        
        self.splash()        
        
        
        
        
        #self.splashfrm.mainloop()
     
    def splash(self):
        '''
        The splash interface code
        '''
        self.root = tk.Tk()
        
        #root.title('Splash')
        #root.wm_attributes('-fullscreen','true')
        #eliminate the titlebar
        self.root.overrideredirect(1)
        
        image = Image.open("medmatix_tilt.png")
        f = tk.Frame(self.root, highlightthickness=0 ).grid()
        canvas=Canvas(f, height=500, width=500, highlightthickness=0, background='SteelBlue3')
        basewidth = 220
        wpercent = (basewidth / float(image.size[0]))
        hsize = int((float(image.size[1]) * float(wpercent)))
        image = image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(250,250, image=photo)
        canvas.create_text(250,161, text='Welcome to', font=('Helvetica', '18', 'italic'))
        canvas.create_text(250,200, text='Open Accounting', font=('Helvetica', '32', 'bold italic' ))
        canvas.create_text(250,239, text='by Medmatix Analytics', font=('Helvetica', '18', 'italic'))
        canvas.create_text(250,470, text='(c)copyright: D A York, Medmatix 2018', font=('Times', '9', 'italic'), fill='white')         
        canvas.grid() #.pack(side = tk.TOP, expand=True, fill=tk.BOTH)
        f2 = f = tk.Frame(self.root, highlightthickness=0, width=500)
        f2.configure(bg='SteelBlue3')
        f2.grid()
        self.btn1 = ttk.Button(f2, text="OK", command=lambda: self.on_OKkill()).grid(column=0,row=2,padx=212, pady=4)
        # Acknowledgement of source:
        # Note the functionality centering the splash window was found in a discussion on stackoverflow blog:
        # https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
        self.root.eval('tk::PlaceWindow %s center' % self.root.winfo_toplevel())
        self.root.mainloop()
        
    def on_OKkill(self):
        self.root.quit()     # stops mainloop
        self.root.destroy()
        
        
        
if __name__ == '__main__':
    spl = splashScreen()