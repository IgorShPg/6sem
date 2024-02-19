import sys
import zlib
import glob

for name in glob.iglob(sys.argv[1] + "/??/*"):
    with open(name, "rb") as f:
        content=zlib.decompress(f.read())
    print(content)
