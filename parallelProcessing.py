from joblib import Parallel, delayed
import time
import sys
import os
import multiprocessing

def check_paths(fp):
    fn = fp.split(".")
    if (fn[1]) in ["sfm", "SFM", "usfm", "USFM"]:
        f = open(fp, mode='r', encoding='utf-8')
        fc = f.read()

    return (fp)

def start():
    now = time.time()
    if len(sys.argv) >= 2:
         j = Parallel(n_jobs=multiprocessing.cpu_count()) (delayed (check_paths)(fileName) for fileName in os.listdir(sys.argv[1]) )
         print(j)
         print ("Finished in", time.time()-now , "sec")

if __name__ == '__main__':
    start()
