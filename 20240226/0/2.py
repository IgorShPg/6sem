import cowsay
import sys 

if sys.argv[2] in cowsay.list_cows():
    print(cowsay.cowsay(sys.argv[2], sys_argv[1]))