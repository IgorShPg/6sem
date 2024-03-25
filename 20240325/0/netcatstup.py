import shlex
import cmd
import socket
import readline
import threading
from copy import copy

def receive(cmdline):
    global receiving, COWsocket, completion
    while receiving:
        msg = COWsocket.recv(1024).decode()
        if msg.strip() == "exit":
            break
        elif msg.startswith("["):
            completion = eval(msg)
        else:
            print(f"\n{msg.strip()}\n{cmdline.prompt}{readline.get_line_buffer()}", end="", flush=True)



class REQ(cmd.Cmd):
    prompt="(SERV)"

    def do_hi(self,args):
        


host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    cmdline=REQ()
    receiver = threading.Thread(target=receive, args=(cmdline,))
    receiver.start()
    cmdline.cmdloop()