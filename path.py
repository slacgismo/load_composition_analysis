import os
x=os.path.abspath(os.getcwd())
f = open("scripts/path.txt", "w")
f.write(x)
