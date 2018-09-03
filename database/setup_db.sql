-- Create the database objects for the application.

DROP DATABASE IF EXISTS flaskapp;

CREATE DATABASE flaskapp;

-- For good security, passwords will have to have a random salt plus password.
-- https://www.postgresql.org/docs/current/static/pgcrypto.html

CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    id              SERIAL,
    username        VARCHAR(100) NOT NULL,
    first_name      VARCHAR(100),
    last_name       VARCHAR(100),
    email_address   VARCHAR(100) NOT NULL,
    phone_number    VARCHAR(50),
    user_status     TINYINT NOT NULL, -- Active, disabled, deactivated - linking to a status table
    password_salt   VARCHAR(128), -- Unique for every user, inserted when the account is created.
    user_password   VARCHAR(128), -- (Hashed with the salt - SHA256, SHA512, RipeMD, or WHIRLPOOL)
    created_at      TIMESTAMP WITH TIME ZONE NOT NULL,
    deactivated_at  TIMESTAMP WITH TIME ZONE
);


DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_date
(
    date_dim_id              INT NOT NULL,
    date_actual              DATE NOT NULL,
    epoch                    BIGINT NOT NULL,
    day_suffix               VARCHAR(4) NOT NULL,
    day_name                 VARCHAR(9) NOT NULL,
    day_of_week              INT NOT NULL,
    day_of_month             INT NOT NULL,
    day_of_quarter           INT NOT NULL,
    day_of_year              INT NOT NULL,
    week_of_month            INT NOT NULL,
    week_of_year             INT NOT NULL,
    week_of_year_iso         CHAR(10) NOT NULL,
    month_actual             INT NOT NULL,
    month_name               VARCHAR(9) NOT NULL,
    month_name_abbreviated   CHAR(3) NOT NULL,
    quarter_actual           INT NOT NULL,
    quarter_name             VARCHAR(9) NOT NULL,
    year_actual              INT NOT NULL,
    first_day_of_week        DATE NOT NULL,
    last_day_of_week         DATE NOT NULL,
    first_day_of_month       DATE NOT NULL,
    last_day_of_month        DATE NOT NULL,
    first_day_of_quarter     DATE NOT NULL,
    last_day_of_quarter      DATE NOT NULL,
    first_day_of_year        DATE NOT NULL,
    last_day_of_year         DATE NOT NULL,
    mmyyyy                   CHAR(6) NOT NULL,
    mmddyyyy                 CHAR(10) NOT NULL,
    weekend_indr             BOOLEAN NOT NULL
);

ALTER TABLE dw.dim_date ADD CONSTRAINT dim_date_date_dim_id_pk PRIMARY KEY (date_dim_id);

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



