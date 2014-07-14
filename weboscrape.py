
import nltk
from urllib import urlopen
from google import search
from bs4 import BeautifulSoup

i = 0
defs = ['']*10
## Webopedia
word1 = 'data'
def webodef(word):
	tdef = ''
	print word
	url = "http://www.webopedia.com/TERM/D/" + word + ".html"
	html = urlopen(url).read()
	print url
	try: 
		#print html
		soup = BeautifulSoup(html)
		strong = soup.find("strong")
		print strong
		next = strong.find_previous("p")
		#next += next.find_next_siblings("p")
		next2 = next.find_next_siblings("p")
		#nextT = next + next2
		strings = next.stripped_strings
		for string in strings:
			tdef += string + " "
			print tdef
		for ps in next2:
			strings = ps.stripped_strings
			for string in strings:
				tdef += string + " "
	#strings = next.stripped_strings
	#for string in strings:
	#	print string
		return str(tdef)
	except:
		return ''

webodef(word1)