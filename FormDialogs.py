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

# #######################################################
# Classes, Independently constructed Forms, Dialogs etc
# #######################################################
'''
Classes, External, independently constructed Forms, Dialogs etc
'''
class insertJournalForm(object):
    '''
    A form-dialog class insertion Form to building and display for Journal Access Dialog
    @summary: A form to collect journal item data to add to journal table,. A Part of Accounting System application
    @see: refer to main module (AccountingSystem) documentation
    created: Oct 17, 2018
    '''
    here = pytz.timezone('America/New_York')
    currentDT = dt.datetime.now(here)
    
    def __init__(self, goal):
        '''
        Constructor for Add to Journal data dialog window
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
    A form-dialog class insertion Form for building and display Chart of Account access Dialog
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
    A form-dialog class insertion Form for building and display Memo Composition Dialog
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