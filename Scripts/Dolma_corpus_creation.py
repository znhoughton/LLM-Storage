from collections import defaultdict
from collections import Counter
import json
import re
import multiprocessing as mp
from os import listdir
from os.path import isfile, join
import gzip
import time
import glob
import pandas as pd
import csv
import os

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
two_gram_counts_serial = Counter()
three_gram_counts_serial = Counter()
#troubleshoot_counter = 0
def process_gzip_file_serial(gzip_file): #open each gzip file and count 1-gram, 2-gram, and 3-gram, might do 4 and 5-grams later
    with gzip.open(gzip_file,'rt', encoding='utf-8') as f:  
        #troubleshoot_counter = 0
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
    with open("two_gram_counts_serial.txt", 'w') as f:
        for k,v in two_gram_counts_serial.items():
            f.write( "{}\t{}".format(k,v))			
    with open("three_gram_counts_serial.txt", 'w') as f:
        for k,v in three_gram_counts_serial.items():
            f.write( "{}\t{}".format(k,v))

# this is for parallel processing
pool_size = 10

#one_gram_counts_parallel = Counter()
#two_gram_counts_parallel = Counter()
#three_gram_counts_parallel = Counter()

def process_individual_file(gzip_file):
     print(f"Current File: {gzip_file}")
     one_gram_ind_counter = Counter()
     two_gram_ind_counter = Counter()
     three_gram_ind_counter= Counter()
     with gzip.open(gzip_file,'rt', encoding='utf-8') as f:
          for line in f:
            try:
                
                one_gram_ind_counter.update(onegram(line))
                two_gram_ind_counter.update(bigrams(line))
                three_gram_ind_counter.update(trigrams(line))
                
            except EOFError:
                print(gzip_file, ' is corrupted')
     write_file_to_csv(counter_file = one_gram_ind_counter, file = gzip_file, ngram_type = 'onegram_files')
     write_file_to_csv(counter_file = two_gram_ind_counter, file = gzip_file, ngram_type = 'bigram_files')
     write_file_to_csv(counter_file = three_gram_ind_counter, file = gzip_file, ngram_type = 'trigram_files')
     #return [one_gram_ind_counter, two_gram_ind_counter, three_gram_ind_counter]
     
     
               
def process_gzip_file_parallel(gzip_file):
     pool = mp.Pool(pool_size)
     results = pool.map(process_individual_file, [file for file in gzip_file])
     #print(results)
     pool.close()




#def process_results(result):
#     for file in result:
#         print('Current file: ', file)
#         one_gram_counts_parallel.update(file[0])
#         two_gram_counts_parallel.update(file[1])
#         three_gram_counts_parallel.update(file[2])


def write_file_to_csv(counter_file, file, ngram_type):
       file_name = (os.path.splitext(file)[0]).split('/')[-1]
       print(f"Currently Writing: {file_name}")
       with open(f'./{ngram_type}/{file_name}.csv', 'w') as csvfile:
            fieldnames = ['ngram', 'count']
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            if ngram_type == 'onegram_files':
                 for k,v in counter_file.items():
                       writer.writerow([k] + [v])
            else:
                  for k,v in counter_file.items():
                   	 writer.writerow(list(k) + [v])	
		
def process_onegram_files():
      print("Currently processing onegram_files")
      onegram_files = glob.glob('./onegram_files/*.csv')
      intermediate_dfs = []
      batch_size = 100
      for i in range(0, len(onegram_files), batch_size):
            print(f"Currently processing batch {i} / {batch_size}")
            batch = onegram_files[i:i + batch_size]
            batch_df = pd.concat(batch).groupby('ngram', as_index=False).sum()
            intermediate_dfs.append(batch_df)
      result_df = pd.concat(intermediate_dfs).groupby('ngram', as_index=False).sum()
      result_df.to_csv('full_onegram_corpus.csv')
      

def process_bigram_files():
      print("Currently processing bigram files")
      bigram_files = glob.glob('./bigram_files/*.csv')
      intermediate_dfs = []
      batch_size = 100
      for i in range(0, len(bigram_files), batch_size):
            print(f"Currently processing batch {i} / {batch_size}")
            batch = bigram_files[i:i + batch_size]
            batch_df = pd.concat(batch).groupby('ngram', as_index=False).sum()
            intermediate_dfs.append(batch_df)  
      result_df = pd.concat(intermediate_dfs).groupby('ngram', as_index=False).sum()
      result_df.to_csv('full_bigram_corpus.csv')
      
	       
	


def process_trigram_files():
      print("Currently processing bigram files")
      trigram_files = glob.glob('./trigram_files/*.csv')
      intermediate_dfs = []
      batch_size = 100
      for i in range(0, len(trigram_files), batch_size):
          print(f"Currently processing batch {i} / {batch_size}")
          batch = trigram_files[i:i + batch_size]
          batch_df = pd.concat(batch).groupby('ngram', as_index=False).sum()
          intermediate_dfs.append(batch_df)
      result_df = pd.concat(intermediate_dfs).groupby('ngram', as_index=False).sum()
      result_df.to_csv('full_trigram_corpus.csv')
      
	


	

### write each file into a txt file separated by tab
#def write_result_to_file():
#    with open("one_gram_counts.txt", 'w') as f:
#            for k,v in one_gram_counts_parallel.items():
#               f.write( "{}\t{}".format(k,v))			
#    with open("two_gram_counts.txt", 'w') as f:
#        for k,v in two_gram_counts_parallel.items():
#            f.write( "{}\t{}".format(k,v))			
#    with open("three_gram_counts.txt", 'w') as f:
#        for k,v in three_gram_counts_parallel.items():
#            f.write( "{}\t{}".format(k,v))
            
            

def main():
    if __name__ == "__main__":
            t1 = time.perf_counter()
            path = 'Dolma/'
            gzip_files = [(path + f) for f in listdir(path) if isfile(join(path, f))]	#all the gzip files in the directory
            process_gzip_file_parallel(gzip_files)
            #process_results(results)
            process_onegram_files()
            process_bigram_files()
            process_trigram_files()
            #write_result_to_file()
            t2 = time.perf_counter()
            print(t2 - t1)
        
        

#def main_serial():
#    if __name__ == "__main__":
#        t1 = time.perf_counter()
#        path = 'Dolma/'
#        gzip_files = [(path + f) for f in listdir(path) if isfile(join(path, f))]	#all the gzip files in the directory
#        for i in gzip_files:
#            print('Current file: ', i)
#            process_gzip_file_serial(i)
#        write_result_to_file_serial()
#        t2 = time.perf_counter()
#        print(t2 - t1)



t1 = time.perf_counter()
main()
t2 = time.perf_counter()
t2 - t1



