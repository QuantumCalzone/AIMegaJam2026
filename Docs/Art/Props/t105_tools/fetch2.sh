#!/bin/bash
B="https://file.hyper3d.com/assets/rodin/$2/pack"
Q="X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Content-Sha256=UNSIGNED-PAYLOAD&X-Tos-Credential=<the X-Tos-Credential from a signed URL>.hyper3d.com%2Ftos%2Frequest&X-Tos-Date=$3&X-Tos-Expires=604800&X-Tos-SignedHeaders=host"
F="$B/fbx/base_basic_pbr.fbx?response-cache-control=private&response-content-type=application%2Fvnd.autodesk.fbx&response-content-disposition=attachment%3B%20filename%3D%22base_basic_pbr.fbx%22&$Q&X-Tos-Signature=$4"
Q2="${Q/$3/${6:-$3}}"
T="$B/texture/basic/texture_diffuse.png?response-cache-control=private&response-content-type=image%2Fpng&response-content-disposition=attachment%3B%20filename%3D%22texture_diffuse.png%22&$Q2&X-Tos-Signature=$5"
exec "$(dirname "$0")/fetch.sh" "$1" "$F" "$T"
