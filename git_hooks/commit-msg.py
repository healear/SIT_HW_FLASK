import re
import sys


regex = r"[0-9a-zA-Zа-яА-Я]+"
msg = open(sys.argv[1], "r").read()
if not re.match(regex, msg):
    print("Incorrect commit format!")
    sys.exit(1)
