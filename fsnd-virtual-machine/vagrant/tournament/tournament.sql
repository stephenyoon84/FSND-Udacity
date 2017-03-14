-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
drop database if exists tournament;
create database tournament;
\c tournament

create table players (name text, player_id serial primary key);

create table matches (round_num serial primary key, winner int references players(player_id) not null,
  loser int references players(player_id));

create view standings as
  select players.player_id, players.name,
  (select count(matches.winner) from matches where players.player_id = matches.winner) as total_wins,
  (select count(matches.round_num) from matches where players.player_id = matches.winner or players.player_id = matches.loser)
  as total_matches from players order by total_wins desc, total_matches desc;
