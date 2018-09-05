-- Be sure to set timezone to UTC in postgresql.conf, then restart the server
-- Create the database objects for the application.
-- As user postgres:

/*
  For good security, passwords will have to have a random salt plus password.
  To enable this functionality, add the pgcrypto extension.
  https://www.postgresql.org/docs/current/static/pgcrypto.html
*/

CREATE EXTENSION pgcrypto;

CREATE ROLE flaskapp_user CREATEDB;

ALTER ROLE flaskapp_user WITH LOGIN;

DROP DATABASE IF EXISTS flaskapp;

CREATE DATABASE flaskapp;

/*
Set password for user: psql# \password flaskapp_user
Run as user flaskapp_user:
psql -d flaskapp -U flaskapp_user
Then connect to the flaskapp database:
\c flaskapp
*/

-- Table for testing database inserts in Flask
DROP TABLE IF EXISTS notes;

CREATE TABLE notes (
    id      SERIAL,
    note    TEXT
);

DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    id              SERIAL,
    username        TEXT NOT NULL,
    first_name      TEXT,
    last_name       TEXT,
    email           TEXT NOT NULL,
    phone           TEXT,
    user_status     TEXT NOT NULL, -- active, locked, inactive
    user_password   TEXT NOT NULL,
    start_time      TIMESTAMP WITH TIME ZONE NOT NULL
 );

CREATE UNIQUE INDEX users_username_unique_idx ON users (username);

DROP TABLE IF EXISTS roles;

CREATE TABLE roles
(
    id          SERIAL,
    role_name   TEXT NOT NULL,
    user_id     INT NOT NULL     
 );

DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_date
(
    date_dim_id              INT NOT NULL,
    date_actual              DATE NOT NULL,
    epoch                    BIGINT NOT NULL,
    day_suffix               TEXT NOT NULL,
    day_name                 TEXT NOT NULL,
    day_of_week              INT NOT NULL,
    day_of_month             INT NOT NULL,
    day_of_quarter           INT NOT NULL,
    day_of_year              INT NOT NULL,
    week_of_month            INT NOT NULL,
    week_of_year             INT NOT NULL,
    week_of_year_iso         TEXT NOT NULL,
    month_actual             INT NOT NULL,
    month_name               TEXT NOT NULL,
    month_name_abbreviated   TEXT NOT NULL,
    quarter_actual           INT NOT NULL,
    quarter_name             TEXT NOT NULL,
    year_actual              INT NOT NULL,
    first_day_of_week        DATE NOT NULL,
    last_day_of_week         DATE NOT NULL,
    first_day_of_month       DATE NOT NULL,
    last_day_of_month        DATE NOT NULL,
    first_day_of_quarter     DATE NOT NULL,
    last_day_of_quarter      DATE NOT NULL,
    first_day_of_year        DATE NOT NULL,
    last_day_of_year         DATE NOT NULL,
    mmyyyy                   TEXT NOT NULL,
    mmddyyyy                 TEXT NOT NULL,
    weekend_indr             BOOLEAN NOT NULL
);

ALTER TABLE dim_date ADD CONSTRAINT dim_date_date_dim_id_pk PRIMARY KEY (date_dim_id);

CREATE INDEX dim_date_date_actual_idx
  ON dim_date(date_actual);

INSERT INTO dim_date
SELECT TO_CHAR(datum,'yyyymmdd')::INT AS date_dim_id,
    datum AS date_actual,
    EXTRACT(epoch FROM datum) AS epoch,
    TO_CHAR(datum,'fmDDth') AS day_suffix,
    TO_CHAR(datum,'Day') AS day_name,
    EXTRACT(isodow FROM datum) AS day_of_week,
    EXTRACT(DAY FROM datum) AS day_of_month,
    datum - DATE_TRUNC('quarter',datum)::DATE + 1 AS day_of_quarter,
    EXTRACT(doy FROM datum) AS day_of_year,
    TO_CHAR(datum,'W')::INT AS week_of_month,
    EXTRACT(week FROM datum) AS week_of_year,
    TO_CHAR(datum,'YYYY"-W"IW-') || EXTRACT(isodow FROM datum) AS week_of_year_iso,
    EXTRACT(MONTH FROM datum) AS month_actual,
    TO_CHAR(datum,'Month') AS month_name,
    TO_CHAR(datum,'Mon') AS month_name_abbreviated,
    EXTRACT(quarter FROM datum) AS quarter_actual,
    CASE
        WHEN EXTRACT(quarter FROM datum) = 1 THEN 'First'
        WHEN EXTRACT(quarter FROM datum) = 2 THEN 'Second'
        WHEN EXTRACT(quarter FROM datum) = 3 THEN 'Third'
        WHEN EXTRACT(quarter FROM datum) = 4 THEN 'Fourth'
    END AS quarter_name,
    EXTRACT(isoyear FROM datum) AS year_actual,
    datum + (1 -EXTRACT(isodow FROM datum))::INT AS first_day_of_week,
    datum + (7 -EXTRACT(isodow FROM datum))::INT AS last_day_of_week,
    datum + (1 -EXTRACT(DAY FROM datum))::INT AS first_day_of_month,
    (DATE_TRUNC('MONTH',datum) + INTERVAL '1 MONTH - 1 day')::DATE AS last_day_of_month,
    DATE_TRUNC('quarter',datum)::DATE AS first_day_of_quarter,
    (DATE_TRUNC('quarter',datum) + INTERVAL '3 MONTH - 1 day')::DATE AS last_day_of_quarter,
    TO_DATE(EXTRACT(isoyear FROM datum) || '-01-01','YYYY-MM-DD') AS first_day_of_year,
    TO_DATE(EXTRACT(isoyear FROM datum) || '-12-31','YYYY-MM-DD') AS last_day_of_year,
    TO_CHAR(datum,'mmyyyy') AS mmyyyy,
    TO_CHAR(datum,'mmddyyyy') AS mmddyyyy,
    CASE
        WHEN EXTRACT(isodow FROM datum) IN (6,7) THEN TRUE
        ELSE FALSE
    END AS weekend_indr
    FROM (SELECT '1970-01-01'::DATE + SEQUENCE.DAY AS datum
    FROM GENERATE_SERIES (0,29219) AS SEQUENCE (DAY)
    GROUP BY SEQUENCE.DAY) DQ
ORDER BY 1;



