# RSS specs:
# https://www.rssboard.org/rss-profile#namespace-elements
# Atom (blogs) specs:
# http://www.atomenabled.org/developers/syndication/

import urllib.request
import html
import re


class Parser:
	''' Simple parser for xml.
	'''
	
	def __init__(self):
		self.title_of_feed = None
		self.data = {}
		self.tags = ['title', 'link']# 'media:content', 'description']
		self.user_agent = 'https://github.com/SamuelKos/simple-rss'
		self.rss_types = {
			'Atom':	'<feed xmlns="http://www.w3.org/2005/Atom">',
			'RSS':  '<rss '
			}

	def parse(self, link):
		'''	link is URL-address to RSS-feed written in XML.
			Returns tuple containing title of feed and two list: 
			news-titles and links to news-page.
		'''
		req = urllib.request.Request(link)
		req.add_header('User-Agent', self.user_agent)
		
		try: r = urllib.request.urlopen(req, timeout = 8)
		except OSError: raise
			
		data_xml = html.unescape(r.read().decode('utf-8', 'ignore'))
		
		# Trying to apply some specs:
		if self.rss_types['RSS'] in data_xml:
			ctag = 'item'
			patt_for_title = '<channel>.*?<title>(.*?)</title>'
			patt_for_link = '<item>.*?<link>(?:<\\!\\[CDATA\[)?(.*?)(?:\\]\\]>)?</link>.*?</item>'
			
		elif self.rss_types['Atom'] in data_xml:
			ctag = 'entry'
			patt_for_title = '<feed.*?<title>(.*?)</title>'
			patt_for_link = '''<entry>.*?<link\\s*href\\s*=.*?(h.*?)['"]*/>.*?</entry>'''
			
		else:
			err_msg =	\
'''simple_rss_parser.py:

Parsing error: unknown RSS-format
'''
			self.err = ValueError(err_msg)
			raise self.err
		
		# Parse title of feed:
		m = re.search(patt_for_title, data_xml, re.DOTALL)
		self.title_of_feed = m.group(1)
		
		
		# Parse tags:
		for tag in self.tags:
			self.data[tag] = list()
			
##			if tag == 'media:content':
##				# grab first link found which hopefully is an image:
##				pattern = f"<{ctag}>.*?<{tag}.*?url.*?=.*?\"(.*?)\""
			
			if tag == 'link':
				pattern = patt_for_link
				
			elif tag == 'title':
				pattern = f"<{ctag}>.*?<{tag}>(?:<\\!\\[CDATA\[)?(.*?)(?:\\]\\]>)?</{tag}>.*?</{ctag}>"
				
			else:
				pass
			
			self.data[tag] = re.findall(pattern, data_xml, flags=re.DOTALL)

				
		return (self.title_of_feed, self.data['title'], self.data['link'])
		
		

