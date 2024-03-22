import sys
import cowsay
import shlex
import readline
from io import StringIO
import cmd
import socket


jgsbat = cowsay.read_dot_cow(StringIO(r"""
$the_cow = <<EOC;
         $thoughts
          $thoughts
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\\\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     __\\\\'--'//__
         (((""`  `"")))
EOC
"""))


pos=0, 0
monster_position={}
custom_monsters={"jgsbat" : jgsbat}
weapons={"sword" : 10, "spear" : 15, "axe" : 20}


def which_cow(name, hello):
    if name in custom_monsters:
        print(cowsay.cowsay(hello, cowfile=custom_monsters[name]))
    else:
        print(cowsay.cowsay(hello, cow=name))


def request(strok):
    global cowsocket
    cowsocket.send(f"{strok}\n".encode())
    ans=cowsocket.recv(1024).decode().strip()
    for i in ans.split("\n"):
        if i.startswith("COW"):
            i=i.split()
            name, hello=i[1]," ".join(i[2:])
            which_cow(name, hello)
        else:
            print(i)

def parse(args):
    return shlex.split(args)

def parse_addmon(args):
    if len(args) != 7:
        print("Invalid arguments")
        return None
    i = 0
    while i < len(args):
        match args[i: i + 2]:
            case ["hello", str(hello_string)]:
                hello = hello_string
            case ["hp", hitpoints]:
                hp = int(hitpoints)
            case ["coords", x]:
                x, y, i = int(x), int(args[i + 2]), i + 1
        i += 2
    return x, y, hello, hp




class MUD(cmd.Cmd):
    intro="<<< Welcome to Python-MUD 0.1 >>>"
    prompt="(MUD)"

    def do_up(self, args):
        request("move 0 -1")

    def do_down(self, args):
        request("move 0 1")
    
    def do_left(self, args):
        request("move -1 0")

    def do_right(self, args):
        request("move 1 0")

    def do_addmon(self, args):
        name, *args=parse(args)
        if args:=parse_addmon(args):
            x, y, hello, hp=args
            request(f"addmon {x} {y} {name} {hp} {hello}")
        
    def do_attack(self, args):
        name, *args, weapon=*parse(args), "sword"
        if args and args[0] == "with":
            if args[1] in weapons:
                weapon=args[1]
            else:
                print("Unknown weapon")
                weapon=None
        if weapon:
            request(f"attack {name} {weapons[weapon]}")

    def complete_attack(self, text, line, begidx, endidx):
        if text and len(shlex.split(line))==2 or not text and len(shlex.split(line))==1:
             return [mon for mon in cowsay.list_cows() + list(custom_monsters.keys()) if mon.startswith(text)]
        elif text and len(shlex.split(line))==3 or not text and len(shlex.split(line))==2:
            return[i for i in ["with"] if i.startswith(text)]
        elif text and len(shlex.split(line))==4 or not text and len(shlex.split(line))==3:
            return[i for i in weapons if i.startswith(text)]
      

    

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cowsocket:
    cowsocket.connect(("localhost", 1337))
    MUD().cmdloop()



    
    
