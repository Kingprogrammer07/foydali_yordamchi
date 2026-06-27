import os
import shutil

# Joriy direktoriyadan boshlash
root_dir = os.getcwd()
print(root_dir)
for dirpath, dirnames, filenames in os.walk(root_dir):
    if "__pycache__" in dirnames:
        cache_path = os.path.join(dirpath, "__pycache__")
        print(f"O'chirilmoqda: {cache_path}")
        shutil.rmtree(cache_path)

print("Barcha __pycache__ papkalari o'chirildi ✅")
