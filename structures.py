class Episode:
	def __init__(self, title, code=None, desc="", rate=-1):
		self.title = title
		self.code = code
		self.description = desc
		self.rating = rate

	def __repr__(self):
		return str(self.code) + ". " + str(self.title) + " ({0}/10)".format(self.rating)

class MaxEpisodeHeap:
	def __init__(self):
		self.items = []

	def __repr__(self):
		return str(self.items)

	def __len__(self):
		return len(self.items)

	def insert(self, x):
		self.items.append(x)
		i = len(self.items) - 1
		while i > 0:
			current = self.items[i]
			parent = self.items[i//2]
			if current.rating <= parent.rating:
				break 
			else:
				self.items[i], self.items[i//2] = self.items[i//2], self.items[i]
				i = i//2 

	def has_left(self, i):
		return 2*(i+1) <= len(self)

	def has_right(self, i):
		return 2*(i+1)+1 <= len(self)

	def bubble_down(self, i):
		while i < len(self.items):
			current = self.items[i]
			if self.has_left(i):
				left = self.items[2*(i+1)-1]
			else:
				return
			if self.has_right(i):
				right = self.items[2*(i+1)]
			else:
				if current.rating >= left.rating:
					break
				else:
					self.items[i], self.items[2*(i+1)-1] = self.items[2*(i+1)-1], self.items[i]
					break
			if current.rating >= left.rating and current.rating >= right.rating:
				break
			elif left.rating >= right.rating:
				self.items[i], self.items[2*(i+1)-1] = self.items[2*(i+1)-1], self.items[i]
				i = 2*(i+1) - 1
			else:
				self.items[i], self.items[2*(i+1)] = self.items[2*(i+1)], self.items[i]
				i = 2*(i+1)

	def get_max(self):
		return self.items[0]

	def extract_max(self):
		mx = self.items[0]
		self.items[0] = self.items[-1]
		self.items = self.items [:len(self)-1]
		self.bubble_down(0)
		return mx

	def build_max_heap(self):
		for i in list(range(len(self)//2))[::-1]:
			self.bubble_down(i)
		return self