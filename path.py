import os
x=os.path.abspath(os.getcwd())
f = open("src/scripts/path.txt", "w")
f.write(x)
