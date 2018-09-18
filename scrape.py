import requests
import re
import sys
from bs4 import BeautifulSoup
from structures import Episode

def download(show):
	file = open("SHOWS")
	for line in file:
		if line.startswith("<SHOW>"):
			name = file.readline().strip()
			if show in name:
				link = file.readline().strip()
				seasons = file.readline().split()
				seasons = [int(x) for x in seasons]
				print(seasons)
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

def make_ep_guide(seasons, fname, link):
	print("Initializing episode guide...")
	f = open(fname, "w")
	for season in seasons:
		f.write("Season " + str(season) + ": \n")
		for episode in get_eps(str(season), link):
			f.write(str(episode) + " \n")
			f.write(episode.description + "\n")
		f.write("------------- \n")
	print("--")
	print("Done!")