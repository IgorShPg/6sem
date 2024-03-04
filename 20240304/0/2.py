import shlex

name=input()
birth=input()

register=shlex.join(["register", name, birth])

print(register)

print(*shlex.split(register))
