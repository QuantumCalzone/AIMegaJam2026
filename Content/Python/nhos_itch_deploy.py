"""Tools > itch.io in the editor's main menu (T89, T91). init_unreal.py, which the Python Script Plugin
runs when the editor starts, calls register().

main is the production branch: it holds the last release, and a release is a merge of dev into
main on the person's word ("Releases" in CLAUDE.md). So the upload ships main's tip, never dev's.

Each build entry starts Tools/deploy_itch.py in its own console window, with the engine's own
Python, and returns at once, so the editor stays usable while it builds:

- Build and upload to itch.io: packages the pushed tip of main (the last release) in the deploy
  worktree (never this folder, so unsaved or uncommitted work here is not in it), checks it for
  secrets and pushes it to the page's channel for this platform. It asks first.
- Build only (dry run of main): the same, but pushes nothing.
- Dry run of dev: packages and checks the pushed tip of dev, pushes nothing. Run it before a
  release, to see that the next release builds.
- Open the last deploy log.

Shipping anything but main's tip needs deploy_itch.py --commit by hand.

Nothing here runs in a packaged game: Content/Python is not cooked or staged.
"""

import os
import subprocess
import sys

import unreal

MENU_OWNER = "NHOS_ItchDeploy"
SECTION = "NHOS"


def _project_dir():
    return os.path.abspath(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()))


def _engine_root():
    # Engine/ is one level below the root that deploy_itch.py calls --ue-root.
    engine = os.path.abspath(unreal.Paths.convert_relative_path_to_full(unreal.Paths.engine_dir()))
    return os.path.dirname(engine.rstrip("/\\"))


def _engine_python(ue_root):
    if sys.platform == "win32":
        exe = os.path.join(ue_root, "Engine", "Binaries", "ThirdParty", "Python3", "Win64", "python.exe")
    else:
        exe = os.path.join(ue_root, "Engine", "Binaries", "ThirdParty", "Python3", "Mac", "bin", "python3")
    return exe if os.path.isfile(exe) else None


def _log_path():
    return os.path.join(_project_dir(), "Saved", "Logs", "DeployItch.log")


def launch(dry_run, commit=None):
    """Starts deploy_itch.py in its own window and returns at once. Returns the command, or None.

    commit None builds deploy_itch.py's default, origin/main (the last release).
    """
    project = _project_dir()
    ue_root = _engine_root()
    script = os.path.join(project, "Tools", "deploy_itch.py")
    python = _engine_python(ue_root)
    if python is None or not os.path.isfile(script):
        unreal.log_error(f"NHOS: DEPLOY cannot start: python={python} script={script}")
        return None
    log = _log_path()
    os.makedirs(os.path.dirname(log), exist_ok=True)
    args = [python, "-u", script, "--repo", project, "--ue-root", ue_root, "--log", log]
    if commit:
        args += ["--commit", commit]
    if dry_run:
        args.append("--dry-run")
    unreal.log(f"NHOS: DEPLOY start dry_run={dry_run} commit={commit or 'origin/main'} log={log}")
    if sys.platform == "win32":
        # A console window of its own that stays open at the end, so the result can be read.
        line = subprocess.list2cmdline(args)
        subprocess.Popen(f'cmd /c "{line} & echo. & pause"', cwd=project,
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        # Terminal on a Mac, through a small command file.
        cmd_file = os.path.join(project, "Saved", "DeployItch.command")
        with open(cmd_file, "w") as fh:
            fh.write("#!/bin/sh\ncd " + subprocess.list2cmdline([project]) + "\n"
                     + " ".join("'" + a.replace("'", "'\\''") + "'" for a in args) + "\n")
        os.chmod(cmd_file, 0o755)
        subprocess.Popen(["open", "-a", "Terminal", cmd_file])
    return args


def build_and_upload():
    answer = unreal.EditorDialog.show_message(
        "Upload to itch.io",
        "Build the last release (the tip of main on GitHub) and upload it to the itch.io page?\n\n"
        "It builds main: not dev's newer work, and not this editor's unsaved or uncommitted work. "
        "To ship newer work, release it first by merging dev into main (see Releases in CLAUDE.md). "
        "It takes a few minutes in its own window, and the editor stays usable.",
        unreal.AppMsgType.YES_NO, unreal.AppReturnType.NO)
    if answer == unreal.AppReturnType.YES:
        launch(dry_run=False)


def build_only():
    launch(dry_run=True)


def dry_run_dev():
    launch(dry_run=True, commit="origin/dev")


def open_log():
    log = _log_path()
    if not os.path.isfile(log):
        unreal.EditorDialog.show_message("itch.io deploy log", f"No deploy log yet ({log}).",
                                         unreal.AppMsgType.OK)
        return
    if sys.platform == "win32":
        os.startfile(log)
    else:
        subprocess.Popen(["open", log])


def _entry(menu, name, label, tooltip, command):
    entry = unreal.ToolMenuEntry(name=name, type=unreal.MultiBlockType.MENU_ENTRY)
    entry.set_label(label)
    entry.set_tool_tip(tooltip)
    entry.set_string_command(unreal.ToolMenuStringCommandType.PYTHON, "", command)
    menu.add_menu_entry(SECTION, entry)


def register():
    menus = unreal.ToolMenus.get()
    # extend_menu works even when the Level Editor hasn't built its Tools menu yet at startup.
    tools = menus.extend_menu("LevelEditor.MainMenu.Tools")
    if tools is None:
        unreal.log_warning("NHOS: ITCH MENU not added (no LevelEditor.MainMenu.Tools)")
        return
    sub = tools.add_sub_menu(MENU_OWNER, "", "NHOS_Itch", "itch.io", "Build the game and upload it to itch.io")
    sub.add_section(SECTION, "No Humans On Set")
    _entry(sub, "NHOS_ItchUpload", "Build and upload to itch.io",
           "Package the pushed tip of main (the last release), check it for secrets and upload it "
           "(asks first)",
           "import nhos_itch_deploy; nhos_itch_deploy.build_and_upload()")
    _entry(sub, "NHOS_ItchDryRun", "Build only (dry run of main)",
           "Package main's tip and check it for secrets, but upload nothing",
           "import nhos_itch_deploy; nhos_itch_deploy.build_only()")
    _entry(sub, "NHOS_ItchDryRunDev", "Dry run of dev",
           "Package the pushed tip of dev and check it for secrets, but upload nothing: "
           "see that the next release builds",
           "import nhos_itch_deploy; nhos_itch_deploy.dry_run_dev()")
    _entry(sub, "NHOS_ItchLog", "Open the last deploy log",
           "Saved/Logs/DeployItch.log", "import nhos_itch_deploy; nhos_itch_deploy.open_log()")
    menus.refresh_all_widgets()
    unreal.log("NHOS: ITCH MENU added (Tools > itch.io, 4 entries)")

