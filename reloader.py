from datetime import datetime
import os
import time


def get_size(start_path="."):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            if f.endswith(".txt"):
                continue
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


prev_size = get_size()


while True:
    try:
        size = get_size()

        if size != prev_size:
            prev_size = size

            f = open("terminate.txt", "w")
            f.write("1")
            f.close()

            print(datetime.now())

            # time.sleep(0.5)

            # os.system("python ./gui.py")

            # os.system("python gui.py")

        time.sleep(0.1)
    except:
        print("Error")
        time.sleep(0.1)
