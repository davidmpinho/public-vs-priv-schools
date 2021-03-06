#!/bin/bash


# TODO: instead of this file, create this file in Python and run it in there
sqlite3 << 'EXIT_SQLITE'
.open './../data/output/iave_db.sqlite'
.cd './../data/output/'
ATTACH DATABASE 'tables_2016.sqlite' AS db16;
ATTACH DATABASE 'tables_2017.sqlite' AS db17;
ATTACH DATABASE 'tables_2018.sqlite' AS db18;
ATTACH DATABASE 'tables_2019.sqlite' AS db19;

ALTER TABLE db16.grades
    ADD year_exam INTEGER;
ALTER TABLE db17.grades
    ADD year_exam INTEGER;
ALTER TABLE db18.grades 
    ADD year_exam INTEGER;
ALTER TABLE db19.grades 
    ADD year_exam INTEGER;

UPDATE db16.grades
    SET year_exam = 2016;
UPDATE db17.grades
    SET year_exam = 2017;
UPDATE db18.grades
    SET year_exam = 2018;
UPDATE db19.grades
    SET year_exam = 2019;

-- Change the column names to distinguish internal grades from exam grades

BEGIN TRANSACTION;
CREATE TABLE db16.grade_averages_internal_temp (
	"index" BIGINT,
    internal_biology_geology TEXT,
	internal_math TEXT,
	internal_portuguese TEXT,
	internal_physics_chemistry TEXT
);
insert into db16.grade_averages_internal_temp("index", internal_math, internal_portuguese, internal_biology_geology, internal_physics_chemistry)
    select "index", math, portuguese, biology_geology, physics_chemistry
    from db16.grade_averages_internal;
drop table db16.grade_averages_internal;
alter table db16.grade_averages_internal_temp
    rename to grade_averages_internal;
COMMIT;

BEGIN TRANSACTION;
CREATE TABLE db17.grade_averages_internal_temp (
	"index" BIGINT,  
    internal_biology_geology TEXT, 
	internal_math TEXT, 
	internal_portuguese TEXT, 
	internal_physics_chemistry TEXT
);
insert into db17.grade_averages_internal_temp("index", internal_math, internal_portuguese, internal_biology_geology, internal_physics_chemistry)
    select "index", math, portuguese, biology_geology, physics_chemistry
    from db17.grade_averages_internal;
drop table db17.grade_averages_internal;
alter table db17.grade_averages_internal_temp
    rename to grade_averages_internal;
COMMIT;

BEGIN TRANSACTION;
CREATE TABLE db18.grade_averages_internal_temp (
	"index" BIGINT,  
    internal_biology_geology TEXT, 
	internal_math TEXT, 
	internal_portuguese TEXT, 
	internal_physics_chemistry TEXT
);
insert into db18.grade_averages_internal_temp("index", internal_math, internal_portuguese, internal_biology_geology, internal_physics_chemistry)
    select "index", math, portuguese, biology_geology, physics_chemistry
    from db18.grade_averages_internal;
drop table db18.grade_averages_internal;
alter table db18.grade_averages_internal_temp
    rename to grade_averages_internal;
COMMIT;

BEGIN TRANSACTION;
CREATE TABLE db19.grade_averages_internal_temp (
	"index" BIGINT,  
    internal_biology_geology TEXT, 
	internal_math TEXT, 
	internal_portuguese TEXT, 
	internal_physics_chemistry TEXT
);
insert into db19.grade_averages_internal_temp("index", internal_math, internal_portuguese, internal_biology_geology, internal_physics_chemistry)
    select "index", math, portuguese, biology_geology, physics_chemistry
    from db19.grade_averages_internal;
drop table db19.grade_averages_internal;
alter table db19.grade_averages_internal_temp
    rename to grade_averages_internal;
COMMIT;

-- Create a table within each db 'merged'

create table db16.merged as
    select a."index", number, Escola, "Pos. +100 Provas", "Pos. Geral", "Média", "N.º Provas", Concelho, "Indicador de Sucesso", pub_or_pri, year_exam,
           biology_geology, math, portuguese, physics_chemistry,
           "12th_grade", "11th_grade", "10th_grade",
           pct_stud_in_need_12th_grade, pct_profs_on_the_board,
           average_dads, average_moms,
           internal_biology_geology, internal_math, internal_portuguese, internal_physics_chemistry
    from db16.grades as a
        left join  db16.grade_averages_exam as b
        on a."index" = b."index"
        left join db16.ret_rate_school as c
        on a."index" = c."index"
        left join db16.indicator_school as d
        on a."index" = d."index"
        left join db16.parental_edu as e
        on a."index" = e."index"
        left join db16.grade_averages_internal as f
        on a."index" = f."index";
create table db17.merged as
    select a."index", number, Escola, "Pos. +100 Provas", "Pos. Geral", "Média", "N.º Provas", Concelho, "Indicador de Sucesso", pub_or_pri, year_exam,
           biology_geology, math, portuguese, physics_chemistry,
           "12th_grade", "11th_grade", "10th_grade", 
           pct_stud_in_need_12th_grade, pct_profs_on_the_board,
           average_dads, average_moms,
           internal_biology_geology, internal_math, internal_portuguese, internal_physics_chemistry
    from db17.grades as a
        left join  db17.grade_averages_exam as b 
        on a."index" = b."index"
        left join db17.ret_rate_school as c
        on a."index" = c."index"
        left join db17.indicator_school as d
        on a."index" = d."index"
        left join db17.parental_edu as e
        on a."index" = e."index"
        left join db17.grade_averages_internal as f
        on a."index" = f."index";
create table db18.merged as 
    select a."index", number, Escola, "Pos. +100 Provas", "Pos. Geral", "Média", "N.º Provas", Concelho, "Indicador de Sucesso", pub_or_pri, year_exam,
           biology_geology, math, portuguese, physics_chemistry,
           "12th_grade", "11th_grade", "10th_grade", 
           pct_stud_in_need_12th_grade, pct_profs_on_the_board,
           average_dads, average_moms,
           internal_biology_geology, internal_math, internal_portuguese, internal_physics_chemistry
    from db18.grades as a
        left join db18.grade_averages_exam as b 
        on a."index" = b."index"
        left join db18.ret_rate_school as c
        on a."index" = c."index"
        left join db18.indicator_school as d
        on a."index" = d."index"
        left join db18.parental_edu as e
        on a."index" = e."index"
        left join db18.grade_averages_internal as f
        on a."index" = f."index";
create table db19.merged as 
    select a."index", number, Escola, "Pos. +100 Provas", "Pos. Geral", "Média", "N.º Provas", Concelho, "Indicador de Sucesso", pub_or_pri, year_exam,
           biology_geology, math, portuguese, physics_chemistry,
           "12th_grade", "11th_grade", "10th_grade", 
           pct_stud_in_need_12th_grade, pct_profs_on_the_board,
           average_dads, average_moms,
           internal_biology_geology, internal_math, internal_portuguese, internal_physics_chemistry
    from db19.grades as a
        left join db19.grade_averages_exam as b 
        on a."index" = b."index"
        left join db19.ret_rate_school as c
        on a."index" = c."index"
        left join db19.indicator_school as d
        on a."index" = d."index"
        left join db19.parental_edu as e
        on a."index" = e."index"
        left join db19.grade_averages_internal as f
        on a."index" = f."index";

-- Join by 'Escola'/school (create two temporary tables for this to be less confusing)

create table main.all_data as
    select *
    from db16.merged;
insert into main.all_data 
    select *
    from db17.merged;
insert into main.all_data
    select * 
    from db18.merged;
insert into main.all_data
    select * 
    from db19.merged;

.headers ON
.mode csv
.output iave_db.csv
select * from main.all_data;
.output stdout

.exit
EXIT_SQLITE

zip -j ./../data/output/iave_db.zip ./../data/output/iave_db.csv
rm ./../data/output/exp*.sqlite ./../data/output/iave_db.sqlite ./../data/output/iave_db.csv

