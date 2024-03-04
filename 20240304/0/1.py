import shlex
import readline

while (s:=input()) != "quit":
    try:
        g=shlex.split(s)
    except Exception as E:
        print()
    print(shlex.join(g))
