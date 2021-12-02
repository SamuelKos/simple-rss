import urllib.request
import html
import re


class Parser:
	''' Simple parser for xml.
	'''
	
	def __init__(self):
		self.data = {}
		self.tags = ['title', 'media:content', 'link', 'description']
		self.user_agent = 'https://github.com/SamuelKos/simple-rss'
	

	def parse(self, link):
		'''	link is URL-address to RSS-feed written in XML.
			Returns tuple containing two list: 
			news-titles and links to news-page.
		'''
		req = urllib.request.Request(link)
		req.add_header('User-Agent', self.user_agent)
		
		try: r = urllib.request.urlopen(req, timeout = 8)
		except OSError: raise
			
		data_xml = html.unescape(r.read().decode('utf-8', 'ignore'))
		
		
		# Check if <entry> is used instead of <item>
		# to separate RSS-items:
		
		if '<item>' in data_xml:
			ctag = 'item'
##		elif '<entry>' in data_xml:
##			ctag = 'entry'
		else:
			pattern =	\
'''simple_rss_parser.py:

Could not identify what is parent-tag of tags: <title> and <link>.
You can fix this easily by yourself by looking the structure of your
xml-file: Copy the URL-address of the feed that caused this error in your
web-browser and look for the the title-tag and then what is its parent tag.
Then add this after elif above:

elif '<parenttag>' in data_xml:
	ctag = 'parenttag'

Or raise an issue in github: https://github.com/SamuelKos/simple-rss
'''
			self.err = ValueError(pattern)
			raise self.err
			
			
		for tag in self.tags:
			self.data[tag] = list()
			
			if tag == 'media:content':
				# grab first link found which hopefully is an image:
				pattern = f"<{ctag}>.*?<{tag}.*?url.*?=.*?\"(.*?)\""
				
			# links can be inside tag or as they should,
			# between opening and closing tags. Pattern is:
			# link inside single tag | link between tags
			# this results to items in self.data['link'] to be tuples like
			# ('', URL-address) or (URL-address, '') which are then fixed.
			
			elif tag == 'link':
				pattern = f'''<{ctag}>.*?<{tag}\\s*href\\s*=.*?(h.*?)['"]*/>.*?</{ctag}>|<{ctag}>.*?<{tag}>(?:<\\!\\[CDATA\[)?(.*?)(?:\\]\\]>)?</{tag}>.*?</{ctag}>'''
				
			else:
				pattern = f"<{ctag}>.*?<{tag}>(?:<\\!\\[CDATA\[)?(.*?)(?:\\]\\]>)?</{tag}>.*?</{ctag}>"
			
			self.data[tag] = re.findall(pattern, data_xml, flags=re.DOTALL)
			
		
		# remove empty capturing group from links
		for i,item in enumerate(self.data['link']):
			if len(item[0]) == 0:
				self.data['link'][i] = item[1]
			else:
				self.data['link'][i] = item[0]
				
		return (self.data['title'], self.data['link'])
		
		

