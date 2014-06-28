from numpy import zeros
from scipy.linalg import svd
from math import log
from numpy import asarray, sum
import nltk
from urllib import urlopen
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import random


#### Input parameters
n_text = 10			### Docs used
#n_words = 50		### Number of keywords to find
seeds = ['email']	### Central word(s) in concept space
n_dim = 4			### Number of dimensions used for clustering
Hits = []
n_iter = 100	### Iterations of random grouping of texts
n_docs_rand = 4 	#### Number of texts in group
doc_name = 'email.search'
stops = stopwords.words('english')
stops += ['mail','wikipedia','encyclopedia','technology','required','new']
punct = [',','.','[',']','(',')',"'",'-','"','?','/','%','$',"\\",'|']

def findwords(doc_list):
	#print "doclist",doc_list
	n_docs = len(doc_list)
	mylsa = LSA()
	for n in doc_list:
		#print '%s%d.txt'%(doc_name, n)
		doc = open('%s.%d.txt'%(doc_name, n),'r').read()
		mylsa.parse(doc)
	mylsa.build(n_docs)
	mylsa.TFIDF()
	#mylsa.printA()
	mylsa.calc()
	#d, results = 
	mylsa.findhits(seeds)
	#return d, results

class LSA(object):
	def __init__(self):
		self.wdict = {}
		self.dcount = 0
		#self.ndim = 10
		self.fdists = []
	#------------- Turn documents into dictionary-----------------#
	def parse(self,doc):		
		doc = doc.split()
		for w in doc:
			w = w.lower()
			#if 'e' in w and 'mail' in w: w = 'email' 
			for l in w:
				try: 
					int(l)
					w = 'new'
					break
				except: 
					if l in punct: 
						w = 'new'
						break
			if w in stops:
				continue
			elif w in self.wdict:
				self.wdict[w].append(self.dcount)
				
			else:
				self.wdict[w] = [self.dcount]

		self.dcount += 1
	#------------- Build word/document matrix-----------------#
	def build(self,n_docs):			
		self.keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 2]
		self.keys.sort()
		n_rows = len(self.keys)
		n_cols = n_docs
		self.A = zeros([n_rows, n_cols])
		for i, k in enumerate(self.keys):
			for d in self.wdict[k]:
				self.A[i,d] += 1
	#-------- Singular Value Decomposition (concept space)-------#
	def calc(self):
		self.U, self.S, self.Vt = svd(self.A)
	#-------- Term Frequency Inverse Document Frequency-------#	
	def TFIDF(self):
		WordsPerDoc = sum(self.A, axis=0)
		DocsPerWord = sum(asarray(self.A > 0, 'i'), axis=1)
		rows, cols = self.A.shape
		for i in range(rows):
			for j in range(cols):

				self.A[i,j] = (self.A[i,j] / WordsPerDoc[j]) * log(float(cols)/DocsPerWord[i])
	def printA(self):
		print "count matrix"
		print self.A[0:3,0:3]
		#print self.keys
		print "First 3 cols of U matrix"
		#print -1*self.U[:, 0:3]
		print "First 3 rows of Vt matrix"
		#print -1*self.Vt[0:3,:]
	#-------- Calculate distance between all words and seed word-------#	
	def findhits(self,seeds):
		self.ind = [self.keys.index(seed) for seed in seeds]
		hits = []
		ds = []
		rows, cols = self.A.shape

		for i in range(rows):
			d = 0
			w = self.keys[i]
			for j in range(1,n_dim):
				for k in self.ind:
					d += (self.U[i][j] - self.U[k][j])**2
			#d = d**0.5
			#hits.append(w) 
			#ds.append(d)
			if d == 0: 
				#print w
				if w not in Hits:
					Hits.append(w)


for i in range(n_iter):
	doc_list =  random.sample(range(n_text),n_docs_rand)
	findwords(doc_list)


print "doc name:",doc_name
#print "d final:", d
print "training iterations:",n_iter
print "# docs chosen randomly:", n_docs_rand
print "total docs input:", n_text
#print "docs with positive strength:", len(new_docs)
print "hit word", "distance from:",seeds
#for n in results:

	#print n[0], n[1]

print sorted(Hits)
