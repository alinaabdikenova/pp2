import os


os.makedirs("test_folder/subfolder/inner_folder", exist_ok=True)
print("folders created")

print("\ncontents of test_folder:")
for item in os.listdir("test_folder"):
    print(item)

# найти .py файлы только в test_folder
print("\n.py files:")
for root, dirs, files in os.walk("test_folder"):
    for file in files:
        if file.endswith(".py"):
            print(os.path.join(root, file))