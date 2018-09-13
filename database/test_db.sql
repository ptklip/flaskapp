-- Insert test data.

INSERT INTO notes (note)
VALUES
('Pick up hot dogs and buns.'),
('Run the pool filter.')
;


-- Users
INSERT INTO users (username, first_name, last_name, email, phone, user_status, user_password, start_time)
VALUES ('johndoe', 'John', 'Doe', 'johndoe@mail.com', '5555551212', 'active', crypt('johnspassword', gen_salt('bf')), now());

-- Authenticate a user.
-- Successful login. Password is correct. 1 row returned.
SELECT username 
FROM users
WHERE username = 'johndoe' AND user_password = crypt('johnspassword', user_password);

-- Change the password.
UPDATE users
SET user_password = crypt('john', user_password)
WHERE username = 'johndoe';

-- Roles
INSERT INTO roles (role_name, user_id)
VALUES ('admin', 1);

-- ETL Jobs
INSERT INTO etl_jobs (job_name, job_description, last_run_time, last_run_status)
VALUES ('red_sox_team_batting_stats', 'Get Red Sox team batting stats from baseball-reference.com and insert into PostgreSQL', now(), 'success');

-- ETL Job Schedule
INSERT INTO etl_job_schedule (job_id, frequency, weekdays, weekends, holidays)
VALUES (1, 'daily', '1', '1', '1');

-- Batting Stats Current Season
INSERT INTO batting_stats_current_season_staging (position, player_name, age, games_played, plate_appearences, at_bats, runs_scored, hits, doubles, \
    triples, home_runs, runs_batted_in, stolen_bases, caught_stealing, bases_on_balls, strike_outs, batting_average, on_base_percentage, \
    slugging_percentage, on_base_plus_slugging, on_base_percentage_plus, total_bases, grounded_into_double_play, hit_by_pitch, sacrifice_hits, \
    sacrifice_flies, intentional_bases_on_balls)
VALUES ('C', 'Sandy Leon', 29, 78, 258, 235, 29, 45, 11, 0, 5, 21, 1, 0, 15, 64, .191, .251, .302, .553, 49, 71, 5, 4, 3, 1, 0);

