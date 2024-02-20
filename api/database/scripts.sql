CREATE DATABASE chat_app;

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    firstName VARCHAR(225) NOT NULL,
    lastName VARCHAR(225) NOT NULL,
    email VARCHAR(225) NOT NULL,
    password VARCHAR(256) NOT NULL
    );

ALTER TABLE users
ADD COLUMN last_active_at timestamp without time zone;

CREATE TABLE messages(
     message_id SERIAL PRIMARY KEY,
	 message_text VARCHAR(225) NOT NULL,
     created_at TIMESTAMP NOT NULL,
     user_id int REFERENCES users(id) NOT NULL
    );