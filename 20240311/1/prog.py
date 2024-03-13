import sys
import cowsay
import shlex
from io import StringIO
import cmd

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

def move(place):
    global pos
    where={"up":(0,-1), "down":(0,1), "left": (-1,0), "right":(1,0)}
    pos=tuple(map(lambda x,y: x+y+(-10 if x+y>9 else 0)+ (10 if x+y<0 else 0), pos, where[place]))
    print(f"Moved to {pos}")

    


def encounter():
    global pos, monster_position
    if mon:=monster_position.get(pos, None):
        name, hello=mon[0], mon[1]
        if name in custom_monsters:
            print(cowsay.cowsay(hello,cowfile=custom_monsters[name]))
        else:
            print(cowsay.cowsay(hello,cow=name))



def addmon(x, y, name, hello, hp):
    if x>9 or x<0 or y>9 or y<0:
        print("Invalid arguments")
    else:
        if name in cowsay.list_cows() or name in custom_monsters:
            global monster_position
            replace=monster_position.get((x,y), None)
            monster_position[(x,y)]=[name, hello, hp]
            print(f"Added monster {name} with {hp} hitpoints to {x, y} saying {hello}")
            if replace:
                print("Replaced the old monster")
        else:
            print("Cannot add unknown monster")

def attack():
    global pos, monster_position
    if mon := monster_position.get(pos, None):
        damage = 10 if mon[2] >= 10 else mon[2]
        print(f"Attacked {mon[0]},  damage {damage} hp")
        monster_position[pos][2]-=damage
        if monster_position[pos][2]:
            print(f"{mon[0]} now has {monster_position[pos][2]}")
        else:
            print(f"{mon[0]} died")
            del monster_position[pos]
    else:
        print("No monster here")
    


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
    prompt="(MUD )"

    def do_up(self, args):
        move("up")
        encounter()

    def do_down(self, args):
        move("down")
        encounter()
    
    def do_left(self, args):
        move("left")
        encounter()
    
    def do_right(self, args):
        move("right")
        encounter()

    def do_addmon(self, args):
        name, *args=parse(args)
        if args:=parse_addmon(args):
            x, y, hello, hp=args
            addmon(x, y, name,  hello, hp)
        
    def do_attack(self, args):
        attack()



        


MUD().cmdloop()

    
