import subprocess

from tqdm import tqdm
from utils.constants import FARIO_CMD_TEMPLATE

from utils.db import get_follows, store_follow


def get_follows_for_fid_from_hub(fid: int, n: int = 5):
    cmd = FARIO_CMD_TEMPLATE.format(fid, n)

    # Execute the command
    process = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print("Error executing command:", stderr.decode())
        return None

    lines = stdout.decode().split("\n")

    ret = []
    for line in lines:
        try:
            line = int(line)
            ret = ret + [line]
        except ValueError:
            pass

    return ret


# to save time while investigating, this code skips over fid's it has seen already
# to flush the data, simply start over by deleting the db file (stored in `data/*.db`)
def store_follows_for_fid(fid: int):
    known = get_follows(fid)
    if len(known) == 0:
        lines = get_follows_for_fid_from_hub(fid, 5000)
        for line in tqdm(lines, desc=str(fid), leave=False):
            store_follow(fid, line)


def store_follows_for_fid_range(start: int, end: int):
    for fid in tqdm(list(range(start, end + 1)), desc="traversing fids", leave=True):
        store_follows_for_fid(fid)


if __name__ == "__main__":
    # @dwr.eth follows @vrypan.eth, the creator of fario-py
    store_follow(3, 280)
    store_follow(280, 3)  # @vrypan.eth follows @dwr.eth
    store_follow(3, 2)  # @dwr.eth follows @v
    store_follows_for_fid(37)  # @balajis.eth

    # network currently has >310k fids, not 20k
    store_follows_for_fid_range(1, 20000)
