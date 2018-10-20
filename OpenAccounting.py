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
from tkinter import Canvas
import sys

# #####################
# Classes
# #####################
class insertJournalForm(object):
    '''
    class insertion Form to build and display for journal access
    @summary: A form to collect journal item data to add to journal table,. A Part of Accounting System application
    @see: refer to main module (AccountingSystem) documentation
    created: Oct 17, 2018
        @
    '''
    def __init__(self, goal):
        '''
        Constructor for Add data dialog window
        '''
        
        # Create instance
        self.goal=goal
        self.frm = tk.Tk()
        # Add a title
        self.frm.title("Add a Movie")
        self.journalForm()
        self.frm.mainloop() 
        
    
        

    def journalForm(self):
        ''' The form for journal access'''
        lbfr = ttk.LabelFrame(self.frm, text=' Input Form ')
        lbfr.grid(column=0, row=0, padx=10, pady=10, sticky='W')
        self.lbl0 = tk.Label(lbfr, text="Transaction").grid(column=0, row=0)
        self.e0 = tk.Entry(lbfr, width=16)
        self.e0.grid(column=1, row=0, padx=5, pady=4, sticky='W')
        self.lbl1 = tk.Label(lbfr, text="Date-Time").grid(column=0, row=1)
        self.e1 = tk.Entry(lbfr,width=16)
        self.e1.grid(column=1, row=1, padx=5, pady=4, sticky='W')
        self.lbl2 = tk.Label(lbfr, text="Description").grid(column=0, row=2)
        self.e2 = tk.Entry(lbfr,width=50)
        self.e2.grid(column=1, row=2, padx=5, pady=4, sticky='W')
        self.lbl3 = tk.Label(lbfr, text="DebitAccount").grid(column=0, row=3)
        self.e3 = tk.Entry(lbfr,width=4)
        self.e3.grid(column=1, row=3, padx=5, pady=4, sticky='W')
        self.lbl4 = tk.Label(lbfr, text="DebitAmount").grid(column=0, row=4)
        self.e4 = tk.Entry(lbfr,width=8)
        self.e4.grid(column=1, row=4, padx=5, pady=4, sticky='W')
        self.lbl5 = tk.Label(lbfr, text="CreditAccount").grid(column=0, row=5)
        self.e5 = tk.Entry(lbfr,width=4)
        self.e5.grid(column=1, row=5, padx=5, pady=4, sticky='W')
        self.lbl6 = tk.Label(lbfr, text="CreditAmount").grid(column=0, row=6)
        self.e6 = tk.Entry(lbfr,width=8)
        self.e6.grid(column=1, row=6, padx=5, pady=4, sticky='W')
        
        self.btn1 = ttk.Button(lbfr, text="Commit", command=lambda: self.on_click()).grid(column=0,row=7,padx=8, pady=4, sticky='W')
        self.btn2 = ttk.Button(lbfr, text="Cancel", command=lambda: self.on_cancel()).grid(column=1,row=7,padx=8, pady=4, sticky='W')
        
    def on_click(self):
        # get debit account balance
        account = int(self.e3.get())        
        debitBalance = 1000.00 #AccountingSystem.getLedgerBalance(self,account)
        # get creit  account balance
        account = int(self.e5.get())
        creditBalance = 1000.00 #AccountingSystem.getLedgerBalance(self,account)
        newDBalance=(debitBalance + float(self.e4.get()))
        newCBalance=(creditBalance + float(self.e6.get()))
        posted = 1
        jrow = (int(self.e0.get()), self.e1.get(), self.e2.get(), int(self.e3.get()), float(self.e4.get()), int(self.e5.get()),float(self.e6.get()), posted)
        lDRow = (int(self.e3.get()),int(self.e0.get()), float(self.e4.get()), newDBalance)
        lCRow = (int(self.e5.get()),int(self.e0.get()), float(self.e6.get()), newCBalance)
        ''' the activation of the form'''
        if (abs(int(self.e6.get())) == abs(int(self.e4.get()))):
            print("commit")
            print(jrow)
            AccountingSystem.insertJournalEntry(self, jrow)
            print(lDRow)
            lrow = lDRow
            AccountingSystem.insertLedgerEntry(self, lrow)
            print(lCRow)
            lrow = lCRow
            AccountingSystem.insertLedgerEntry(self, lrow)
            print("journalForm closed")
            self.frm.destroy()
        else:
            print("ERROR: Credits and Debits do not balance")
        
    def on_cancel(self):
        print("Cancelled action")
        self.frm.destroy()
        
class insertChartForm(object):
    '''
    class insertion Form for build and display Chart of Account access
    @summary: A form to collect movie data to add to list, and send to addMovietoList function. A Part of MomsMovies application
    @see: refer to main module (MomsMovies) documentation
    created: Oct 14, 2018
        @
    '''
    def __init__(self, goal):
        '''
        Constructor for Add New Account dialog window
        '''
        
        # Create instance
        self.frm = tk.Tk()
        # Add a title
        self.frm.title("Add Entry into Chart of Accounts")
        self.chartForm()
        self.frm.mainloop() 
                
    def chartForm(self):
        ''' The form for Chart of Account access '''
        lbfr = ttk.LabelFrame(self.frm, text=' Input Form ')
        lbfr.grid(column=0, row=0, padx=10, pady=10, sticky='W')
        self.lbl0 = tk.Label(lbfr, text="Account").grid(column=0, row=0)
        self.e0 = tk.Entry(lbfr, width=16)
        self.e0.grid(column=1, row=0, padx=5, pady=4, sticky='W')
        self.lbl2 = tk.Label(lbfr, text="Name").grid(column=0, row=2)
        self.e2 = tk.Entry(lbfr,width=50)
        self.e2.grid(column=1, row=2, padx=5, pady=4, sticky='W')
        self.lbl3 = tk.Label(lbfr, text="Type of Account").grid(column=0, row=3)
        self.e3 = tk.Entry(lbfr,width=6)
        self.e3.grid(column=1, row=3, padx=5, pady=4, sticky='W')
                
        self.btn1 = ttk.Button(lbfr, text="Commit", command=lambda: self.on_click()).grid(column=0,row=7,padx=8, pady=4, sticky='W')
        self.btn2 = ttk.Button(lbfr, text="Cancel", command=lambda: self.on_cancel()).grid(column=1,row=7,padx=8, pady=4, sticky='W')
        
    def on_click(self):
        # Check if account exits
        account = int(self.e0.get())
        existAccount = AccountingSystem.existChartAccount(self,account)
        row = (int(self.e0.get()), self.e2.get(), self.e3.get())
        ''' the activation of the form'''
        if (not existAccount):
            print("commit")
            print(row)
            AccountingSystem.insertChartEntry(self, row)
            print("journalForm closed")
            self.frm.destroy()
        else:
            print("ERROR: An Account Already Exists with this Number")
        
    def on_cancel(self):
        print("Cancelled action")
        self.frm.destroy()   
 
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
        Return all Chart of Accounts
        '''
        chart = list() 
        db = sqlite3.connect('OpenAccounting.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM chart ORDER BY Account")
        for row in cursor:            
            chart.append(row)        
        db.close()
        return chart
    
    def existChartAccount(self, account):
        '''
        '''
        pass
    
    def getLedgerAccount(self,account):
        '''
        Return all entries for an account
        '''
        pass
    
    def getJournalAccount(self,dates):
        '''
        Return all of a journal date range
        '''
        pass
    def insertJournalEntry(self, jrow):
        '''
        Insert an entry into Journal
        '''
        pass
    
    def insertLedgerEntry(self, lrow):
        '''
        Post journal debit or credit to Ledger
        '''
        pass
    
    def insertChartAccount(self):
        '''
        Insert an entry into Journal
        '''
        pass
    
    def getLedgerBalance(self,laccount):
        '''
        Get LAST ledger balance for specified account
        '''
        pass
    
        # return balance
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
        self.scrolList3.delete(1.0,tk.END)
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
            
    def do_showLedger(self, account):        
        self.scrolList2.delete(1.0,tk.END)
        listAll = self.getLedgerAccount(account)
        for row in listAll:
            #self.do_formatedList(row) 
            self.scrolList2.insert(tk.END,row[0])
            self.scrolList2.insert(tk.END,'\t    ')
            mName = row[1]
            nameLength = len(mName)+(50-len(mName))
            mName = mName.ljust(nameLength)
            self.scrolList2.insert(tk.END,mName)
            self.scrolList2.insert(tk.END,'\t  ')
            mType = row[2]
            typeLength = len(row[2])+(12-len(row[2]))
            mType = mType.ljust(typeLength)
            self.scrolList2.insert(tk.END,mType)
            self.scrolList2.insert(tk.END,'\n')
            
    def do_showJournal(self, dates):
        '''
        Show formatted journal
        '''  
        self.scrolList1.delete(1.0,tk.END)
        listAll = self.getJournalAccount(dates)
        for row in listAll:
            #self.do_formatedList(row) 
            self.scrolList1.insert(tk.END,row[0])
            self.scrolList1.insert(tk.END,'\t    ')
            mName = row[1]
            nameLength = len(mName)+(50-len(mName))
            mName = mName.ljust(nameLength)
            self.scrolList1.insert(tk.END,mName)
            self.scrolList1.insert(tk.END,'\t  ')
            mType = row[2]
            typeLength = len(row[2])+(12-len(row[2]))
            mType = mType.ljust(typeLength)
            self.scrolList1.insert(tk.END,mType)
            self.scrolList1.insert(tk.END,'\n')
                
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
        tabControl.add(tab5, text='Accounting Memo')
        
        tab6 = ttk.Frame(tabControl)
        tabControl.add(tab6, text='Maintenance')
        
        tabControl.grid()  # Pack to make visible
        
        frm1 = ttk.Labelframe(tab1, text='General Journal', width= 400, height=600)
        frm1.grid()
        frm1a = ttk.Labelframe(frm1, width= 400, height=500)
        frm1a.grid()
        self.updateJournal = ttk.Button(frm1a, text="Update Display", command=lambda: self.do_showJournal()).grid(column=0,row=0,padx=4, pady=4)
        self.printJournal = ttk.Button(frm1a, text="PRINT").grid(column=1,row=0,padx=4, pady=4)
        self.newEntry = ttk.Button(frm1a, text="New Entry").grid(column=2,row=0,padx=4, pady=4)
        ttk.Label(frm1, text="Account \tTransaction\t Amount \tBalance \t\t").grid(column=0, row=1, padx=4, pady=4,sticky='W')
        scrolW1  = 80; scrolH1  =  40
        self.scrolList1 = scrolledtext.ScrolledText(frm1, width=scrolW1, height=scrolH1, wrap=tk.WORD)
        self.scrolList1.grid(column=0, row=2, padx=4, pady=4, sticky='WE', columnspan=3)
        # self.do_showJournal(dates)
        
        frm2 = ttk.Labelframe(tab2, text='General Ledger', width= 400, height=600)
        frm2.grid()
        frm2a = ttk.Labelframe(frm2, width= 400, height=500)
        frm2a.grid()
        self.updateLedger = ttk.Button(frm2a, text="Update Display", command=lambda: self.do_showChart()).grid(column=0,row=0,padx=4, pady=4)
        self.printLedger = ttk.Button(frm2a, text="PRINT").grid(column=1,row=0,padx=4, pady=4)
        self.newAccount = ttk.Button(frm2a, text="Show Another").grid(column=2,row=0,padx=4, pady=4)
        ttk.Label(frm2, text="Account \tTransaction\t Amount \tBalance \t\t").grid(column=0, row=1, padx=4, pady=4,sticky='W')
        scrolW1  = 80; scrolH1  =  40
        self.scrolList2 = scrolledtext.ScrolledText(frm2, width=scrolW1, height=scrolH1, wrap=tk.WORD)
        self.scrolList2.grid(column=0, row=2, padx=4, pady=4, sticky='WE', columnspan=3)
        # self.do_showLedger(account)
        
        ## Set tab and contents for the CHar of Accounts
        frm3 = ttk.Labelframe(tab3, text='Chart of Accounts', width= 400, height=600)
        frm3.grid()
        frm3a = ttk.Labelframe(frm3, width= 400, height=500)
        frm3a.grid()
        self.updateChart = ttk.Button(frm3a, text="Update Display", command=lambda: self.do_showChart()).grid(column=0,row=0,padx=4, pady=4)
        self.printChart = ttk.Button(frm3a, text="PRINT").grid(column=1,row=0,padx=4, pady=4)
        self.newAccount = ttk.Button(frm3a, text="New Account").grid(column=2,row=0,padx=4, pady=4)
        ttk.Label(frm3, text="Account \t Name \t\t\t\t\t\t\t\t\tType\t\t").grid(column=0, row=1, padx=4, pady=4,sticky='W')
        scrolW1  = 80; scrolH1  =  40
        self.scrolList3 = scrolledtext.ScrolledText(frm3, width=scrolW1, height=scrolH1, wrap=tk.WORD)
        self.scrolList3.grid(column=0, row=2, padx=4, pady=4, sticky='WE', columnspan=3)
        self.do_showChart()
        
        frm4 = ttk.Labelframe(tab4, text='Accounting Reports', width= 500, height=600)
        frm4.grid(padx=8, pady=4)
        reportWin = Canvas(frm4, width=450, height=550, offset='20,10')
        reportWin.grid(column=0, row=0, padx=8,pady=4)
        reportWin.create_text(225,10, text="This is a dummy accounting report on the canvas") 
        
        frm5 = ttk.Labelframe(tab5, text='Associated Journal or Ledger Note', width= 400, height=600)
        frm5.grid()             
        scrolW1  = 80; scrolH1  =  20
        self.scr_memo = scrolledtext.ScrolledText(frm5, width=scrolW1, height=scrolH1, wrap=tk.WORD)
        self.scr_memo.grid(column=0, row=6, padx=4, pady=4, sticky='WE', columnspan=3)
        
        self.memoctl = ttk.LabelFrame(frm5, width=56)
        self.memoctl.grid(column=0, row=0, padx=8, pady=4, sticky='W') 
        self.action_clrnotes = ttk.Button(self.memoctl, text="NEW MEMO")
        self.action_clrnotes.grid(column=0, row=0, padx=4, pady=6)        
        self.action_prtnotes = ttk.Button(self.memoctl, text="PRINT MEMO")
        self.action_prtnotes.grid(column=1, row=0, padx=4, pady=6)        
        self.action_savenotes = ttk.Button(self.memoctl, text="SAVE MEMO")
        self.action_savenotes.grid(column=3, row=0, padx=4, pady=6)
        self.action_loadnotes = ttk.Button(self.memoctl, text="GET ANOTHER")
        self.action_loadnotes.grid(column=4, row=0, padx=4, pady=6)
        
        frm6 = ttk.Labelframe(tab6, text='System Maintenance', width= 400, height=600)
        frm6.pack()
        
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
        entryMenu = Menu(menuBar, tearoff=0)
        entryMenu.add_command(label="Journal Entry", command=lambda: insertJournalForm(self))
        entryMenu.add_command(label="New Account", command=lambda: insertChartForm(self))
        entryMenu.add_command(label="Make Memo")
        entryMenu.add_separator()
        entryMenu.add_command(label="Trial Balance")
        entryMenu.add_command(label="End of Year")
        menuBar.add_cascade(label="Entry", menu=entryMenu)
        
        # Add an Edit Menu
        reportMenu = Menu(menuBar, tearoff=0)
        reportMenu.add_command(label="Balance Sheet")
        reportMenu.add_command(label="Ledger Account")
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
    w = asys.win.winfo_screenwidth()/2
    h = asys.win.winfo_screenheight()
    asys.win.geometry("%dx%d+0+0" % (w, h))
    asys.win.mainloop()