import random

def Unicode():
    val = random.randint(0x20000, 0x2A6D6)
    return chr(val)

s= Unicode();
print(s)
