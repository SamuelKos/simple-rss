
from html.parser import HTMLParser
from urllib import request
from urllib.error import URLError
from html2text import HTML2Text
from re import sub
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.font import Font
import rssfeed

# Main-class is Browser and it is last at the bottom 

#TODO: load feeds at startup and make a new class for them. 
# When you choose a feed, titles are fetched from that class.
# History should remember if view was a news-page or title-page.
# self.hyperlink is in two places.

# Files that needs to be supplied: ICON, FONT, SOURCES.LST



# uncomment if you have icon:
##ICONPATH = "./icons/rssicon.png"

RSSLINKS = r'./sources.lst'
HELPTXT = '''
	left: previous view
	ESC:  usually the obvious action
		
	At bottom-pane, when clicked address with mouse-right: copy link
	
	When editing sources, leave an empty line after last line and then
	write name for the feed in dropdown-menu and then add the
	URL-address of the RSS-feed to next line.

		
		'''


class HyperlinkManager:
	''' Manage hyperlinks in tkinter Text-widget
	'''

	def __init__(self, text):
		self.text = text
		self.text.tag_config("hyper", underline=1)
		self.text.tag_bind("hyper", "<Button-1>", self.lclick)
		self.text.tag_bind("hyper", "<Button-3>", self.rclick)
		# Had to make the same method with two different names:
		# self.lclick and self.rclick for binding two events into a single tag.
		self.text.tag_bind("hyper", "<Enter>", self.enter)
		self.text.tag_bind("hyper", "<Leave>", self.leave)
		self.reset()


	def enter(self, event):
		self.text.config(cursor="hand2")


	def leave(self, event):
		self.text.config(cursor="")


	def reset(self):
		self.links = {}


	def add(self, action):
		# Add an action to the manager. Returns tags to use in
		# associated text widget.
		tag = "hyper-%d" % len(self.links)
		self.links[tag] = action
		return "hyper", tag


	def rclick(self, event):
		for tag in self.text.tag_names(CURRENT):
			if tag[:6] == "hyper-":
				self.links[tag](event)                
				return


	def lclick(self, event):
		for tag in self.text.tag_names(CURRENT):
			if tag[:6] == "hyper-":
				self.links[tag](event)                
				return
			


class MyHTMLParser(HTMLParser):
	''' Parse URL-links in HTML-page. Methods are all wrappers of those in 
		parent-class, except chk_ignores. These are stored in a list:
		self.addresses as tuples: (link-name, link-address). These tuples
		are used (in Browser-class: get_html() and tag_link()) 
		to make hyper-links for tkinter Text-widget.
		
		Certain types of links are ignored to shorten the list.
	'''
	
	def __init__(self):        
		super().__init__()
		self.flag = False
		self.ignore = ['#','facebook','twitter', 'whatsapp', 'mailto:?']
		self.address = ""
		self.linkname = ""        
		self.addresses = list()
		self.domain = ""
	
	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			for item in attrs:
				if item[0] == "href":
					tmp = item[1]
					
					if self.chk_ignores(tmp): break

					if self.domain not in tmp:
						
						# is it an internal link:
						if "http" not in tmp:
							# from this:
							#'spam?ref=nav/page/page2'
							# to this:
							#'page/page2'
							tmp = sub('[^/]*/', '', tmp, 1)
							# and then add domain
							tmp = self.domain + '/' + tmp
							
						# no, it was not internal:
						#'http://anotherdomain.com/spam?ref=nav/page/page2'
						# so do nothing:
						else:
							pass
					else:
						# it is full URL, including current domain,
						# so do nothing:
						pass                        

					self.address = tmp
					self.flag = True
					break          
	

	def chk_ignores(self, spam):
		for item in self.ignore:
			if item in spam:
				return True
		return False


	def handle_data(self, data):
		if self.flag:
			self.linkname = data
			
			
	def handle_endtag(self, tag):    
		if tag == 'a' and self.flag:
			self.linkname = " ".join(self.linkname.split())
			self.addresses.append((self.linkname, self.address))
			self.flag = False



class Browser(Toplevel):
	''' RSS-browser made with tkinter PanedWindow and ScrolledText -widgets
		to name a few. It needs a root-window to run event loop. So:
		
		import simple_rss
		from tkinter import Tk
		root=Tk().withdraw()
		u=simple_rss.Browser(root)

	'''

	def __init__(self, root, url=None, hdpi=True):
		super().__init__(root, class_='Simple RSS')
		self.protocol("WM_DELETE_WINDOW", self.quit_me)
		self.user_agent = "simple-rss"
		self.history = []
		self.input = url
		self.flag_back = False
		self.flag_rss = False
		self.helptxt = HELPTXT
		# uncomment if you have icon:
##		self.iconpath = ICONPATH
		self.title('Simple RSS')
		self.hdpi_screen = hdpi

		if self.hdpi_screen == False:
			self.font1 = Font(family='Noto Mono', size=12)
			self.font2 = Font(family='Noto Mono', size=10)
		else:
			self.font1 = Font(family='Noto Mono', size=24)
			self.font2 = Font(family='Noto Mono', size=20)
		
		# uncomment if you have icon:
##		self.img = Image("photo", file=self.iconpath)
##		self.tk.call('wm','iconphoto', self._w, self.img)
		
		self.rsslinks = RSSLINKS
		self.u = rssfeed.RssFeed(RSSLINKS)
		self.sources = list(self.u._sources.keys())
		
		########### Layout Begin ############################################
		self.framtop = Frame(self)
		self.framtop.pack(side=TOP, fill=X)
		self.frambottom = Frame(self)		
		self.frambottom.pack(side=TOP, fill=BOTH)
		
		self.entry = Entry(self.framtop, font=self.font2)
		self.entry.pack(side=LEFT, expand=True, fill=X)
		self.entry.focus_set()
		
		self.btn_open=Button(self.framtop, font=self.font2, text='Open', command=self.chk)
		self.btn_open.pack(side=LEFT)
		
		self.var = StringVar()
		self.var.set(self.sources[0])
		self.optionmenu = OptionMenu(self.framtop, self.var, *self.sources, command=self.chk)
		
		# set font of dropdown button:
		self.optionmenu.config(font=self.font2)
		
		# set font of dropdown items:
		menu = self.nametowidget(self.optionmenu.menuname)
		menu.config(font=self.font2)
		
		self.optionmenu.pack(side=LEFT)

		self.pane = PanedWindow(self.frambottom, bg='grey', sashpad=1, orient=VERTICAL)
		self.pane.pack(fill=BOTH, expand=True)
 
		self.fram1 = Frame(self.pane)
		self.fram2 = Frame(self.pane)
		self.pane.add(self.fram1)
		self.pane.add(self.fram2)

		self.text1 = ScrolledText(self.fram1, font=self.font1, tabstyle='wordprocessor', background='#000000', foreground='#D3D7CF', insertbackground='#D3D7CF', blockcursor=True)
		self.text2 = ScrolledText(self.fram2, font=self.font2, background='#000000', foreground='#D3D7CF')
		
		if self.hdpi_screen:
			self.text1.vbar.config(width=30)
			self.text2.vbar.config(width=30)
			self.text1.vbar.config(elementborderwidth=4)
			self.text2.vbar.config(elementborderwidth=4)
			self.titletabs=('2c', )
			self.lmarg2='2c'
		else:
			self.text1.vbar.config(width=20)
			self.text2.vbar.config(width=20)
			self.text1.vbar.config(elementborderwidth=3)
			self.text2.vbar.config(elementborderwidth=3)
			self.titletabs=('1c', )
			self.lmarg2='1c'

		self.text1.config(state='disabled')
		self.text2.config(state='disabled')
		# Because texts are disabled, we must make next lambda to
		# be able copy text from them with ctrl-c:
		self.text1.bind("<1>", lambda event: self.text1.focus_set())
		self.text2.bind("<Enter>", self.enter)
		self.text2.bind("<Leave>", self.leave)            
		self.text1.pack(side=BOTTOM,  expand=True, fill=BOTH)
		self.text2.pack(side=BOTTOM,  expand=True, fill=BOTH)
		
		# links at text2 are parsed with:
		self.parser = MyHTMLParser()
		# page at text1 is parsed with:
		self.h = HTML2Text()
		self.h.ignore_links = True
		self.h.ignore_images = True
		
		self.bind("<Return>", lambda a: self.gethtml())
		self.bind("<Escape>", lambda e: self.iconify())
		self.bind("<Left>", lambda event: self.back_hist(event))
		self.bind("<Button-3>", lambda event: self.raise_popup(event))
		
		self.popup_whohasfocus = None
		self.popup = Menu(self, font=self.font2, tearoff=0)
		self.popup.bind("<FocusOut>", self.popup_focusOut)
		# so that popup would go away when clicked somewhere else
		
		self.popup.add_command(label=" editsources", command=self.editsources)
		self.popup.add_command(label="        help", command=self.help)
		######## End of Layout ###############################################
		
		if self.input:
			self.gethtml(self.input)

		
	def raise_popup(self, event, *args):
		self.popup_whohasfocus = event.widget
		self.popup.post(event.x_root, event.y_root)
		self.popup.focus_set()
		# needed to remove popup when clicked somewhere else
		
		
	def popup_focusOut(self, event=None):
		self.popup.unpost()
		
		
	def rebind(self, event=None):
		return 'break'
		
		
	def chk(self, event=None):
		''' Fetch selected feed with rssfeed (titles and links).
			Then make title-page with hyperlinks. 
		'''
		source = self.var.get()
		self.u.select_source(source)
		count = len(self.u._titles)
		self.wipe()
		self.hyperlink = HyperlinkManager(self.text1)
		self.flag_rss = True
	
		for i in range(count):
			tmp = ''
			title = self.u._titles[i]
			addr = self.u._links[i]
			self.parser.addresses.append((addr, addr))
			self.text1.insert(INSERT, str(i+1), self.hyperlink.add(self.tag_link))
			tmp += ':\t%s' % title	
			tmp += '\n\n'
			self.text1.insert(END, tmp)
		
		# set indentation of titles:
		self.text1.tag_add('indent_tag', '1.0', END)
		
		self.text1.tag_config('indent_tag', lmargin2=self.lmarg2, wrap='word', tabs=self.titletabs)
		# not sure if this is necessary:
		self.text1.tag_lower('indent_tag')
		
		self.text1.config(state='disabled')
		self.text2.config(state='disabled')
		
		
	def stop_editsources(self, event=None):
		self.wipe()
		
		self.bind("<Return>", lambda a: self.gethtml())
		self.bind("<Escape>", lambda e: self.iconify())
		self.bind("<Left>", lambda event: self.back_hist(event))
		
		self.btn_open.config(text='Open', command=self.chk)
		
		self.optionmenu = OptionMenu(self.framtop, self.var, *self.sources, command=self.chk)
		self.optionmenu.config(font=self.font2)
		menu = self.nametowidget(self.optionmenu.menuname)
		menu.config(font=self.font2)
		self.optionmenu.pack(side=LEFT)
		
		self.entry.config(state='normal')
		self.back_hist(flag_help=True)
		
		if event != None:
			return 'break'
		
		
	def save_sources(self):
		tmp = self.text1.get('1.0', END).splitlines()
		names = list()
		addresses = list()

		for line in tmp:
			if 'http' in line: 
				addresses.append(line.strip())
			else:
				if len(line.strip()) > 0:
					names.append(line.strip())
		
		data = dict()
		
		if len(names) == len(addresses) and len(names) != 0:
			for i in range(len(names)):
				data[names[i]] = addresses[i]

			#save data with rssfeed.save() into sources.lst
			self.u._save(RSSLINKS, data)
			self.u = rssfeed.RssFeed(RSSLINKS)
			self.sources = list(self.u._sources.keys())
			self.var.set(self.sources[0])
			self.stop_editsources()
			
				
	def editsources(self):
		self.wipe()
		self.entry.config(state='disabled')
		self.optionmenu.destroy()
		self.btn_open.config(text='Save', command=self.save_sources)
		self.bind("<Return>", lambda e: self.rebind())
		self.bind("<Left>", lambda e: self.rebind())
		self.bind("<Escape>", self.stop_editsources)
		
		for name in self.u._sources:
			addr = self.u._sources[name]
			self.text1.insert(INSERT, '%s\n%s\n\n' % (name, addr))

				
	def stop_help(self, event=None):
		self.bind("<Escape>", lambda e: self.iconify())
		self.entry.config(state='normal')
		self.back_hist(flag_help=True)
		
		if event != None:
			return 'break'

	
	def help(self):
		self.wipe()
		self.text1.insert(INSERT, self.helptxt)
		self.text1.config(state='disabled')
		self.text2.config(state='disabled')
		self.entry.config(state='disabled')
		self.bind("<Escape>", self.stop_help)
		

	def back_hist(self, event=None, flag_help=False):
		if event != None:
			if 'entry' in str(event.widget).split('.')[-1]:
				return
		
		self.flag_back = True
		
		if flag_help and len(self.history) > 0:
			self.wipe()
			self.gethtml(self.history[-1])
		elif len(self.history) > 1:        
			self.history = self.history[:-1]
			self.wipe()
			self.gethtml(self.history[-1])
		else:
			self.flag_back = False 


	def enter(self, event):
		self.text2.config(cursor="hand2")


	def leave(self, event):
		self.text2.config(cursor="")
	

	def wipe(self):     
		self.entry.delete(0,END)    
		self.parser.addresses.clear()
		self.text1.config(state='normal')
		self.text2.config(state='normal')
		self.text1.delete(1.0, END)
		self.text2.delete(1.0, END)
		
		for tag in self.text2.tag_names():
			self.text2.tag_delete(tag)
		for tag in self.text1.tag_names():
			self.text1.tag_delete(tag)
			
		
	def tag_link(self, event):
		if self.flag_rss:
			i = int(self.text1.tag_names(CURRENT)[2].split("-")[1])
		else:
			i = int(self.text2.tag_names(CURRENT)[1].split("-")[1])
		addr = self.parser.addresses[i][1]
		
		if event.num == 1:# mouse left
			self.wipe()
			
			if self.flag_rss:
				self.input = addr
				self.gethtml(addr, i)
			else:
				self.gethtml(addr)
			
		if event.num == 3:# mouse right
			self.clipboard_append(addr)			
			
			
	def gethtml(self, link=None, title_index=None):     

		# address is not from hyperlink: 
		if link == None or self.input:
			if link == None:
				link = self.entry.get().strip()
			if self.input:
				link = self.input
				self.input = None
			self.parser.domain = sub('(//[^/]*)/.*', r'\1', link)
			self.wipe()
							
		if self.parser.domain not in link:
			# wipe already done in taglink
			# current domain: http://onepage.com
			# link: 'http://anotherpage.com/spam?ref=nav/page/page2'
			
			# need to parse new domain from this:
			#'http://anotherpage.com/spam?ref=nav/page/page2'
			# to this:
			#'http://anotherpage.com'
			self.parser.domain = sub('(//[^/]*)/.*', r'\1', link)

		# final check
		if self.parser.domain.endswith('/'):        
			self.parser.domain = self.parser.domain[:-1]

		if not self.flag_back:
			self.history.append(link)
			
		self.flag_back = False
		self.flag_rss = False
		self.entry.insert(END, link)
		
		req = request.Request(link)
		req.add_header('User-Agent', self.user_agent)
		self.text1.config(cursor="")
		self.text2.config(cursor="")
		
		# Fetch html-page
		try:
			res = request.urlopen(req, timeout = 8)
			res = res.read().decode('utf-8')
			self.parser.feed(res) # HTMLParser parses links               
			s = self.h.handle(res)    # html2text parses page
			
			self.text1.insert(END, s)
			self.hyperlink = HyperlinkManager(self.text2)     
			
			for item in self.parser.addresses:
				name = item[0] +" "+  item[1] +"\n"
				self.text2.insert(INSERT, name, self.hyperlink.add(self.tag_link))            
			
			if title_index != None:
				# try to get linenum of title in page. Pattern is list
				# with three first words in title.
				# For skipping to right place in page.
				pattern = self.u._titles[title_index].split()[:3]
				pos = self.text1.search(pattern, '1.0', END)
				if pos:
					self.text1.see(pos)
					
		except URLError as err:
			s  = 'Something went wrong:\n\n%s\n\nErrorcode:\n\n%s' % (link, err.reason)
			self.text1.insert(END, s)
		
		
		self.text1.config(state='disabled')
		self.text2.config(state='disabled')


	def quit_me(self, event=None):
		self.quit()
		self.destroy()


if __name__ == '__main__':
	root = Tk().withdraw()
	b = Browser(root)
	b.mainloop()
