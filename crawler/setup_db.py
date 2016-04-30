import sqlite3

DBROWS = []
DBROWS += ['Champion%i' % i for i in range(1,11)]
DBROWS += ['MasteryLevel%i' % i for i in range(1,11)]
DBROWS += ['Rank%i' % i for i in range(1,11)]
DBROWS += ['Role%i' % i for i in range(1,11)]
DBROWS.append('Patch')
DBROWS.append('Region')
DBROWS.append('WinningTeam')
DBROWS.append('MatchId')
DBROWS.append('MatchCreationTime')

DBTYPES = []
DBTYPES += ['TEXT']*42
DBTYPES += ['INTEGER']*3

DBNAME = 'games.db'

SQL_CREATE = 'CREATE TABLE games (' + ','.join([' '.join(pair) for pair in zip(DBROWS, DBTYPES)]) + ')'


if __name__ == '__main__':

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    cur.execute(SQL_CREATE)