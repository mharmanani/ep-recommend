from structures import *
from similiarity import *
from scrape import *
import sqlite3 as sql

KEYS = ["\x1b[A", "^[[C", "^[[D", "^[[B"]
ALIAS_F = "ALIAS"
SHOWS = "SHOWS.db"

def init_ep_heap(ep_table):
	db = sql.connect(SHOWS)
	cursor = db.cursor()
	H = MaxEpisodeHeap()
	cursor.execute(""" SELECT * FROM {0}""".format(ep_table))
	for ep in cursor.fetchall():
		e = Episode(title=ep[1].replace("_", " "), rate=ep[2], 
					code=ep[0].replace("_", ""), desc=ep[2].replace("._", " "))
		H.insert(e)
	return H

def get_top_rated(H, n):
	while n > 0:
		print(H.extract_max())
		n -= 1

def display():
	print("\n"*100)
	print("--")
	print("Welcome to epRec! (v1.1) : an interactive episode recommendation system for your favourite tv series! \n")
	print("Use the commands below to get started: \n")
	print("\t* [load] Select your TV show")
	print("\t* [download] Load the contents of a TV show onto the system")
	print("\t\t (use if load fails)")
	print("\t* [top n] Get top 'n' rated episodes for your selected show")
	print("\t* [recommend] Find the 'n' episodes most similiar to the description 'desc'")

def main():
	display()
	print("-- \n")
	on = True
	show = None
	command_stack = []
	while on:
		usr_in = input("epRec 1.1 > ")
		if usr_in not in KEYS: command_stack += [usr_in]
		else:
			prev = 0
			print(command_stack)
			while command_stack and usr_in != "":
				prev += 1
				usr_in = usr_in[1+usr_in.find("A"):]
			usr_in = command_stack[prev]
		if usr_in == "quit":
			on = False
		elif usr_in.startswith("load"):
			line = usr_in.split()
			try: 
				show = line[1]
			except IOError: 
				print("[ERROR] No such file: " + line[1])
		elif usr_in.startswith("top"):
			line = usr_in.split()
			try: 
				n = int(line[1])
				if show: 
					H = init_ep_heap(show)
					print("--")
					get_top_rated(H, n)
					print("--")
				else: print("[ERROR] No show selected :/")
			except: print("[ERROR] Invalid n - not a number: " + line[1]) 
		elif usr_in == "find":
			if show:
				try: 
					n = input("[MAX RECOMMENDATIONS] ")
					n = int(n)
				except: 
					print("[ERROR] Invalid n - not a number: " + str(n))
					continue
				H = MaxEpisodeHeap()
				desc = input("[KEYWORDS] ").lower()
				eps = clean_dict(parse_eps(SHOWS, show))
				rates = []
				for ep in eps:
					j = jaccard(desc.split(), eps[ep])
					ep.rating = (j*(float(ep.rating)))
					H.insert(ep)
				if H.get_max().rating == 0:
					print("No matches! Sorry :(")
					continue
				while n > 0:
					e = H.extract_max()
					if e.rating != 0:
						print(e.code + " " + e.title + " ({0}%)".format(round(e.rating, 2)) )
					n -= 1
		elif usr_in.startswith("download"):
			line = usr_in.split()
			show = ' '.join(line[1:])
			link, seasons, name = download(show)
			alias = input("[ALIAS] ")
			name = alias
			if seasons and name and link:
				make_ep_guide(seasons, name, link)
			else: print("[ERROR] Missing data in SHOWS file...")
		elif usr_in.startswith("compare"):
			if show:
				n = input("[COMPARE EP] ")
				eps = parse_ep(open(show))
				eps = clean_dict(eps)
				ep1 = None
				for ep in eps:
					if n == ep.title:
						ep1 = ep
						break
				if not ep1: 
					print("[ERROR] Invalid episode name - not found: " + str(n))
					continue
				m = input("[WITH EP] ")
				

	
main()