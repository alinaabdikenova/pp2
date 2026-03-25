''' import os
os.remove("test.txt")

import os 
if os.path.exists("test.txt"):
    os.remove("test.txt")
else:
    print("The file does not exist")
'''
import shutil
import os

shutil.copy("test.txt", "dva.txt")

if os.path.exists("test.txt"):
    os.remove("test.txt")
    print("FIle deleted")