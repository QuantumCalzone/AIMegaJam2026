"""Runs when the editor starts: the Python Script Plugin runs Content/Python/init_unreal.py.

Keep it small: each feature lives in its own module here and registers itself.
"""

import unreal

if not unreal.is_running_commandlet():
    import nhos_itch_deploy

    nhos_itch_deploy.register()
