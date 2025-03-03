--
-- File generated with SQLiteStudio v3.4.4 on pon. mar 3 20:12:36 2025
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: Admin
CREATE TABLE IF NOT EXISTS Admin (
    User_ID       REFERENCES User (User_ID),
    Admin_ID TEXT PRIMARY KEY
);


-- Table: Card
CREATE TABLE IF NOT EXISTS Card (
    Card_ID  INTEGER PRIMARY KEY,
    Votes    NUMERIC,
    Team_ID  NUMERIC REFERENCES Team (Team_ID),
    Trend    INTEGER,
    State    INTEGER,
    Comments TEXT
);


-- Table: Sessions
CREATE TABLE IF NOT EXISTS Sessions (
    Session_ID      INTEGER PRIMARY KEY,
    Date,
    Update_Progress TEXT,
    User_ID                 REFERENCES User (User_ID) 
);


-- Table: Team
CREATE TABLE IF NOT EXISTS Team (
    Team_ID     INTEGER PRIMARY KEY,
    Team_Name   TEXT,
    Team_Leader TEXT
);


-- Table: User
CREATE TABLE IF NOT EXISTS User (
    User_ID  INTEGER PRIMARY KEY,
    Name     TEXT,
    Username TEXT,
    Email    TEXT,
    Password TEXT,
    Role     TEXT,
    Team_ID  NUMERIC REFERENCES Team (Team_ID),
    Card_ID  NUMERIC REFERENCES Card (Card_ID),
    Admin_ID NUMERIC REFERENCES Admin (Admin_ID) 
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
