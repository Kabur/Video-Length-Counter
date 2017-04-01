import os
import subprocess
from pathlib import Path

os.chdir(os.environ["PROGRAMFILES"] + "\\mediainfo")
from MediaInfoDLL3 import MediaInfo, Stream

MI = MediaInfo()


def get_length(path, recursive=False, mode=1):
    sum = 0
    for thing in os.listdir(path):
        # if its a file
        if os.path.isfile(path + thing):
            MI.Open(path + thing)
            if mode is 1:
                duration = MI.Get(Stream.Video, 0, "Duration")
            if mode is 2:
                duration = MI.Get(Stream.Audio, 0, "Duration")
            try:
                sum += int(duration)
                print("added duration {0} from file: {1}".format(int(duration), path + thing))
            except ValueError:
                print("Skipping a file: " + path + thing)
            MI.Close()

        # if its a dir
        elif os.path.isdir(path + thing):
            if recursive:
                print("diving into: " + thing)
                sum += get_length(path + thing + "\\", True)
            else:
                print("Skipping a folder: " + path + thing)
        else:
            print("Skipping a thing: " + path + thing)

    return sum

root_path = input("Type the root path: ")
# root_path = "E:\Movies - Watched\\"
ms = get_length(root_path + "\\", True)
days, ms = divmod(ms, 1000 * 60 * 60 * 24)
hours, ms = divmod(ms, 1000 * 60 * 60)
minutes, ms = divmod(ms, 1000 * 60)
seconds = ms // 1000

print("Length: {0}:{1}:{2}:{3}".format(days, hours, minutes, seconds))


# manually format the time
# days = ms // (1000 * 60 * 60 * 24)
# ms %= 1000 * 60 * 60 * 24
# hours = ms // (1000 * 60 * 60)
# ms %= 1000 * 60 * 60
# minutes = ms // (1000 * 60)
# ms %= 1000 * 60
# seconds = ms // 1000


# def get_length(filename):
#     result = subprocess.Popen(["ffprobe", filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#
#     return [x for x in result.stdout.readlines() if "Duration" in x]
#
# root = os.getcwd()
# path = Path(root)
#
#
# # for dir in path.iterdir():
# #     if dir.is_dir():
# #         print(dir)
# #
# path2 = Path(root + "\\folder")
# print(path2)
#
# print(list(path2.glob('*')))
#
# for thing in list(path2.glob('*')):
#     print(thing)
#     if thing.is_file():
#         print(thing.stat().st_size)
#         print(thing.stat().st_mtime)
#         print("Length: ", get_length(thing))
