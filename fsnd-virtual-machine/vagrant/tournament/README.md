# Tournament Project  03/06/2017
=================================

* PostgreSQL

* python

* Databases - tournament.SQL
  - Operate on the VM(vagrant).
  - Import database with "\i tournament.sql"
    - drop exists database named "tournament"
    - create new database and connect
    - create two table "players" and "matches"
    - create one view "standings"

* Python - tournament.py
  - import PostgreSQL
  - code functions
    - connect() : connect to the PostgreSQL database
    - deleteMatches() : remove all the match records from the database
    - deletePlayers() : remove all the player records from the database
    - countPlayers() : returns the number of players
    - registerPlayer() :
        - adds a player to the tournament database
        - assigns a unique serial id for the player
    - playerStandings():
        - returns a list of the players and their win records, sorted by wins
    - reportMatch() : records the match result between two players
    - swissPairings() :
        - returns a list of pairs of players
        - match with equal or nearly-equal win recorded players
        - each player appears exactly once in the pairings

* Python - tournament_test.py
  - test file for the project
