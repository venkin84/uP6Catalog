DROP DATABASE IF EXISTS catalogDB;

CREATE DATABASE catalogDB;

\connect catalogDB;

CREATE TABLE categories(
	catID SERIAL PRIMARY	KEY,
	catName varchar(50) NOT NULL
);

-- CREATE VIEW FOR Latest Added Items