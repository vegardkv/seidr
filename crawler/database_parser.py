import numpy as np
import sqlite3


def parse(cursor):
    cursor.execute('SELECT * FROM games')
    db_data = cursor.fetchall()
    jng_winner =[]
    top_winner =[]
    mid_winner =[]
    jng_loser = []
    top_loser = []
    mid_loser = []
    for d in db_data:
        try:
            jng = ([i for i in range(30, 35) if d[i] == 'JUNGLE'][0], [i for i in range(35, 40) if d[i] == 'JUNGLE'][0])
            mid = ([i for i in range(30, 35) if d[i] == 'MIDDLE'][0], [i for i in range(35, 40) if d[i] == 'MIDDLE'][0])
            top = ([i for i in range(30, 35) if d[i] == 'TOP'][0], [i for i in range(35, 40) if d[i] == 'TOP'][0])
        except IndexError:
            continue
        winning_team = d[42]
        jng_winner.append(jng[winning_team])
        top_winner.append(top[winning_team])
        mid_winner.append(mid[winning_team])
        jng_loser.append(jng[not winning_team])
        top_loser.append(top[not winning_team])
        mid_loser.append(mid[not winning_team])
    return jng_winner, top_winner, mid_winner, jng_loser, top_loser, mid_loser


if __name__ == '__main__':
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    parse(cursor)
    conn.close()