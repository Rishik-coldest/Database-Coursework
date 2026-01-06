Create Schema "Coursework";
Set SEARCH_PATH to "Coursework", public;

-- Exam table
CREATE TABLE exam (
excode CHAR(4) PRIMARY KEY,
extitle VARCHAR(200) UNIQUE NOT NULL,
exlocation VARCHAR(200) NOT NULL,
exdate DATE NOT NULL CHECK (EXTRACT (MONTH FROM  exdate) = 11 and EXTRACT (YEAR FROM exdate) = 2025),
extime TIME NOT NULL CHECK (extime >= '09:00:00' and extime <= '18:00:00')
);

-- Student table
CREATE TABLE student (
sno INTEGER PRIMARY KEY,
sname VARCHAR(200) NOT NULL,
semail VARCHAR(200) UNIQUE NOT NULL
);

--Entry table
CREATE TABLE entry (
eno INTEGER PRIMARY KEY,
excode CHAR(4),
sno INTEGER,
egrade DECIMAL(5,2) CHECK (egrade >= 0 and egrade <= 100),
FOREIGN KEY (excode) REFERENCES exam(excode) ON DELETE CASCADE,
FOREIGN KEY (sno) REFERENCES student(sno) ON DELETE CASCADE
);

-- Cancel
CREATE TABLE cancel (
eno INTEGER PRIMARY KEY,
excode CHAR(4),
sno INTEGER,
cdate TIMESTAMP,
cuser VARCHAR(200)
);