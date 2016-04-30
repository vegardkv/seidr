import random
import sqlite3
from time import sleep
from crawler.setup_db import DBROWS

import requests, json

# Test match id: 2596705919
# Test mastery https://euw.api.pvp.net/championmastery/location/euw1/player/34378680/champion/59?

def get_mastery_level(player, champion, session):
    while True:
        r_mastery = session.get(CHAMPION_MASTERY_URL.replace('{P}', str(player)).replace('{C}', str(champion)) + '?api_key=' + API_KEY)
        if r_mastery.status_code == 200:
            return r_mastery.json()['championPoints']
        elif r_mastery.status_code == 429:
            handle_429()
        elif r_mastery.status_code == 204:
            return 0
        else:
            return 0


def insert_match_in_db(match, cursor, session):
    data = {key: None for key in DBROWS}
    data['WinningTeam'] = match['teams'][0]['winner']
    data['Patch'] = match['matchVersion']
    data['Region'] = match['region']
    data['MatchId'] = match['matchId']
    data['MatchCreationTime'] = match['matchCreation']

    team_a = 0
    team_b = 0
    for p in match['participants']:
        player_id = match['participantIdentities'][int(p['participantId'])-1]['player']['summonerId']
        if p['teamId'] == 100:
            data['Champion%i' % (team_a+1)] = p['championId']
            data['Role%i' % (team_a+1)] = p['timeline']['lane']
            data['Rank%i' % (team_a+1)] = p['highestAchievedSeasonTier']
            data['MasteryLevel%i' % (team_a+1)] = get_mastery_level(player_id, p['championId'], session)
            team_a += 1
        if p['teamId'] == 200:
            data['Champion%i' % (team_b+6)] = p['championId']
            data['Role%i' % (team_b+6)] = p['timeline']['lane']  # role?
            data['Rank%i' % (team_b+6)] = p['highestAchievedSeasonTier']
            data['MasteryLevel%i' % (team_b+6)] = get_mastery_level(player_id, p['championId'], session)
            team_b += 1
    cursor.execute('INSERT INTO games VALUES (' + ','.join(['?']*len(DBROWS))+ ')',
                   [data[row] for row in DBROWS])

def handle_429():
    print('Rate limit exceed, sleeping 10 s')
    sleep(10)


def update_queue(queue, match, session):
    if random.random() > len(queue)/MAX_QUEUE_SIZE or len(queue) < MIN_QUEUE_SIZE:
        params = {
            'rankedQueues': 'TEAM_BUILDER_DRAFT_RANKED_5x5',
            'seasons': 'SEASON2016',
            'api_key': API_KEY,
            'beginIndex':0,
            'endIndex':15
        }
        while True:
            summoner_id = random.choice(match['participantIdentities'])['player']['summonerId']
            r_matchlist = session.get(MATCHLIST_URL + str(summoner_id), params=params)
            if r_matchlist.status_code == 200:
                if 'matches' in r_matchlist.json():
                    for m in r_matchlist.json()['matches']:
                        queue.append(m['matchId'])
                    return
                else:
                    continue
            elif r_matchlist.status_code == 429:
                handle_429()


MAX_QUEUE_SIZE = 200
MIN_QUEUE_SIZE = 50
MATCH_URL = 'https://euw.api.pvp.net/api/lol/euw/v2.2/match/'
MATCHLIST_URL = 'https://euw.api.pvp.net/api/lol/euw/v2.2/matchlist/by-summoner/'

CHAMPION_MASTERY_URL = 'https://euw.api.pvp.net/championmastery/location/euw1/player/{P}/champion/{C}'


if __name__ == '__main__':
    seed = 2613878094
    seed_is_used = False
    with open('../api_key.txt', 'r') as f:
        API_KEY = f.readline()

    db_connection = sqlite3.connect('games.db')
    db_cursor = db_connection.cursor()

    try:
        match_q = [seed]
        session = requests.Session()
        match_id = match_q.pop(0)

        while True:
            db_cursor.execute('SELECT MatchId FROM games WHERE MatchId=?', (match_id,))
            if not db_cursor.fetchone() or not seed_is_used:  # MatchId is not represented in DB
                r_match = session.get(MATCH_URL + str(match_id) + '?api_key=' + API_KEY)
                if r_match.status_code == 200:
                    print('Fetching match %i' % match_id)
                    if seed_is_used:
                        insert_match_in_db(r_match.json(), db_cursor, session)
                    db_connection.commit()
                    update_queue(match_q, r_match.json(), session)
                    seed_is_used = True
                elif r_match.status_code == 404:
                    print('Match %i not found, continuing' % match_id)
                elif r_match.status_code == 429:
                    handle_429()
                    continue
            match_id = match_q.pop(0)


    except KeyboardInterrupt:
        db_connection.close()
    finally:
        db_connection.close()