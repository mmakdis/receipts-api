# Use in directory

import io
import os
import sys
from pathlib import Path

rootdir = "./maximages"
REMOVE_DIR = False

if len(sys.argv) > 1:
    if sys.argv[1] in ["-c", "--clean"]:
        REMOVE_DIR = True
    else:
        print("use -c or --clean to remove empty dirs")

def clean_name(dir: str, count: int) -> str:
    path = dir.split("/")
    if len(path) < 4:
        return
    path.pop(2)
    file_info = path[-1].split(".")
    file_info[0] = f"{file_info[0]}{count}"
    if file_info[1] not in ["jpeg", "png"]:
        file_info[1] = "jpeg"
    path[-1] = ".".join(file_info)
    return '/'.join(path)

def move_files():
    for count, (subdir, dirs, files) in enumerate(os.walk(rootdir)):
        for file in files:
            image = os.path.join(subdir, file)
            p = Path(image)
            if new_path := clean_name(image, count):
                p.rename(new_path)
        if subdir != rootdir and REMOVE_DIR: 
            os.rmdir(subdir)

  
if __name__ == "__main__":
    move_files()