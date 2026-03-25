import os
import shutil

# создать папки
os.makedirs("src", exist_ok=True)
os.makedirs("dst", exist_ok=True)

# создать файл
with open("src/file.txt", "w") as f:
    f.write("hello")

# копировать файл
shutil.copy("src/file.txt", "dst/file.txt")

# переместить файл
shutil.move("src/file.txt", "dst/file_moved.txt")