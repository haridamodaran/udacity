#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
# Test with tournament_test.py
import psycopg2

# Database connection
DB = "dbname=tournament"
conn = psycopg2.connect(DB)
cursor = conn.cursor()

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

def getPlayers():
    cursor.execute("select * from players order by id")
    players = cursor.fetchall()
    return players


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
    cursor.execute("SELECT * FROM Players order by wins desc, omw desc")
    players = cursor.fetchall()
    return(players)


def registerMatch(winner, loser):
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

    # Before a match, update the omw of player A to reflect the previous wins of player B
    cursor.execute("SELECT omw FROM Players where id = %s" % (winner))
    winner_omw = cursor.fetchall()[0][0]
    cursor.execute("SELECT omw FROM Players where id = %s" % (loser))
    loser_omw = cursor.fetchall()[0][0]
    cursor.execute("SELECT wins FROM Players where id = %s" % (winner))
    winner_prev_wins = cursor.fetchall()[0][0]
    cursor.execute("SELECT wins FROM Players where id = %s" % (loser))
    loser_prev_wins = cursor.fetchall()[0][0]
    updated_winner_omw = winner_omw + loser_prev_wins
    updated_loser_omw = loser_omw + winner_prev_wins
    cursor.execute('UPDATE Players SET omw = (%s) where id = %s', (updated_winner_omw, winner))
    conn.commit()
    cursor.execute('UPDATE Players SET omw = (%s) where id = %s', (updated_loser_omw, loser))
    conn.commit()
    
    # After the match, increment the omw of all participants who have played against the winner
    cursor.execute("SELECT * FROM matches WHERE winner = %s OR loser = %s" % (winner, winner))
    players_for_omw_update = cursor.fetchall()
    for tuple in players_for_omw_update:
        for p in tuple:
            if (p == winner):
                pass
            else:
                cursor.execute('UPDATE Players SET omw = omw + 1 where id = %s' % (p))
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
    cursor.execute("SELECT * FROM Players order by wins DESC, omw desc")
    players = cursor.fetchall()
    total = len(players)
    pairings = []
    # pairs each person with the adjacent person in the list of players sorted by wins
    for i in range(0, total-1, 2):
        pairings = pairings + [(players[i][0], players[i][1], players[i+1][0], players[i+1][1])]
    return pairings
