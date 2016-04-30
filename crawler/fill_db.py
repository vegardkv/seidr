import sqlite3
from time import sleep
from crawler.setup_db import DBROWS

import requests, json


def insert_match_in_db(j_match, cursor, session):
    if j_match['queueType'] == 'RANKED_SOLO_5x5':
        data = {key: None for key in DBROWS}
    return

if __name__ == '__main__':
    match_id = 2222222222
    with open('../api_key.txt', 'r') as f:
        API_KEY = f.readline()

    db_connection = sqlite3.connect('games.db')
    db_cursor = db_connection.cursor()

    try:
        
        MATCH_URL = 'https://euw.api.pvp.net/api/lol/euw/v2.2/match/'
        session = requests.Session()
        params = dict(api_key=API_KEY)
        while True:
            r_match = session.get(MATCH_URL + match_id, params=params)
            if r_match.status_code == 200:
                print('Fetching match %i' % match_id)
                insert_match_in_db(r_match.json(), db_cursor, session)
            elif r_match.status_code == 404:
                print('Match %i not found, continuing' % match_id)
            elif r_match.status_code == 429:
                print('Rate limit exceed, sleeping 10 s')
                sleep(10)
                continue
            match_id += 1


    except KeyboardInterrupt:
        db_connection.close()
    finally:
        db_connection.close()