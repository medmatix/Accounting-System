'''
OpenAccounting
Created on Oct 17, 2018
@summary: An open source double entry accounting system based on SQLite and written in python
@note: Project pages at: https://medmatix.github.io/Accounting-System/
@author: David York
@copyright: David A York 2018
@license: MIT
@contact: http://crunches-data.appspot.com/contact.html
'''

# #####################
# Imports
# #####################
# Standard library and third party imports
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as mBox
from tkinter import simpledialog
from tkinter import Canvas
from tkinter import font
import sys

# Custom module imports
from Tooltips import createToolTip, ToolTip as tip

# #######################################################
# Classes, Independently constructed Forms, Dialogs etc
# #######################################################
'''
Classes, External, independently constructed Forms, Dialogs etc
'''
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
        self.frm.title("Insert a Journal Entry")
        self.journalForm()
        self.frm.mainloop() 
        
    
        

    def journalForm(self):
        ''' The form for journal access'''
        lbfr = ttk.LabelFrame(self.frm, text=' Input Form ')
        lbfr.grid(column=0, row=0, padx=10, pady=10, sticky='W')
        self.lbl0 = tk.Label(lbfr, text="Transaction").grid(column=0, row=0)
        self.e0 = tk.Entry(lbfr, width=16)
        self.e0.grid(column=1, row=0, padx=5, pady=4, sticky='W')
        self.lbl1 = tk.Label(lbfr, text="Date").grid(column=0, row=1)
        self.e1 = tk.Entry(lbfr,width=10)
        self.e1.grid(column=1, row=1, padx=5, pady=4, sticky='W')
        self.lbl2 = tk.Label(lbfr, text="Time").grid(column=0, row=2)
        self.e2 = tk.Entry(lbfr,width=9)
        self.e2.grid(column=1, row=2, padx=5, pady=4, sticky='W')
        self.lbl3 = tk.Label(lbfr, text="Description").grid(column=0, row=3)
        self.e3 = tk.Entry(lbfr,width=50)
        self.e3.grid(column=1, row=3, padx=5, pady=4, sticky='W')
        self.lbl4 = tk.Label(lbfr, text="DebitAccount").grid(column=0, row=4)
        self.e4 = tk.Entry(lbfr,width=4)
        self.e4.grid(column=1, row=4, padx=5, pady=4, sticky='W')
        self.lbl5 = tk.Label(lbfr, text="DebitAmount").grid(column=0, row=5)
        self.e5 = tk.Entry(lbfr,width=8)
        self.e5.grid(column=1, row=5, padx=5, pady=4, sticky='W')
        self.lbl6 = tk.Label(lbfr, text="CreditAccount").grid(column=0, row=6)
        self.e6 = tk.Entry(lbfr,width=4)
        self.e6.grid(column=1, row=6, padx=5, pady=4, sticky='W')
        self.lbl7 = tk.Label(lbfr, text="CreditAmount").grid(column=0, row=7)
        self.e7 = tk.Entry(lbfr,width=8)
        self.e7.grid(column=1, row=7, padx=5, pady=4, sticky='W')
        
        self.btn1 = ttk.Button(lbfr, text="Commit", command=lambda: self.on_click()).grid(column=0,row=9,padx=8, pady=4, sticky='W')
        self.btn2 = ttk.Button(lbfr, text="Cancel", command=lambda: self.on_cancel()).grid(column=1,row=9,padx=8, pady=4, sticky='W')
        
    def on_click(self):
        '''Save new Journal Entry and update Ledger accounts
        '''
        # get debit account balance
        daccount = int(self.e4.get())   
        txType = 'DEBIT'     
        debitBalance = AccountingSystem.getAccountBalance(self,daccount)
        debitSgn = AccountingSystem.getsgnAdjust(self,daccount,txType)
        debitAmount = debitSgn * round(float(self.e7.get()),2)
        # get credit  account balance
        caccount = int(self.e6.get())
        txType = 'CREDIT'         
        creditBalance= AccountingSystem.getAccountBalance(self, caccount)
        creditSgn = AccountingSystem.getsgnAdjust(self, caccount,txType)
        creditAmount = creditSgn * round(float(self.e5.get()),2)
        newDBalance=(debitBalance + debitAmount)
        newCBalance=(creditBalance + creditAmount)
        posted = 1
        jrow = (int(self.e0.get()), self.e1.get(), self.e2.get(), self.e3.get(), int(self.e4.get()), debitAmount, int(self.e6.get()),creditAmount, posted)
        lDRow = (int(self.e4.get()),int(self.e0.get()), debitAmount, newDBalance)
        lCRow = (int(self.e6.get()),int(self.e0.get()), creditAmount, newCBalance)
        ''' the activation of the form'''
        if (abs(creditAmount) == abs(debitAmount)):
            print("commit")
            print(jrow)
            AccountingSystem.insertJournalEntry(self, jrow)
            print(lDRow)
            lrow = lDRow
            AccountingSystem.insertLedgerEntry(self, lrow)
            print(lCRow)
            lrow = lCRow
            AccountingSystem.insertLedgerEntry(self, lrow)
            AccountingSystem.updateChartBalance(self, daccount, newDBalance)
            AccountingSystem.updateChartBalance(self, caccount, newCBalance)
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
        self.lbl4 = tk.Label(lbfr, text="Starting Balance").grid(column=0, row=4)
        self.e4 = tk.Entry(lbfr,width=10)
        self.e4.grid(column=1, row=4, padx=5, pady=4, sticky='W')
                
        self.btn1 = ttk.Button(lbfr, text="Commit", command=lambda: self.on_click()).grid(column=0,row=7,padx=8, pady=4, sticky='W')
        self.btn2 = ttk.Button(lbfr, text="Cancel", command=lambda: self.on_cancel()).grid(column=1,row=7,padx=8, pady=4, sticky='W')
        
    def on_click(self):
        account = self.e0.get()
        if(account in (100,200,300,400,500,120,220,320)):
            print("ERROR, account is system reserved account, do not use.")
            self.on_cancel()
        # Check if account exits
        if (self.e0.get() == ''): 
            self.on_cancel()
        else:    
            account = int(self.e0.get())
            existAccount = AccountingSystem.existChartAccount(self,account)
            row = (int(self.e0.get()), self.e2.get(), self.e3.get(), self.e4.get())
            ''' the activation of the form'''
            if (not existAccount):
                print("commit")
                print(row)
                AccountingSystem.insertChartAccount(self, row)
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
        @summary: Creates a fully new accounting set-up. The System accounts are 
            fixed by accounting convention and may not be changed of reused for 
            other purposes.
        @warning: Will not allow overwriting so any old data tables should be moved from the directory.
        '''
        # Check that a fully new set-up is intended
        proceedAnswer = mBox.askyesno("Initial Set-up","This is The New System Set-up.\nThere should be no old data tables in directory,\n Proceed?")
        if (not proceedAnswer):
            print('aborted new setup')
            return
        # Some local, set-up related message boxes
        def setupError(self):
            mBox.showerror(title='Set-up Error', message='Chart of Accounts already populated, you may not overwrite')
        def setupInfo(self):
            mBox.showinfo('Set-up Information' , 'Adding System Accounts to Chart of Accounts.') 
        
        #If Not Existing, Create batabase, data tables and system ledger accounts  
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
            Amount REAL    NOT NULL, 
            Balance REAL    NOT NULL)''')
        
        db.execute('''CREATE TABLE IF NOT EXISTS chart 
            (Account INTEGER PRIMARY KEY    NOT NULL, 
            Name STRING(60)    NOT NULL, 
            Type STRING(10)    NOT NULL,
            Balance REAL       NOT NULL)''')
        
        db.execute('''CREATE TABLE IF NOT EXISTS accountmemos 
            (MemoID INTEGER PRIMARY KEY    NOT NULL,
            Transact INTEGER    NOT NULL,
            Date DATETIME    NOT NULL, 
            Memo BLOB    NOT NULL)''')
        
        # Check if Chart of Accounts already set-up, may not be overwritten
        count = db.execute("SELECT count(Account) FROM chart")
        for row in count:
            tableFull=bool(row[0])
        if (not tableFull):
            setupInfo(self)
            db.execute('''INSERT INTO chart VALUES (100, "ASSETS", "DEBIT", 0),
                (120, "RECEIVABLES","DEBIT",0),
                (200, "LIABILITIES","CREDIT",0), 
                (220, "PAYABLES","CREDIT",0), 
                (300, "EQUITY","CREDIT",0),  
                (400, "REVENUE","CREDIT",0),
                (500, "EXPENSES","DEBIT",0)        
                ''')      
            db.commit()  
        else:
            setupError(self)
        
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
        ledger = list() 
        db = sqlite3.connect('OpenAccounting.db')
        cursor = db.cursor()
        if account == 0:
            cursor.execute("SELECT * FROM ledger ORDER BY Account")
        else:
            cursor.execute("SELECT * FROM ledger WHERE Account = {} ORDER BY Transact".format(account,))
        for row in cursor:            
            ledger.append(row)        
        db.close()
        return ledger
    
    def getJournalEntries(self, jDates):
        '''
        Return all of a journal date range
        '''
        journal = list() 
        db = sqlite3.connect('OpenAccounting.db')
        cursor = db.cursor()
        if jDates == (0,0):
            cursor.execute("SELECT * FROM journal ORDER BY Date")
        else:
            cursor.execute("SELECT * FROM journal WHERE Date = {} ORDER BY Transact".format(jDates[0]))
        for row in cursor:            
            journal.append(row)        
        db.close()
        return journal
    
    def insertJournalEntry(self, jrow):
        '''
        Insert an entry into Journal
        '''
        db = sqlite3.connect('OpenAccounting.db')
        db.execute("INSERT INTO journal VALUES {}".format(jrow))
        db.commit()
        db.close()
        
    def insertLedgerEntry(self, lrow):
        '''
        Post journal debit or credit to Ledger
        '''
        db = sqlite3.connect('OpenAccounting.db')
        db.execute("INSERT INTO ledger VALUES {}".format(lrow))
        db.commit()
        db.close()
    
    def insertChartAccount(self, row):
        '''
        Update an Balance into Chart Account
        '''
        db = sqlite3.connect('OpenAccounting.db')
        db.execute("INSERT INTO chart VALUES {}".format(row))
        db.close()
    
    def updateChartBalance(self, account, balance):  # Account balance in chart of accounts
        db = sqlite3.connect('OpenAccounting.db')
        cursor = db.cursor()
        cursor.execute("UPDATE Chart SET Balance = {} WHERE Account = {}".format(balance, account))
        db.commit()
        db.close()
        
    def getAccountBalance(self,laccount):
        '''
        Get LAST ledger balance for specified account
        '''
        balance = list() 
        db = sqlite3.connect('OpenAccounting.db')
        cursor = db.cursor()
        cursor.execute("SELECT Balance FROM Chart WHERE Account = {}".format(laccount,))
        for row in cursor:            
            balance.append(row) 
        oldBalance = balance[0][0]     
        db.close()
        return oldBalance
    
    def getsgnAdjust(self, laccount, txType):
        actyType = list()
        db = sqlite3.connect('OpenAccounting.db')
        cursor = db.cursor()
        cursor.execute("SELECT actyType FROM Chart WHERE Account = {}".format(laccount,))
        for row in cursor:            
            actyType.append(row)
        if (txType=='DEBIT' and actyType=='DEBIT') or (txType=='CREDIT' and actyType=='CREDIT' ):            
            db.close()
            return 1
        else:
            db.close()            
            return -1
        
        # return balance
        
    def packDatabase(self):
        db = sqlite3.connect('OpenAccounting.db')
        mBox.showinfo('Maintenance' , 'PACKING Database for Clean-up, Defragmentation and Improved Performance.')
        db.execute('VACUUM')        
        db.close()
        
    # #################################
    # GUI callback functions 
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
            nameLength = len(mName)+(40-len(mName))
            mName = mName.ljust(nameLength)
            self.scrolList3.insert(tk.END,mName)
            self.scrolList3.insert(tk.END,'  ')
            mType = row[2]
            typeLength = len(row[2])+(12-len(row[2]))
            mType = mType.ljust(typeLength)
            self.scrolList3.insert(tk.END,mType)
            self.scrolList3.insert(tk.END,'\t') 
            mBalance = str(round(row[3],2))
            balanceLength = len(mBalance)+(8-len(mBalance))
            mBalance = mBalance.rjust(balanceLength)
            self.scrolList3.insert(tk.END,mBalance)
            self.scrolList3.insert(tk.END,'\n')
            
    def do_showLedger(self, account):   
        self.scrolList2.delete(1.0,tk.END)
        account = int(account)

        listAll = self.getLedgerAccount(account)
        for row in listAll:
            #self.do_formatedList(row) 
            self.scrolList2.insert(tk.END,row[0])
            self.scrolList2.insert(tk.END,'\t    ')
            mTransact = str(row[1])
            transactLength = len(mTransact)+(10-len(mTransact))
            mTransact = mTransact.ljust(transactLength)
            self.scrolList2.insert(tk.END,mTransact)
            self.scrolList2.insert(tk.END,'\t  ')
            mAmount = str(row[2])
            amountLength = len(mAmount)+(8-len(mAmount))
            mAmount = mAmount.ljust(amountLength)
            self.scrolList2.insert(tk.END,mAmount)
            self.scrolList2.insert(tk.END,'\t')
            mBalance = str(round(row[3],2))
            balanceLength = len(mBalance)+(8-len(mBalance))
            mBalance = mBalance.rjust(balanceLength)
            self.scrolList2.insert(tk.END,mBalance)
            self.scrolList2.insert(tk.END,'\n')
            
    def do_showJournal(self, jDates):
        '''
        Show formatted journal
        '''  
        self.scrolList1.delete(1.0,tk.END)
        listAll = self.getJournalEntries(jDates)
        for row in listAll:
            self.scrolList1.insert(tk.END,row[0])
            self.scrolList1.insert(tk.END,'\t')
            mDate  = row[1]
            dateLength = 10
            mDate = mDate.ljust(dateLength)
            self.scrolList1.insert(tk.END,mDate)
            self.scrolList1.insert(tk.END,'  ')
            mTime  = row[2]
            timeLength = 9
            mTime = mTime.ljust(timeLength)
            self.scrolList1.insert(tk.END,mTime)
            self.scrolList1.insert(tk.END,'  ')
            mDescription = row[3]
            descLength = len(row[3])+(30-len(row[3]))
            mDescription = mDescription.ljust(descLength)
            self.scrolList1.insert(tk.END,mDescription)
            self.scrolList1.insert(tk.END,'  \t')
            mdAccount = str(row[4])
            daccountLength = len(mdAccount)+(4-len(mdAccount))
            mdAccount = mdAccount.ljust(daccountLength)
            self.scrolList1.insert(tk.END,mdAccount)
            self.scrolList1.insert(tk.END,' ')
            mdAmount = str(round(row[5],2))
            damountLength = len(mdAmount)+(8-len(mdAmount))
            mdAmount = mdAmount.rjust(damountLength)
            self.scrolList1.insert(tk.END,mdAmount)
            self.scrolList1.insert(tk.END,'\t\t     ')
            mcAccount = str(row[6])
            caccountLength = len(mcAccount)+(4-len(mcAccount))
            mcAccount = mcAccount.ljust(caccountLength)
            self.scrolList1.insert(tk.END,mcAccount)
            self.scrolList1.insert(tk.END,'\t')
            mcAmount = str(round(row[7],2))
            camountLength = len(mcAmount)+(8-len(mcAmount))
            mcAmount = mcAmount.rjust(camountLength)
            self.scrolList1.insert(tk.END,mcAmount)
            self.scrolList1.insert(tk.END,'\n')
            
    # #################################
    # Other Control Functions etc.
    # #################################
    def newMemo(self):
        '''
        Method to start a new accounting memo
        '''
        proceedAnswer = mBox.askyesno("New Memo","Save current memo and start a new one?")
        pass
    
    def printMemo(self):
        '''
        Method to Print a selected accounting memo        
        '''
        proceedAnswer = mBox.askyesno("print Memo","Send the current memo to the printer?")
        pass
    
    def saveMemo(self):
        '''
        Method to save the current accounting memo
        '''
        proceedAnswer = mBox.askyesno("Save Memo","Save current memo and continue?")
        pass
    
    def fetchMemo(self):
        '''
        Method to fetch a selected accounting memo
        '''
        proceedAnswer = mBox.askyesno("Get a Memo","Fetch a Previous Memo?")
        pass
    
    def do_balSheet(self):
        '''
        '''
        proceedAnswer = mBox.askyesno("Balance Sheet Report","Prepare report now?")
        pass
    
    def do_journalRpt(self):
        '''
        '''
        proceedAnswer = mBox.askyesno("Journal Report","Prepare report now?")
        pass
    
    def do_LedgerAcct(self):
        '''
        '''
        proceedAnswer = mBox.askyesno("Ledger Account Report","Prepare report now?")
        pass
    
    def list_Accounts(self):
        '''
        '''
        proceedAnswer = mBox.askyesno("List of Accounts Report","Prepare report now?")
        pass
    
    def do_RevandExp(self):
        '''
        '''
        proceedAnswer = mBox.askyesno("Revenu and Expense Report","Prepare report now?")
        pass
    
    # #####################################
    # Create GUI Functions (Visualization)
    # #####################################   
    def createWidgets(self):
        '''
        Create the GUI interfaces
        '''
        # Messages and Dialogs -------------------------------------------
        def info(self):
            mBox.showinfo('About OpenAccounting, ' , 'Application to Perform Basic GAAP Accounting functions.\n\n (c) David A York, 2018\n http:crunches-data.appspot.com \nVersion: 0.0, development version 0.01a \nlicense: MIT')
        
        
        
        def getLedgerAccount(self):
            answer = simpledialog.askstring("Input", "What Account Number to retrieve?", parent=self.win)
            if answer is not None:
                self.do_showLedger(answer)
            else:
                print("No Value entered")
                return 0
            
        def getJournalDates(self):
            answer = simpledialog.askstring("Input", "Start and End Date for Journal Retrieval\n, a comma separated pair", parent=self.win)
            if answer is not None:
                jDates = (answer,)
                self.do_showJournal((jDates))
            else:
                print("No Value entered")
                return 0
           
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
        
        frm1 = ttk.Labelframe(tab1, text='General Journal', width= 600, height=600)
        frm1.grid()
        ttk.Label(frm1, text="The General Journal is the book of first entry in the accounting system. It is accessed directly in the course of recording the daily activities of the enterprise.\n All other related books are accessible as appropriate for addition and update from the general journal.").grid(column=0, row=0, padx=4, pady=4,sticky='W')
        frm1a = ttk.Labelframe(frm1, width= 550, height=500)
        frm1a.grid()
        jDates = (0,0)
        self.updateJournal = ttk.Button(frm1a, text="Update Display", command=lambda: self.do_showJournal(jDates)).grid(column=0,row=1,padx=4, pady=4)
        self.printJournal = ttk.Button(frm1a, text="PRINT").grid(column=1,row=1,padx=4, pady=4)
        self.newEntry = ttk.Button(frm1a, text="New Entry", command=lambda: insertJournalForm(self)).grid(column=2,row=1,padx=4, pady=4)
        ttk.Label(frm1, text="Transact\t    Date\t\t        Time\t\tDescription\t\t\tDebit:   Account    Amount\t   Credit:  Account    Amount").grid(column=0, row=2, padx=4, pady=4,sticky='W')
        scrolW1  = 100; scrolH1  =  40
        self.scrolList1 = scrolledtext.ScrolledText(frm1, width=scrolW1, height=scrolH1, wrap=tk.WORD)
        self.scrolList1.grid(column=0, row=2, padx=4, pady=4, sticky='WE', columnspan=3)
        self.do_showJournal(jDates)
        
        frm2 = ttk.Labelframe(tab2, text='General Ledger', width= 400, height=600)
        frm2.grid()
        ttk.Label(frm2, text="The General Ledger is the main book in the accounting system. It is accessed indirectly by the General Journal in the \ncourse of daily activity. As a result there will be found no menu or button actions that allow direct entry or edit of \nthe Ledger accounts.").grid(column=0, row=0, padx=4, pady=4,sticky='W')
        frm2a = ttk.Labelframe(frm2, width= 400, height=500)
        frm2a.grid()
        self.updateLedger = ttk.Button(frm2a, text="Update Display", command=lambda: self.do_showLedger(0)).grid(column=0,row=0,padx=4, pady=4)
        self.printLedger = ttk.Button(frm2a, text="PRINT").grid(column=1,row=0,padx=4, pady=4)
        self.newAccount = ttk.Button(frm2a, text="Show Another").grid(column=2,row=0,padx=4, pady=4)
        ttk.Label(frm2, text="Account \tTransaction\t Amount \tBalance \t\t").grid(column=0, row=2, padx=4, pady=4,sticky='W')
        scrolW1  = 80; scrolH1  =  40
        self.scrolList2 = scrolledtext.ScrolledText(frm2, width=scrolW1, height=scrolH1, wrap=tk.WORD)
        self.scrolList2.grid(column=0, row=3, padx=4, pady=4, sticky='WE', columnspan=3)
        self.do_showLedger(0)
        
        ## Set tab and contents for the CHar of Accounts
        frm3 = ttk.Labelframe(tab3, text='Chart of Accounts', width= 400, height=600)
        frm3.grid()
        frm3a = ttk.Labelframe(frm3, width= 400, height=500)
        frm3a.grid()
        self.updateChart = ttk.Button(frm3a, text="Update Display", command=lambda: self.do_showChart()).grid(column=0,row=0,padx=4, pady=4)
        self.printChart = ttk.Button(frm3a, text="PRINT").grid(column=1,row=0,padx=4, pady=4)
        self.newAccount = ttk.Button(frm3a, text="New Account", command=lambda: insertChartForm(self)).grid(column=2,row=0,padx=4, pady=4)
        ttk.Label(frm3, text="Account \t Name \t\t\t\t\t\t\tType\t\tBalance").grid(column=0, row=1, padx=4, pady=4,sticky='W')
        scrolW1  = 80; scrolH1  =  40
        self.scrolList3 = scrolledtext.ScrolledText(frm3, width=scrolW1, height=scrolH1, wrap=tk.WORD)
        self.scrolList3.grid(column=0, row=2, padx=4, pady=4, sticky='WE', columnspan=3)
        self.do_showChart()
        
        frm4 = ttk.Labelframe(tab4, text='Accounting Reports', width= 500, height=600)
        frm4.grid(padx=8, pady=4)
        self.reportctl = ttk.LabelFrame(frm4, text = "List of Report")
        self.reportctl.grid(column=0, row=0, padx=8, pady=4, sticky='W') 
        self.action_balanceSheet = ttk.Button(self.reportctl, text="Balance Sheet", command=lambda: self.do_balSheet())
        self.action_balanceSheet.grid(column=0, row=0, padx=4, pady=6)        
        self.action_journalReport = ttk.Button(self.reportctl, text="Journal Report", command=lambda: self.do_journalRpt())
        self.action_journalReport.grid(column=1, row=0, padx=4, pady=6)        
        self.action_ledgerAccount = ttk.Button(self.reportctl, text="Ledger Account", command=lambda: self.do_LedgerAcct())
        self.action_ledgerAccount.grid(column=3, row=0, padx=4, pady=6)
        self.action_listAccounts = ttk.Button(self.reportctl, text="List Accounts", command=lambda: self.list_Accounts())
        self.action_listAccounts.grid(column=4, row=0, padx=4, pady=6)
        self.action_revenueExpense = ttk.Button(self.reportctl, text="Revenue and Expenses", command=lambda: self.do_RevandExp())
        self.action_revenueExpense.grid(column=5, row=0, padx=4, pady=6)
        reportWin = Canvas(frm4, width=450, height=550, offset='20,10')
        reportWin.grid(column=0, row=2, padx=8,pady=4)
        reportWin.create_text(225,10, text="This is a dummy accounting report on the canvas") 
        
        frm5 = ttk.Labelframe(tab5, text='Associated Journal or Ledger Note', width= 400, height=600)
        frm5.grid()             
        scrolW1  = 80; scrolH1  =  20
        self.scr_memo = scrolledtext.ScrolledText(frm5, width=scrolW1, height=scrolH1, wrap=tk.WORD)
        self.scr_memo.grid(column=0, row=6, padx=4, pady=4, sticky='WE', columnspan=3)
        
        self.memoctl = ttk.LabelFrame(frm5, width=56)
        self.memoctl.grid(column=0, row=0, padx=8, pady=4, sticky='W') 
        self.action_clrmemo = ttk.Button(self.memoctl, text="NEW MEMO", command=lambda: self.newMemo())
        self.action_clrmemo.grid(column=0, row=0, padx=4, pady=6)        
        self.action_prtmemo = ttk.Button(self.memoctl, text="PRINT MEMO", command=lambda: self.printMemo())
        self.action_prtmemo.grid(column=1, row=0, padx=4, pady=6)        
        self.action_savememo = ttk.Button(self.memoctl, text="SAVE MEMO", command=lambda: self.saveMemo())
        self.action_savememo.grid(column=3, row=0, padx=4, pady=6)
        self.action_loadmemo = ttk.Button(self.memoctl, text="GET ANOTHER", command=lambda: self.fetchMemo())
        self.action_loadmemo.grid(column=4, row=0, padx=4, pady=6)
        
        frm6 = ttk.Labelframe(tab6, text='System Maintenance', width= 400, height=600)
        frm6.grid()
        self.action_sysSetup = ttk.Button(frm6, text=" NEW SET-UP ", command=lambda:self.createAccounts()).grid(column=0,row=0, padx=8, pady=4)
        self.action_sysPack = ttk.Button(frm6, text=" PACK DB ", command=lambda:self.packDatabase()).grid(column=1,row=0, padx=8, pady=4)
        self.action_sysTrialBal = ttk.Button(frm6, text="TRIAL BALANCE", command=lambda:self.createAccounts()).grid(column=0,row=1, padx=8, pady=4)
        self.action_sysFiscalClose = ttk.Button(frm6, text="FISCAL CLOSE", command=lambda:self.packDatabase()).grid(column=1,row=1, padx=8, pady=4)
        
        # meubar created here --------------------------------------------
        menuBar = Menu(self.win)
        self.win.config(menu=menuBar)
        # Add menu items
        # Add System Menu
        sysMenu = Menu(menuBar, tearoff=0)
        sysMenu.add_command(label="New Set-up", command=lambda: self.createAccounts())
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
        
        # Add an Data entry Menu
        entryMenu = Menu(menuBar, tearoff=0)
        entryMenu.add_command(label="Journal Entry", command=lambda: insertJournalForm(self))
        entryMenu.add_command(label="New Account", command=lambda: insertChartForm(self))
        entryMenu.add_command(label="Make Memo")
        entryMenu.add_separator()
        entryMenu.add_command(label="Trial Balance")
        entryMenu.add_command(label="End of Year")
        menuBar.add_cascade(label="Entry", menu=entryMenu)
        
        # Add an Data entry Menu
        viewMenu = Menu(menuBar, tearoff=0)
        viewMenu.add_command(label="View Journal", command=lambda: getJournalDates(self))
        viewMenu.add_command(label="View Accounts")
        viewMenu.add_command(label="View Ledger", command=lambda: getLedgerAccount(self))
        viewMenu.add_separator()
        viewMenu.add_command(label="Trial Balance")
        viewMenu.add_command(label="End of Year")
        menuBar.add_cascade(label="View", menu=viewMenu)
        
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
    w = (2*asys.win.winfo_screenwidth())/3
    h = asys.win.winfo_screenheight()
    asys.win.geometry("%dx%d+0+0" % (w, h))
    asys.win.mainloop()