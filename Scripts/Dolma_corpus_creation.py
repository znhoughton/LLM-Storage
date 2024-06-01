from collections import defaultdict
from collections import Counter
import json
import re
import multiprocessing as mp
from os import listdir
from os.path import isfile, join
import gzip
import time

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

# This is for serial processing
one_gram_counts = Counter()
two_gram_counts = Counter()
three_gram_counts = Counter()
#troubleshoot_counter = 0
def process_gzip_file_serial(gzip_file): #open each gzip file and count 1-gram, 2-gram, and 3-gram, might do 4 and 5-grams later
    with gzip.open(gzip_file,'rt', encoding='utf-8') as f:  
        troubleshoot_counter = 0
        for line in f:
            #troubleshoot_counter += 1
            #if troubleshoot_counter % 100000 == 0:
                #print(troubleshoot_counter)
            one_gram_counts.update(line)
            two_gram_counts.update(bigrams(line))
            three_gram_counts.update(trigrams(line))

# this is for parallel processing
pool_size = 50

def process_individual_file(gzip_file):
     one_gram_ind_counter = Counter()
     two_gram_ind_counter = Counter()
     three_gram_ind_counter= Counter()
     with gzip.open(gzip_file,'rt', encoding='utf-8') as f:
          for line in f:
            one_gram_ind_counter.update(line)
            two_gram_ind_counter.update(bigrams(line))
            three_gram_ind_counter.update(trigrams(line))
     return [one_gram_ind_counter, two_gram_ind_counter, three_gram_ind_counter]
               
def process_gzip_file_parallel(gzip_file):
     pool = mp.Pool(pool_size)
     results = pool.map(process_individual_file, [file for file in gzip_file])
     print(results)
     pool.close()

def process_results(result):
     for file in result:
         one_gram_counts.update(file[0])
         two_gram_counts.update(file[1])
         three_gram_counts.update(file[2])

### write each file into a txt file separated by tab
def write_result_to_file():
    with open("one_gram_counts.txt", 'w') as f:
            for k,v in one_gram_counts.items():
                f.write( "{}\t{}".format(k,v))			
    with open("two_gram_counts.txt", 'w') as f:
        for k,v in two_gram_counts.items():
            f.write( "{}\t{}".format(k,v))			
    with open("three_gram_counts.txt", 'w') as f:
        for k,v in three_gram_counts.items():
            f.write( "{}\t{}".format(k,v))

def main():
    if __name__ == "__main__":
        t1 = time.perf_counter()

        path = 'Dolma/'
        gzip_files = [(path + f) for f in listdir(path) if isfile(join(path, f))]	#all the gzip files in the directory
        results = process_gzip_file_parallel(gzip_files)
        process_results(results)

        write_result_to_file()

        t2 = time.perf_counter()
        print(t2 - t1)




main()