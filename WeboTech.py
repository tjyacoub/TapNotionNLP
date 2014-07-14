from nltk.corpus import wordnet
import nltk
import urllib
from urllib import urlopen
from weboscrape import webodef
from bs4 import BeautifulSoup
import sys


techtermsfile = open("techterms.txt",'r').readlines()
techterms = []
for term in techtermsfile:
	techterms.append(term.rstrip('\n').lower())
#print techterms

dbtermfile = open("techtermsshort.txt",'r').readlines()
dbterms = []
for term in dbtermfile:
	dbterms.append(term.rstrip('\n').lower())
print dbterms

#initial_word = 'computer'
wordlist = {}
i = 0
max_iter = 8
master_list = []

def is_tech(word):
	if word in techterms: return True
	else: return False

def MerWeb(word):
    api_key = 'd6ed294b-9e3a-4897-8281-2c4c5ae8f2b1'
    query = ''
    service_url = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/'
    search_term = word

    url = service_url + search_term + '?key=' + api_key
    print url
    xmlread = urllib.urlopen(url).read()
    x = BeautifulSoup(xmlread, "xml")
    try: 
    	l1 = x.dt.get_text()
    	temp_def = ''
    	for t in l1:
    		try:
    			temp_def += str(t)
    		except:
    			None
    	return temp_def
    except:
    	return ''


def getdef(word): 
	 
	#print word
	text = ''
	text2 = ''
	try: 
		text = MerWeb(word)
	except: None

	try:
		text2 = webodef(word)
	except: None
	text = text + text2
	print text
	if word not in wordlist: wordlist[word] = []
	tokens = nltk.word_tokenize(text)
	tags = nltk.pos_tag(tokens)
	for tag in tags:
		word_2, pos = tag
		word_2 = str(word_2)
		if pos == 'NN' and word_2 not in wordlist[word]:
			print tag
			wordlist[word].append(word_2)
			if word_2 not in master_list:
				master_list.append(word_2)
			
out = open("defnouns.txt",'w')
#def is_tech(word):
for term in dbterms[:2]:
	getdef(term)
print master_list

for term in master_list:
	print term
	out.write((term + '\n'))
#print wordlist
#print wordlist.keys()
