![Accounting System](/images/Number_cruncherCr3.png)

# Accounting System

A basic accounting system compliant with Generally Accepted Accounting Practice (or Principles) (GAAP). It is written in python 3.7 and SQLite3.

## Introduction  
  
There are lots of accounting information systems both proprietary and free and open source. I needed a project to exercise my python, sql and tkinter coding. The fact that it is a necessary review of my MBA curriculum doesn't hurt either after a long absence of my attention there. Finally, I think another open source offering is good and this is intened be a simple, straight forward, and transparent development offering of a accounting application. 

## Principle 
The central core of accounting is considered to be the General Ledger. The instrument of first entry however is the General Journal. All other aspects of the system are either suecondary entry or subsidieary journals and reoprts. The well known Balance Sheet, the consolidated picture of an enterprise, is a report based on the General Ledger contents.

The entry of business activities is first into the Journal, or day book. The items of the Journal are posted then to the Ledger. The double entry technique of accounting ensures that the credit accounts and the debit accounts remain in balance. If the credits always equal the the debits from the outset, and there is no other confounding entries allowed balance is retained. This is a kind of drudge task for which computer programs is eminently suited.

It should be impossible to enter any accounting data except through the general journal. Accounts should be easily added but not removable unless never referenced in transactions (i.e There must never have been any entries for the account in the current fiscal cycle (year), meaning since the books were last closed out).

## Approach
Thus the Journal is where data enters the system and is the date-time record of activity. Data is then reorganized and transferred to the Ledger. The ledger is the categorized permanent record of the enterprise's functioning - taking in revenue and paying expenses to produce some value. The business operation is accountable to internal and external stakeholders. This accounting to stakeholders requires a data trail is maintained with integrity and be demonstable on demand. The audit trailas it is called must be immutable right to the reports needed to account to stakeholders.

![Accounting Relationships](AccountingSystemOrganization.png)

The underlying categorization is defined by a set of accounts to which activities are attributated. This is kept in the Chart of Accounts. In modern American GAAP there are five essential accounts aways present as prinary accounts with variable kinds of subsidiary accounts providing a detailed breakdown of these five. These in the US, Canada and the UK are 1) Assets Account, 2) Liabilities Account, 3) Equity or Capital Accounts, 4) Revenue or Income Account and 5) Expense of Costs Account. There is usually some way to remove bad data or expired value from the system. This sixth account or Disposables (6) is how depreciated value, bad debts and perhaps erroneous data, can be removed from the system in a clearly demonstrable and auditable way. 
  
Often the write-offs are kept as an account in expenses as the result of their access is to expense a bad dept of similar business losses. It is more difficult to retrieve expensed write-offs in a future accounting cycle however so there are advantages to retained write-offs in their own ledger.
  
DEBIT ACCOUNTS | NUMBERING | CREDIT ACCOUNTS | EXAMPLES
---------------|-----------|-----------------|-----------------------------
Assets         |   1xx     | |101 Bank, 120 Receivables
| |   2xx     | Liabilities | 220 Payables
| |   3xx     | Equity     | 301 Retained Earnings
| |   4xx     | Revenue    | 420 Sales
Expenses       |   5xx     | | 520 Mortgage
| |   6xx     | Disposables | 620 Write-offs (Bad Debts)

To debit a Debit Account is to increase it, similarly for crediting an Credit Account. Crediting a Debit Account reduces it and vis-a-versa. Addition and subtraction of figures are implied and automatic. That is what the program must do in the database table. Thus to balance accounts all debits have a credit somewhere and all credits have and offsetting debit - double entry.
  
  
## Implementation:

The Context of the development can be best represented by the list of imports. All non-standard libraries are pip installable.


#### Imports

- Standard library and third party imports
- tkinter imports

```
import tkinter as tk

from tkinter import ttk

from tkinter import scrolledtext

from tkinter import Menu

from tkinter import messagebox as mBox

from tkinter import simpledialog

from tkinter import Scrollbar

from tkinter import Canvas

from tkinter import font
```

  - other standard and third party imports
  - all 3rd party are pip installable
  
```

import sqlite3

import datetime as dt

import pytz

import math as mt

import numpy as np

import sys
```

# Custom module imports
from AccountDB import AccountDB
from FormDialogs import insertJournalForm, insertChartForm, insertMemoForm
from FormDialogs import ReportFormats
from Tooltips import createToolTip, ToolTip
from ReportPreps import TrialBalance 
Once the structure is decided on, the creation of the database, and it's tables behind the interface then the needed enabling code guided the development. The stored data must be clearly separated in development from the derived data. The latter are the reports and summaries also central to accounting, the balance sheet, revenue and expense reports and special or subsidiary journals which may play important parts in therereporting for some enterprises. The stored data which are SQLite Database and tables with keys and indexes are as follows.

### Tables of OpenAccounting.db:

Ref | Accounting Reference | Table
-----|----------------------|------------
1|The Chart of Accounts | chart
2|The General Journal | journal
3|The General Ledger | ledger
4|The Accounting Annotation| accountmemos

Eash table structure is shown by the SQL DDL statement that created it.

#### Structure of chart Table

```
CREATE TABLE chart (
    Account  INTEGER     PRIMARY KEY
                         NOT NULL,
    Name     STRING (50) NOT NULL,
    ActyType STRING (6)  NOT NULL,
    Balance  REAL
);
```

#### Structure of journal Table

```

CREATE TABLE journal (
    [Transaction] INT         PRIMARY KEY
                              NOT NULL,
    Date          DATETIME    NOT NULL,
    Time          DATETIME,
    Description   STRING (40) NOT NULL,
    DebitAccount  INTEGER (4) NOT NULL,
    DebitAmount   REAL        NOT NULL,
    CreditAccount INTEGER (4) NOT NULL,
    CreditAmount  DECIMAL     NOT NULL,
    Posted        BOOLEAN     NOT NULL
                              DEFAULT (0) 
);

```

#### Structure of ledger Table

```

CREATE TABLE ledger (
    Account  INTEGER       NOT NULL,
    Transact [INTEGER KEY] NOT NULL,
    Amount   REAL          NOT NULL,
    Balance  REAL          NOT NULL
);

```

#### Structure of accountmemos Table

```

CREATE TABLE accountmemos (
    MemoID        INTEGER  PRIMARY KEY
                           UNIQUE
                           NOT NULL,
    [Transaction] INTEGER  REFERENCES journal ([Transaction]) 
                           NOT NULL,
    MemoDate      DATETIME NOT NULL,
    Memo          BLOB     NOT NULL
);

```
In spite of the predominantly top-down approach evident, the functionality is determined by the data tables at the system's core. It is reasonable that a data heavy application be at it's heart data driven (here, bottom-up). The manipulation of the data is guided by the the needs of accounting, and the interface is key to that.

Coding was M-V-C modular and this can be seen from the organization of the source. Starting with the interface, we present the screenshots that lead the bookkeeper to the accounting activities.

![Accounting System](/images/ScreenJournalTab.png)
  
Discussing the 'Accounting Functions' specifically  in light of the interface presented, consider the entry point to the system - the General Journal. The other accessible information is this accounting set-up reflected in the Chart of Accounts.

![Accounting System](/images/ScreenChartTab.png)
  
The Ledger accounts set up via the Chart of Account are the records of where moneys are flowing from and to. The permanent account are those of the balance sheet, - in general terms the Assets and Liabilities. When the enterprise starts operating funds provided are the owner's equity, Accounts 300 and so on. The Core assets, 100 series accounts, are the Bank holding the capital itself and the incoming cash. Moneys owed to but not yet held by the compant are Accounts recevable (120). Obligations the company aquires are it's liabilities, 200 series accounts, principal among which is the Accounts Payable (220) as bills received but not yet paid. Other 100, 200 (and less so 300) series accounts may be used BUT the ones already mentioned are immutable and present in all accounting set-ups. At the start of use, the System provides these with the database tables created.

Passing mention, for now, of the General Ledger is sufficient as this is not directly accessible, ever, but populated as Transactions in the Daily Journal entries. 

![Accounting System](/images/ScreenLedgerTab.png)

Later the General ledger is the source of the required and useful accounting reporting.

![Accounting System](/images/ScreenReportTab1.png)

![Accounting System](/images/ScreenReportTab2.png)

The ability to annoted journal entries in more detail than the Transaction Descriptiong allows is desirable but not a canonical requirement per se in accounting systems. For our system the accounting memo interface expediteds this.
  
![Accounting System](/images/ScreenMemoTab.png)

Lastly we consider the more general control required for any database systems and the consideration too of the face that accounting is a cyclical process focused on (rather artificial) fiscal periods of business activity. We need to be able to manage the system so a maintenance interface is provided.

![Accounting System](/images/ScreenMaintenanceTab.png)

====

Project Repository maintained by David York.
  
Copyright Medmatix, David York 2018.
  
License under: MIT license.
