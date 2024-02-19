import sys
import zlib
import glob

for name in glob.iglob(sys.argv[1] + "/??/*"):
    with open(name, "rb") as f:
        bulk=zlib.decompress(f.read())
    kindsize, _, content = bulk.partition(b'\x00')
    kind, size=kindsize.split()
    match kind:
        case b"commit":
            print("\tCommit:")
            print(content.decode().rstrip())
        case b"tree":
            while content:
                namesize, _, content=content.partition(b'\x00')
                ID, content=content[:20],content[20:]
                print(namesize.decode(), ID.hex())
        case _:
            print("\tOther:", kind.decode())
            print(content)
    
