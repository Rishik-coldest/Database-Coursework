Set SEARCH_PATH to "Coursework", public;



--------All four table viewing transactions--------
Select * from student;
Select * from exam;
Select * from entry;
Select * from cancel;


------------Inserts into student, exam and entry tables-------------------------
INSERT into student (sno, sname, semail) 
VALUES
(100000, 'Bruno Fernandes', 'Bruno@gmail.com'),
(200000, 'Oscar Tom', 'Oscar@gmail.com'),
(400000, 'Saul Goodman', 'Saul@gmail.com'),
(30000, 'Manor Gnonto', 'Manor@gmail,com');

INSERT into exam (excode, extitle, exlocation, exdate, extime) 
VALUES 
('EX09', 'Programming', 'Exam hall B', '2025-11-5', '11:00:00'),
('EX08', 'English', 'Exam hall Y', '2025-11-8', '12:00:00'),
('EX06', 'Biology', 'Exam hall H', '2025-11-14', '15:00:00'),
('EX30', 'Data Science', 'Exam hall W', '2025-11-18', '12:00:00');

INSERT INTO entry (eno, excode, sno, egrade)
VALUES 
(9000, 'EX09', 30000, NULL),
(2900, 'EX08', 100000, null),
(5555, 'EX06', 200000, 70.5);

----------Function and Trigger to delete student and move entry to cancel table---------
CREATE or REPLACE FUNCTION delete_student()
RETURNS TRIGGER AS $$
BEGIN
INSERT INTO cancel (eno, excode, sno, cdate, cuser)
SELECT eno, excode, sno, CURRENT_TIMESTAMP, 'admin'
FROM entry 
WHERE sno = OLD.sno;
DELETE FROM entry WHERE sno = OLD.sno;
RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_student
BEFORE DELETE ON student
FOR EACH ROW 
EXECUTE FUNCTION delete_student();

----------Transaction that deletes student--------
DELETE FROM student WHERE sno = 100000;


--------------Function and Trigger to delete an exam given no entries for it exist----------
CREATE OR REPLACE FUNCTION exam_deletion()
RETURNS TRIGGER AS $$
BEGIN
IF EXISTS(SELECT * FROM entry WHERE excode = OLD.excode) THEN
RAISE EXCEPTION 'Cannot delete exam, entries still exist';
END IF;
RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER exam_deletion
BEFORE DELETE ON exam
FOR EACH ROW
EXECUTE FUNCTION exam_deletion();

-------------Transaction that deletes exam--------
DELETE FROM exam WHERE excode = 'EX30';


-------------Function and Trigger to insert an entry to a student given they do not have an existing one--------------
CREATE OR REPLACE FUNCTION    insert_entry()
RETURNS TRIGGER AS $$
DECLARE
exam_date DATE;
BEGIN
SELECT exdate 
INTO exam_date
FROM exam
WHERE excode = NEW.excode;
IF EXISTS
(SELECT * FROM entry 
JOIN exam ON entry.excode = exam.excode 
WHERE entry.sno = NEW.sno 
AND exam.exdate = exam_date) THEN 
RAISE EXCEPTION 'Student is occupied on this date';
END IF;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER insert_entry
BEFORE INSERT ON entry
FOR EACH ROW
EXECUTE FUNCTION insert_entry();

---------Transaction to update entry with grade-------------
UPDATE entry
SET egrade = 60
WHERE eno = 9000;


-------------A view to represent an individual student's timetable----------------------
CREATE OR REPLACE VIEW timetable AS
SELECT student.sno, student.sname, exam.exlocation, exam.excode, exam.extitle, exam.exdate, exam.extime
FROM student, entry, exam
WHERE student.sno = entry.sno AND entry.excode = exam.excode;

---------Transaction to show a students timetable------
SELECT * FROM timetable WHERE sno = 30000;

------------A view to represent all exam results for all students-----------
CREATE OR REPLACE VIEW exam_results AS
SELECT exam.excode, exam.extitle, student.sname,
CASE
WHEN entry.egrade IS NULL THEN
'Not taken'
WHEN entry.egrade >= 70 THEN 'Distinction'
WHEN entry.egrade >= 50 THEN 'Pass'
ELSE 'Fail'
END AS RESULT
FROM exam, entry, student
WHERE exam.excode = entry.excode
AND entry.sno = student.sno
ORDER BY exam.excode, student.sname, exam.extitle;

-------------Transaction to show all exam results------
SELECT * FROM exam_results;

-------------Transaction to show all results for a specific exam----------
SELECT * FROM exam_results WHERE excode = 'EX09';