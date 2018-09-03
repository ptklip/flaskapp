-- Insert test data.

-- Users
INSERT INTO users (username, first_name, last_name, email, phone, user_status, user_password, start_time)
VALUES ('johndoe', 'John', 'Doe', 'johndoe@mail.com', '5555551212', 'active', crypt('johnspassword', gen_salt('bf')), now());

-- Successful login. Password is correct. 1 row returned.
SELECT username 
FROM users
WHERE username = 'johndoe' AND user_password = crypt('johnspassword', user_password);

UPDATE users
SET user_password = crypt('johnsnewpassword', user_password);
WHERE username = 'johndoe';

