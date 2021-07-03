import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_player (url, namef):
	p_response = requests.get(url)
	p_page = BeautifulSoup(p_response.content, 'html.parser')
	tabs = p_page.find_all('table', {'class':'infobox biography vcard'}) + p_page.find_all('table', {'class':'infobox vcard'}) + p_page.find_all('table', {'class':'infobox'})
	matches, runs, wickets, bat_av, bowl_av = None, None, None, None, None
	if (len(tabs) == 0):
		return (None)
	name = namef
	flag = 0
	for tab in tabs:
		stats_tab = tab.find_all('table')
		if (len(stats_tab) == 0):
			continue
		for stats in stats_tab:
			stats = stats.tbody
			if (stats == None):
				continue
			stats_arr = stats.find_all('tr')
			for entry in stats_arr:
				if (entry.th) == None:
					flag = 0
					break
				if (str(entry.th.text).startswith('Matches')):
					matches = entry.td.text
					flag = 1
				elif (str(entry.th.text).startswith('Runs scored')):
					runs = entry.td.text
					flag = 1
				elif (str(entry.th.text).startswith('Batting average')):
					bat_av = entry.td.text
					flag = 1
				elif (str(entry.th.text).startswith('Wickets')):
					wickets = entry.td.text
					flag = 1
				elif (str(entry.th.text).startswith('Bowling average')):
					bowl_av = entry.td.text
					flag = 1
				else:
					pass
			if (flag == 0):
				continue
			else:
				break
		if (flag == 0):
			continue
		else:
			break
	if (flag == 0):
		return (None)
	Name.append(name)
	Matches.append(matches)
	Runs.append(runs)
	Wickets.append(wickets)
	Batting_av.append(bat_av)
	Bowling_av.append(bowl_av)
	return (name)

url = 'https://en.m.wikipedia.org/wiki/List_of_Test_cricketers'
response = requests.get(url)

page = BeautifulSoup(response.content, 'html.parser')

container = page.find('div', {'class':'mw-parser-output'})
countries = container.find_all('section')
l = len(countries)
countries = countries[1:l-1]


Name = []
Matches = []
Runs = []
Wickets = []
Batting_av = []
Bowling_av = []

countries_count = 0
count = 0
discarded = 0


for country in countries:
	countries_count += 1
	print ('\n\n\n\n\t\t\t\tcountry number: {}'.format(countries_count))
	players = country.small.find_all('a')
	for player in players:
		count += 1
		purl = player['href']
		purl = 'https://en.m.wikipedia.org/' + purl
		name = player.text
		name = get_player(purl, name)
		if (name == None):
			discarded += 1
			print ('{}'.format(count) + '\t' + purl)
		else:
			print ('{}'.format(count) + '\t' + name)

print (discarded)
		
dataf = pd.DataFrame({'Name': Name,
						'Matches': Matches,
						'Runs': Runs,
						'Wickets': Wickets,
						'Batting_average': Batting_av,
						'Bowling_average': Bowling_av})


dataf.to_excel('Test_player_data.xlsx', index = False)