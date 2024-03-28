import cowsay
import asyncio




pos=0, 0
monster_position={}
custom_monsters={"jgsbat"}
clients={}
logins={}
weapons={"sword" : 10, "spear" : 15, "axe" : 20}


def move(x, y):
    global pos
    pos=tuple(map(lambda x,y: x+y+(-10 if x+y>9 else 0)+ (10 if x+y<0 else 0), pos, (x, y)))
    return f"Moved to {pos}"


def addmon(x, y, name, hello, hp, gamer):
    ans=[]
    if x>9 or x<0 or y>9 or y<0:
        ans.append("Invalid arguments")
    else:
        if name in cowsay.list_cows() or name in custom_monsters:
            global monster_position,logins
            flag=True
            replace=monster_position.get((x,y), None)
            monster_position[(x,y)]=[name, hello, hp]
            ans.append(f"{logins[gamer]} added monster {name} with {hp} hitpoints to {x, y} saying {hello}")
            if replace:
                ans.append(f"{logins[gamer]} Replaced the old monster")
        else:
            ans.append("Cannot add unknown monster")
            flag=False

    return "\n".join(ans), flag



def encounter():
    global pos, monster_position
    if mon:=monster_position.get(pos, None):
        name, hello=mon[0], mon[1]
        if name in custom_monsters:
            return cowsay.cowsay(hello, cowfile=custom_monsters[name])
        else:
            return cowsay.cowsay(hello, cow=name)


    return None

def attack(name,damage,gamer):
    global pos, monster_position,logins
    ans=[]
    flag=True
    if (mon := monster_position.get(pos, None)) and mon[0] == name:
        damage = damage if mon[2] >= damage else mon[2]
        ans.append(f"{logins[gamer]} attacked {mon[0]},  damage {damage} hp")
        monster_position[pos][2]-=damage
        if monster_position[pos][2]:
            ans.append(f"{mon[0]} now has {monster_position[pos][2]}")
        else:
            ans.append(f"{mon[0]} died")
            del monster_position[pos]
    else:
        ans.append(f"No {name} here")
        flag=False
    return "\n".join(ans),flag


def login(me, nickname):
    global logins
    if nickname in logins.values():
        return "This login is already taken", False
    else:
        logins[me] = nickname
        return f"You logged in as {nickname}", True


async def cowhandler(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                match q.result().decode().split():
                    case ["login", nickname]:
                        login_msg, login_info = login(me, nickname)
                        print(clients, logins)
                        await clients[me].put(login_msg)
                        if login_info:
                            for client in clients:
                                await clients[client].put(f"{nickname} has connected to MUD")

                    case ["move", x, y]:
                        if me in logins:
                            ans = [move(int(x), int(y))]
                            if enc := encounter():
                                ans.append(enc)
                            await clients[me].put("\n".join(ans))

                    case ["addmon", x, y, name, hp, *hello]:
                        if me in logins:
                            hello = " ".join(hello)
                            msg, broadcast = addmon(int(x), int(y), name, hello, int(hp), me)
                            if broadcast:
                                for client in clients:
                                    await clients[client].put(msg)
                            else:
                                await clients[me].put(msg)

                    case ["attack", name, damage]:
                        if me in logins:
                            msg, broadcast = attack(name, int(damage), me)
                            if broadcast:
                                for client in clients:
                                    await clients[client].put(msg)
                            else:
                                await clients[me].put(msg)

                    case ["exit", ]:
                        if me in logins:
                            await clients[me].put("exit")
                            for client in clients:
                                if client != me:
                                    await clients[client].put(f"{logins[me]} has disconnected from MUD")
                            receive.cancel()
                            writer.close()
                            await writer.wait_closed()

                            del logins[me]
                            del clients[me]

            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()


    writer.close()
    await writer.wait_closed()






async def main():
    server = await asyncio.start_server(cowhandler, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())

