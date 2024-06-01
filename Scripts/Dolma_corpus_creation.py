from collections import defaultdict
from collections import Counter
import json
import re
from multiprocessing import Pool
import os
from os import listdir
from os.path import isfile, join
import gzip
import time

one_gram_counts = Counter()
two_gram_counts = Counter()
three_gram_counts = Counter()



def onegram(sentence):
	text = re.sub("[^\w\d'\s]+",'',sentence)
	words = text.split()
	return words
	
	


def bigrams(sentence):
	text = re.sub("[^\w\d'\s]+",'',sentence)
	words = text.split()
	return zip(words, words[1:])
	
	


def trigrams(sentence):
	text = re.sub("[^\w\d'\s]+",'',sentence)
	words = text.split()
	return zip(words, words[1:], words[2:])
	


#troubleshoot_counter = 0
def process_gzip_file(gzip_file): #open each gzip file and count 1-gram, 2-gram, and 3-gram, might do 4 and 5-grams later
    with gzip.open(gzip_file,'rt') as f:  
        troubleshoot_counter = 0
        for line in f:
            #troubleshoot_counter += 1
            #if troubleshoot_counter % 100000 == 0:
                #print(troubleshoot_counter)
            one_gram_counts.update(line)
            two_gram_counts.update(bigrams(line))
            three_gram_counts.update(trigrams(line))

###### without multiprocess


t1 = time.perf_counter()	
if __name__ == "__main__":
    path = 'Dolma/'
    gzip_files = [(path + f) for f in listdir(path) if isfile(join(path, f))]	#all the gzip files in the directory
    for i in gzip_files: #for each gzip file:
        print('Current file: ', i)  #keep track of the current file
        process_gzip_file(i)    #process the file

t2 = time.perf_counter()
t2 - t1

### write each file into a txt file separated by tab
with open("one_gram_counts.txt", 'w') as f:
		for k,v in one_gram_counts.items():
			f.write( "{}\t{}".format(k,v))			
with open("two_gram_counts.txt", 'w') as f:
    for k,v in two_gram_counts.items():
        f.write( "{}\t{}".format(k,v))			
with open("three_gram_counts.txt", 'w') as f:
    for k,v in three_gram_counts.items():
        f.write( "{}\t{}".format(k,v))
