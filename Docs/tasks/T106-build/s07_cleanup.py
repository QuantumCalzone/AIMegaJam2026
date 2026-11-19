"""T106 step 7: delete the old set assets that nothing references any more (after the level is
saved with the new house). Lists what it keeps, and why. DRY_RUN first."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, t106lib
importlib.reload(t106lib)
from t106lib import *

DRY_RUN = True
CANDIDATES = [SET + '/' + n for n in ('SM_Chandelier', 'SM_Cherub', 'SM_TheaterBox', 'M_Chandelier', 'M_Cherub', 'M_TheaterBox',
                                      'T_Chandelier_BaseColor', 'T_Cherub_BaseColor', 'T_TheaterBox_BaseColor')]
CANDIDATES += [MATS + '/' + n for n in ('MI_Clay_AudRose', 'MI_Clay_AudPlum', 'MI_Clay_AudMustard', 'MI_Clay_AudBrick',
                                        'MI_Clay_AudLilac', 'MI_Theater_Gunmetal', 'MI_Clay_Black', 'MI_Clay_Knit', 'MI_Clay_Denim')]
CANDIDATES += ['/Game/NHOS/Stage/Headpieces/' + n for n in ('SM_TopHat', 'SM_Fedora', 'SM_Beanie')]
# order matters: meshes before their materials, materials before their textures


def referencers(path):
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    o = unreal.AssetRegistryDependencyOptions(include_soft_package_references=True, include_hard_package_references=True,
                                              include_searchable_names=False, include_soft_management_references=False,
                                              include_hard_management_references=False)
    return [str(x) for x in (ar.get_referencers(path, o) or []) if str(x) != path]


def go():
    res = {'deleted': [], 'kept': {}}
    for p in CANDIDATES:
        if not EAL.does_asset_exist(p):
            continue
        r = [x for x in referencers(p) if x not in res['deleted']]
        if r:
            res['kept'][p] = r
            continue
        if not DRY_RUN:
            EAL.delete_asset(p)
        res['deleted'].append(p)
    res['dry_run'] = DRY_RUN
    return res


run('s07_cleanup', go)
