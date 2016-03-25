-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
CREATE DATABASE tournament;
\c tournament;

DROP TABLE IF EXISTS tournaments CASCADE;

CREATE TABLE tournaments (
tournamentid serial primary key,
sportname text
);

DROP TABLE IF EXISTS players CASCADE;

CREATE TABLE players (
playerid serial primary key,
playername text,
tournamentid integer references tournaments(tournamentid)
);

DROP TABLE IF EXISTS matches CASCADE;

CREATE TABLE matches (
matchid serial primary key,
tournamentid integer references tournaments(tournamentid),
playerid_winner integer references players(playerid),
playerid_loser integer references players(playerid)
);

DROP VIEW IF EXISTS wincount CASCADE;

CREATE VIEW wincount as (SELECT players.playerid, count(matches.matchid) AS wins, matches.tournamentid
						From players LEFT JOIN matches ON players.playerid = matches.playerid_winner
						GROUP BY players.playerid, matches.tournamentid ORDER BY count(matches.matchid) DESC);
						
DROP VIEW IF EXISTS losscount CASCADE;
						
CREATE VIEW losscount as (SELECT players.playerid, count(matches.matchid) AS losses, matches.tournamentid
						From players LEFT JOIN matches ON players.playerid = matches.playerid_loser
						GROUP BY players.playerid, matches.tournamentid ORDER BY count(matches.matchid) DESC);

DROP VIEW IF EXISTS standings CASCADE;
						
CREATE VIEW standings as (SELECT players.playerid, wincount.wins, SUM(wincount.wins + losscount.losses) AS matchcount, players.tournamentid	FROM players, wincount, losscount WHERE players.playerid = wincount.playerid AND players.playerid = losscount.playerid GROUP BY players.tournamentid, players.playerid, wincount.wins, losscount.losses);