-- Insert test data.

INSERT INTO notes (note)
VALUES
('Pick up hot dogs and buns.'),
('Run the pool filter.')


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
SET user_password = crypt('johnsnewpassword', user_password)
WHERE username = 'johndoe';

