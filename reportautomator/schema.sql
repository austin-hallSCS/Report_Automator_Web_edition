DROP TABLE IF EXISTS report;
DROP TABLE IF EXISTS dellkey;

CREATE TABLE report (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    computername TEXT NOT NULL,
    serialnumber TEXT NOT NULL,
    warrantyenddate DATE NOT NUll,
    code TEXT NOT NULL
);

CREATE TABLE dellkey (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    serialnum TEXT NOT NULL,
    warrantyenddate TEXT NOT NULL
);