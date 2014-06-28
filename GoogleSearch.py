
import nltk
from urllib import urlopen
from google import search


i = 0

N_urls = 10
SearchTerm = 'email'
Search = 'how does' + SearchTerm + 'work?'
for url in search(Search,stop=(N_urls)):
	print(url)
	if 'pdf' in url:
		i -= 1
	else:
		html = urlopen(url).read()
		raw = nltk.clean_html(html)
	#tokens = nltk.word_tokenize(raw)
	#raw = raw[:1000]
	#print url
		with open('%s.search.%d.txt'%(SearchTerm,i),'w') as fid:
			fid.write(raw)
	#text.append(raw)
	#print "text",text
	i += 1
	if i == N_urls: break

