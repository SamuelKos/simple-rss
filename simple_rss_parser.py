from html import unescape
from re import findall, DOTALL, VERBOSE
from urllib.request import Request, urlopen


class Parser:
	''' Parser for xml. Parses <title> and <link>.
	'''
	
	def __init__(self):
		self.titles = None
		self.links = None
		self.user_agent = 'simple-rss'
	

	def parse(self, link):
		''' link is URL-address to RSS-feed written in XML.
			Returns tuple containing two list: 
			news-titles and links to news-page.
		'''
		
		req = Request(link)
		req.add_header('User-Agent', self.user_agent)
		
		r = urlopen(req, timeout = 8)
		data_xml = unescape(r.read().decode('utf-8', 'ignore'))
		
		self.links = findall(r"""<item>.*?
					<link>(.*?)</link>
					.*?</item>""", data_xml, flags=DOTALL|VERBOSE)
		
		self.titles = findall(r"""<item>.*?
					<title>(?:<\!\[CDATA\[)?(.*?)(?:\]\]>)?</title>
					.*?</item>""", data_xml, flags=DOTALL|VERBOSE)
		
		return (self.titles, self.links)
		
		

