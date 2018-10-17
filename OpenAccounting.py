'''
OpenAccounting
Created on Oct 17, 2018
@summary: An open source double entry accounting system based on SQLite and written in python
@note: Project pages at: https://medmatix.github.io/Accounting-System/
@author: david
@copyright: David A York 2018
@license: MIT
@contact: http://crunches-data.appspot.com/contact.html
'''

# #####################
# Imports
# #####################
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as mBox
from tkinter import simpledialog
import sys

# #####################
# Classes
# #####################

class AccountingSystem():
    '''
    Class for the Main Application
    '''


    def __init__(self):
        '''
        Constructor Setup the Application
        '''
        # Create instance
        self.win = tk.Tk()
           
        # Add a title
        self.win.title("Open Accounting")
        # Add a icon
        if not sys.platform.startswith('linux'):
            self.win.iconbitmap('./images/medmatix_tilt.ico')
            
        # Initialize widgets
        self.createWidgets()
    
    
    
    # #################################
    # Database Functions
    # #################################   
    def createAccounts(self):
        '''
        Create New Database and Tables if not existing
        '''
        db = sqlite3.connect('OpenAccounting.db')
        db.execute('''CREATE TABLE IF NOT EXISTS journal 
            (Transact INTEGER PRIMARY KEY NOT NULL, 
            Date DATETIME NOT NULL, 
            Description STRING(50) NOT NULL, 
            DebitAccount INT(4) NOT NULL,  
            CreditAccount INT(4) NOT NULL, 
            Amount DECIMAL NOT NULL)''')
        
        db.execute('''CREATE TABLE IF NOT EXISTS ledger 
            (Account INTEGER     NOT NULL, 
            Transact INTEGER     KEY NOT NULL, 
            Amount REA    NOT NULL, 
            Balance REAL    NOT NULL)''')
        
        db.execute('''CREATE TABLE IF NOT EXISTS chart 
            (Account INTEGER PRIMARY KEY    NOT NULL, 
            Name STRING(60)    NOT NULL, 
            Type STRING(10)    NOT NULL)''')
        
        db.close()
    def getChartAccounts(self):
        '''
        Return all records
        '''
        chart = list() 
        db = sqlite3.connect('OpenAccounting.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM chart ORDER BY Account")
        for row in cursor:            
            chart.append(row)        
        db.close()
        return chart
    
    # #################################
    # Other functions 
    # #################################   
    # -- Exit GUI cleanly -------------
    def _quit(self):
        self.win.quit()
        self.win.destroy()
        print('run is done, exited normally!')
        exit() 
        
    def do_showChart(self):
        listAll = self.getChartAccounts()
        for row in listAll:
            #self.do_formatedList(row) 
            self.scrolList3.insert(tk.END,row[0])
            self.scrolList3.insert(tk.END,'\t    ')
            mName = row[1]
            nameLength = len(mName)+(50-len(mName))
            mName = mName.ljust(nameLength)
            self.scrolList3.insert(tk.END,mName)
            self.scrolList3.insert(tk.END,'\t  ')
            mType = row[2]
            typeLength = len(row[2])+(12-len(row[2]))
            mType = mType.ljust(typeLength)
            self.scrolList3.insert(tk.END,mType)
            self.scrolList3.insert(tk.END,'\n') 
            
            
    # #################################
    # Create GUI Functions
    # ################################   
    def createWidgets(self):
        '''
        Create the GUI interfaces
        '''
        # Messages and Dialogs -------------------------------------------
        def info(self):
            mBox.showinfo('About OpenAccounting, ' , 'Application to Perform Basic GAAP Accounting functions.\n\n (c) David A York, 2018\n http:crunches-data.appspot.com \nVersion: 0.0, development version 0.01a \nlicense: MIT')
        
        # Tab Controls created here --------------------------------------
        tabControl = ttk.Notebook(self.win)     # Create Tab Controls

        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1, text='Journal')
                
        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2, text='Ledger')
        
        tab3 = ttk.Frame(tabControl)
        tabControl.add(tab3, text='Chart of Accounts')
        
        tab4 = ttk.Frame(tabControl)
        tabControl.add(tab4, text='Reports')
        
        tab5 = ttk.Frame(tabControl)
        tabControl.add(tab5, text='Maintenance')
        
        tabControl.pack(expand=1, fill="both")  # Pack to make visible
        
        frm1 = ttk.Labelframe(tab1, text='General Journal', width= 400, height=600)
        frm1.pack()
        
        frm2 = ttk.Labelframe(tab2, text='General Ledger', width= 400, height=600)
        frm2.pack()
        
        frm3 = ttk.Labelframe(tab3, text='Chart of Accounts', width= 400, height=600)
        frm3.pack()
        ttk.Label(frm3, text="Account \t Name \t\t\t\t\t\t\t\t\tType\t\t").grid(column=0, row=0, padx=4, pady=4,sticky='W')
        scrolW1  = 80; scrolH1  =  40
        self.scrolList3 = scrolledtext.ScrolledText(frm3, width=scrolW1, height=scrolH1, wrap=tk.WORD)
        self.scrolList3.grid(column=0, row=1, padx=4, pady=4, sticky='WE', columnspan=3)
        
        frm4 = ttk.Labelframe(tab4, text='Accounting Reports', width= 400, height=600)
        frm4.pack()
        
        frm5 = ttk.Labelframe(tab5, text='System Maintenance', width= 400, height=600)
        frm5.pack()
        
        # meubar created here --------------------------------------------
        menuBar = Menu(self.win)
        self.win.config(menu=menuBar)
        # Add menu items
        # Add System Menu
        sysMenu = Menu(menuBar, tearoff=0)
        sysMenu.add_command(label="New", command=lambda: self.createAccounts())
        sysMenu.add_command(label="Open")
        sysMenu.add_command(label="Save")
        sysMenu.add_command(label="Print")
        sysMenu.add_command(label="Copy Database")
        sysMenu.add_separator()
        sysMenu.add_command(label="Exit", command=self._quit)
        menuBar.add_cascade(label="System", menu=sysMenu)
        
        # Add an Edit Menu
        editMenu = Menu(menuBar, tearoff=0)
        editMenu.add_command(label="Cut")
        editMenu.add_command(label="Copy")
        editMenu.add_command(label="Paste")
        editMenu.add_command(label="Delete")
        editMenu.add_command(label="Clear")
        editMenu.add_command(label="Select")
        editMenu.add_separator()
        editMenu.add_command(label="Options")
        menuBar.add_cascade(label="Edit", menu=editMenu)
        
        # Add an Edit Menu
        reportMenu = Menu(menuBar, tearoff=0)
        reportMenu.add_command(label="Balance Sheet")
        reportMenu.add_command(label="Ledger Account", command=lambda: self.do_showChart())
        reportMenu.add_command(label="Journal Transactions")
        reportMenu.add_command(label="Income Report")
        reportMenu.add_command(label="Expense Report")
        reportMenu.add_command(label="Payroll Report")
        reportMenu.add_command(label="Inventory Report")
        menuBar.add_cascade(label="Reports", menu=reportMenu)
        
        # Add a Help Menu 
        helpMenu = Menu(menuBar, tearoff=0)
        helpMenu.add_command(label="Context Help")
        helpMenu.add_command(label="Documentation")
        helpMenu.add_command(label="About", command=lambda: info(self))
        menuBar.add_cascade(label="Help", menu=helpMenu)
        
if __name__ == '__main__':
    asys = AccountingSystem()
    w = asys.win.winfo_screenwidth()
    h = asys.win.winfo_screenheight()
    asys.win.geometry("%dx%d+0+0" % (w, h))
    asys.win.mainloop()