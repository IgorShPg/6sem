import sys
import socket
import cmd



class obraz(socket s, cmd.Cmd):
    def do_print(self, args):
        self.s.sendall(args)

    def do_info(self,args):
        self.s.sendall(args)

    def do_exit(self, args):
        return True




if __name__=="__main__":
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        obraz(s).cmdloop()
