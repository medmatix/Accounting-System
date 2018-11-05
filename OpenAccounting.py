'''
OpenAccounting
Created on Oct 17, 2018
@summary: An open source double entry accounting system based on SQLite and written in python
@note: Project pages at: https://medmatix.github.io/Accounting-System/
@author: David York
@version: 0.17
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
from tkinter import Scrollbar
from tkinter import Canvas
from tkinter import font
import math as mt
import numpy as np
import sys

# Custom module imports
from AccountDB import AccountDB
from FormDialogs import insertJournalForm, insertChartForm, insertMemoForm
from FormDialogs import ReportFormats
from Tooltips import createToolTip, ToolTip
from ReportPreps import TrialBalance 


 
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
        listAll = AccountDB.getChartAccounts(self)
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

        listAll = AccountDB.getLedgerAccount(self,account)
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
        listAll = AccountDB.getJournalEntries(self,jDates)
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
    
    
              
    # #################################
    # Other Control Functions etc.
    # #################################
    
    def click_on_widget(self, widget, button=1):
        widget.focus_force()
        self.win.update()
        widget.event_generate("<Button-{}>".format(button))
        self.win.update()

    def newMemo(self):
        '''
        Method to start a new accounting memo
        '''
        proceedAnswer = mBox.askyesno("New Memo","Save current memo and start a new one?")
        if proceedAnswer==True:
            '''
            Insert an entry into Journal
            '''
            id = int(self.ememoID.get())
            transact = int(self.ememoTransact.get())
            memo=str(self.scr_memo.get(1.0,tk.END))
            row = (id, transact,self.ememoDate.get(),memo)
            try:
                AccountDB.insertAccountMemos(row)
            except:
                print("not saved, probable duplicate memo")
            # clear the memo
            self.scr_memo.delete(1.0,tk.END)
            self.scr_memo.see(tk.END)
            print('cleared the notes pad')
        else:
            pass
    
    def printMemo(self):
        '''
        Method to Print a selected accounting memo        
        '''
        proceedAnswer = mBox.askyesno("print Memo","Send the current memo to the printer?")
        if proceedAnswer==True:
            pass
        else:
            pass
    
    def saveMemo(self):
        '''
        Method to save the current accounting memo
        '''
        proceedAnswer = mBox.askyesno("Save Memo","Save current memo and continue?")
        if (proceedAnswer):
            '''
            Save a Memo 
            '''
            mid = int(self.ememoID.get())
            transact = int(self.ememoTransact.get())
            memo=str(self.scr_memo.get(1.0,tk.END))
            row = (mid, transact,self.ememoDate.get(),memo)
            try:
                AccountDB.insertAccountMemos(row)
            except:
                print("not saved, probable duplicate memo")
          
    
    def fetchMemo(self):
        '''
        Method to fetch a selected accounting memo
        '''
        answer1 = simpledialog.askstring("Input", "How Do you want to retrieve, MemoNo or Date-Transact", parent=self.win)
        if answer1=="MemoNo":
            answer2 = simpledialog.askstring("Input", "Enter the Memo ID Number", parent=self.win)
        elif answer1=="Date-Transact":
            answer2 = simpledialog.askstring("Input", "Enter Date and Transaction (separated by a comma", parent=self.win)
        else:
            pass
    
    def do_balSheet(self):
        '''
        '''
        
        proceedAnswer = mBox.askyesno("Balance Sheet Report","This can take a while.\nPrepare report now?")
        if (proceedAnswer):
            debandcred = TrialBalance.trialBalance(self)
            if (debandcred[0]-debandcred[1]==0):
                ReportFormats.do_reptBalSheet(self)
            else:
                mBox.showinfo('Failed trial balance' , 'The Ledger appears to be out of balance. \n A balance sheet may have errors\nPerform a Trial Balance to Investigate')
    def do_LedgerAcct(self):
        '''
        '''
        proceedAnswer = mBox.askyesno("Ledger Account Report","Prepare report now?")
        pass
    
       
    def do_RevandExp(self):
        '''
        '''
        
        proceedAnswer = mBox.askyesno("Revenue and Expense Report","Prepare report now?")
        if (proceedAnswer):
            debandcred = TrialBalance.trialBalance(self)
            if (debandcred[0]-debandcred[1]==0):
                ReportFormats.do_reptRevandExp(self)
            else:
                mBox.showinfo('Failed trial balance' , 'The Ledger appears to be out of balance. \nAn Income statment may have errors\nPerform a Trial Balance to Investigate')


    def do_trialBalance(self):
        '''
        Calculate net balances for each chart account and compare to Chart of 
        Account balances. If any do not agree, notify which are out and return results
        '''
        proceedAnswer = mBox.askyesno("Trial Balance Report","This can take a while.\nPerform a trail balance now?")
        if (proceedAnswer):
            ReportFormats.do_reptTrialBalance(self)
        
    def do_printCurrentView(self):
        '''
        '''
        
        
    
    # #####################################
    # Create GUI Functions (Visualization)
    # #####################################   
    def createWidgets(self):
        '''
        Create the GUI interfaces
        '''
        # Messages and Dialogs -------------------------------------------
        def info(self):
            mBox.showinfo('About OpenAccounting, ' , 'Application to Perform Basic GAAP Accounting functions.\n\n (c) David A York, 2018\n http:crunches-data.appspot.com \nVersion: 0.2, development version 0.17 \nlicense: MIT')
        
        
        def notImplementedInfo(self):
            mBox.showinfo('Function Not Implemented Yet, ' , 'Sorry this is not implemented in full yet.\n\n Note For Printing: This is a high priority for me but tkinter is not very amenable to printing widget contents. However, at this time, you can take a screen shot and print from clipboard')
        
        def notImplementedPayroll(self):
            mBox.showinfo('Payroll Not Implemented Yet, ' , 'Sorry this functionality is not implemented yet.\n\n This specialized journal will be developed after all basic accounting \nfunctionality is in place. Your support is appreciated')
        
        def notImplementedInventory(self):
            mBox.showinfo('Inventory Not Implemented Yet, ' , 'Sorry this functionality is not implemented yet.\n\n This specialized journal will be developed after all basic accounting \nfunctionality is in place. Your support is appreciated')
        
        def notImplementedHelp(self):
            mBox.showinfo('Help Not Implemented Yet, ' , 'Sorry the Help is not implemented in full yet.\n\n This is part of the basic application functionality and is next in priority. \nFor now the background in the github repository readme \nmay be helpful. See about, in help.')
            
        def notImplementedEndofCycle(self):
            mBox.showinfo('End of Cycle Not Implemented Yet, ' , 'Sorry the comprehensive End of Cycle is not implemented in full yet.\n\n This is part of the basic application functionality and is a high priority for me.\n\nFor now, all closing activities can be carried out with the \nGeneral Journal if you are familiar with those tasks.')
        
        def fetchLedgerAccount(self):
            answer = simpledialog.askstring("Get Ledger Account", "What Account Number to retrieve?\n Enter '0' for ALL\n", parent=self.win)
            if answer is not None:
                ReportFormats.do_reptLedger(self,answer)
            else:
                print("No Value entered")
                return 0
            
        def getJournalDates(self):
            answer = simpledialog.askstring("Get Journal Range", "Start and End Date for Journal Retrieval\n, a comma separated pair. \n Enter '0,0' for ALL\n", parent=self.win)
            if answer is not None:
                jDates = (answer,)
                self.do_showJournal((jDates))
            else:
                print("No Value entered")
                return 0
        
        def getTransact(self):
            answer = simpledialog.askstring("Get Transaction", "Transaction to retrieve?\n\nEnter a Transaction Number\n Enter '0' for ALL \n", parent=self.win)
            if answer is not None:
                jTransact = (answer)
                self.do_reptTransact(jTransact)                
            else:
                print("No Value entered")
                return 0

            
        # Tab Controls created here --------------------------------------
        self.tabControl = ttk.Notebook(self.win)     # Create Tab Controls

        self.tab1 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='Journal')
                
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab2, text='Ledger')
        
        self.tab3 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab3, text='Chart of Accounts')
        
        self.tab4 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab4, text='Views and Reports')
        
        self.tab5 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab5, text='Accounting Memo')
        
        self.tab6 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab6, text='Maintenance')
        
        self.tabControl.grid()  # Pack to make visible
        
        frm1 = ttk.Labelframe(self.tab1, text='General Journal', width= 650, height=600)
        frm1.grid()
        ttk.Label(frm1, text="The General Journal is the book of first entry in the accounting system. It is accessed directly in the course of recording the daily activities of the enterprise.\n All other related books are accessible as appropriate for addition and update from the general journal.").grid(column=0, row=0, padx=4, pady=4,sticky='W')
        frm1a = ttk.Labelframe(frm1, width= 550, height=500)
        frm1a.grid(column=0,row=1)
        jDates = (0,0)
        self.updateJournal = ttk.Button(frm1a, text="Update Display", command=lambda: self.do_showJournal(jDates)).grid(column=0,row=1,padx=4, pady=4)
        self.printJournal = ttk.Button(frm1a, text="PRINT", command=lambda: notImplementedInfo(self)).grid(column=1,row=1,padx=4, pady=4)
        self.newEntry = ttk.Button(frm1a, text="New Entry", command=lambda: insertJournalForm(self)).grid(column=2,row=1,padx=4, pady=4)
        ttk.Label(frm1, text="Transact\t    Date\t\t        Time\t\tDescription\t\t\tDebit:   Account    Amount\t   Credit:  Account    Amount").grid(column=0, row=2, padx=4, pady=4,sticky='W')
        scrolW1  = 100; scrolH1  =  35
        self.scrolList1 = scrolledtext.ScrolledText(frm1, width=scrolW1, height=scrolH1, wrap=tk.WORD)
        self.scrolList1.grid(column=0, row=3, padx=4, pady=4, sticky='WE', columnspan=3)
        self.do_showJournal((0,0))
        
        frm2 = ttk.Labelframe(self.tab2, text='General Ledger', width= 650, height=600)
        frm2.grid()
        ttk.Label(frm2, text="The General Ledger is the main book in the accounting system. It is accessed indirectly by the General Journal in the \ncourse of daily activity. As a result there will be found no menu or button actions that allow direct entry or edit of \nthe Ledger accounts.").grid(column=0, row=0, padx=4, pady=4,sticky='W')
        frm2a = ttk.Labelframe(frm2, width= 400, height=500)
        frm2a.grid(column=0,row=1)
        self.updateLedger = ttk.Button(frm2a, text="Update Display", command=lambda: self.do_showLedger(0)).grid(column=0,row=0,padx=4, pady=4)
        self.printLedger = ttk.Button(frm2a, text="PRINT", command=lambda: notImplementedInfo(self)).grid(column=1,row=0,padx=4, pady=4)
        self.newAccount = ttk.Button(frm2a, text="Show Another").grid(column=2,row=0,padx=4, pady=4)
        ttk.Label(frm2, text="Account \tTransaction\t Amount \tBalance \t\t").grid(column=0, row=2, padx=4, pady=4,sticky='W')
        scrolW1  = 80; scrolH1  =  35
        self.scrolList2 = scrolledtext.ScrolledText(frm2, width=scrolW1, height=scrolH1, wrap=tk.WORD)
        self.scrolList2.grid(column=0, row=3, padx=4, pady=4, sticky='WE', columnspan=3)
        self.do_showLedger(0)
        
        ## Set tab and contents for the Chart of Accounts
        frm3 = ttk.Labelframe(self.tab3, text='Chart of Accounts', width= 650, height=600)
        frm3.grid()
        ttk.Label(frm3, text="The Chart of Accounts is the organizing principle of the accounting system. It is accessed directly in defining the business\n activities for the of the enterprise.\n\n At system initialization the basic default accounts are automatically configured. Subsequently the chart is accessible as\n needed to set up new customer and supplier accounts for ongoing operation of the business").grid(column=0, row=0, padx=4, pady=4,sticky='W')
        frm3a = ttk.Labelframe(frm3, width= 400, height=450)
        frm3a.grid()
        self.updateChart = ttk.Button(frm3a, text="Update Display", command=lambda: self.do_showChart()).grid(column=0,row=0,padx=4, pady=4)
        self.printChart = ttk.Button(frm3a, text="PRINT", command=lambda: notImplementedInfo(self)).grid(column=1,row=0,padx=4, pady=4)
        self.newAccount = ttk.Button(frm3a, text="New Account", command=lambda: insertChartForm(self)).grid(column=2,row=0,padx=4, pady=4)
        ttk.Label(frm3, text="Account \t Name \t\t\t\t\t\t\tType\t\tBalance").grid(column=0, row=2, padx=4, pady=4,sticky='W')
        scrolW1  = 80; scrolH1  =  32
        self.scrolList3 = scrolledtext.ScrolledText(frm3, width=scrolW1, height=scrolH1, wrap=tk.WORD)
        self.scrolList3.grid(column=0, row=3, padx=4, pady=4, sticky='WE', columnspan=3)
        self.do_showChart()
        
        frm4 = ttk.Labelframe(self.tab4, text='Accounting Reports', width= 800, height=590)
        frm4.grid(padx=8, pady=4)
        self.reportctl = ttk.LabelFrame(frm4, text = "List of Reports")
        self.reportctl.grid(column=0, row=0, padx=8, pady=4, sticky='W')
        frm4b = ttk.Frame(frm4, width= 700, height=450)
        frm4b.grid(column=0, row=3)                       
        self.action_balanceSheet = ttk.Button(self.reportctl, text="Balance Sheet", command=lambda: self.do_balSheet())
        self.action_balanceSheet.grid(column=0, row=0, padx=4, pady=6)        
        self.action_journalReport = ttk.Button(self.reportctl, text="Journal Report", command=lambda: self.do_reptTransact(0))
        self.action_journalReport.grid(column=1, row=0, padx=4, pady=6)
        self.action_journalReport = ttk.Button(self.reportctl, text="Single Transact", command=lambda: getTransact(self))
        self.action_journalReport.grid(column=2, row=0, padx=4, pady=6)         
        self.action_ledgerAccount = ttk.Button(self.reportctl, text="Ledger Account", command=lambda: fetchLedgerAccount(self))
        self.action_ledgerAccount.grid(column=3, row=0, padx=4, pady=6)
        self.action_listAccounts = ttk.Button(self.reportctl, text="List Accounts", command=lambda: self.do_reptChart())
        self.action_listAccounts.grid(column=4, row=0, padx=4, pady=6)
        self.action_revenueExpense = ttk.Button(self.reportctl, text="Revenue and Expenses", command=lambda: self.do_RevandExp())
        self.action_revenueExpense.grid(column=5, row=0, padx=4, pady=6)
        self.action_viewPrint = ttk.Button(self.reportctl, text="Print", command=lambda: notImplementedInfo(self))
        self.action_viewPrint.grid(column=6, row=0, padx=4, pady=6)
        self.reportWin = Canvas(frm4b, width=700, height=550,bg='#FFFFFF',scrollregion=(0,0,1000,2000)) 
        hbar=Scrollbar(frm4b,orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM,fill=tk.X)
        hbar.config(command=self.reportWin.xview)
        vbar=Scrollbar(frm4b,orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT,fill=tk.Y)
        vbar.config(command=self.reportWin.yview)
        self.reportWin.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.reportWin.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
               
        self.reportWin.create_text(10,10, anchor=tk.NW, text="Select a view or report, it will display here") 
        
        frm5 = ttk.Labelframe(self.tab5, text='Journal or Ledger Associated Note', width= 650, height=600)
        frm5.grid()
        self.memofields = ttk.LabelFrame(frm5, width=56)
        self.memofields.grid(column=0, row=1, padx=8, pady=4, sticky='W') 
        self.lblmemoID = tk.Label(self.memofields, text="ID").grid(column=0, row=1)
        self.ememoID = tk.Entry(self.memofields, width=10)
        self.ememoID.grid(column=1, row=1, padx=5, pady=4, sticky='W')
        self.lblmemoTransact = tk.Label(self.memofields, text="Transact").grid(column=2, row=1)
        self.ememoTransact = tk.Entry(self.memofields, width=16)
        self.ememoTransact.grid(column=3, row=1, padx=5, pady=4, sticky='W')
        self.lblmemoDate = tk.Label(self.memofields, text="Date").grid(column=4, row=1)
        self.ememoDate = tk.Entry(self.memofields,width=18)
        self.ememoDate.grid(column=5, row=1, padx=5, pady=4, sticky='W')        
                     
        scrolW1  = 80; scrolH1  =  20
        self.scr_memo = scrolledtext.ScrolledText(frm5, width=scrolW1, height=scrolH1, wrap=tk.WORD)
        self.scr_memo.grid(column=0, row=7, padx=4, pady=4, sticky='WE', columnspan=3)
        
        self.memoctl = ttk.LabelFrame(frm5, width=56)
        self.memoctl.grid(column=0, row=0, padx=8, pady=4, sticky='W') 
        self.action_clrmemo = ttk.Button(self.memoctl, text="NEW MEMO", command=lambda: self.newMemo())
        self.action_clrmemo.grid(column=0, row=0, padx=4, pady=6)        
        self.action_prtmemo = ttk.Button(self.memoctl, text="PRINT MEMO", command=lambda: notImplementedInfo(self))
        self.action_prtmemo.grid(column=1, row=0, padx=4, pady=6)        
        self.action_savememo = ttk.Button(self.memoctl, text="SAVE MEMO", command=lambda: self.saveMemo())
        self.action_savememo.grid(column=3, row=0, padx=4, pady=6)
        self.action_loadmemo = ttk.Button(self.memoctl, text="GET ANOTHER", command=lambda: self.fetchMemo())
        self.action_loadmemo.grid(column=4, row=0, padx=4, pady=6)
        
        frm6 = ttk.Labelframe(self.tab6, text='System Maintenance', width= 650, height=600)
        frm6.grid()
        self.action_sysSetup = ttk.Button(frm6, text=" NEW SET-UP ", command=lambda:AccountDB.createAccounts(self)).grid(column=0,row=0, padx=8, pady=4)
        self.action_sysPack = ttk.Button(frm6, text=" PACK DB ", command=lambda:AccountDB.packDatabase(self)).grid(column=1,row=0, padx=8, pady=4)
        self.action_sysSetup = ttk.Button(frm6, text="BACK-UP FILES", command=lambda:AccountDB.packDatabase(self)).grid(column=2,row=0, padx=8, pady=4)
        self.action_sysPack = ttk.Button(frm6, text=" RESTORE FILES", command=lambda:AccountDB.packDatabase(self)).grid(column=3,row=0, padx=8, pady=4)
        self.action_sysTrialBal = ttk.Button(frm6, text="COMPANY NAME", command=lambda:notImplementedInfo(self)).grid(column=0,row=1, padx=8, pady=4)
        self.action_sysTrialBal = ttk.Button(frm6, text="TRIAL BALANCE").grid(column=1,row=1, padx=8, pady=4)
        self.action_sysFiscalClose = ttk.Button(frm6, text="FISCAL CLOSE").grid(column=2,row=1, padx=8, pady=4)
        self.action_sysFiscalClose = ttk.Button(frm6, text="Unassigned").grid(column=3,row=1, padx=8, pady=4)
        
        # meubar created here --------------------------------------------
        menuBar = Menu(self.win)
        self.win.config(menu=menuBar)
        # Add menu items
        # Add System Menu
        sysMenu = Menu(menuBar, tearoff=0)
        sysMenu.add_command(label="New Set-up", command=lambda: AccountDB.createAccounts())
        sysMenu.add_command(label="Open")
        sysMenu.add_command(label="Save")
        sysMenu.add_command(label="Print", command=lambda: notImplementedInfo(self))
        sysMenu.add_command(label="Back-up Database")
        sysMenu.add_command(label="Restore Database")
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
        entryMenu.add_command(label="Make Memo", command=lambda: insertMemoForm(self))
        entryMenu.add_separator()
        entryMenu.add_command(label="Perform Trial Balance", command=lambda: self.do_trialBalance())
        entryMenu.add_command(label="Perform End of Cycle", command=lambda: notImplementedEndofCycle(self))
        menuBar.add_cascade(label="Activity", menu=entryMenu)
        
        # Add an Data entry Menu
        viewMenu = Menu(menuBar, tearoff=0)
        viewMenu.add_command(label="View Journal", command=lambda: self.do_reptTransact(0))
        viewMenu.add_command(label="View Transaction", command=lambda: getTransact(self))
        viewMenu.add_command(label="View Accounts", command=lambda: self.do_reptChart())
        viewMenu.add_command(label="View Ledger", command=lambda: fetchLedgerAccount(self))
        viewMenu.add_command(label="View a Memo", command=lambda: getTransact(self))
        viewMenu.add_separator()
        viewMenu.add_command(label="Trial Balance", command=lambda: self.do_trialBalance())
        viewMenu.add_command(label="End of Year")
        menuBar.add_cascade(label="View", menu=viewMenu)
        
        # Add an Edit Menu
        reportMenu = Menu(menuBar, tearoff=0)
        reportMenu.add_command(label="Balance Sheet", command=lambda: self.do_balSheet())
        reportMenu.add_command(label="Ledger Account", command=lambda: fetchLedgerAccount(self))
        reportMenu.add_command(label="Income Report", command=lambda: self.do_RevandExp())
        reportMenu.add_command(label="Expense Report", command=lambda: self.do_RevandExp())
        reportMenu.add_command(label="Payroll Report", command=lambda: notImplementedPayroll(self))
        reportMenu.add_command(label="Inventory Report",command=lambda: notImplementedInventory(self))
        menuBar.add_cascade(label="Reports", menu=reportMenu)
        
        # Add a Help Menu 
        helpMenu = Menu(menuBar, tearoff=0)
        helpMenu.add_command(label="Context Help",command=lambda: notImplementedHelp(self))
        helpMenu.add_command(label="Documentation",command=lambda: notImplementedHelp(self))
        helpMenu.add_command(label="About", command=lambda: info(self))
        menuBar.add_cascade(label="Help", menu=helpMenu)

        
if __name__ == '__main__':
    asys = AccountingSystem()
    w = (2*asys.win.winfo_screenwidth())/3
    h = (3*asys.win.winfo_screenheight())/4
    asys.win.geometry("%dx%d+0+0" % (w, h))
    asys.win.mainloop()