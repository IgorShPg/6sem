import os
import sys
import glob
import zlib











if len(sys.argv)==1:
    for i in glob.iglob(".git/refs/heads/*"):
        print(i.split(os.sep)[-1])