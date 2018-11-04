'''
Module for view and report forms and input form dialogs
Created on Oct 30, 2018
@license: MIT
@author: David York
@copyright: 2018 D A York
'''

# ######################################
# Imports
# ######################################
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import datetime as dt
import pytz 
from AccountDB import AccountDB
from Tooltips import createToolTip
from tkinter import font
import math as mt
import numpy as np

# #######################################################
# Classes, Independently constructed Forms, Dialogs etc
# #######################################################
'''
Classes, External, independently constructed Forms, Dialogs etc
'''
class insertJournalForm(object):
    '''
    A form-dialog class insertion Form to building and display for Journal Access 
    in it's own pop-up Dialog window
    @summary: A form to collect journal item data to add to journal table,. A Part of Accounting System application
    @see: refer to main module (AccountingSystem) documentation
    created: Oct 17, 2018
    '''
    here = pytz.timezone('America/New_York')
    currentDT = dt.datetime.now(here)
    
    def __init__(self, goal):
        '''
        Constructor for Add to Journal in it's own pop-up data dialog window
        '''
        
        # Create instance
        self.goal=goal
        self.frm = tk.Tk()
        # Add a title
        self.frm.title("Insert a Journal Entry")
        self.journalForm()
        self.frm.mainloop() 

        

    def journalForm(self):
        ''' 
        The form for journal access for anew transaction entry
        '''
        # Whole form label frame---------------------------------------
        lbfr = ttk.LabelFrame(self.frm, text=' Input Form ')
        lbfr.grid(column=0, row=0, padx=10, pady=10, sticky='W')
        # Transaction Entry field -------------------------------------
        self.lbl0 = tk.Label(lbfr, text="Transaction").grid(column=0, row=0)
        self.e0 = tk.Entry(lbfr, width=16)
        self.e0.grid(column=1, row=0, padx=5, pady=4, sticky='W')
            # Associated tool tip
        transEnter = 'Unique transaction ID number. Is all numeric'
        createToolTip(self.e0, transEnter)
        # -------------------------------------------------------------
        self.lbl1 = tk.Label(lbfr, text="Date").grid(column=0, row=1)
        self.e1 = tk.Entry(lbfr,width=10)
        self.e1.grid(column=1, row=1, padx=5, pady=4, sticky='W')
        rnow = str(self.currentDT.year)+'-'+str(self.currentDT.month)+'-'+str(self.currentDT.day)
        self.e1.insert(0, rnow)
            # Associated tool tip
        dateEnter = 'Date  transaction entered, yyyy-mm-dd, defaults to today, '
        createToolTip(self.e1, dateEnter)
        # -------------------------------------------------------------
        self.lbl2 = tk.Label(lbfr, text="Time").grid(column=0, row=2)
        self.e2 = tk.Entry(lbfr,width=9)
        self.e2.grid(column=1, row=2, padx=5, pady=4, sticky='W')
        rtime = str(self.currentDT.hour)+':'+str(self.currentDT.minute)+':'+str(self.currentDT.second)
        self.e2.insert(0, rtime)
            # Associated tool tip
        timeEnter = 'Time transaction is entered. [hh:mm:ss] optional, defaults to Now'
        createToolTip(self.e2, timeEnter)
        # -------------------------------------------------------------
        self.lbl3 = tk.Label(lbfr, text="Description").grid(column=0, row=3)
        self.e3 = tk.Entry(lbfr,width=50)
        self.e3.grid(column=1, row=3, padx=5, pady=4, sticky='W')
            # Associated tool tip
        descEnter = 'transaction description.'
        createToolTip(self.e3, descEnter)
        # -------------------------------------------------------------
        self.lbl4 = tk.Label(lbfr, text="DebitAccount").grid(column=0, row=4)
        self.e4 = tk.Entry(lbfr,width=4)
        self.e4.grid(column=1, row=4, padx=5, pady=4, sticky='W')
            # Associated tool tip
        dAcctsEnter = 'Account to Debit'
        createToolTip(self.e4, dAcctsEnter)
        # -------------------------------------------------------------
        self.lbl5 = tk.Label(lbfr, text="DebitAmount").grid(column=0, row=5)
        self.e5 = tk.Entry(lbfr,width=8)
        self.e5.grid(column=1, row=5, padx=5, pady=4, sticky='W')
            # Associated tool tip
        dAmtEnter = 'Amount to debit, dollars and cents, no not include sign, will be added by system'
        createToolTip(self.e5, dAmtEnter)
        # -------------------------------------------------------------
        self.lbl6 = tk.Label(lbfr, text="CreditAccount").grid(column=0, row=6)
        self.e6 = tk.Entry(lbfr,width=4)
        self.e6.grid(column=1, row=6, padx=5, pady=4, sticky='W')
            # Associated tool tip
        cAcctEnter = 'Account to Credit'
        createToolTip(self.e6, cAcctEnter)
        # -------------------------------------------------------------
        self.lbl7 = tk.Label(lbfr, text="CreditAmount").grid(column=0, row=7)
        self.e7 = tk.Entry(lbfr,width=8)
        self.e7.grid(column=1, row=7, padx=5, pady=4, sticky='W')
            # Associated tool tip
        cAmtEnter = 'Amount to credit, dollars and cents, no not include sign, will be added by system'
        createToolTip(self.e7, cAmtEnter)
        # --------------------------------------------------------------
        self.btn1 = ttk.Button(lbfr, text="Commit", command=lambda: self.on_click()).grid(column=0,row=9,padx=8, pady=4, sticky='W')
        self.btn2 = ttk.Button(lbfr, text="Cancel", command=lambda: self.on_cancel()).grid(column=1,row=9,padx=8, pady=4, sticky='W')
        
        
    def on_click(self):
        '''
        Save new Journal Entry and update associated General Ledger accounts
        '''
        # get debit account balance
        daccount = int(self.e4.get())   
        txType = 'DEBIT'     
        debitBalance = AccountDB.getAccountBalance(self,daccount)
        debitSgn = AccountDB.getsgnAdjust(self,daccount,txType)
        debitAmount = debitSgn * round(float(self.e7.get()),2)
        # get credit  account balance
        caccount = int(self.e6.get())
        txType = 'CREDIT'         
        creditBalance= AccountDB.getAccountBalance(self, caccount)
        creditSgn = AccountDB.getsgnAdjust(self, caccount,txType)
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
            AccountDB.insertJournalEntry(self, jrow)
            lrow = lDRow
            AccountDB.insertLedgerEntry(self, lrow)
            lrow = lCRow
            AccountDB.insertLedgerEntry(self, lrow)
            AccountDB.updateChartBalance(self, daccount, newDBalance)
            AccountDB.updateChartBalance(self, caccount, newCBalance)
            print("journalForm closed")
            self.frm.destroy()
        else:
            print("ERROR: Credits and Debits do not balance")
        
    def on_cancel(self):
        print("Cancelled action")
        self.frm.destroy()
        
class insertChartForm(object):
    '''
    A form-dialog class insertion Form for building and display Chart of Account 
    access in it's own pop-up Dialog window
    @summary: A form to collect new account to add to Chart, and send to database. 
    created: Oct 14, 2018
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
        ''' 
        The form for Chart of Account access 
        '''
        # Whole form label frame --------------------------------------
        lbfr = ttk.LabelFrame(self.frm, text=' Input Form ')
        lbfr.grid(column=0, row=0, padx=10, pady=10, sticky='W')
        # -------------------------------------------------------------
        self.lbl0 = tk.Label(lbfr, text="Account").grid(column=0, row=0)
        self.e0 = tk.Entry(lbfr, width=16)
        self.e0.grid(column=1, row=0, padx=5, pady=4, sticky='W')
        acctEnter = 'Number of the New Account being Opened'
        createToolTip(self.e0, acctEnter)
        # -------------------------------------------------------------
        self.lbl2 = tk.Label(lbfr, text="Name").grid(column=0, row=2)
        self.e2 = tk.Entry(lbfr,width=50)
        self.e2.grid(column=1, row=2, padx=5, pady=4, sticky='W')
        nameEnter = 'Name or Description of the new account'
        createToolTip(self.e2, nameEnter)
        # -------------------------------------------------------------
        self.lbl3 = tk.Label(lbfr, text="Type of Account").grid(column=0, row=3)
        choices = ['DEBIT', 'CREDIT']
        self.vtype = tk.StringVar()
        self.e3 = tk.OptionMenu(lbfr, self.vtype, *choices, command=self.func)
        self.e3.configure(width = 12)
        self.e3.grid(column=1, row=3, padx=5, pady=4, sticky='W')
        atypeEnter = 'SELECT the Type of account, Credit vs Debit. Used to determine if transactions add to or subtract from balance'
        createToolTip(self.e3, atypeEnter)
        # -------------------------------------------------------------
        self.lbl4 = tk.Label(lbfr, text="Starting Balance").grid(column=0, row=4)
        self.e4 = tk.Entry(lbfr,width=10)
        self.e4.grid(column=1, row=4, padx=5, pady=4, sticky='W')
        self.e4.insert(0, 0)
        balEnter = 'Starting Account balance when opened'
        createToolTip(self.e4, balEnter)
        # -------------------------------------------------------------        
        self.btn3 = ttk.Button(lbfr, text="Commit", command=lambda: self.on_click()).grid(column=0,row=7,padx=8, pady=4, sticky='W')
        self.btn4 = ttk.Button(lbfr, text="Cancel", command=lambda: self.on_cancel()).grid(column=1,row=7,padx=8, pady=4, sticky='W')
    
    def func(self,value):
        pass
    
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
            existAccount = AccountDB.existChartAccount(self,account)
            atype = self.vtype.get()
            
            row = (int(self.e0.get()), self.e2.get(), atype, self.e4.get())
            ''' the activation of the form'''
            if (not existAccount):
                print("commit")
                print(row)
                AccountDB.insertChartAccount(self, row)
                print("journalForm closed")
                self.frm.destroy()
            else:
                print("ERROR: An Account Already Exists with this Number")
                self.on_cancel()
        
    def on_cancel(self):
        print("Cancelled action")
        self.frm.destroy()   
        
class insertMemoForm(object):
    '''
    A form-dialog class insertion Form for building and display Memo Composition 
    in it's own pop-up Dialog window
    @summary: A form to collect memo input, 
    created: Oct 14, 2018
    '''
    here = pytz.timezone('America/New_York')
    currentDT = dt.datetime.now(here)
    
    def __init__(self, goal):
        '''
        Constructor for Add New Memo dialog window
        '''
        
        # Create instance
        self.frmFD3 = tk.Tk()
        # Add a title
        self.frmFD3.title("Add a Memorandum")
        self.memoForm()
        self.frmFD3.mainloop() 
                
    def memoForm(self):
        ''' 
        The form for Memo Composition and adding 
        '''
        # frame for reference fields for memo--------------------------
        lbfr = ttk.LabelFrame(self.frmFD3, width= 560, height=200)
        lbfr.grid(column=0, row=0, padx=10, pady=10)
        # -------------------------------------------------------------
        self.lbl0 = tk.Label(lbfr, text="Memo Number").grid(column=0, row=0, sticky="W")
        self.e0 = tk.Entry(lbfr, width=11)
        self.e0.grid(column=1, row=0, padx=5, pady=4, sticky='W')
        # -------------------------------------------------------------
        self.lbl1 = tk.Label(lbfr, text="Transaction").grid(column=2, row=0, sticky='W')
        self.e1 = tk.Entry(lbfr, width=16)
        self.e1.grid(column=3, row=0, padx=5, pady=4, sticky='W')
        # -------------------------------------------------------------
        self.lbl2 = tk.Label(lbfr, text="Date Time").grid(column=4, row=0, sticky='W')
        self.e2 = tk.Entry(lbfr,width=18)
        self.e2.grid(column=5, row=0, padx=5, pady=4, sticky='W')
        self.e2.insert(0, self.currentDT)
        # -------------------------------------------------------------
        lbfr2 = ttk.LabelFrame(self.frmFD3, text='Memo Attaching', width= 560, height=200)
        lbfr2.grid(column=0, row=1, padx=10, pady=10)
        # frame around memo text --------------------------------------
        scrolW1  = 80; scrolH1  =  20
        self.scr_memo = scrolledtext.ScrolledText(lbfr2, width=scrolW1, height=scrolH1, wrap=tk.WORD)
        self.scr_memo.grid(column=0, row=0, padx=4, pady=4, sticky='WE', columnspan=3)
        # -------------------------------------------------------------                
        self.btn5 = ttk.Button(lbfr2, text="Commit", command=lambda: self.on_commit3()).grid(column=0,row=27,padx=8, pady=4, sticky='W')
        self.btn6 = ttk.Button(lbfr2, text="Cancel", command=lambda: self.on_cancel()).grid(column=1,row=27,padx=8, pady=4, sticky='W')
        
    def on_commit3(self):
        '''
        Save a Memo 
        '''
        if (self.e0.get() == ''): 
            self.on_cancel()
        else:
            row = (self.e0.get(),self.e1.get(),self.e2.get(),self.scr_memo.get(1.0, tk.END))
            ''' the activation of the form'''
            print("commit")
            AccountDB.insertAccountMemos(self, row)
            print("memoForm closed")
            self.frmFD3.destroy()
        
    def on_cancel(self):
        print("Cancelled action")
        self.frmFD3.destroy()   
        
class ReportFormats():

    def do_reptLedger(self, account):
        '''
        Report formating and data retrieval for Ledger account reports
        '''
        self.win.update()
        self.tab4.focus_force()
        self.tabControl.update()
        self.tab4.lift(aboveThis=None)
        self.tabControl.update()
        ledgerAcct=AccountDB.getLedgerAccount(self,account)        
        self.reportWin.delete("all")
        self.reportWin.create_text(5,18,anchor=tk.NW, text='Account')  
        self.reportWin.create_text(56,18,anchor=tk.NW, text='Transaction: ')        
        # self.reportWin.create_text(150,18,anchor=tk.NW, text='Date')
        # self.reportWin.create_text(196,18,anchor=tk.NW, text='Time')
        self.reportWin.create_text(150,18,anchor=tk.NW, text='Description')
        self.reportWin.create_text(420,18,anchor=tk.NW, text='Amount')
        self.reportWin.create_text(485,18,anchor=tk.NW, text='Balance')
        cline = 18
        cline = cline + 20
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        for row in ledgerAcct:
            cline = cline + 13
            maccount = str(row[0])        
            maccountLength = len(maccount)+(4-len(maccount))    # 4 x 7 =28
            maccount = maccount.ljust(maccountLength)
            self.reportWin.create_text(10,cline,anchor=tk.NW, text=maccount)
            mTransact = str(row[1])
            transactLength = 16                                 # 16 x 7 = 112
            mTransact = mTransact.ljust(transactLength)
            self.reportWin.create_text(62,cline,anchor=tk.NW, text=mTransact)
            mAmount = str(round(row[2],2))        
            mamountLength = len(mAmount)+(8-len(mAmount))     # 8 x 7 = 56
            mAmount = mAmount.rjust(mamountLength)
            self.reportWin.create_text(420,cline,anchor=tk.NW, text=mAmount)
            mBalance = str(round(row[3],2))        
            mbalanceLength = len(mBalance)+(8-len(mBalance))     # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(485,cline,anchor=tk.NW, text=mBalance)
        cline = cline + 20
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        
    def do_reptTransact(self, jTransact):
        '''
        Show formatted journal transaction
        font conversion factor is 7 = 10pt
        '''       
        self.win.update()
        self.tab4.focus_force()
        self.tabControl.update()
        self.tab4.lift(aboveThis=None)
        self.tabControl.update()
        transaction = AccountDB.getJournalTransact(self,jTransact)
        self.reportWin.delete("all")
        self.reportWin.create_text(10,18,anchor=tk.NW, text='Transaction: ')        
        self.reportWin.create_text(112,18,anchor=tk.NW, text='Date')
        self.reportWin.create_text(189,18,anchor=tk.NW, text='Time')
        self.reportWin.create_text(252,18,anchor=tk.NW, text='Description')
        self.reportWin.create_text(522,18,anchor=tk.NW, text='Debit')
        self.reportWin.create_text(606,18,anchor=tk.NW, text='Credit')
        cline = 18
        cline = cline + 20
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        for row in transaction:
            cline = cline + 13
            mTransact = str(row[0])
            transactLength = 16                # 16 x 7 = 112
            mTransact = mTransact.ljust(transactLength)
            self.reportWin.create_text(10,cline,anchor=tk.NW, text=mTransact)
            mDate  = row[1]
            #mDate ="2018-10-24"
            dateLength = 11                # 11 x 7 = 77
            mDate = mDate.ljust(dateLength)
            self.reportWin.create_text(112,cline,anchor=tk.NW, text=mDate)
            mTime  = row[2]
            #mTime = "12:40:00"
            timeLength = 9                  # 9 x 7 = 63
            mTime = mTime.ljust(timeLength)
            self.reportWin.create_text(189,cline,anchor=tk.NW, text=mTime)
            mDescription = row[3]
            #mDescription ="Pay bills"       # 30 x 9 = 270
            descLength = len(mDescription)+(30-len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(252,cline,anchor=tk.NW, text=mDescription)
            mdAccount = str(row[4])
            #mdAccount = "100"               # 4 x 7 =28
            daccountLength = len(mdAccount)+(4-len(mdAccount))
            mdAccount = mdAccount.ljust(daccountLength)
            self.reportWin.create_text(522,cline,anchor=tk.NW, text=mdAccount)
            mdAmount = str(round(row[5],2))
            #mdAmount = "-24.91 "            # 8 x 7 = 56
            damountLength = len(mdAmount)+(8-len(mdAmount))
            mdAmount = mdAmount.rjust(damountLength)
            self.reportWin.create_text(550,cline,anchor=tk.NW, text=mdAmount)
            mcAccount = str(row[6])
            #mcAccount = "220"
            caccountLength = len(mcAccount)+(4-len(mcAccount))
            mcAccount = mcAccount.ljust(caccountLength)
            self.reportWin.create_text(606,cline,anchor=tk.NW, text=mcAccount)
            mcAmount = str(round(row[7],2))
            #mcAmount = "-24.91 "
            camountLength = len(mcAmount)+(8-len(mcAmount))
            mcAmount = mcAmount.rjust(camountLength)
            self.reportWin.create_text(634,cline,anchor=tk.NW, text=mcAmount)
            
        cline = cline + 20
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        if (int(jTransact) != 0):
            '''
            If only a single transaction is to be reported, 
            then include all associated accounting memos with it
            '''
            memo = AccountDB.getTransactMemo(self,jTransact)
            cline = cline + 26
            self.reportWin.create_text(10,cline,anchor=tk.NW, text='Memos')
            cline = cline + 13
            self.reportWin.create_text(10,cline,anchor=tk.NW, text='Number')        
            self.reportWin.create_text(112,cline,anchor=tk.NW, text='Date')
            self.reportWin.create_text(189,cline,anchor=tk.NW, text='Time')
            for mrow in memo:
                cline = cline + 13
                memoDate  = mrow[2]
                dateLength = 11                # 11 x 7 = 77
                memoDate = memoDate.ljust(dateLength)
                self.reportWin.create_text(112,cline,anchor=tk.NW, text=memoDate)
                
                cline = cline + 13
                memoID  = mrow[0]
                self.reportWin.create_text(10,cline,anchor=tk.NW, text=memoID)
                memoText  = mrow[3]
                self.reportWin.create_text(55,cline,anchor=tk.NW, text=memoText)
                    
    def do_reptChart(self):
        '''
        '''        
        self.win.update()
        self.tab4.focus_force()
        self.tabControl.update()
        self.tab4.lift(aboveThis=None)
        self.tabControl.update()
        chartAcct=AccountDB.getChartAccounts(self)       
        self.reportWin.delete("all")
        self.reportWin.create_text(5,18,anchor=tk.NW, text='Account')  
        self.reportWin.create_text(56,18,anchor=tk.NW, text='Description')
        self.reportWin.create_text(420,18,anchor=tk.NW, text='Type')
        self.reportWin.create_text(485,18,anchor=tk.NW, text='Balance')
        cline = 18
        cline = cline + 20
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        for row in chartAcct:
            cline = cline + 13
            maccount = str(row[0])        
            maccountLength = len(maccount)+(4-len(maccount))    # 4 x 7 =28
            maccount = maccount.ljust(maccountLength)
            self.reportWin.create_text(10,cline,anchor=tk.NW, text=maccount)
            mDescription = row[1]
            descLength = len(mDescription)+(30-len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(56,cline,anchor=tk.NW, text=mDescription)
            mType = row[2]       
            mTypeLength = len(mType)+(8-len(mType))     # 6 x 7 = 42
            mType = mType.rjust(mTypeLength)
            self.reportWin.create_text(420,cline,anchor=tk.NW, text=mType)
            mBalance = str(round(row[3],2))        
            mbalanceLength = len(mBalance)+(8-len(mBalance))     # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(485,cline,anchor=tk.NW, text=mBalance)
        cline = cline + 20
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")

    def do_reptRevandExp(self):
        '''
        '''
        # Fetch revenue accounts
        #Fetch Expense accounts
        
        # Get Balance totals for each account 
        
        # Display the Revenue and Expense accounts in a table
        self.reportWin.delete("all")
        self.reportWin.create_text(150,5,  anchor=tk.NW, font=font.BOLD, text='Revenue', fill='blue') 
        self.reportWin.create_text(460,5,anchor=tk.NW, font=font.BOLD, text='Expenses',fill='blue') 
        self.reportWin.create_text(12,22,anchor=tk.NW, text='Account', fill='blue')  
        self.reportWin.create_text(63,22,anchor=tk.NW, text='Name', fill='blue')
        self.reportWin.create_text(273,22,anchor=tk.NW, text='Balance', fill='blue')
        self.reportWin.create_text(344,22,anchor=tk.NW, text='Account', fill='blue')  
        self.reportWin.create_text(395,22,anchor=tk.NW, text='Name', fill='blue')
        self.reportWin.create_text(605,22,anchor=tk.NW, text='Balance', fill='blue')
        cline = 22
        cline = cline + 20
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        # get assets block       
        blockAcct=AccountDB.getBalSheetAccounts(self,(400,499))
        revenueTotal = 0.0
        for row in blockAcct:
            revenueTotal = revenueTotal + float(row[3])
            cline = cline + 13
            maccount = str(row[0])        
            maccountLength = len(maccount)+(4-len(maccount))    # 4 x 7 =28
            maccount = maccount.ljust(maccountLength)
            self.reportWin.create_text(12,cline,anchor=tk.NW, text=maccount)
            mDescription = row[1]
            descLength = len(mDescription)+(30-len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(63,cline,anchor=tk.NW, text=mDescription)
            mBalance = str(round(row[3],2))        
            mbalanceLength = len(mBalance)+(8-len(mBalance))     # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(273,cline,anchor=tk.NW, text=mBalance)
        
        cline = cline + 20
        self.reportWin.create_line(265,cline, 325,cline, fill="blue")
        cline = cline + 13
        mTotal = str(round(revenueTotal,2))        
        mTotalLength = len(mTotal)+(10-len(mTotal))     # 8 x 7 = 56
        mTotal = mTotal.rjust(mTotalLength)
        self.reportWin.create_text(265,cline,anchor=tk.NW, text=mTotal)    
        
        #get liabilities
        # get liability block       
        blockAcct=AccountDB.getBalSheetAccounts(self,(500,599))
        expenseTotal = 0.0
        # reset cline to top right
        cline = 44
        for row in blockAcct:
            expenseTotal = expenseTotal + float(row[3])
            cline = cline + 13
            maccount = str(row[0])        
            maccountLength = len(maccount)+(4-len(maccount))    # 4 x 7 =28
            maccount = maccount.ljust(maccountLength)
            self.reportWin.create_text(344,cline,anchor=tk.NW, text=maccount)
            mDescription = row[1]
            descLength = len(mDescription)+(30-len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(395,cline,anchor=tk.NW, text=mDescription)
            mBalance = str(round(row[3],2))        
            mbalanceLength = len(mBalance)+(8-len(mBalance))     # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(605,cline,anchor=tk.NW, text=mBalance)
        
        cline = cline + 20
        self.reportWin.create_line(598,cline, 663,cline, fill="blue")
        cline = cline + 13
        mrTotal = str(round(expenseTotal,2))        
        mrTotalLength = len(mrTotal)+(10-len(mrTotal))     # 8 x 7 = 56
        mrTotal = mrTotal.rjust(mrTotalLength)
        self.reportWin.create_text(598,cline,anchor=tk.NW, text=mrTotal)  
        
        retainedEarnings = revenueTotal - expenseTotal
        
        cline = cline + 20
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")        
        cline = cline + 13
        maccount = str(399)        
        maccountLength = len(maccount)+(4-len(maccount))    # 4 x 7 =28
        maccount = maccount.ljust(maccountLength)
        self.reportWin.create_text(12,cline,anchor=tk.NW, text=maccount)
        mDescription = 'Retained Earnings'
        descLength = len(mDescription)+(30-len(mDescription))
        mDescription = mDescription.ljust(descLength)
        self.reportWin.create_text(63,cline,anchor=tk.NW, text=mDescription)
        mBalance = str(round(retainedEarnings,2))        
        mbalanceLength = len(mBalance)+(8-len(mBalance))     # 8 x 7 = 56
        mBalance = mBalance.rjust(mbalanceLength)
        self.reportWin.create_text(273,cline,anchor=tk.NW, text=mBalance)
        

    def do_reptBalSheet(self):
        '''
        '''
        # Fetch all Account Balances
        
        # Do trial Balances of each account, notify if any balances do not 
        #    agree with Chart of Account balances
        
        #Make and display the Balance Sheet   
        self.reportWin.delete("all")
        self.reportWin.create_text(150,5,  anchor=tk.NW, font=font.BOLD, text='Assets', fill='blue') 
        self.reportWin.create_text(460,5,anchor=tk.NW, font=font.BOLD, text='Liabilities',fill='blue') 
        self.reportWin.create_text(12,22,anchor=tk.NW, text='Account', fill='blue')  
        self.reportWin.create_text(63,22,anchor=tk.NW, text='Name', fill='blue')
        self.reportWin.create_text(273,22,anchor=tk.NW, text='Balance', fill='blue')
        self.reportWin.create_text(344,22,anchor=tk.NW, text='Account', fill='blue')  
        self.reportWin.create_text(395,22,anchor=tk.NW, text='Name', fill='blue')
        self.reportWin.create_text(605,22,anchor=tk.NW, text='Balance', fill='blue')
        cline = 22
        cline = cline + 20
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        # get assets block       
        blockAcct=AccountDB.getBalSheetAccounts(self,(100,199))
        assetTotal = 0.0
        for row in blockAcct:
            assetTotal = assetTotal + float(row[3])
            cline = cline + 13
            maccount = str(row[0])        
            maccountLength = len(maccount)+(4-len(maccount))    # 4 x 7 =28
            maccount = maccount.ljust(maccountLength)
            self.reportWin.create_text(12,cline,anchor=tk.NW, text=maccount)
            mDescription = row[1]
            descLength = len(mDescription)+(30-len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(63,cline,anchor=tk.NW, text=mDescription)
            mBalance = str(round(row[3],2))        
            mbalanceLength = len(mBalance)+(8-len(mBalance))     # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(273,cline,anchor=tk.NW, text=mBalance)
        
        cline = cline + 20
        self.reportWin.create_line(265,cline, 325,cline, fill="blue")
        cline = cline + 13
        mTotal = str(round(assetTotal,2))        
        mTotalLength = len(mTotal)+(10-len(mTotal))     # 8 x 7 = 56
        mTotal = mTotal.rjust(mTotalLength)
        self.reportWin.create_text(265,cline,anchor=tk.NW, text=mTotal)    
        
        #get liabilities
        # get liability block       
        blockAcct=AccountDB.getBalSheetAccounts(self,(200,299))
        liabilityTotal = 0.0
        # reset cline to top right
        cline = 44
        for row in blockAcct:
            assetTotal = assetTotal + float(row[3])
            cline = cline + 13
            maccount = str(row[0])        
            maccountLength = len(maccount)+(4-len(maccount))    # 4 x 7 =28
            maccount = maccount.ljust(maccountLength)
            self.reportWin.create_text(344,cline,anchor=tk.NW, text=maccount)
            mDescription = row[1]
            descLength = len(mDescription)+(30-len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(395,cline,anchor=tk.NW, text=mDescription)
            mBalance = str(round(row[3],2))        
            mbalanceLength = len(mBalance)+(8-len(mBalance))     # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(605,cline,anchor=tk.NW, text=mBalance)
        
        cline = cline + 20
        self.reportWin.create_line(598,cline, 663,cline, fill="blue")
        cline = cline + 13
        msTotal = str(round(liabilityTotal,2))        
        msTotalLength = len(msTotal)+(10-len(msTotal))     # 8 x 7 = 56
        msTotal = msTotal.rjust(msTotalLength)
        self.reportWin.create_text(598,cline,anchor=tk.NW, text=msTotal)  
        
        cline = cline + 33
        self.reportWin.create_text(467,cline,anchor=tk.NW, font=font.BOLD, text='Equity',fill='blue')
        
        cline = cline + 20
        self.reportWin.create_line(335,cline, 670,cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(335,cline, 670,cline, fill="blue")
        
        # get income block total       
        blockAcct=AccountDB.getBalSheetAccounts(self,(400,499))
        incomeTotal = 0.0
        for row in blockAcct:
            incomeTotal = incomeTotal + float(row[3])   
        # get expense block total 
        blockAcct=AccountDB.getBalSheetAccounts(self,(500,599))
        expenseTotal = 0.0
        for row in blockAcct:
            expenseTotal = expenseTotal + float(row[3]) 
        retainedEarnings = incomeTotal - expenseTotal
        
        # get equity block       
        blockAcct=AccountDB.getBalSheetAccounts(self,(300,399))
        equityTotal = 0.0
        # reset cline to top right
        for row in blockAcct:
            equityTotal = equityTotal + float(row[3])
            cline = cline + 13
            maccount = str(row[0])        
            maccountLength = len(maccount)+(4-len(maccount))    # 4 x 7 =28
            maccount = maccount.ljust(maccountLength)
            self.reportWin.create_text(344,cline,anchor=tk.NW, text=maccount)
            mDescription = row[1]
            descLength = len(mDescription)+(30-len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(395,cline,anchor=tk.NW, text=mDescription)
            mBalance = str(round(row[3],2))        
            mbalanceLength = len(mBalance)+(8-len(mBalance))     # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(605,cline,anchor=tk.NW, text=mBalance)
        
        cline = cline + 13
        maccount = str(399)        
        maccountLength = len(maccount)+(4-len(maccount))    # 4 x 7 =28
        maccount = maccount.ljust(maccountLength)
        self.reportWin.create_text(344,cline,anchor=tk.NW, text=maccount)
        mDescription = 'Retained Earnings'
        descLength = len(mDescription)+(30-len(mDescription))
        mDescription = mDescription.ljust(descLength)
        self.reportWin.create_text(395,cline,anchor=tk.NW, text=mDescription)
        mBalance = str(round(retainedEarnings,2))        
        mbalanceLength = len(mBalance)+(8-len(mBalance))     # 8 x 7 = 56
        mBalance = mBalance.rjust(mbalanceLength)
        self.reportWin.create_text(605,cline,anchor=tk.NW, text=mBalance)
        
        cline = cline + 20
        self.reportWin.create_line(598,cline, 663,cline, fill="blue")
        cline = cline + 13
        msTotal = str(round((equityTotal + retainedEarnings),2))
        
              
            
        msTotalLength = len(msTotal)+(10-len(msTotal))    
        msTotal = msTotal.rjust(msTotalLength)
        self.reportWin.create_text(598,cline,anchor=tk.NW, text=msTotal) 
        
        cline = cline + 20
        self.reportWin.create_line(598,cline, 663,cline, fill="blue")
        cline = cline + 13
        mrTotal = str(round((equityTotal + liabilityTotal),2))         
        mrTotalLength = len(mrTotal)+(10-len(mrTotal))    
        mrTotal = msTotal.rjust(mrTotalLength)
        self.reportWin.create_text(598,cline,anchor=tk.NW, text=mrTotal) 
        
         
        