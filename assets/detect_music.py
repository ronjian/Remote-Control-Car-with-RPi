import os
from shutil import copy2

def greedy_seek(path, dst):
    """greedy search all music files under search path, 
    and copy all found to the destination path
    
    :param path: search path
    :param dst: destination path
    """
    for x in os.listdir(path):
        if os.path.isdir(path + x):
            greedy_seek(path + x + "/" )
        else:
            if x.endswith('.mp3') or x.endswith('.wma') or x.endswith('.m4a'): 
                print(path + x)
                copy2(path + x, dst)

# my case
path = "/Volumes/XiaoMi/音乐/Music/"
dst = "/Users/user/Desktop/music/"
greedy_seek(path)