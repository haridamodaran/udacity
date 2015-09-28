#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
# Test with tournament_test.py
import psycopg2

# Database connection
DB = "dbname=tournament"
conn = psycopg2.connect(DB)
# single cursor used by all of the functions
cursor = conn.cursor()


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""

    cursor.execute("DELETE FROM Matches;")
    conn.commit()


def deletePlayers():
    """Remove all the player records from the database."""
    cursor.execute("DELETE FROM Players;")
    conn.commit()


def countPlayers():
    """Returns the number of players currently registered."""
    cursor.execute("SELECT count(*) FROM Players;")
    count = cursor.fetchall()[0][0]
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    cursor.execute('INSERT into Players (name) VALUES (%s)', (name,))
    conn.commit()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    cursor.execute("SELECT * FROM Players order by wins desc")
    players = cursor.fetchall()
    return(players)


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    cursor.execute('INSERT into Matches (winner, loser) VALUES (%s, %s)', (winner, loser))
    conn.commit()

    cursor.execute("SELECT matches FROM Players where id = %s" % (loser))
    loser_matches = cursor.fetchall()[0][0]
    updated_loser_matches = loser_matches + 1
    cursor.execute('UPDATE Players SET matches = (%s) where id = %s', (updated_loser_matches, loser))
    conn.commit()

    cursor.execute("SELECT matches FROM Players where id = %s" % (winner))
    winner_matches = cursor.fetchall()[0][0]
    updated_winner_matches = winner_matches + 1
    cursor.execute('UPDATE Players SET matches = (%s) where id = %s', (updated_winner_matches, winner))
    conn.commit()

    winner_wins = cursor.execute("SELECT wins FROM Players where id = %s" % (winner))
    winner_wins = cursor.fetchall()[0][0]
    updated_winner_wins = winner_wins + 1
    cursor.execute('UPDATE Players SET wins = (%s) where id = %s', (updated_winner_wins, winner))
    conn.commit()


def swissPairings():
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
    cursor.execute("SELECT * FROM Players order by wins DESC")
    players = cursor.fetchall()
    total = len(players)
    pairings = []
    # pairs each person with the adjacent person in the list of players sorted by wins
    for i in range(0, total-1, 2):
        pairings = pairings + [(players[i][0], players[i][1], players[i+1][0], players[i+1][1])]
    return pairings
