-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament;

CREATE TABLE Matches (
	-- To support multiple matches in future, an id field would be required
	-- id 	serial PRIMARY KEY,
	winner	integer references Players(id),
	loser	integer references Players(id)
);

CREATE TABLE Players (
	id		serial PRIMARY KEY,
	name	text,
 	wins	integer DEFAULT 0,
 	matches integer DEFAULT 0



);