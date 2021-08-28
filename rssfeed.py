import pickle
import simple_rss_parser


class RssFeed:
	''' Helper-class for simple_rss
	'''

	def __init__(self, file):
		self._sourcefile = file
		self._sources = self._load(self._sourcefile)
		self._source = list(self._sources.keys())[1]
		self._titles = None
		self._links = None
		self._parser = simple_rss_parser.Parser()


	def _save(self, file, data):
		with open(file, 'bw') as f:
			pickle.dump(data, f)


	def _load(self, file):
		with open(file, 'br') as f:
			return pickle.load(f)


	def add_source(self, key, addr):
		''' Add new feed to sources: key is name for dropdown-menu and 
			addr is its URL-address.
		'''
		self._sources[key] = addr
		
		
	def del_source(self, key=None):
		''' Key can be the name of the feed or index-number of the feed.
			Remove one feed from sources.
		'''
		if isinstance(key, int): key = sorted(self._sources.keys())[key]
		self._sources.pop(key)
		

	def show_sources(self):
		''' Print all names and URLs of sources.
		'''
		for i,key in enumerate(sorted(self._sources.keys())):
			print('{}: {}\t{}'.format(i, key, self._sources[key]))
			

	def current_source(self):
		''' Print the name and URL of current feed.
		'''
		print(self._source, self._sources[self._source])
		

	def select_source(self, key):
		''' Key can be the name of the feed or index-number of the feed.
		'''
		if isinstance(key, str):
			self._source = key    
		else:
			self._source = sorted(self._sources.keys())[key]

		self._titles, self._links = self._parser.parse(self._sources[self._source])
		