from joblib import Parallel, delayed
import time
import sys
import os
import multiprocessing
import codecs
import re
import pdb

def check_paths(fp):
    refID = []
    fn = fp.split(".")
    vCount = 0
    vNum = "xxx"
    if (fn[-1]) in ["sfm", "SFM", "usfm", "USFM"]:
        f = codecs.open("Hii/" + fp, mode='r', encoding='utf-8')
        fc = f.read()
        ch = fc.split("\\c")
        # pdb.set_trace()
        # vCount = vCount + len(v)
        for vs in ch[1:]:
            v = vs.split("\\v")
            for vt in v:
                v1  = re.match("(.*?) (.*)", vt)
                try:
                    vNum = str(v1.group(0).strip())
                    # print(vNum)
                except:
                    print v1.group(0).strip()
                    pass
                cNum = v[0].split("\r\n")[0].strip()
                refID.append("0" + str(fp[:2]) + " -" + cNum + " -" + vNum + " - 00")
        print("\r\n".join(refID))
    return (fp)

def start():
    now = time.time()
    if len(sys.argv) >= 2:
         j = Parallel(n_jobs=1) (delayed (check_paths)(fileName) for fileName in os.listdir(sys.argv[1]) )
        #  j = Parallel(n_jobs=multiprocessing.cpu_count()) (delayed (check_paths)(fileName) for fileName in os.listdir(sys.argv[1]) )
        #  print(j)
         print ("Finished in", time.time()-now , "sec")

if __name__ == '__main__':
    start()
