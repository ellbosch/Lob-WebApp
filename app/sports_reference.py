from app import db
from models import Player, Team, Playeralias
from bs4 import BeautifulSoup
import requests
import csv

def populate_db_playerinfo():
    player_data = get_all_player_info()

    for player in player_data:

        if not Player.query.filter_by(site_id=player['site_id']).first():
            # add to player table
            p = Player(id=player['site_id'],
                      fullname=player['fullname'],
                      player_url=player['player_url'])
            db.session.merge(p)
            db.session.commit()

        # add to playeralias table
        for alias in player['aliases']:
            player_id = Player.query.filter_by(site_id=player['site_id']).first().id
            alias_id = "%s-%s" % (alias, player_id)
            a = Playeralias(id=alias_id, player_id=player_id, alias=alias)
            db.session.merge(a)
            db.session.commit()

def populate_db_teaminfo():
    from webapp import team_data
    team_data_nba = team_data.get_nba()

    for team in team_data_nba:
        t = Team(league=team['league'],
                 id="%s-%s" % (team['league'], team['site_id']),
                 name=team['name'],
                 location=team['location'])
        db.session.merge(t)
        db.session.commit()



def create_player_csv():
    player_data = get_all_player_info()

    with open('player_info.csv', 'w') as csvfile:
        fieldnames = player_data.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for player in player_data:
            writer.writerow(player)

def get_all_player_info():
    player_links = get_links_players_list('basketball')
    player_data = []

    for player in player_links:
        # returns dict of player info
        player_data.append(get_player_info('basketball', player))

    return player_data

def get_links_players_list(sport):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    links_all = []

    # sports reference has player glossary broken down by alphabetical letter
    for letter in alphabet:
        print("Getting names with: %s" % letter)
        link = 'https://www.%s-reference.com/players/%s' % (sport, letter)
        
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
    
        # make sure players exist with letter
        try:
            players_table = soup.find(id='players')
            rows = players_table.find_all('tr')
            for row in rows:
                player = row.find('th')
                players_links = [a['href'] for a in player.find_all('a', href=True)]
                links_all.extend(players_links)
        except Exception as e:
            continue
        
    return links_all

# returns dict of player info with id, fullname, aliases
def get_player_info(sport, player_link):
    player_dict = {}

    link = 'https://www.%s-reference.com%s' % (sport, player_link)
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    info = soup.find(id='info').find(id='meta')

    # gets player_id
    player_dict['site_id'] = "%s-%s" % (sport, player_link.split('/')[3].rstrip('.html'))

    # gets fullname
    player_dict['fullname'] = info.find('h1').string.lower()

    # gets nicknames
    nicknames = []
    try:
        nicknames_raw = info.find_all('p')[1].string.strip()
        nicknames.extend([name.strip().lower() for name in nicknames_raw.strip('()').split(',')])
    except Exception as e:
        pass
    player_dict['aliases'] = nicknames

    # get link to player basketball-reference page
    player_dict['player_url'] = link

    return player_dict

# populate_db_playerinfo()
# populate_db_teaminfo()
