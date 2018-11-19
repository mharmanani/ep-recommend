import requests
import re
import sys
from bs4 import BeautifulSoup
import sqlite3 as sql
from structures import Episode

SHOWS_DB = "SHOWS.db"

def download(show):
	file = open("SHOWS")
	for line in file:
		if line.startswith("<SHOW>"):
			name = file.readline().strip()
			if show in name:
				link = file.readline().strip()
				seasons = list(range(1,int(file.readline())+1))
				#print(seasons)
				return link, seasons, name
			else: continue
	return (None, None, None)

def get_eps(season, location):
	ep_num = 1
	eps = []
	page = requests.get(location + season)
	soup = BeautifulSoup(page.text, "html.parser")

	links = soup.find_all('strong')
	episodes = []
	print("Loading episodes for Season " + season + " ...")
	for link in links:
		l = (str(link))
		if "title=" in l:
			ep = Episode(link.getText())
			if ep_num < 10:
				ep.code = "S{0}E{1}. ".format(str(season), "0" + str(ep_num))
			else:
				ep.code = "S{0}E{1}. ".format(str(season), str(ep_num))
			ep_num += 1
			episodes += [ep]

	blurbs, ratings = get_blurbs_and_ratings(season, location)
	for i in blurbs:
		episodes[i-1].description = blurbs[i]
		episodes[i-1].rating = ratings[i]
	return episodes

def get_blurbs_and_ratings(season, location):
	ep_num = 1
	eps = []
	page = requests.get(location + season)
	soup = BeautifulSoup(page.text, "html.parser")

	descriptions = {}
	ratings = {}

	links = soup.find_all('div')
	print("Scraping blurbs and ratings for Season " + season + " ...")
	for link in links:
		if link.get('class') == ['item_description']:
			descriptions[ep_num] = link.getText().strip()
			ep_num += 1

	ep_num = 1
	links = soup.find_all('div')
	for link in links:
		if link.get('class') == ['ipl-rating-widget']:
			l = link.getText().strip()
			ratings[ep_num] = l[:l.find("\n")]
			ep_num += 1

	return descriptions, ratings

def make_ep_guide(seasons, name, link):
	#f = open(fname, "w")
	db = sql.connect(SHOWS_DB)
	cursor = db.cursor()
	cursor.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
	tables = [x[0] for x in cursor.fetchall()]
	if name in tables:
		print("TV show already exists: table name", name)
		return 0
	else:
		print("Initializing episode guide...")
		cmd = """CREATE TABLE {0} 
				( ep_code TEXT PRIMARY KEY NOT NULL
				, ep_name TEXT NOT NULL
				, ep_rating TEXT NOT NULL 
				, ep_desc TEXT NOT NULL ); """.format(name)
		cursor.execute(cmd)
		show = name
	for season in seasons:
		#f.write("Season " + str(season) + ": \n")
		for episode in get_eps(str(season), link):
			name = str(episode.title.replace(" ", "_"))
			rating = str(episode.rating.replace(" ", "_"))
			code = str(episode.code.replace(" ", "_"))
			des = str(episode.description.replace(" ", "_"))
			cmd = """ INSERT INTO {0} VALUES (?, ?, ?, ?);""".format(show)
			params = (code, name, rating, des)
			#print(cmd, params)
			with db: cursor.execute(cmd, params)
		#f.write("------------- \n")
	print("--")
	print("Done!")
	return 0
