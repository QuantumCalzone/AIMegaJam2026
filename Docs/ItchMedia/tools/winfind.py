"""Finds a top-level window of one process by its title, for ffmpeg's gfxcapture (hwnd=...).

    python Docs/ItchMedia/tools/winfind.py <pid> [title regex]

Prints one line per match: hwnd, client size, title. Matching by PID keeps other editors' PIE windows
(which have the same title) out of the recording.
"""
import ctypes
import ctypes.wintypes as wt
import re
import sys

user32 = ctypes.windll.user32
try:
    user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))  # per-monitor v2: real pixel sizes
except Exception:
    pass


def windows(pid, pattern=""):
    rx = re.compile(pattern)
    found = []

    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(hwnd, _):
        if not user32.IsWindowVisible(hwnd):
            return True
        p = wt.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
        if p.value != pid:
            return True
        n = user32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(n + 1)
        user32.GetWindowTextW(hwnd, buf, n + 1)
        if rx.search(buf.value):
            r = wt.RECT()
            user32.GetClientRect(hwnd, ctypes.byref(r))
            found.append((hwnd, r.right - r.left, r.bottom - r.top, buf.value))
        return True

    user32.EnumWindows(cb, 0)
    return found


if __name__ == "__main__":
    for hwnd, w, h, title in windows(int(sys.argv[1]), sys.argv[2] if len(sys.argv) > 2 else ""):
        print(f"{hwnd}\t{w}x{h}\t{title}")
