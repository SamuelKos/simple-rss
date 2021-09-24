from html import unescape
from re import findall, DOTALL
from urllib.request import Request, urlopen

class Parser:
    ''' Simple parser for xml.
    '''
    
    def __init__(self):
        self.data = {}
        self.tags = ['title', 'media:content', 'link', 'description']
        self.user_agent = 'https://github.com/SamuelKos/simple-rss'
    

    def parse(self, link):
        ''' link is URL-address to RSS-feed written in XML.
            Returns tuple containing two list: 
            news-titles and links to news-page.
        '''
        req = Request(link)
        req.add_header('User-Agent', self.user_agent)
        
        r = urlopen(req, timeout = 8)
        data_xml = unescape(r.read().decode('utf-8', 'ignore'))
        
        for tag in self.tags:
            self.data[tag] = list()
            
            if tag == 'media:content':
                # grab first link found which hopefully is an image:
                pattern = f"<item>.*?<{tag}.*?url.*?=.*?\"(.*?)\""
            else:
                pattern = f"<item>.*?<{tag}>(?:<\\!\\[CDATA\[)?(.*?)(?:\\]\\]>)?</{tag}>.*?</item>"
            
            self.data[tag] = findall(pattern, data_xml, flags=DOTALL)
        
        
        return (self.data['title'], self.data['link'])
        
        



