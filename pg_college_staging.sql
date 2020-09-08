DROP SCHEMA IF EXISTS college CASCADE;
CREATE SCHEMA college;
SET SCHEMA 'college';

-- create Classes
-- tid,instructor,dept,cno,cname,credits
CREATE TABLE Classes(
    tid varchar(50),
    instructor varchar(200),
    dept varchar(50),
    cno char(6),
    cname varchar(200),
    credits integer
);

-- create Current_Students
-- sid,fname,lname,dob,cno,cname,credits,grade
CREATE TABLE Current_Students(
    sid varchar(50),
    fname varchar(200),
    lname varchar(200),
    dob varchar(20),
    cno char(6),
    cname varchar(200),
    credits integer,
    grade char(2)
);

-- create New_Students
-- sid,fname,lname,dob
CREATE TABLE New_Students(
    sid varchar(50),
    fname varchar(200),
    lname varchar(200),
    dob date
);