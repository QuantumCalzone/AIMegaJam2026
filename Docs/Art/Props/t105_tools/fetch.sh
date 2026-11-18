#!/bin/bash
# fetch.sh <prop> <fbx url> <diffuse url>: downloads into scratch/dl/<prop>/, converts, renders
S=/private/tmp/claude-502/-Users-personal-Projects-AIMegaJam2026/40a040f7-078e-4213-bdcf-d79e6c2dc028/scratchpad/t105
D=$S/dl/$1; mkdir -p $D
curl -s -o $D/model.fbx "$2" && curl -s -o $D/texture_diffuse.png "$3"
cd $S && python3 fbx2obj.py $D/model.fbx $D/model.obj $D/texture_diffuse.png $D/mesh_stats.json >/dev/null && ./render $D/model.obj $D/turntable.png $D/thumbnail.png && ls -la $D | awk '{print $5, $9}' | tr '\n' ' '; echo; cat $D/mesh_stats.json | tr -d '\n '; echo
