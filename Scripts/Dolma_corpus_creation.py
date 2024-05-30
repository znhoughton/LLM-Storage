from collections import defaultdict
from collections import Counter
import json
import re
from multiprocessing import Pool
import os
from os import listdir
from os.path import isfile, join

#we will ignore case and punctuation

one_gram_counts = Counter()
two_gram_counts = Counter()
three_gram_counts = Counter()

	
def onegram(sentence):
	text = re.sub('\W', ' ', sentence.lower())
	words = text.split()
	return words
	
	

def bigrams(sentence):
	text = re.sub('\W', ' ', sentence.lower())
	words = text.split()
	return zip(words, words[1:])
	
	
	
	
	
def trigrams(sentence):
	text = re.sub('\W', ' ', sentence.lower())
	words = text.split()
	return zip(words, words[1:], words[2:])
	
	
	
	

def process_gzip_file(gzip_file):
	with gzip.open(gzip_file,'rt') as f:    
		for line in f:
			one_gram_counts.update(onegram(line))
			two_gram_counts.update(bigrams(line))
			three_gram_counts.update(trigrams(line))


		
if __name__ == "__main__":
	path = 'test'
	gzip_files = [f for f in listdir(path) if isfile(join(path, f))]
		
	num_processes = min(20, os.cpu_count())
		
	with Pool(processes = num_processes) as pool:
		pool.map(process_gzip_file, gzip_files)
			

	with open("one_gram_counts.txt", 'w') as f:
		for k,v in one_gram_counts.items():
			f.write( "{}\t{}".format(k,v))
				
				
	with open("one_gram_counts.txt", 'w') as f:
		for k,v in two_gram_counts.items():
			f.write( "{}\t{}".format(k,v))
				
				
	with open("one_gram_counts.txt", 'w') as f:
		for k,v in three_gram_counts.items():
			f.write( "{}\t{}".format(k,v))
			
			
			
			
			