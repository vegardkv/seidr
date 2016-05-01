import numpy as np
import sqlite3


def masterylevel_by_role(cursor):
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
        # Subtract 20 to get mastery level score
        jng_winner.append(float(d[jng[winning_team]-20]))
        top_winner.append(float(d[top[winning_team]-20]))
        mid_winner.append(float(d[mid[winning_team]-20]))
        jng_loser.append(float(d[jng[not winning_team]-20]))
        top_loser.append(float(d[top[not winning_team]-20]))
        mid_loser.append(float(d[mid[not winning_team]-20]))
    return jng_winner, top_winner, mid_winner, jng_loser, top_loser, mid_loser


if __name__ == '__main__':
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()
    a,b,c,d,e,f = masterylevel_by_role(cursor)
    conn.close()