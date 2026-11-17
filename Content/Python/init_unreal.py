"""Runs when the editor starts: the Python Script Plugin runs Content/Python/init_unreal.py.

It also runs in commandlets (the cook, -run=pythonscript), where there are no menus, so it does
nothing there. Keep it small: each feature lives in its own module here and registers itself.
"""

import unreal


def _in_commandlet():
    return "-run=" in unreal.SystemLibrary.get_command_line().lower()


if not _in_commandlet():
    try:
        import nhos_itch_deploy

        nhos_itch_deploy.register()
    except Exception as e:  # a broken menu must never stop the editor from starting
        unreal.log_warning(f"NHOS: init_unreal could not add Tools > itch.io: {e}")
