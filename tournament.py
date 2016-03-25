#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")
    #I bet this can be optimized to return a cursor instead.


def deleteAllTournaments():
    """Remove all the tournament records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM tournaments;")
    DB.commit()
    DB.close()
    
def deleteTournament(tournamentid):
    """Remove specified tournament record from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM tournaments WHERE tournamentid = %s;", (tournamentid,))
    DB.commit()
    DB.close()
    
def deleteAllMatches():
    """Remove all the match records from the database.

    Args:
      tournamentid: the id of the tournament you're looking at.
    """
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches;")
    DB.commit()
    DB.close()
    
def deleteMatchesFromTournament(tournamentid):
    """Remove all the match records from the database for the specified tournamentid.

    Args:
      tournamentid: the id of the tournament you're looking at.
    """
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches WHERE tournamentid = %s;", (tournamentid,))
    DB.commit()
    DB.close()

def deleteAllPlayers():
    """Remove all the player records from the database.

    Args:
      tournamentid: the id of the tournament you're looking at.
    """
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players;")
    DB.commit()
    DB.close()
    
def deleteAllPlayersFromTournament(tournamentid):
    """Remove all the player records from the database for the specified tournamentid.

    Args:
      tournamentid: the id of the tournament you're looking at.
    """
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players WHERE tournamentid = %s;", (tournamentid,))
    DB.commit()
    DB.close()

def allPlayerMatches(tournamentid):
    """Return a list of all players in all matches for the specified tournament.

    Args:
      tournamentid: the id of the tournament you're looking at.
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT DISTINCT a.playerid, a.playername, b.playerid, b.playername FROM matches, "
              "players as a, players as b WHERE matches.playerid_winner = a.playerid AND "
              "matches.playerid_loser = b.playerid AND tournamentid = %s;", (tournamentid,))
    playermatches = ({'a.playerid': int(row[0]), 'a.playername': str(row[1]), 'b.playerid': int(row[2]),
                      'b.playername': str(row[3])} for row in c.fetchall())
    return playermatches

def countPlayers(tournamentid):
    """Returns the number of players currently registered.

    Args:
      tournamentid: the id of the tournament you're looking at.
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT count(playerid) AS playercount FROM players WHERE tournamentid = %s;", (tournamentid,))
    tup = c.fetchone()
    result = tup[0]
    """result = ({'playercount': int(row[0])} for row in c.fetchall())"""
    DB.close()
    return result

def countTournaments():
    """Returns the number of tournaments."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT count(tournamentid) AS tournamentidcount FROM tournaments;")
    tup = c.fetchone()
    result = tup[0]
    """result = ({'playercount': int(row[0])} for row in c.fetchall())"""
    DB.close()
    return result

def registerPlayer(name, tournamentid):
    """Adds a player to the tournament database for a particular tournament.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
      tournamentid: the id of the tournament you're looking at.
    """
    DB = connect()
    c = DB.cursor()
    """bleach.clean(name)"""
    c.execute("INSERT INTO players (playername, tournamentid) VALUES (%s, %s);", (name, tournamentid,))
    DB.commit()
    DB.close()
    
def newTournament(sportname):
    """Adds a Tournament to the tournament database.
  
    The database assigns a unique serial id number for the tournament.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      sportname: the name of the sport played(need not be unique).

    Returns:
        tournamentid: the integer id of the tournament just submitted.
    """
    DB = connect()
    c = DB.cursor()
    bleach.clean(sportname)
    c.execute("INSERT INTO tournaments (sportname) VALUES (%s) RETURNING tournamentid;", (sportname,))
    tournamentid = c.fetchone()[0]
    DB.commit()
    DB.close()
    return tournamentid


def playerStandings(tournamentid):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT players.playerid, players.playername, standings.wins, standings.matchcount "
              "FROM players, standings WHERE players.playerid = standings.playerid AND standings.tournamentid = %s "
              "ORDER BY standings.wins DESC, standings.matchcount ASC, players.playername ASC;", (tournamentid,))
    standings = c.fetchall()
    return list(standings)


def allPairs(tournamentid):
    """Returns a list of all match pairings.

    Returns:
      A list of tuples, each of which contains (id1, id2):
        id1: the winning player's unique id
        id2: the losing player's unique id
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT DISTINCT matches.playerid_winner, matches.playerid_loser FROM matches "
              "WHERE matches.tournamentid= %s;", (tournamentid,))
    pairs = c.fetchall()
    return list(pairs)

def reportMatch(winner, loser, tournamentid):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      match:  the id number of the match played
    """
    DB =  connect()
    c = DB.cursor()
    c.execute("INSERT INTO matches (tournamentid, playerid_winner, playerid_loser) "
              "VALUES (%s, %s, %s);", (tournamentid, winner, loser,))
    DB.commit()
    DB.close()

def havePlayed(player1, player2, allPairs):
    """If these two players have played each other, return TRUE. Otherwise return FALSE.

    Args:
        player1: a player<int, string>
        player2: another player (order doesn't matter)<int, string>
        allPairs: a list of tuples <int, string><int, string> representing players of all previous games
    """
    t1 = player1, player2
    t2 = player2, player1
    if (t1 in allPairs) or (t2 in allPairs):
        return True
    else:
        return False
 
def swissPairings(tournamentid):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    winlossrecord = playerStandings(tournamentid)
    allmatches = allPairs(tournamentid)
    pairingList = []
    matchFound = False
    icount = 0
    while icount < len(winlossrecord):
        matchFound = False
        p1 = winlossrecord[icount]
        icount+=1
        p2 = winlossrecord[icount]
        icount+=1

        while matchFound==False:
            if havePlayed(p1,p2,allmatches)==False:
                # They haven't played together.
                match = (p1[0], p1[1], p2[0], p2[1])
                pairingList.append(match)
                matchFound=True
            else:
                # They have played together
                matchFound=False
                p2 = winlossrecord[icount]
                icount+=1

    if matchFound==False:
        match = (p1, p2)
        pairingList.append(match)

    return pairingList


