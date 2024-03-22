import cowsay
import asyncio




pos=0, 0
monster_position={}
custom_monsters={"jgsbat"}
weapons={"sword" : 10, "spear" : 15, "axe" : 20}


def move(x, y):
    global pos
    pos=tuple(map(lambda x,y: x+y+(-10 if x+y>9 else 0)+ (10 if x+y<0 else 0), pos, (x, y)))
    return f"Moved to {pos}"


def addmon(x, y, name, hello, hp):
    ans=[]
    if x>9 or x<0 or y>9 or y<0:
        ans.append("Invalid arguments")
    else:
        if name in cowsay.list_cows() or name in custom_monsters:
            global monster_position
            replace=monster_position.get((x,y), None)
            monster_position[(x,y)]=[name, hello, hp]
            ans.append(f"Added monster {name} with {hp} hitpoints to {x, y} saying {hello}")
            if replace:
                ans.append("Replaced the old monster")
        else:
            ans.append("Cannot add unknown monster")

    return "\n".join(ans)



def encounter():
    global pos, monster_position
    if mon:=monster_position.get(pos, None):
        name, hello=mon[0], mon[1]
        return f"COW {name} {hello}"

    return None

def attack(name,damage):
    global pos, monster_position
    ans=[]
    if (mon := monster_position.get(pos, None)) and mon[0] == name:
        damage = damage if mon[2] >= damage else mon[2]
        ans.append(f"Attacked {mon[0]},  damage {damage} hp")
        monster_position[pos][2]-=damage
        if monster_position[pos][2]:
            ans.append(f"{mon[0]} now has {monster_position[pos][2]}")
        else:
            ans.append(f"{mon[0]} died")
            del monster_position[pos]
    else:
        ans.append(f"No {name} here")
    return "\n".join(ans)


async def cowhandler(reader, writer):
    host, port = writer.get_extra_info('peername')
    while not reader.at_eof():
        request = (await reader.readline()).strip().decode()
        match request.split():
            case ["move", x, y]:
                ans = [move(int(x), int(y))]
                if enc := encounter():
                    ans.append(enc)
                ans = "\n".join(ans)
            case ["addmon", x, y, name, hp, *hello]:
                hello = " ".join(hello)
                ans = addmon(int(x), int(y), name, hello, int(hp))
            case ["attack", name, damage]:
                ans = attack(name, int(damage))

        writer.write(ans.encode())

    writer.close()
    await writer.wait_closed()





async def main():
    server = await asyncio.start_server(cowhandler, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
