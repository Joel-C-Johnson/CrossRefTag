from joblib import Parallel, delayed
import time
import sys
import os
import multiprocessing
import pdb

def check_paths(fp):
    # codes...
      .....
      .....
    #
    return (fp)

def start():
    now = time.time()
    if len(sys.argv) >= 2:
         j = Parallel(n_jobs=1) (delayed (check_paths)(fileName) for fileName in os.listdir(sys.argv[1]) )
        #  j = Parallel(n_jobs=multiprocessing.cpu_count()) (delayed (check_paths)(fileName) for fileName in os.listdir(sys.argv[1]) )   # to autodetect cpu cores
        #  print(j)
         print ("Finished in", time.time()-now , "sec")

if __name__ == '__main__':
    start()
