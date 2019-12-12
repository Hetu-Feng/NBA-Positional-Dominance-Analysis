import requests
from bs4 import BeautifulSoup, Comment


## Build scrapers and API crawlers to create functions 
## Retrieve URLs with parameters pages/years, return the corresponding soup objects 
def url_to_soup_API():
    
    API_url = 'https://www.fantasybasketballnerd.com/service/players'
    API_response = requests.get(API_url)
    position_soup = BeautifulSoup(API_response.content, 'lxml')
    
    return position_soup


def url_to_soup_FGA(year):
    
    FGA_url = f'https://www.basketball-reference.com/leagues/NBA_{year + 1}_per_game.html'
    
    try:
        FGA_response = requests.get(FGA_url)
        FGA_response.raise_for_status()
          
    except requests.exceptions.HTTPError as e:
        print(e)
        return None
    
    FGA_soup = BeautifulSoup(FGA_response.content, 'lxml')
    
    return FGA_soup
    

def url_to_soup_USG(year):
    
    USG_url = f'https://www.basketball-reference.com/leagues/NBA_{year + 1}_advanced.html'

    try:
        USG_response = requests.get(USG_url)
        USG_response.raise_for_status()
          
    except requests.exceptions.HTTPError as e:
        print(e)
        return None
    
    USG_soup = BeautifulSoup(USG_response.content, 'lxml')
    
    return USG_soup
    
    
def url_to_soup_salary(year_start, year_end):
    
    salary_url = f'https://hoopshype.com/salaries/players/{year_start}-{year_end}/'
    
    if type(year_start) == int and type(year_end) == int: 
        if year_start >= 1998 and year_start <= 2018 and year_end >= 1999 and year_end <= 2019 and year_end - year_start == 1:        
            salary_response = requests.get(salary_url)
        else:
            print('Year number out of range!')
            return None 
    else:
        print('Year number accepts integer only!')
        return None 
    
    salary_soup = BeautifulSoup(salary_response.content, 'lxml')
    
    return salary_soup


def url_to_soup_draft(year):
    
    draft_url = f'https://www.basketball-reference.com/draft/NBA_{year}.html'
    
    try:
        draft_response = requests.get(draft_url)
        draft_response.raise_for_status()
          
    except requests.exceptions.HTTPError as e:
        print(e)
        return None
    
    draft_soup = BeautifulSoup(draft_response.content, 'lxml')
    
    return draft_soup


def url_to_soup_EV():
    
    EV_url = 'https://www.basketball-reference.com/draft/preview.html'
    EV_response = requests.get(EV_url)
    EV_soup = BeautifulSoup(EV_response.content, 'lxml')
            
    return EV_soup

    
## Transfer soup objects into data structures
def soup_API_to_list(position_soup):
    
    position_record = []
    name = []
    position = []
    
    main_table = position_soup.find_all('player')
    
    for player in main_table:
        player_name = player.find('name').text
        player_position = player.find('position').text
        
        name.append(player_name)
        position.append(player_position)
       
    for i in range(len(name)):
        position_record.append((name[i], position[i]))
        
    return position_record


def soup_FGA_to_list(FGA_soup):
    
    FGA_record_old = []
    name = []
    FGA = []
    games_played = []
    minutes_played_per_game = []
    
    main_table = FGA_soup.find('table', {'id': 'per_game_stats'})
    
    for player in main_table.find_all('tr')[1:]:
        if len(player.find_all('td')) > 0:
            ## player name
            player_name = player.find_all('td')[0].text.strip('*')
            ## player FGA
            player_FGA = player.find_all('td')[8].text
            ## player total games played
            player_GP = player.find_all('td')[4].text
            ## player minutes played per game 
            player_MP = player.find_all('td')[6].text
            
            name.append(player_name)
            FGA.append(player_FGA)
            games_played.append(player_GP)
            minutes_played_per_game.append(player_MP)
                
    for i in range(len(name)):
        FGA_record_old.append((name[i], FGA[i], games_played[i], minutes_played_per_game[i]))
       
    name_no_repeat = [i for n, i in enumerate(name) if i not in name[:n]]
    FGA_record = []
    
    for item in name_no_repeat:
        index = name.index(item)
        FGA_record.append(FGA_record_old[index])
    
    return FGA_record


def soup_USG_to_list(USG_soup):
    
    USG_record_old = []
    name = []
    USG = []
    games_played = []
    minutes_played = []

    main_table = USG_soup.find('table', {'id': 'advanced_stats'})

    for player in main_table.find_all('tr')[1:]:
        if len(player.find_all('td')) > 0:
            ## player name
            player_name = player.find_all('td')[0].text.strip('*')
            ## player USG%
            player_USG = player.find_all('td')[17].text
            ## player total games played
            player_GP = player.find_all('td')[4].text
            ## player total minutes played 
            player_MP = player.find_all('td')[5].text
            
            name.append(player_name)
            USG.append(player_USG)
            games_played.append(player_GP)
            minutes_played.append(player_MP)
    
    for i in range(len(name)):
        USG_record_old.append((name[i], USG[i], games_played[i], minutes_played[i]))
    
    name_no_repeat = [i for n, i in enumerate(name) if i not in name[:n]]
    USG_record = []
    
    for item in name_no_repeat:
        index = name.index(item)
        USG_record.append(USG_record_old[index])
       
    return USG_record


def soup_salary_to_list(salary_soup):
    
    salary_record = []
    name = []
    salary = []
    
    main_table = salary_soup.find('table', {'class': 'hh-salaries-ranking-table hh-salaries-table-sortable responsive'})

    for player in main_table.find_all('tr')[1:]:
        if len(player.find_all('td')) > 0:
            ## player name
            player_name = player.find_all('td')[1].find('a').text.strip()
            ## player salary
            player_salary = player.find_all('td')[2].get('data-value')
            
            name.append(player_name)
            salary.append(player_salary)
    
    for i in range(len(name)):
        salary_record.append((name[i], salary[i]))
    
    return salary_record
      
    
def soup_draft_to_list(draft_soup):
    
    draft_record = []
    Pk = []
    name = []
    
    
    main_table = draft_soup.find('table', {'id': 'stats'})
    
    for player in main_table.find_all('tr'):
        if (len(player.find_all('td')) > 2):
            ## player pick rank
            player_Pk = player.find_all('td')[0].get('csk')
            ## player name 
            player_name = player.find_all('td')[2].text
                
            Pk.append(player_Pk)
            name.append(player_name)
            
                   
    for i in range(len(Pk)):
        draft_record.append((Pk[i], name[i]))
    
    return draft_record


def soup_EV_to_list(EV_soup):
    
    EV_record = []
    Pk = []
    EV = []
      
    comments = EV_soup.find_all(string = lambda text: isinstance(text, Comment))

    for comment in comments:
        if comment.find("table") > 0:
            EV_soup = BeautifulSoup(comment, 'lxml')
            main_table = EV_soup.find('table', {'id': 'picks'})
            if main_table == None:
                break
            else:
                for player in main_table.find_all('tr')[1:]:
                    if len(player.find_all('td')) > 0:
                        ## player pick rank 
                        player_Pk = player.find_all('td')[0].text
                        ## pick's expected value 
                        pick_EV = player.find_all('td')[2].text
            
                        Pk.append(player_Pk)
                        EV.append(pick_EV)
    
    for i in range(len(Pk)):
        EV_record.append((Pk[i], EV[i]))
    
    return EV_record


## Collect each data set individually 
def position():
    
    position_records = []
    
    
    position_soup = url_to_soup_API()
    position_record = soup_API_to_list(position_soup)    
    position_records = [list(record) for record in position_record]
    #print(len(position_records))
    
    return position_records


def FGA():
    
    FGA_records = []
    
    for year in range(1998, 2019):
        FGA_soup = url_to_soup_FGA(year)
        FGA_record = soup_FGA_to_list(FGA_soup)
        
        for item in FGA_record:
            item += (year,)
            FGA_records.append(item)
    
    FGA_records = [list(FGA_record) for FGA_record in FGA_records]
    #print(len(FGA_records))
      
    return FGA_records


def USG():
    
    USG_records = []
    
    for year in range(1998, 2019):
        USG_soup = url_to_soup_USG(year)
        USG_record = soup_USG_to_list(USG_soup)
        
        for item in USG_record:
            item += (year,)
            USG_records.append(item)
    
    USG_records = [list(USG_record) for USG_record in USG_records]
    #print(len(USG_records))
      
    return USG_records


def salary(): 
    
    salary_records = []
    
    for year in range(1998, 2019):
        salary_soup = url_to_soup_salary(year, year + 1)
        salary_record = soup_salary_to_list(salary_soup)
        
        for item in salary_record:
            item += (year,)
            salary_records.append(item)
    
    salary_records = [list(salary_record) for salary_record in salary_records]
    #print(len(salary_records))
      
    return salary_records


def draft():
    
    draft_records = []
    
    for year in range(1998, 2019):
        draft_soup = url_to_soup_draft(year)
        draft_record = soup_draft_to_list(draft_soup)
        
        for item in draft_record:
            item += (year,)
            draft_records.append(item)
    
    draft_records = [list(draft_record) for draft_record in draft_records]
    #print(len(draft_records))
      
    return draft_records


def EV():
    
    EV_records = []
    
    EV_soup = url_to_soup_EV()
    EV_record = soup_EV_to_list(EV_soup)
    EV_records = [list(record) for record in EV_record]
    #print(len(EV_record))
    
    return EV_records


## Driver function that collect all information from 1998 to 2018
def scrape_all():

    NBA_records = [position(), FGA(), USG(), salary(), draft(), EV()]
    
    return NBA_records

