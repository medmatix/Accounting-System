CREATE DATABASE OpenAccounting;
USE OpenAccounting;

CREATE TABLE chart (
    Account  INTEGER     PRIMARY KEY
                         NOT NULL,
    Name     STRING (50) NOT NULL,
    ActyType STRING (6)  NOT NULL,
    Balance  REAL
);

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

CREATE TABLE ledger (
    Account  INTEGER       NOT NULL,
    Transact [INTEGER KEY] NOT NULL,
    Amount   REAL          NOT NULL,
    Balance  REAL          NOT NULL
);

CREATE TABLE accountmemos (
    MemoID        INTEGER  PRIMARY KEY
                           UNIQUE
                           NOT NULL,
    [Transaction] INTEGER  REFERENCES journal ([Transaction]) 
                           NOT NULL,
    MemoDate      DATETIME NOT NULL,
    Memo          BLOB     NOT NULL
);

INSERT INTO chart VALUES ((100, "ASSETS", "DEBIT", 0),
                (120, "RECEIVABLES","DEBIT",0),
                (200, "LIABILITIES","CREDIT",0), 
                (220, "PAYABLES","CREDIT",0), 
                (300, "EQUITY","CREDIT",0),  
                (400, "REVENUE","CREDIT",0),
                (500, "EXPENSES","DEBIT",0));
                
