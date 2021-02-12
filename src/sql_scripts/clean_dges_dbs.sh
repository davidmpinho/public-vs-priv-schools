#!/bin/bash


# TODO: instead of this file, create this file in Python and run it
sqlite3 << 'EXIT_SQLITE'
.open './../data/output/dges_db.sqlite'
.cd './../data/output/'
ATTACH DATABASE 'dges_2016.sqlite' AS db16;
ATTACH DATABASE 'dges_2017.sqlite' AS db17;
ATTACH DATABASE 'dges_2018.sqlite' AS db18;
ATTACH DATABASE 'dges_2019.sqlite' AS db19;

-- Add year to the "Homologa" tables
-- TODO: add at the end: "WHERE year_exam is NULL"
ALTER TABLE db16.tblHomologa_2016
    ADD year_exam INTEGER;
ALTER TABLE db17.tblHomologa_2017
    ADD year_exam INTEGER;
ALTER TABLE db18.tblHomologa_2018
    ADD year_exam INTEGER;
ALTER TABLE db19.tblHomologa_2019
    ADD year_exam INTEGER;

UPDATE db16.tblHomologa_2016
    SET year_exam = 2016;
UPDATE db17.tblHomologa_2017
    SET year_exam = 2017;
UPDATE db18.tblHomologa_2018
    SET year_exam = 2018;
UPDATE db19.tblHomologa_2019
    SET year_exam = 2019;

-- Put all the information in the "Homologa" tables

CREATE TABLE main.all_data AS 
    SELECT * FROM (SELECT * FROM db16.tblHomologa_2016 AS a
                   LEFT JOIN (SELECT b.Escola, b.Descr as 'EscolaDescr', b.Distrito, 
                                     b.Concelho, b.PubPriv, b.CodDGAE, b.CodDGEEC
                              FROM db16.tblEscolas AS b) AS b
                   USING (Escola)
                   LEFT JOIN (SELECT c.Distrito, c.Concelho, c.Descr AS 'ConcelhoDescr', c.Nuts3
                              FROM db16.tblCodsConcelho AS c) AS c
                   USING (Concelho, Distrito)
                   LEFT JOIN (SELECT d.Distrito, d.Descr AS 'DistritoDescr' 
                              FROM db16.tblCodsDistrito AS d) AS d
                   USING (Distrito)
                   LEFT JOIN (SELECT e.Exame, e.TipoExame, e.Descr AS 'ExameDescr' 
                              FROM db16.tblExames AS e) AS e
                   USING (Exame)
                   LEFT JOIN (SELECT f.Nuts3, f.Descr AS 'Nuts3Descr' 
                              FROM db16.tblNuts3 AS f) AS f
                   USING (Nuts3)
                   LEFT JOIN (SELECT g.Curso, g.TpCurso, g.SubTipo, g.Descr AS 'CursoDescr' 
                              FROM db16.tblCursos AS g) AS g
                   USING (Curso)
                   LEFT JOIN (SELECT h.TpCurso, h.Ano_Ini, h.Ano_Term, h.Ordena, h.Descr as 'TpCursoDescr'
                              FROM db16.tblCursosTipos AS h) AS h
                   USING (TpCurso)
                   LEFT JOIN (SELECT i.SubTipo, i.Descr as 'SubTipoDescr' 
                              FROM db16.tblCursosSubTipos AS i) AS i 
                   USING (SubTipo)
                   LEFT JOIN (SELECT j.SitFreq, j.Descr as 'SitFreqDescr'
                              FROM db16.tblSitFreq AS j) AS j 
                   USING (SitFreq));
INSERT INTO main.all_data 
    SELECT * FROM (SELECT * FROM db17.tblHomologa_2017 AS a
                   LEFT JOIN (SELECT b.Escola, b.Descr as 'EscolaDescr', b.Distrito, 
                                     b.Concelho, b.PubPriv, b.CodDGAE, b.CodDGEEC
                              FROM db17.tblEscolas AS b) AS b
                   USING (Escola)
                   LEFT JOIN (SELECT c.Distrito, c.Concelho, c.Descr AS 'ConcelhoDescr', c.Nuts3
                              FROM db17.tblCodsConcelho AS c) AS c
                   USING (Concelho, Distrito)
                   LEFT JOIN (SELECT d.Distrito, d.Descr AS 'DistritoDescr' 
                              FROM db17.tblCodsDistrito AS d) AS d
                   USING (Distrito)
                   LEFT JOIN (SELECT e.Exame, e.TipoExame, e.Descr AS 'ExameDescr' 
                              FROM db17.tblExames AS e) AS e
                   USING (Exame)
                   LEFT JOIN (SELECT f.Nuts3, f.Descr AS 'Nuts3Descr' 
                              FROM db17.tblNuts3 AS f) AS f
                   USING (Nuts3)
                   LEFT JOIN (SELECT g.Curso, g.TpCurso, g.SubTipo, g.Descr AS 'CursoDescr' 
                              FROM db17.tblCursos AS g) AS g
                   USING (Curso)
                   LEFT JOIN (SELECT h.TpCurso, h.Ano_Ini, h.Ano_Term, h.Ordena, h.Descr as 'TpCursoDescr'
                              FROM db17.tblCursosTipos AS h) AS h
                   USING (TpCurso)
                   LEFT JOIN (SELECT i.SubTipo, i.Descr as 'SubTipoDescr' 
                              FROM db17.tblCursosSubTipos AS i) AS i 
                   USING (SubTipo)
                   LEFT JOIN (SELECT j.SitFreq, j.Descr as 'SitFreqDescr'
                              FROM db17.tblCodsSitFreq AS j) AS j 
                   USING (SitFreq));
INSERT INTO main.all_data 
    SELECT * FROM (SELECT * FROM db18.tblHomologa_2018 AS a
                   LEFT JOIN (SELECT b.Escola, b.Descr as 'EscolaDescr', b.Distrito, 
                                     b.Concelho, b.PubPriv, b.CodDGAE, b.CodDGEEC
                              FROM db18.tblEscolas AS b) AS b
                   USING (Escola)
                   LEFT JOIN (SELECT c.Distrito, c.Concelho, c.Descr AS 'ConcelhoDescr', c.Nuts3
                              FROM db18.tblCodsConcelho AS c) AS c
                   USING (Concelho, Distrito)
                   LEFT JOIN (SELECT d.Distrito, d.Descr AS 'DistritoDescr' 
                              FROM db18.tblCodsDistrito AS d) AS d
                   USING (Distrito)
                   LEFT JOIN (SELECT e.Exame, e.TipoExame, e.Descr AS 'ExameDescr' 
                              FROM db18.tblExames AS e) AS e
                   USING (Exame)
                   LEFT JOIN (SELECT f.Nuts3, f.Descr AS 'Nuts3Descr' 
                              FROM db18.tblNuts3 AS f) AS f
                   USING (Nuts3)
                   LEFT JOIN (SELECT g.Curso, g.TpCurso, g.SubTipo, g.Descr AS 'CursoDescr' 
                              FROM db18.tblCursos AS g) AS g
                   USING (Curso)
                   LEFT JOIN (SELECT h.TpCurso, h.Ano_Ini, h.Ano_Term, h.Ordena, h.Descr as 'TpCursoDescr'
                              FROM db18.tblCursosTipos AS h) AS h
                   USING (TpCurso)
                   LEFT JOIN (SELECT i.SubTipo, i.Descr as 'SubTipoDescr' 
                              FROM db18.tblCursosSubTipos AS i) AS i 
                   USING (SubTipo)
                   LEFT JOIN (SELECT j.SitFreq, j.Descr as 'SitFreqDescr'
                              FROM db18.tblCodsSitFreq AS j) AS j 
                   USING (SitFreq));
INSERT INTO main.all_data 
    SELECT * FROM (SELECT * FROM db19.tblHomologa_2019 AS a
                   LEFT JOIN (SELECT b.Escola, b.Descr as 'EscolaDescr', b.Distrito, 
                                     b.Concelho, b.PubPriv, b.CodDGAE, b.CodDGEEC
                              FROM db19.tblEscolas AS b) AS b
                   USING (Escola)
                   LEFT JOIN (SELECT c.Distrito, c.Concelho, c.Descr AS 'ConcelhoDescr', c.Nuts3
                              FROM db19.tblCodsConcelho AS c) AS c                              
                   USING (Concelho, Distrito)
                   LEFT JOIN (SELECT d.Distrito, d.Descr AS 'DistritoDescr' 
                              FROM db19.tblCodsDistrito AS d) AS d
                   USING (Distrito)
                   LEFT JOIN (SELECT e.Exame, e.TipoExame, e.Descr AS 'ExameDescr' 
                              FROM db19.tblExames AS e) AS e
                   USING (Exame)
                   LEFT JOIN (SELECT f.Nuts3, f.Descr AS 'Nuts3Descr' 
                              FROM db18.tblNuts3 AS f) AS f                                -- NOTE: this has to be 2018
                   USING (Nuts3)
                   LEFT JOIN (SELECT g.Curso, g.TpCurso, g.SubTipo, g.Descr AS 'CursoDescr' 
                              FROM db19.tblCursos AS g) AS g
                   USING (Curso)
                   LEFT JOIN (SELECT h.TpCurso, h.Ano_Ini, h.Ano_Term, h.Ordena, h.Descr as 'TpCursoDescr'
                              FROM db19.tblCursosTipos AS h) AS h
                   USING (TpCurso)
                   LEFT JOIN (SELECT i.SubTipo, i.Descr as 'SubTipoDescr' 
                              FROM db19.tblCursosSubTipos AS i) AS i 
                   USING (SubTipo)
                   LEFT JOIN (SELECT j.SitFreq, j.Descr as 'SitFreqDescr'
                              FROM db19.tblCodsSitFreq AS j) AS j 
                   USING (SitFreq));

.headers ON
.mode csv
.output dges_db.csv
select * from main.all_data;
.output stdout

.exit
EXIT_SQLITE

zip -j ./../data/output/dges_db.zip ./../data/output/dges_db.csv
rm ./../data/output/dges_*.csv ./../data/output/dges_*.sqlite 

