"""Generate art with Leonardo.ai (images) and Meshy (3D models), standard library only.

Keys are read from Local/ (git ignores it) and never printed:
  Local/leonardo_key.json   {"key": "..."}
  Local/meshy_key.json      {"key": "..."}

Every command writes what it asked for and what it cost into a JSON log in its --out folder,
so Docs/Assets.md can say how each asset was made.

Commands:
  python Tools/art_gen.py balance
      Meshy credit balance (free call).
  python Tools/art_gen.py fetch --kind image|text|remesh --task ID --out DIR --name NAME
      Download the files of a Meshy task that already finished (free).
  python Tools/art_gen.py image --out DIR --prompt "..." [--model lucid-origin] [--width 1024]
                                [--height 1024] [--count 4] [--negative "..."]
      Leonardo v2 generation. Saves DIR/candidate_1.png ... and DIR/leonardo.json.
  python Tools/art_gen.py mesh-image --out DIR --name NAME --image DIR/ref.png
                                     [--polycount 5000] [--no-texture] [--model meshy-7.1]
      Meshy image to 3D (20 credits mesh only, 30 with a 2K texture). Saves DIR/NAME.fbx (its
      texture is inside), a thumbnail and DIR/meshy_image.json. --all-files also saves the GLB and
      the texture maps, into Local/art/props/<DIR name>/ (not in git).
  python Tools/art_gen.py mesh-text --out DIR --name NAME --prompt "..."
                                    [--polycount 5000] [--no-texture] [--model meshy-7.1]
      Meshy text to 3D: a preview (20 credits), then a texture refine (10 credits) unless
      --no-texture. Saves DIR/NAME_text.fbx, a thumbnail and DIR/meshy_text.json.

Meshy keeps files for 3 days and its download links expire, so every command downloads at once.
"""
import argparse
import base64
import json
import mimetypes
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCAL = ROOT / "Local"
UA = "nhos-art-gen/1.0"
LEO = "https://cloud.leonardo.ai/api/rest"
MESHY = "https://api.meshy.ai/openapi"


def key(name):
    p = LOCAL / f"{name}_key.json"
    if not p.exists():
        sys.exit(f"Missing {p.relative_to(ROOT)}. Put {{\"key\": \"...\"}} in it.")
    k = json.loads(p.read_text(encoding="utf-8")).get("key", "").strip()
    if not k:
        sys.exit(f"{p.relative_to(ROOT)} has no \"key\".")
    return k


def call(method, url, token, body=None, retries=4):
    data = json.dumps(body).encode() if body is not None else None
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=data, method=method, headers={
            "Authorization": f"Bearer {token}", "Accept": "application/json",
            "Content-Type": "application/json", "User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode() or "{}")
        except urllib.error.HTTPError as e:
            text = e.read().decode(errors="replace")[:500]
            if e.code == 429 and attempt < retries and "NoMorePendingTasks" not in text:
                time.sleep(float(e.headers.get("Retry-After") or 5))
                continue
            if e.code >= 500 and attempt < retries:
                time.sleep(5 * (attempt + 1))
                continue
            sys.exit(f"{method} {url.split('?')[0]} failed: HTTP {e.code}: {text}")
        except urllib.error.URLError as e:
            if attempt < retries:
                time.sleep(5 * (attempt + 1))
                continue
            sys.exit(f"{method} {url.split('?')[0]} failed: {e.reason}")


def download(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=300) as r:
        path.write_bytes(r.read())
    print(f"  saved {path} ({path.stat().st_size // 1024} KB)")


def outdir(a):
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    return out


def log(out, name, entry):
    p = out / name
    entries = json.loads(p.read_text(encoding="utf-8")) if p.exists() else []
    entries.append(entry)
    p.write_text(json.dumps(entries, indent=2), encoding="utf-8")


def find(obj, field):
    """First value of `field` anywhere in a nested JSON object."""
    if isinstance(obj, dict):
        if field in obj:
            return obj[field]
        for v in obj.values():
            hit = find(v, field)
            if hit is not None:
                return hit
    elif isinstance(obj, list):
        for v in obj:
            hit = find(v, field)
            if hit is not None:
                return hit
    return None


# ---- Leonardo -------------------------------------------------------------------------------

def cmd_image(a):
    token, out = key("leonardo"), outdir(a)
    params = {"prompt": a.prompt, "width": a.width, "height": a.height, "quantity": a.count}
    if a.negative:
        params["negative_prompt"] = a.negative
    body = {"model": a.model, "parameters": params, "public": False}
    res = call("POST", f"{LEO}/v2/generations", token, body)
    gen_id = find(res, "generationId")
    if not gen_id:
        sys.exit(f"No generationId in the reply: {json.dumps(res)[:400]}")
    cost = find(res, "apiCreditCost")
    print(f"Leonardo generation {gen_id} ({a.model}, {a.count} images, cost {cost})")
    for _ in range(120):
        time.sleep(5)
        got = call("GET", f"{LEO}/v1/generations/{gen_id}", token)
        g = got.get("generations_by_pk") or {}
        status = g.get("status")
        if status == "COMPLETE":
            imgs = g.get("generated_images") or []
            for i, img in enumerate(imgs, 1):
                download(img["url"], out / f"candidate_{i}.png")
            log(out, "leonardo.json", {"time": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
                                       "generation": gen_id, "model": a.model, "parameters": params,
                                       "api_credit_cost": cost, "seed": g.get("seed"),
                                       "images": [f"candidate_{i}.png" for i in range(1, len(imgs) + 1)]})
            return
        if status == "FAILED":
            sys.exit(f"Leonardo generation {gen_id} failed.")
    sys.exit(f"Leonardo generation {gen_id} timed out.")


# ---- Meshy ----------------------------------------------------------------------------------

def wait_meshy(token, path, task_id, label):
    last = -1
    for _ in range(360):
        t = call("GET", f"{MESHY}/{path}/{task_id}", token)
        status, prog = t.get("status"), t.get("progress", 0)
        if prog != last:
            print(f"  {label}: {status} {prog}%")
            last = prog
        if status == "SUCCEEDED":
            return t
        if status in ("FAILED", "CANCELED"):
            sys.exit(f"{label} {task_id} {status}: {t.get('task_error')}")
        time.sleep(5)
    sys.exit(f"{label} {task_id} timed out.")


EXTRAS = ROOT / "Local" / "art" / "props"


def save_meshy(t, out, stem, all_files=False):
    """FBX and thumbnail into out; with all_files, the GLB and texture maps into Local/art/props/<folder>/.
    The FBX carries its texture, so the extras are only for a re-import by hand."""
    urls = t.get("model_urls") or {}
    if urls.get("fbx"):
        download(urls["fbx"], out / f"{stem}.fbx")
    if all_files:
        extra = EXTRAS / out.name
        extra.mkdir(parents=True, exist_ok=True)
        if urls.get("glb"):
            download(urls["glb"], extra / f"{stem}.glb")
        for maps in t.get("texture_urls") or []:
            for kind, url in maps.items():
                if url:
                    download(url, extra / f"{stem}_{kind}.png")
    if t.get("thumbnail_url"):
        download(t["thumbnail_url"], out / f"{stem}_thumb.png")


def mesh_options(a):
    return {"ai_model": a.model, "should_remesh": True, "topology": "triangle",
            "target_polycount": a.polycount, "target_formats": ["fbx", "glb"]}


def cmd_mesh_image(a):
    token, out = key("meshy"), outdir(a)
    img = Path(a.image)
    mime = mimetypes.guess_type(img.name)[0] or "image/png"
    data_uri = f"data:{mime};base64," + base64.b64encode(img.read_bytes()).decode()
    body = {"image_url": data_uri, "should_texture": not a.no_texture, **mesh_options(a)}
    task = call("POST", f"{MESHY}/v1/image-to-3d", token, body)["result"]
    print(f"Meshy image to 3D {task} ({a.model}, texture {not a.no_texture})")
    t = wait_meshy(token, "v1/image-to-3d", task, "image-to-3d")
    save_meshy(t, out, a.name, a.all_files)
    log(out, "meshy_image.json", {"time": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
                                  "task": task, "image": img.name, "consumed_credits": t.get("consumed_credits"),
                                  **{k: v for k, v in body.items() if k != "image_url"}})
    print(f"Done. Credits used: {t.get('consumed_credits')}")


def cmd_mesh_text(a):
    token, out = key("meshy"), outdir(a)
    body = {"mode": "preview", "prompt": a.prompt, **mesh_options(a)}
    pre = call("POST", f"{MESHY}/v2/text-to-3d", token, body)["result"]
    print(f"Meshy text to 3D preview {pre} ({a.model})")
    t = wait_meshy(token, "v2/text-to-3d", pre, "preview")
    used = t.get("consumed_credits") or 0
    entry = {"time": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()), "preview": pre, **body}
    if not a.no_texture:
        ref = call("POST", f"{MESHY}/v2/text-to-3d", token,
                   {"mode": "refine", "preview_task_id": pre, "target_formats": ["fbx", "glb"]})["result"]
        print(f"Meshy text to 3D refine {ref}")
        t = wait_meshy(token, "v2/text-to-3d", ref, "refine")
        used += t.get("consumed_credits") or 0
        entry["refine"] = ref
    save_meshy(t, out, f"{a.name}_text", a.all_files)
    entry["consumed_credits"] = used
    log(out, "meshy_text.json", entry)
    print(f"Done. Credits used: {used}")


def cmd_fetch(a):
    """Download the files of a Meshy task that already finished (no credits)."""
    token, out = key("meshy"), outdir(a)
    path = {"image": "v1/image-to-3d", "text": "v2/text-to-3d", "remesh": "v1/remesh"}[a.kind]
    t = call("GET", f"{MESHY}/{path}/{a.task}", token)
    if t.get("status") != "SUCCEEDED":
        sys.exit(f"Task {a.task} is {t.get('status')}.")
    save_meshy(t, out, a.name, a.all_files)
    log(out, f"meshy_{a.kind}.json", {"time": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
                                      "task": a.task, "fetched": True, "consumed_credits": t.get("consumed_credits"),
                                      "prompt": t.get("prompt"), "texture_prompt": t.get("texture_prompt")})


def cmd_balance(a):
    b = call("GET", f"{MESHY}/v1/balance", key("meshy"))
    print(f"Meshy balance: {b.get('balance')} (monthly {b.get('monthly_credits')}, "
          f"permanent {b.get('permanent_credits')}, resets {b.get('monthly_resets_at')})")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("balance")
    f = sub.add_parser("fetch")
    f.add_argument("--kind", choices=["image", "text", "remesh"], required=True)
    f.add_argument("--task", required=True)
    f.add_argument("--out", required=True)
    f.add_argument("--name", required=True)
    f.add_argument("--all-files", action="store_true")
    i = sub.add_parser("image")
    i.add_argument("--out", required=True)
    i.add_argument("--prompt", required=True)
    i.add_argument("--negative")
    i.add_argument("--model", default="lucid-origin")
    i.add_argument("--width", type=int, default=1024)
    i.add_argument("--height", type=int, default=1024)
    i.add_argument("--count", type=int, default=4)
    for name in ("mesh-image", "mesh-text"):
        m = sub.add_parser(name)
        m.add_argument("--out", required=True)
        m.add_argument("--name", required=True)
        m.add_argument("--model", default="meshy-7.1")
        m.add_argument("--polycount", type=int, default=5000)
        m.add_argument("--no-texture", action="store_true")
        m.add_argument("--all-files", action="store_true")
        if name == "mesh-image":
            m.add_argument("--image", required=True)
        else:
            m.add_argument("--prompt", required=True)
    a = p.parse_args()
    {"balance": cmd_balance, "fetch": cmd_fetch, "image": cmd_image, "mesh-image": cmd_mesh_image,
     "mesh-text": cmd_mesh_text}[a.cmd](a)


if __name__ == "__main__":
    main()
