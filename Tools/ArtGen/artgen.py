#!/usr/bin/env python3
"""Take 37 art production flow: concept image -> your approval -> 3D model.

Stage 1  concept   Generate concept images with local Flux (free, runs in your ComfyUI).
Stage 1b revise    Change the look: add notes and regenerate, or edit an existing concept (img2img).
Stage 2  approve   You pick the concept that becomes the source of truth. Nothing is sent to a 3D service before this.
Stage 3  model     Send ONLY the approved image to Meshy, Hyper3D Rodin and/or Tripo through ComfyUI partner nodes.
         rig       Optional: rig the Meshy result (Meshy's rig includes basic walk and run clips).

Everything is stdlib Python. ComfyUI is started automatically when it is not running.

Usage (run from the repo root):
  python Tools/ArtGen/artgen.py concept brick                      # 4 options for one character
  python Tools/ArtGen/artgen.py concept all
  python Tools/ArtGen/artgen.py revise brick --notes "bigger hat, red bandana, less buff"
  python Tools/ArtGen/artgen.py revise brick --notes "make the vest green" --edit r001_2   # tweak a specific image
  python Tools/ArtGen/artgen.py styles brick                      # 10 different art styles for one character
  python Tools/ArtGen/artgen.py approve brick r002_3
  python Tools/ArtGen/artgen.py status
  python Tools/ArtGen/artgen.py model brick --provider all --yes   # spends partner API credits
  python Tools/ArtGen/artgen.py rig brick --yes
  python Tools/ArtGen/artgen.py --set props concept hero_camera    # same flow for set pieces

The 3D stage needs a Comfy.org API key (partner nodes bill credits to that account). Put it in the environment
variable COMFY_API_KEY or in Tools/ArtGen/.comfy_api_key (git ignores that file). It is never printed or logged.
"""
import argparse
import base64
import html
import io
import json
import mimetypes
import os
import random
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
OUT_ROOT = REPO / "Art" / "Generated"
COMFY_URL = os.environ.get("COMFY_URL", "http://127.0.0.1:8188")
COMFY_DIR = Path(os.environ.get("COMFY_DIR", str(Path.home() / "ComfyUI")))
CKPT = os.environ.get("ARTGEN_CKPT", "flux1-schnell-fp8.safetensors")
VARIATIONS = 4
SIZE = (896, 1152)

PROVIDERS = ("meshy", "rodin", "tripo")

# Art-direction options for the "styles" command: one concept per style so you can compare looks side by side.
POSE = ("full body, standing in a neutral A-pose with arms slightly away from the body and legs shoulder width apart, "
        "front view, plain light grey studio background, soft even lighting, no shadows on the ground, "
        "game character concept art, a single character, centered")
STYLES = [
    ("Pixar 3D", "glossy Pixar-style 3D animated movie character, soft subsurface skin, big expressive eyes, polished and warm"),
    ("Claymation", "handmade claymation plasticine character in the style of Aardman stop-motion, visible thumbprints and clay texture"),
    ("Low Poly", "low-poly faceted 3D game character with flat shaded triangles and a limited saturated palette"),
    ("Cel Shaded", "cel-shaded Saturday-morning cartoon character, thick black outlines, flat bold colors, exaggerated proportions"),
    ("Vinyl Toy", "collectible designer vinyl toy figure, smooth glossy plastic, chunky simplified shapes, big head, tiny hands"),
    ("Rubber Hose 1930s", "1930s rubber-hose vintage cartoon character, pie-cut eyes, noodle limbs, white gloves, black-and-cream palette with spot color"),
    ("Felt Puppet", "hand-sewn felt and fabric puppet character, stitched seams, fuzzy textures, button eyes, Muppet-like"),
    ("Storybook Paint", "painterly children's storybook illustration character, gouache brush strokes, warm textured paper feel, whimsical"),
    ("Anime", "stylized Japanese anime character design rendered as a clean 3D model, sharp eyes, detailed hair, crisp shading"),
    ("Blocky Brick Toy", "chunky blocky plastic brick-toy minifigure style character, rounded cylinder head, simple printed face, snap-together parts"),
]


# ----------------------------------------------------------------------------- ComfyUI plumbing

def http(method, path, data=None, headers=None, timeout=60):
    req = urllib.request.Request(COMFY_URL + path, data=data, method=method, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def comfy_up():
    try:
        http("GET", "/system_stats", timeout=3)
        return True
    except Exception:
        return False


def ensure_comfy():
    if comfy_up():
        return
    py = COMFY_DIR / ".venv" / "Scripts" / "python.exe"
    if not py.exists():
        py = COMFY_DIR / ".venv" / "bin" / "python"
    if not py.exists():
        sys.exit(f"ComfyUI not running at {COMFY_URL} and no install found at {COMFY_DIR}. Set COMFY_DIR.")
    print("Starting ComfyUI...")
    subprocess.Popen([str(py), "main.py", "--port", "8188"], cwd=str(COMFY_DIR),
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(90):
        time.sleep(2)
        if comfy_up():
            return
    sys.exit("ComfyUI did not start in time.")


def queue(prompt, extra_data=None):
    body = {"prompt": prompt, "client_id": str(uuid.uuid4())}
    if extra_data:
        body["extra_data"] = extra_data
    try:
        out = http("POST", "/prompt", json.dumps(body).encode(), {"Content-Type": "application/json"})
    except urllib.error.HTTPError as e:
        sys.exit("ComfyUI rejected the workflow:\n" + e.read().decode(errors="replace")[:3000])
    return json.loads(out)["prompt_id"]


def wait(prompt_id, timeout=1800):
    start = time.time()
    while time.time() - start < timeout:
        hist = json.loads(http("GET", f"/history/{prompt_id}"))
        if prompt_id in hist:
            h = hist[prompt_id]
            status = h.get("status", {})
            if status.get("status_str") == "error":
                msgs = [m for m in status.get("messages", []) if m and m[0] == "execution_error"]
                detail = msgs[-1][1].get("exception_message", "") if msgs else ""
                sys.exit("Generation failed: " + detail[:800])
            if h.get("outputs") or status.get("completed"):
                return h
        time.sleep(3)
    sys.exit("Timed out waiting for ComfyUI.")


def fetch(info, dest):
    q = urllib.parse.urlencode({"filename": info["filename"], "subfolder": info.get("subfolder", ""), "type": info.get("type", "output")})
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(http("GET", "/view?" + q, timeout=300))


def upload_image(path):
    boundary = uuid.uuid4().hex
    name = f"artgen_{uuid.uuid4().hex[:8]}_{path.name}"
    ctype = mimetypes.guess_type(path.name)[0] or "image/png"
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{name}\"\r\n"
            f"Content-Type: {ctype}\r\n\r\n").encode() + path.read_bytes() + (
            f"\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue\r\n--{boundary}--\r\n").encode()
    out = http("POST", "/upload/image", body, {"Content-Type": f"multipart/form-data; boundary={boundary}"})
    return json.loads(out)["name"]


# ----------------------------------------------------------------------------- state

def load_manifest(set_name):
    return json.loads((HERE / f"{'cast' if set_name == 'cast' else set_name}.json").read_text(encoding="utf-8"))


def item_dir(set_name, item):
    return OUT_ROOT / set_name / item


def load_state(set_name, item):
    p = item_dir(set_name, item) / "state.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"rounds": [], "approved": None, "models": {}}


def save_state(set_name, item, state):
    d = item_dir(set_name, item)
    d.mkdir(parents=True, exist_ok=True)
    (d / "state.json").write_text(json.dumps(state, indent=2), encoding="utf-8")
    write_review(set_name)


def build_prompt(manifest, item, notes):
    spec = manifest["items"][item]
    parts = [spec["description"], manifest["style"]]
    if notes:
        parts.insert(1, "Important changes: " + "; ".join(notes))
    return ", ".join(parts)


# ----------------------------------------------------------------------------- stage 1: concepts

def concept_workflow(prompt_text, seed, batch, prefix, source_image=None, denoise=0.62):
    wf = {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CKPT}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt_text, "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": "", "clip": ["1", 1]}},
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["4", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage", "inputs": {"images": ["6", 0], "filename_prefix": prefix}},
    }
    ks = {"model": ["1", 0], "seed": seed, "steps": 4, "cfg": 1.0, "sampler_name": "euler",
          "scheduler": "simple", "positive": ["2", 0], "negative": ["3", 0], "denoise": 1.0}
    if source_image:
        wf["8"] = {"class_type": "LoadImage", "inputs": {"image": source_image}}
        wf["9"] = {"class_type": "ImageScale", "inputs": {"image": ["8", 0], "upscale_method": "lanczos",
                                                           "width": SIZE[0], "height": SIZE[1], "crop": "center"}}
        wf["10"] = {"class_type": "VAEEncode", "inputs": {"pixels": ["9", 0], "vae": ["1", 2]}}
        wf["11"] = {"class_type": "RepeatLatentBatch", "inputs": {"samples": ["10", 0], "amount": batch}}
        ks["latent_image"] = ["11", 0]
        ks["denoise"] = denoise
    else:
        wf["5"] = {"class_type": "EmptyLatentImage", "inputs": {"width": SIZE[0], "height": SIZE[1], "batch_size": batch}}
        ks["latent_image"] = ["5", 0]
    wf["4"] = {"class_type": "KSampler", "inputs": ks}
    return wf


def run_round(set_name, item, notes, edit_from=None):
    manifest = load_manifest(set_name)
    if item not in manifest["items"]:
        sys.exit(f"Unknown {set_name} item '{item}'. Known: {', '.join(manifest['items'])}")
    state = load_state(set_name, item)
    d = item_dir(set_name, item)
    idx = len(state["rounds"]) + 1
    all_notes = []
    for r in state["rounds"]:
        all_notes += r.get("notes", [])
    all_notes += notes
    prompt_text = build_prompt(manifest, item, all_notes)
    seed = random.randint(1, 2**31 - 1)

    source = None
    if edit_from:
        src = d / "concepts" / f"{edit_from}.png"
        if not src.exists():
            sys.exit(f"No such concept: {src}")
        ensure_comfy()
        source = upload_image(src)
    ensure_comfy()
    prefix = f"artgen/{set_name}_{item}_r{idx:03d}"
    pid = queue(concept_workflow(prompt_text, seed, VARIATIONS, prefix, source))
    print(f"[{item}] round {idx}: generating {VARIATIONS} options{' (editing ' + edit_from + ')' if edit_from else ''}...")
    hist = wait(pid)
    files = []
    n = 0
    for out in hist["outputs"].values():
        for img in out.get("images", []):
            n += 1
            name = f"r{idx:03d}_{n}.png"
            fetch(img, d / "concepts" / name)
            files.append(name)
    state["rounds"].append({"round": idx, "notes": notes, "edit_from": edit_from, "seed": seed,
                            "prompt": prompt_text, "files": files,
                            "time": datetime.now(timezone.utc).isoformat()})
    save_state(set_name, item, state)
    print(f"[{item}] saved: " + ", ".join(files))
    print(f"  review page: {OUT_ROOT / set_name / 'review.html'}")


def cmd_concept(a):
    manifest = load_manifest(a.set)
    items = list(manifest["items"]) if a.item == "all" else [a.item]
    for it in items:
        run_round(a.set, it, [])


def cmd_styles(a):
    """One concept per art style, all in one round, so you can pick the look that makes the most sense."""
    manifest = load_manifest(a.set)
    items = list(manifest["items"]) if a.item == "all" else [a.item]
    chosen = [int(x) for x in a.only.split(",")] if a.only else list(range(1, min(a.count, len(STYLES)) + 1))
    per = max(1, a.per)
    jobs = [(n, STYLES[n - 1]) for n in chosen for _ in range(per)]
    count = len(jobs)
    ensure_comfy()
    for it in items:
        if it not in manifest["items"]:
            sys.exit(f"Unknown {a.set} item '{it}'.")
        state = load_state(a.set, it)
        d = item_dir(a.set, it)
        idx = len(state["rounds"]) + 1
        desc = manifest["items"][it]["description"]
        files, labels = [], {}
        for k, (sn, (style_name, style_text)) in enumerate(jobs, 1):
            n = k
            prompt_text = f"{desc}, {style_text}, {POSE}"
            seed = random.randint(1, 2**31 - 1)
            print(f"[{it}] {n}/{count}: {style_name}...")
            pid = queue(concept_workflow(prompt_text, seed, 1, f"artgen/{a.set}_{it}_r{idx:03d}_s{n:02d}"))
            hist = wait(pid)
            for out in hist["outputs"].values():
                for img in out.get("images", []):
                    name = f"r{idx:03d}_{n}.png"
                    fetch(img, d / "concepts" / name)
                    files.append(name)
                    labels[name] = style_name
                    break
        state["rounds"].append({"round": idx, "notes": ["style exploration"], "edit_from": None, "seed": None,
                                "prompt": "per-style prompts", "files": files, "labels": labels,
                                "time": datetime.now(timezone.utc).isoformat()})
        save_state(a.set, it, state)
        print(f"[{it}] saved {len(files)} styles in round {idx}")
    print(f"review page: {OUT_ROOT / a.set / 'review.html'}")


def cmd_revise(a):
    if not a.notes:
        sys.exit("revise needs --notes \"what to change\"")
    run_round(a.set, a.item, [n.strip() for n in a.notes.split(";") if n.strip()], a.edit)


def cmd_approve(a):
    d = item_dir(a.set, a.item)
    src = d / "concepts" / f"{a.image}.png"
    if not src.exists():
        sys.exit(f"No such concept: {src}")
    state = load_state(a.set, a.item)
    shutil.copy2(src, d / "approved.png")
    state["approved"] = {"image": a.image, "time": datetime.now(timezone.utc).isoformat()}
    save_state(a.set, a.item, state)
    print(f"Approved {a.item}: {a.image}. 3D generation can now run: artgen.py model {a.item} --provider all --yes")


def cmd_status(a):
    manifest = load_manifest(a.set)
    for it, spec in manifest["items"].items():
        st = load_state(a.set, it)
        rounds = len(st["rounds"])
        appr = st["approved"]["image"] if st["approved"] else "-"
        models = ", ".join(f"{p}:{len(v)}" for p, v in st["models"].items()) or "-"
        print(f"{it:14s} {spec['name']:34s} rounds={rounds:2d} approved={appr:8s} models={models}")
    print(f"\nreview page: {OUT_ROOT / a.set / 'review.html'}")


# ----------------------------------------------------------------------------- stage 3: 3D models

def api_key():
    key = os.environ.get("COMFY_API_KEY", "").strip()
    if not key:
        f = HERE / ".comfy_api_key"
        if f.exists():
            key = f.read_text().strip()
    if not key:
        sys.exit("No Comfy.org API key. Set COMFY_API_KEY or create Tools/ArtGen/.comfy_api_key. "
                 "Meshy, Rodin and Tripo run through ComfyUI partner nodes and bill that account.")
    return key


def meshy_nodes(img, height_m, rig):
    wf = {
        "m1": {"class_type": "MeshyImageToModelNode", "inputs": {
            "model": "latest", "image": [img, 0],
            "should_remesh": "true", "should_remesh.topology": "triangle", "should_remesh.target_polycount": 30000,
            "symmetry_mode": "auto",
            "should_texture": "true", "should_texture.enable_pbr": True, "should_texture.texture_prompt": "",
            "should_texture.texture_resolution": "4k",
            "pose_mode": "A-pose", "seed": random.randint(0, 2**31 - 1), "ultra_mode": False}},
        "m2": {"class_type": "SaveGLB", "inputs": {"mesh": ["m1", 2], "filename_prefix": "artgen/meshy"}},
    }
    if rig:
        wf["m3"] = {"class_type": "MeshyRigModelNode", "inputs": {"meshy_task_id": ["m1", 1], "height_meters": height_m}}
        wf["m4"] = {"class_type": "SaveGLB", "inputs": {"mesh": ["m3", 2], "filename_prefix": "artgen/meshy_rigged"}}
    return wf


def rodin_nodes(img, pose):
    return {
        "r1": {"class_type": "Rodin3D_Gen25_Image", "inputs": {
            "images.image0": [img, 0],
            "mode": "Regular", "mode.tier": "Gen-2.5-High", "mode.polygon_count": "20K-Triangle", "mode.creative": False,
            "material": "PBR", "geometry_file_format": "glb", "seed": random.randint(0, 65535),
            "TAPose": pose}},
        "r2": {"class_type": "SaveGLB", "inputs": {"mesh": ["r1", 0], "filename_prefix": "artgen/rodin"}},
    }


def tripo_nodes(img):
    return {
        "t1": {"class_type": "TripoImageToModelNode", "inputs": {
            "image": [img, 0], "texture": True, "pbr": True, "face_limit": 30000, "quad": False}},
        "t2": {"class_type": "SaveGLB", "inputs": {"mesh": ["t1", 2], "filename_prefix": "artgen/tripo"}},
    }


def cmd_model(a, rig=False):
    d = item_dir(a.set, a.item)
    approved = d / "approved.png"
    if not approved.exists():
        sys.exit(f"{a.item} has no approved concept. Run 'approve' first; nothing is sent to 3D services without approval.")
    if not a.yes:
        sys.exit("This sends the approved image to partner 3D services and spends credits. Re-run with --yes.")
    key = api_key()
    ensure_comfy()
    manifest = load_manifest(a.set)
    height = float(manifest["items"][a.item].get("height_m", 1.75 if a.set == "cast" else 1.0))
    providers = PROVIDERS if a.provider == "all" else (a.provider,)
    state = load_state(a.set, a.item)
    for prov in providers:
        img_name = upload_image(approved)
        wf = {"img": {"class_type": "LoadImage", "inputs": {"image": img_name}}}
        if prov == "meshy":
            wf.update(meshy_nodes("img", height, rig))
        elif prov == "rodin":
            if rig:
                print("rodin: rigging is not part of this flow; skipping rig."); continue
            wf.update(rodin_nodes("img", a.set == "cast"))
        else:
            if rig:
                print("tripo: rig flow not wired yet; use --provider meshy --rig."); continue
            wf.update(tripo_nodes("img"))
        print(f"[{a.item}] {prov}{' + rig' if rig else ''}: submitting (this can take several minutes)...")
        pid = queue(wf, {"api_key_comfy_org": key})
        try:
            hist = wait(pid, timeout=3600)
        except SystemExit as e:
            print(f"[{a.item}] {prov} failed: {e}")
            continue
        saved = []
        for out in hist["outputs"].values():
            for m in out.get("3d", []) or out.get("images", []):
                suffix = Path(m["filename"]).suffix
                n = len(list((d / "models" / prov).glob("*"))) + 1 if (d / "models" / prov).exists() else 1
                name = f"{prov}_{'rigged_' if 'rigged' in m['filename'] else ''}v{n:02d}{suffix}"
                fetch(m, d / "models" / prov / name)
                saved.append(name)
        state["models"].setdefault(prov, []).extend(saved)
        save_state(a.set, a.item, state)
        print(f"[{a.item}] {prov}: saved {', '.join(saved) or 'nothing'} to {d / 'models' / prov}")


# ----------------------------------------------------------------------------- review page

def data_uri(path, max_side=640):
    """Embed the image so the review page works wherever it is opened (previews often block relative links)."""
    raw = path.read_bytes()
    mime = "image/png"
    try:
        from PIL import Image
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        im.thumbnail((max_side, max_side))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=88)
        raw, mime = buf.getvalue(), "image/jpeg"
    except Exception:
        pass
    return f"data:{mime};base64," + base64.b64encode(raw).decode()


def write_review(set_name):
    manifest = load_manifest(set_name)
    rows = []
    for it, spec in manifest["items"].items():
        st = load_state(set_name, it)
        d = item_dir(set_name, it)
        if not st["rounds"]:
            continue
        cells = [f"<h2>{html.escape(spec['name'])} <small>{html.escape(spec['role'])}</small></h2>"]
        if st["approved"]:
            cells.append(f"<p class='ok'>Approved: {st['approved']['image']}</p>")
        for r in st["rounds"]:
            note = "; ".join(r["notes"]) or ("first pass" if r["round"] == 1 else "")
            cells.append(f"<h3>Round {r['round']} <small>{html.escape(note)}"
                         f"{' (edit of ' + r['edit_from'] + ')' if r.get('edit_from') else ''}</small></h3><div class='row'>")
            for f in r["files"]:
                stem = f[:-4]
                mark = " approved" if st["approved"] and st["approved"]["image"] == stem else ""
                cells.append(f"<figure class='{mark}'><img src='{data_uri(d / "concepts" / f)}'><figcaption><b>{html.escape(r.get('labels', {}).get(f, ''))}</b> {stem}<br>"
                             f"<code>artgen.py approve {it} {stem}</code></figcaption></figure>")
            cells.append("</div>")
        rows.append("\n".join(cells))
    page = ("<!doctype html><meta charset='utf-8'><title>Take 37 concepts</title><style>"
            "body{font-family:Georgia,serif;background:#fbf4de;color:#1c1a1f;margin:24px}"
            "h2 small,h3 small{font-weight:normal;color:#7a6f55;font-size:.7em}"
            ".row{display:flex;gap:14px;flex-wrap:wrap}figure{margin:0;background:#fff;padding:8px;border:3px solid #1c1a1f;"
            "box-shadow:6px 6px 0 #1c1a1f}figure.approved{border-color:#1a9b4d;box-shadow:6px 6px 0 #1a9b4d}"
            "img{width:300px;display:block}figcaption{font-size:.8em;text-align:center;margin-top:6px}.ok{color:#1a9b4d;font-weight:bold}"
            "</style><h1>Take 37 concept review</h1>" + "\n<hr>\n".join(rows))
    (OUT_ROOT / set_name).mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / set_name / "review.html").write_text(page, encoding="utf-8")


# ----------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--set", default="cast", choices=["cast", "props"], help="manifest to use (default: cast)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("concept"); p.add_argument("item"); p.set_defaults(fn=cmd_concept)
    p = sub.add_parser("styles"); p.add_argument("item"); p.add_argument("--count", type=int, default=10,
        help="how many styles (default 10)"); p.add_argument("--only", help="style numbers, e.g. 1,3,6")
    p.add_argument("--per", type=int, default=1, help="images per style"); p.set_defaults(fn=cmd_styles)
    p = sub.add_parser("revise"); p.add_argument("item"); p.add_argument("--notes", required=True,
        help="what to change; separate several with ;"); p.add_argument("--edit", help="edit this concept (img2img), e.g. r001_2")
    p.set_defaults(fn=cmd_revise)
    p = sub.add_parser("approve"); p.add_argument("item"); p.add_argument("image", help="e.g. r002_3"); p.set_defaults(fn=cmd_approve)
    p = sub.add_parser("status"); p.set_defaults(fn=cmd_status)
    p = sub.add_parser("model"); p.add_argument("item"); p.add_argument("--provider", default="all", choices=["all", *PROVIDERS])
    p.add_argument("--yes", action="store_true"); p.set_defaults(fn=lambda a: cmd_model(a, False))
    p = sub.add_parser("rig"); p.add_argument("item"); p.add_argument("--provider", default="meshy", choices=["meshy"])
    p.add_argument("--yes", action="store_true"); p.set_defaults(fn=lambda a: cmd_model(a, True))
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
