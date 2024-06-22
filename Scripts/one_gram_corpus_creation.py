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
one_gram_counts_serial = Counter()
#two_gram_counts_serial = Counter()
#three_gram_counts_serial = Counter()
#troubleshoot_counter = 0
def process_gzip_file_serial(gzip_file): #open each gzip file and count 1-gram, 2-gram, and 3-gram, might do 4 and 5-grams later
    with gzip.open(gzip_file,'rt', encoding='utf-8') as f:  
        troubleshoot_counter = 0
        for line in f:
            try: 
                #troubleshoot_counter += 1
                #if troubleshoot_counter % 100000 == 0:
                    #print(troubleshoot_counter)
                one_gram_counts_serial.update(line)
                two_gram_counts_serial.update(bigrams(line))
                three_gram_counts_serial.update(trigrams(line))
            except EOFError:
                print(gzip_file, ' is corrupted')
                
                
def write_result_to_file_serial():
    with open("one_gram_counts_serial.txt", 'w') as f:
            for k,v in one_gram_counts_serial.items():
                f.write( "{}\t{}".format(k,v))			
    #with open("two_gram_counts_serial.txt", 'w') as f:
        #for k,v in two_gram_counts_serial.items():
            #f.write( "{}\t{}".format(k,v))			
    #with open("three_gram_counts_serial.txt", 'w') as f:
        #for k,v in three_gram_counts_serial.items():
            #f.write( "{}\t{}".format(k,v))

# this is for parallel processing
pool_size = 50

one_gram_counts_parallel = Counter()
#two_gram_counts_parallel = Counter()
#three_gram_counts_parallel = Counter()

def process_individual_file(gzip_file):
     one_gram_ind_counter = Counter()
     #two_gram_ind_counter = Counter()
     #three_gram_ind_counter= Counter()
     with gzip.open(gzip_file,'rt', encoding='utf-8') as f:
          print(gzip_file)
          for line in f:
            try:
                
                one_gram_ind_counter.update(onegram(line))
                #two_gram_ind_counter.update(bigrams(line))
                #three_gram_ind_counter.update(trigrams(line))
                
            except EOFError:
                print(gzip_file, ' is corrupted')
     return [one_gram_ind_counter]
     
     
               
def process_gzip_file_parallel(gzip_file):
     pool = mp.Pool(pool_size)
     results = pool.map(process_individual_file, [file for file in gzip_file])
     #print(results)
     pool.close()




def process_results(result):
     for file in result:
         print('Current file: ', file)
         one_gram_counts_parallel.update(file[0])
         #two_gram_counts_parallel.update(file[1])
         #three_gram_counts_parallel.update(file[2])




### write each file into a txt file separated by tab
def write_result_to_file():
    with open("one_gram_counts.txt", 'w') as f:
            for k,v in one_gram_counts_parallel.items():
                f.write( "{}\t{}".format(k,v))			
    #with open("two_gram_counts.txt", 'w') as f:
        #for k,v in two_gram_counts_parallel.items():
            #f.write( "{}\t{}".format(k,v))			
    #with open("three_gram_counts.txt", 'w') as f:
        #for k,v in three_gram_counts_parallel.items():
            #f.write( "{}\t{}".format(k,v))
            
            

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
        
        

def main_serial():
    if __name__ == "__main__":
        t1 = time.perf_counter()
        path = 'Dolma/'
        gzip_files = [(path + f) for f in listdir(path) if isfile(join(path, f))]	#all the gzip files in the directory
        for i in gzip_files:
            print('Current file: ', i)
            process_gzip_file_serial(i)
        write_result_to_file_serial()
        t2 = time.perf_counter()
        print(t2 - t1)



t1 = time.perf_counter()
main()
t2 = time.perf_counter()
t2 - t1



