"""Scratch probe: where does an unprefixed open() actually start failing on this Windows host?"""

import os
import tempfile
import winreg


key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\FileSystem")
print("LongPathsEnabled =", winreg.QueryValueEx(key, "LongPathsEnabled")[0])

directory = tempfile.mkdtemp()
first_fail = None
for total in range(250, 275):
    path = os.path.join(directory, "x" * (total - len(directory) - 1))
    assert len(path) == total, (len(path), total)
    try:
        open(path, "wb").close()
        os.unlink(path)
        print("len={} open OK".format(total))
    except OSError as exc:
        winerror = getattr(exc, "winerror", None)
        print("len={} {} winerror={} {}".format(total, type(exc).__name__, winerror, exc.strerror))
        if first_fail is None:
            first_fail = total

print("FIRST FAILING LENGTH:", first_fail)
