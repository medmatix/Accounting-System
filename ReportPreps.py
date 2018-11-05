'''
Created on Nov 3, 2018

@author: david
'''
import tkinter as tk
from tkinter import messagebox as mBox
import math as mt
import numpy as np
import sqlite3
from AccountDB import AccountDB

class TrialBalance(object):
    '''
    Class for Trial Balance Calculations
    '''


    def __init__(self, params):
        '''
        Constructor set up the trial balance
        '''
        

    
    def getLedgerData(self):
        '''
        '''
        # Call database get ledger(all)
        # Get a current list of account numbers from chart
        accList = []
        db = sqlite3.connect('OpenAccounting.db')
        cursor = db.cursor()
        cursor.execute("SELECT Account FROM chart ORDER BY Account")
        for row in cursor:            
            accList.append(row[0])        
        db.close()
        balDict = {0:0.0}     
        for account in accList:
            accTotal = 0
            ldgrAccount = AccountDB.getLedgerAccount(self, account)
            # sum transactions by account 
            for row in ldgrAccount:
                accTotal = accTotal + row[2]            
            #record balances and account numbers in balList
            balDict[account] = accTotal            
        # display the balances in a dialog
        return(balDict)
        # mBox._show(title="Partial Trial Balance", message="Compare to Balances in Chart of Accounts \n\n"+tbal+"\n If they do not match the account is out of balance", _icon="", _type="")
        
        
        
        

        
    def trialBalance(self):
        '''
        '''
        # Get account transactions totals
        acctBalances = TrialBalance.getLedgerData(self)
        debitBalances = 0.0
        for x, y in acctBalances.items():
            if (x >= 100 and x<= 199):
                debitBalances = debitBalances + y
            if (x >= 500 and x<= 599):
                debitBalances = debitBalances + y
        creditBalances = 0.0
        for x, y in acctBalances.items():
            if (x >= 200 and x<= 499):
                creditBalances = creditBalances + y    
        return (debitBalances, creditBalances)

        # Compare with Chart of Accounts balances for Chart integrity
                
        # Report Discrepancies
        
