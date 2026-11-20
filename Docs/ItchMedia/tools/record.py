"""Records a PIE window with its own sound, for T113's screenshots and trailer.

Run from the repo root while a second editor (started from the same checkout, with
-ModelContextProtocolPort=<port>) plays PIE in a floating 1920 x 1080 window:

    python Docs/ItchMedia/tools/record.py --pid <editor pid> --port <mcp port> --name <clip> [--seconds 10]

Without --seconds it records until the file Saved/ItchMedia/<clip>.stop exists (touch it from another
shell, or let a play script create it). It writes, under Saved/ItchMedia/ (out of git):

    <clip>.video.mkv   the picture only, H.264 (NVENC), every frame stamped with the wall clock
    <clip>.wav         the game's own sound, from the PIE world's main submix (ue_audio.py)
    <clip>.mp4         both together, lined up by the two clocks: the clip to cut from

How the two line up: ffmpeg's gfxcapture (Windows Graphics Capture) grabs the PIE window by its HWND, so
other windows over it don't matter and no other editor's PIE window gets in. setpts=RTCTIME stamps each
frame with the wall clock, and ue_audio.py writes time.time() when it starts the submix recording. The
difference between the first frame and the sound's start becomes the sound's -itsoffset.

The PIE window: the editor's PlayIn settings (Editor > Level Editor > Play) set its size and place; this
script sets them to 1920 x 1080 before you start PIE if you pass --setup. The window's own frame
(Unreal draws it) is cropped off: the game's picture is at x 3, y 36 inside it.
"""
import argparse
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mcp import Mcp  # noqa: E402
from winfind import windows  # noqa: E402

FFMPEG = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Links\ffmpeg.exe")
FFPROBE = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Links\ffprobe.exe")
CROP = "crop=1920:1080:3:36"  # the game's picture inside Unreal's own window frame


def setup_pie(m, x=1440, y=80):
    t = "ConfigSettingsToolset.ConfigSettingsToolset"
    sec = {"containerName": "Editor", "categoryName": "LevelEditor", "sectionName": "PlayIn"}
    m.call(t, "SetSectionProperties", {**sec, "propertiesJson": json.dumps({
        "newWindowWidth": 1920, "newWindowHeight": 1080, "centerNewWindow": False,
        "newWindowPosition": {"x": x, "y": y}})})


def pie_hwnd(pid):
    found = windows(pid, r"Preview \[NetMode")
    if not found:
        raise SystemExit(f"no PIE window for PID {pid}: start PIE in a floating window first")
    hwnd, w, h, _ = found[0]
    if (w, h) != (1926, 1120):
        print(f"warning: the PIE window is {w} x {h}, not 1926 x 1120; check the crop ({CROP})")
    return hwnd


def first_pts(path):
    out = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-read_intervals", "%+#1",
                          "-show_entries", "frame=pts_time", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout.split()
    return float(out[0])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pid", type=int, required=True, help="the second editor's process id")
    ap.add_argument("--port", type=int, default=8031)
    ap.add_argument("--name", required=True)
    ap.add_argument("--seconds", type=float, default=0, help="0: until Saved/ItchMedia/<name>.stop exists")
    ap.add_argument("--out", default=os.path.join("Saved", "ItchMedia"))
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--setup", action="store_true", help="only set the PIE window to 1920 x 1080, then exit")
    a = ap.parse_args()

    m = Mcp(a.port)
    if a.setup:
        setup_pie(m)
        print("PIE window set to 1920 x 1080; start PIE in a floating window (PlayMode_InEditorFloating)")
        return
    out = os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    video = os.path.join(out, f"{a.name}.video.mkv")
    wav = os.path.join(out, f"{a.name}.wav")
    final = os.path.join(out, f"{a.name}.mp4")
    stop_file = os.path.join(out, f"{a.name}.stop")
    for p in (video, wav, final, stop_file):
        if os.path.exists(p):
            os.remove(p)

    hwnd = pie_hwnd(a.pid)
    base = int(time.time()) - 5          # whole seconds; frame pts are seconds since this
    graph = (f"gfxcapture=hwnd={hwnd}:capture_cursor=0:max_framerate={a.fps},hwdownload,format=bgra,{CROP},"
             f"settb=1/1000000,setpts=RTCTIME-{base * 1000000}")
    # -copyts keeps the wall-clock stamps (ffmpeg would rebase the input to 0); -bf 0 keeps DTS simple.
    ff = subprocess.Popen([FFMPEG, "-hide_banner", "-loglevel", "warning", "-y", "-copyts", "-f", "lavfi", "-i", graph,
                           "-fps_mode", "passthrough", "-c:v", "h264_nvenc", "-preset", "p5", "-tune", "hq",
                           "-rc", "vbr", "-cq", "17", "-b:v", "0", "-bf", "0", "-pix_fmt", "yuv420p", video],
                          stdin=subprocess.PIPE)
    time.sleep(1.5)
    audio_py = os.path.join(HERE, "ue_audio.py").replace("\\", "/")
    outs = out.replace("\\", "/")
    m.py(f'{audio_py}" "start" "{outs}" "{a.name}')
    print(f"recording {a.name}: " + (f"{a.seconds:g} s" if a.seconds else f"until {stop_file} exists"))
    t0 = time.time()
    while (time.time() - t0 < a.seconds) if a.seconds else not os.path.exists(stop_file):
        if ff.poll() is not None:
            raise SystemExit("ffmpeg stopped early")
        time.sleep(0.2)
    m.py(f'{audio_py}" "stop" "{outs}" "{a.name}')
    time.sleep(0.5)
    ff.communicate(b"q")

    for _ in range(100):  # the wav is written on a background task
        if os.path.exists(wav) and os.path.getsize(wav) > 44:
            break
        time.sleep(0.2)
    else:
        raise SystemExit(f"no sound file at {wav}: check the editor log for T113 AUDIO and LogPython errors")
    with open(os.path.join(out, f"{a.name}.start.json"), encoding="utf-8") as f:
        audio_start = json.load(f)["time"] - base
    video_start = first_pts(video)
    offset = audio_start - video_start
    # The cut list (cut.py) needs the same number: the sound's 0 is this far into the picture.
    with open(os.path.join(out, f"{a.name}.sync.json"), "w", encoding="utf-8") as f:
        json.dump({"video": os.path.basename(video), "wav": os.path.basename(wav), "audio_offset": offset}, f)
    # The review copy: only the stretch that has both, at a constant 60 fps (the capture's rate varies).
    subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", video,
                    "-itsoffset", f"{offset:.4f}", "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-ss", f"{max(offset, 0):.4f}", "-shortest", "-fps_mode", "cfr", "-r", str(a.fps),
                    "-c:v", "h264_nvenc", "-preset", "p5", "-cq", "18", "-b:v", "0", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", final], check=True)
    print(f"wrote {final} (sound starts {offset:+.3f} s after the first frame; trimmed to where both run)")


if __name__ == "__main__":
    main()
