from structures import *
from similiarity import *
from scrape import *

KEYS = ["\x1b[A", "^[[C", "^[[D", "^[[B"]

def init_ep_heap(ep_file):
	H = MaxEpisodeHeap()
	for line in ep_file:
		if line.startswith("Season"):
			continue
		if line.startswith("S"):
			ep = Episode( title=line[line.find(" "):line.find("(")], 
						  code=line[:line.find(" ")],
						  rate=line[line.find("(")+1:line.rfind("/")] 
						)
			ep.description = ep_file.readline()
			H.insert(ep)
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
					H = init_ep_heap(open(show))
					print("--")
					get_top_rated(H, n)
					print("--")
				else: print("[ERROR] No show selected :/")
			except: print("[ERROR] Invalid n - not a number: " + line[1]) 
		elif usr_in == "recommend":
			if show:
				try: 
					n = input("[MAX RECOMMENDATIONS] ")
					n = int(n)
				except: 
					print("[ERROR] Invalid n - not a number: " + str(n))
					continue
				desc = input("[KEYWORDS] ")
				desc = desc.lower()
				eps = parse_ep(open(show))
				eps = clean_dict(eps)
				rates = []
				for ep in eps:
					j = jaccard(desc.split(), eps[ep])
					rates += [(j*(float(ep.rating)/10), ep.title)]
				rates.sort()
				rates = rates[::-1]
				matches = []
				while n > 0:
					if rates[0][0] > 0:
						matches += [rates[0]]
					rates = rates[1:]
					n -= 1
				if matches:
					for match in matches: print(match)
				else: print("No matches! Please try again :(")
		elif usr_in.startswith("download"):
			if 1: 
				line = usr_in.split()
				show = ''.join(line[1:])
				link, seasons, name = download(show)
				alias = input("Use an alias? (y/n) ")
				if alias == "y":
					alias = input("[ALIAS] ")
					name = alias
				make_ep_guide(seasons, name, link)
			else: print("[ERROR] Something went wrong :/")
	
main()