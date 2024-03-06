import sys
import cowsay
import shlex

pos=0, 0
monster_position={}

def move(place):
    global pos
    where={"up":(0,-1), "down":(0,1), "left": (-1,0), "right":(1,0)}
    pos=tuple(map(lambda x,y: x+y+(-10 if x+y>9 else 0)+ (10 if x+y<0 else 0), pos, where[place]))
    print(f"Moved to {pos}")

    


def encounter():
    global pos, monster_position
    if mon:=monster_position.get(pos, None):
        name, hello=mon
        print(cowsay.cowsay(hello,cow=name))



def addmon(x, y, name, hello):
    if x>9 or x<0 or y>9 or y<0:
        print("Invalid arguments")
    else:
        if name in cowsay.list_cows():
            global monster_position
            replace=monster_position.get((x,y), None)
            monster_position[(x,y)]=name, hello
            print(f"Added monster {name} to {x,y} saying {hello}")
            if replace:
                print("Replaced the old monster")
        else:
            print("Cannot add unknown monster")


for word in sys.stdin:
    match shlex.split(word):
        case ["up"|"down"| "left"| "right"]:
            move(word.strip().split()[0])
            encounter()
        case ["addmon",str(name),*args]:
            if len(args) != 7:
                print("Invalid arguments")
            else:
                i=0
                while i < 7:
                    match args[i:i+2]:
                        case ["hello", str(hel_str)]:
                            hello=hel_str
                        case ["hp", hitpoints]:
                            hp=int(hitpoints)
                        case ["coords", x]:
                            x,y,i=int(x), int(args[i+2]), i+1
                    i+=2
                addmon(x,y,name,hello,hp)
        case _:
            print("Invalid command")




    
