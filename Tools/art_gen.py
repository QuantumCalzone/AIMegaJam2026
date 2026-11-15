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
  python Tools/art_gen.py edit --out DIR --image SRC.png --prompt "..." [--ref OTHER.png ...] [--count 2]
      Leonardo instruction edit (gemini-2.5-flash-image): changes SRC.png as the prompt says ("remove the
      hair, keep everything else") and keeps the rest, at SRC's size. --ref adds more images the prompt can
      use (a headpiece to put on, say). Saves DIR/edit_1.png ... and DIR/edit.json.
  python Tools/art_gen.py mesh-image --out DIR --name NAME --image DIR/ref.png
                                     [--polycount 5000] [--no-texture] [--model meshy-7.1]
      Meshy image to 3D (20 credits mesh only, 30 with a 2K texture). Saves DIR/NAME.fbx (its
      texture is inside), a thumbnail and DIR/meshy_image.json. --all-files also saves the GLB and
      the texture maps, into Local/art/props/<DIR name>/ (not in git).
  python Tools/art_gen.py mesh-text --out DIR --name NAME --prompt "..."
                                    [--polycount 5000] [--no-texture] [--model meshy-7.1]
      Meshy text to 3D: a preview (20 credits), then a texture refine (10 credits) unless
      --no-texture. Saves DIR/NAME_text.fbx, a thumbnail and DIR/meshy_text.json.

Batch commands, over the asset list Docs/PropArt/manifest.json (one entry per asset; see Docs/PropArt.md).
They are resumable: a step an asset already has is skipped. Each one writes its status fields (images, pick,
ref, task, credits, fbx) back into the manifest as soon as it has them.
  python Tools/art_gen.py status [--kind K]
      What each asset has so far, and the credits spent.
  python Tools/art_gen.py batch-images --kind K [--ids ID ...] [--count 4] [--parallel 3] [--force]
      Leonardo candidates for every asset with no images yet, into Local/art/props/<id>/ (not git), a few
      assets at a time. The log goes to Docs/PropArt/<id>/leonardo.json.
  python Tools/art_gen.py pick ID N [--force]
      Copies candidate N to Docs/PropArt/<id>/ref.png. --force re-picks an asset that has a model, and
      clears its model so the next batch-meshes makes it again.
  python Tools/art_gen.py batch-meshes --kind K [--ids ID ...] --max-credits C [--parallel 8] [--all-files]
      Meshy image to 3D for every asset with a ref and no fbx, up to 8 at once (Pro allows 10). Checks the
      balance first and never starts a task that would take the run past C credits (estimates: meshy-7.1
      20, meshy-6-lite 5, +10 with a texture). FBX and thumbnail into Docs/PropArt/<id>/. An asset whose
      task started but never downloaded is fetched, not paid for again.
  python Tools/art_gen.py sheet --kind K [--candidates]
      Local/art/sheet_<kind>.html: every thumbnail with its id (or, with --candidates, the four Leonardo
      candidates of each asset, numbered for pick).

Meshy keeps files for 3 days and its download links expire, so every command downloads at once.
"""
import argparse
import base64
import concurrent.futures
import html
import json
import mimetypes
import os
import shutil
import sys
import threading
import time
import uuid
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


def now():
    return time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())


# ---- Leonardo -------------------------------------------------------------------------------

def leonardo(prompt, img_dir, model, width, height, count, negative=None, label="Leonardo"):
    """One Leonardo v2 generation. Saves img_dir/candidate_N.png and returns the log entry."""
    token = key("leonardo")
    img_dir.mkdir(parents=True, exist_ok=True)
    params = {"prompt": prompt, "width": width, "height": height, "quantity": count}
    if negative:
        params["negative_prompt"] = negative
    body = {"model": model, "parameters": params, "public": False}
    res = call("POST", f"{LEO}/v2/generations", token, body)
    gen_id = find(res, "generationId")
    if not gen_id:
        sys.exit(f"No generationId in the reply: {json.dumps(res)[:400]}")
    cost = find(res, "apiCreditCost")
    print(f"{label}: Leonardo generation {gen_id} ({model}, {count} images, cost {cost})")
    for _ in range(120):
        time.sleep(5)
        got = call("GET", f"{LEO}/v1/generations/{gen_id}", token)
        g = got.get("generations_by_pk") or {}
        status = g.get("status")
        if status == "COMPLETE":
            imgs = g.get("generated_images") or []
            for i, img in enumerate(imgs, 1):
                download(img["url"], img_dir / f"candidate_{i}.png")
            return {"time": now(), "generation": gen_id, "model": model, "parameters": params,
                    "api_credit_cost": cost, "seed": g.get("seed"),
                    "images": [f"candidate_{i}.png" for i in range(1, len(imgs) + 1)]}
        if status == "FAILED":
            sys.exit(f"Leonardo generation {gen_id} failed.")
    sys.exit(f"Leonardo generation {gen_id} timed out.")


def cmd_image(a):
    out = outdir(a)
    entry = leonardo(a.prompt, out, a.model, a.width, a.height, a.count, a.negative)
    log(out, "leonardo.json", entry)


def upload_init_image(token, path):
    """Uploads a PNG to Leonardo (a presigned S3 POST, no auth header) and returns its init image id."""
    up = call("POST", f"{LEO}/v1/init-image", token, {"extension": "png"}).get("uploadInitImage") or {}
    fields = up.get("fields")
    fields = json.loads(fields) if isinstance(fields, str) else (fields or {})
    boundary = uuid.uuid4().hex
    body = b"".join(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
                    for k, v in fields.items())
    body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{Path(path).name}\"\r\n"
             f"Content-Type: image/png\r\n\r\n").encode() + Path(path).read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(up["url"], data=body, method="POST",
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=120):
        pass
    return up["id"]


def cmd_edit(a):
    """Leonardo instruction edit: the source image as a HIGH reference, any --ref images as MID ones. Width and
    height 0 keep the source's size (the model takes only a fixed list of sizes otherwise)."""
    token, out = key("leonardo"), outdir(a)
    refs = [{"image": {"id": upload_init_image(token, a.image), "type": "UPLOADED"}, "strength": "HIGH"}]
    refs += [{"image": {"id": upload_init_image(token, r), "type": "UPLOADED"}, "strength": "MID"} for r in a.ref]
    params = {"width": 0, "height": 0, "prompt": a.prompt, "quantity": a.count, "prompt_enhance": "OFF",
              "guidances": {"image_reference": refs}}
    res = call("POST", f"{LEO}/v2/generations", token,
               {"model": "gemini-2.5-flash-image", "parameters": params, "public": False})
    gen_id = find(res, "generationId")
    if not gen_id:
        sys.exit(f"No generationId in the reply: {json.dumps(res)[:400]}")
    cost = find(res, "apiCreditCost")
    print(f"Leonardo edit {gen_id} (gemini-2.5-flash-image, {a.count} images, cost {cost})")
    for _ in range(120):
        time.sleep(5)
        g = call("GET", f"{LEO}/v1/generations/{gen_id}", token).get("generations_by_pk") or {}
        if g.get("status") == "COMPLETE":
            imgs = g.get("generated_images") or []
            for i, img in enumerate(imgs, 1):
                download(img["url"], out / f"edit_{i}.png")
            log(out, "edit.json", {"time": now(), "generation": gen_id, "model": "gemini-2.5-flash-image",
                                   "source": rel(Path(a.image).resolve()), "refs": [rel(Path(r).resolve()) for r in a.ref],
                                   "prompt": a.prompt, "api_credit_cost": cost,
                                   "images": [f"edit_{i}.png" for i in range(1, len(imgs) + 1)]})
            return
        if g.get("status") == "FAILED":
            sys.exit(f"Leonardo edit {gen_id} failed.")
    sys.exit(f"Leonardo edit {gen_id} timed out.")


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
            raise TaskFailed(f"{label} {task_id} {status}: {t.get('task_error')}")
        time.sleep(5)
    sys.exit(f"{label} {task_id} timed out.")


class TaskFailed(Exception):
    """A Meshy task ended FAILED or CANCELED."""


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


def meshy_image_task(token, image, model, polycount, texture):
    """Starts a Meshy image-to-3D task. Returns its id and the request body without the image."""
    img = Path(image)
    mime = mimetypes.guess_type(img.name)[0] or "image/png"
    data_uri = f"data:{mime};base64," + base64.b64encode(img.read_bytes()).decode()
    opts = {"ai_model": model, "should_remesh": True, "topology": "triangle", "target_polycount": polycount,
            "target_formats": ["fbx", "glb"]}
    body = {"image_url": data_uri, "should_texture": texture, **opts}
    task = call("POST", f"{MESHY}/v1/image-to-3d", token, body)["result"]
    return task, {k: v for k, v in body.items() if k != "image_url"}


def cmd_mesh_image(a):
    token, out = key("meshy"), outdir(a)
    task, body = meshy_image_task(token, a.image, a.model, a.polycount, not a.no_texture)
    print(f"Meshy image to 3D {task} ({a.model}, texture {not a.no_texture})")
    t = wait_meshy(token, "v1/image-to-3d", task, "image-to-3d")
    save_meshy(t, out, a.name, a.all_files)
    log(out, "meshy_image.json", {"time": now(), "task": task, "image": Path(a.image).name,
                                  "consumed_credits": t.get("consumed_credits"), **body})
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


# ---- Batch over the asset list ------------------------------------------------------------

MANIFEST = ROOT / "Docs" / "PropArt" / "manifest.json"
PROPART = ROOT / "Docs" / "PropArt"
MESH_COST = {"meshy-7.1": 20, "meshy-7": 20, "meshy-6": 20, "meshy-6-lite": 5}
TEXTURE_COST = 10
_manifest_lock = threading.Lock()


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def save_manifest(m):
    tmp = MANIFEST.with_suffix(".tmp")
    tmp.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, MANIFEST)


def update_asset(asset_id, **fields):
    """Writes status fields into the manifest. It reloads the file first, so runs on other assets keep theirs."""
    with _manifest_lock:
        m = load_manifest()
        next(x for x in m["assets"] if x["id"] == asset_id).update(fields)
        save_manifest(m)


def select(m, kind=None, ids=None):
    known = {x["id"] for x in m["assets"]}
    for i in ids or []:
        if i not in known:
            sys.exit(f"No asset {i!r} in {rel(MANIFEST)}.")
    return [x for x in m["assets"] if (not kind or x["kind"] == kind) and (not ids or x["id"] in ids)]


def rel(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def mesh_cost(x):
    return MESH_COST.get(x["meshy_model"], 30) + (TEXTURE_COST if x["texture"] else 0)


def run_parallel(items, work, parallel):
    """Runs work(item) on a few threads. A failure stops that item only. Returns {id: result or None}."""
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, parallel)) as pool:
        futures = {pool.submit(work, x): x["id"] for x in items}
        for f in concurrent.futures.as_completed(futures):
            asset_id = futures[f]
            try:
                results[asset_id] = f.result()
            except (SystemExit, Exception) as e:
                print(f"{asset_id}: FAILED: {e}")
                results[asset_id] = None
    return results


def cmd_status(a):
    rows = select(load_manifest(), a.kind)
    for x in rows:
        step = "model" if x.get("fbx") else "picked" if x.get("ref") else "images" if x.get("images") else "-"
        extra = f" (task {x['task']} not downloaded)" if x.get("task") and not x.get("fbx") else ""
        print(f"{x['kind']:9} {x['id']:22} {step:7} {x['meshy_model']:12} credits {x.get('credits') or 0}{extra}")
    done = sum(1 for x in rows if x.get("fbx"))
    spent = sum(x.get("credits") or 0 for x in rows)
    left = sum(mesh_cost(x) for x in rows if not x.get("fbx"))
    print(f"{len(rows)} assets, {done} with a model, {spent} credits spent, about {left} to make the rest.")


def cmd_batch_images(a):
    m = load_manifest()
    todo = []
    for x in select(m, a.kind, a.ids):
        if (x.get("images") or x.get("ref")) and not a.force:
            print(f"{x['id']}: skip, has images")
        else:
            todo.append(x)

    def work(x):
        entry = leonardo(x["prompt"], EXTRAS / x["id"], m.get("leonardo_model", "lucid-origin"), 1024, 1024,
                         a.count, m.get("negative"), x["id"])
        out = PROPART / x["id"]
        out.mkdir(parents=True, exist_ok=True)
        log(out, "leonardo.json", entry)
        update_asset(x["id"], images=entry["generation"])
        return entry["generation"]

    res = run_parallel(todo, work, a.parallel)
    ok = sum(1 for v in res.values() if v)
    print(f"Images for {ok} of {len(todo)} assets, in {rel(EXTRAS)}/<id>/. Look at them, then: pick ID N")


def cmd_pick(a):
    x = select(load_manifest(), ids=[a.id])[0]
    src = EXTRAS / a.id / f"candidate_{a.n}.png"
    if not src.exists():
        sys.exit(f"No {rel(src)}. Run batch-images first.")
    if x.get("fbx") and not a.force:
        sys.exit(f"{a.id} already has a model ({x['fbx']}). Use --force to pick again and remake it.")
    dst = PROPART / a.id / "ref.png"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    fields = {"pick": a.n, "ref": rel(dst)}
    if a.force:
        fields.update(task=None, credits=None, fbx=None)
    update_asset(a.id, **fields)
    print(f"{a.id}: candidate {a.n} -> {rel(dst)}")


def balance(token):
    return call("GET", f"{MESHY}/v1/balance", token).get("balance")


def cmd_batch_meshes(a):
    token, m = key("meshy"), load_manifest()
    todo = []
    for x in select(m, a.kind, a.ids):
        if x.get("fbx"):
            print(f"{x['id']}: skip, has {x['fbx']}")
        elif not x.get("ref"):
            print(f"{x['id']}: skip, no ref yet (batch-images, then pick)")
        else:
            todo.append(x)
    before = balance(token)
    print(f"Meshy balance before: {before}. Cap for this run: {a.max_credits} credits.")
    budget = {"committed": 0}
    lock = threading.Lock()

    def work(x):
        out = PROPART / x["id"]
        if x.get("task"):
            task, body = x["task"], {"resumed": True}
            print(f"{x['id']}: resuming task {task} (already paid for)")
        else:
            est = mesh_cost(x)
            with lock:
                if budget["committed"] + est > (a.max_credits if before is None else min(a.max_credits, before)):
                    print(f"{x['id']}: not started, {est} more credits would pass the cap or the balance")
                    return None
                budget["committed"] += est
            task, body = meshy_image_task(token, ROOT / x["ref"], x["meshy_model"], x["polycount"], x["texture"])
            update_asset(x["id"], task=task)
            print(f"{x['id']}: Meshy image to 3D {task} ({x['meshy_model']}, texture {x['texture']}, about {est})")
        try:
            t = wait_meshy(token, "v1/image-to-3d", task, x["id"])
        except TaskFailed as e:
            update_asset(x["id"], task=None)  # so the next run starts it again
            raise SystemExit(str(e))
        save_meshy(t, out, x["id"], a.all_files)
        used = t.get("consumed_credits")
        log(out, "meshy_image.json", {"time": now(), "task": task, "image": "ref.png",
                                      "consumed_credits": used, **body})
        update_asset(x["id"], credits=used, fbx=rel(out / f"{x['id']}.fbx"))
        if not body.get("resumed"):
            with lock:
                budget["committed"] += (used or 0) - mesh_cost(x)
        return used or 0

    res = run_parallel(todo, work, min(a.parallel, 8))
    after = balance(token)
    made = sum(1 for v in res.values() if v is not None)
    used = sum(v or 0 for v in res.values())
    drop = before - after if before is not None and after is not None else "?"
    print(f"Made {made} of {len(todo)}. Credits in the logs: {used}. Balance after: {after} (dropped {drop}).")


def cmd_sheet(a):
    m = load_manifest()
    sheet_dir = ROOT / "Local" / "art"
    sheet_dir.mkdir(parents=True, exist_ok=True)

    def src(path):
        return html.escape(Path(path).resolve().as_uri())

    cards = []
    for x in select(m, a.kind):
        if a.candidates:
            figs = []
            for p in sorted((EXTRAS / x["id"]).glob("candidate_*.png")):
                n = int(p.stem.split("_")[1])
                figs.append(f'<figure><img src="{src(p)}"><figcaption>{n}'
                            f'{" (picked)" if x.get("pick") == n else ""}</figcaption></figure>')
            pics = "".join(figs) or "<p>no candidates yet</p>"
        else:
            thumb = PROPART / x["id"] / f"{x['id']}_thumb.png"
            ref = PROPART / x["id"] / "ref.png"
            pics = (f'<img src="{src(thumb)}">' if thumb.exists() else
                    f'<img class="ref" src="{src(ref)}"><p>ref only, no model yet</p>' if ref.exists() else
                    "<p>nothing yet</p>")
        bits = [x.get("story"), "spare" if x.get("core") is False else None, x["meshy_model"],
                f"{x['credits']} credits" if x.get("credits") else None]
        info = " · ".join(str(b) for b in bits if b)
        cards.append(f'<section><h2>{html.escape(x["id"])}</h2><p class="info">{html.escape(info)}</p>'
                     f'<div class="pics">{pics}</div></section>')
    title = f"{a.kind} {'candidates' if a.candidates else 'models'}"
    col, img = (520, 120) if a.candidates else (240, 220)
    page = f"""<!doctype html><meta charset="utf-8"><title>{title}</title>
<style>
body {{ font: 14px system-ui, sans-serif; background: #222; color: #eee; margin: 16px; }}
main {{ display: grid; grid-template-columns: repeat(auto-fill, minmax({col}px, 1fr)); gap: 12px; }}
section {{ background: #333; border-radius: 8px; padding: 8px; }}
h2 {{ font-size: 16px; margin: 0; }} .info {{ color: #aaa; margin: 2px 0 6px; }}
.pics {{ display: flex; flex-wrap: wrap; gap: 4px; }} figure {{ margin: 0; text-align: center; }}
img {{ width: {img}px; background: #ddd; border-radius: 4px; }} img.ref {{ opacity: .6; }}
</style><h1>{title} ({len(cards)})</h1><main>{"".join(cards)}</main>
"""
    out = sheet_dir / f"sheet_{a.kind}{'_candidates' if a.candidates else ''}.html"
    out.write_text(page, encoding="utf-8")
    print(f"Saved {out}")


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
    e = sub.add_parser("edit")
    e.add_argument("--out", required=True)
    e.add_argument("--image", required=True)
    e.add_argument("--prompt", required=True)
    e.add_argument("--ref", action="append", default=[])
    e.add_argument("--count", type=int, default=2)
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
    kinds = ["headpiece", "prop", "set"]
    st = sub.add_parser("status")
    st.add_argument("--kind", choices=kinds)
    bi = sub.add_parser("batch-images")
    bi.add_argument("--kind", choices=kinds, required=True)
    bi.add_argument("--ids", nargs="+")
    bi.add_argument("--count", type=int, default=4)
    bi.add_argument("--parallel", type=int, default=3)
    bi.add_argument("--force", action="store_true")
    pk = sub.add_parser("pick")
    pk.add_argument("id")
    pk.add_argument("n", type=int)
    pk.add_argument("--force", action="store_true")
    bm = sub.add_parser("batch-meshes")
    bm.add_argument("--kind", choices=kinds, required=True)
    bm.add_argument("--ids", nargs="+")
    bm.add_argument("--max-credits", type=int, required=True)
    bm.add_argument("--parallel", type=int, default=8)
    bm.add_argument("--all-files", action="store_true")
    sh = sub.add_parser("sheet")
    sh.add_argument("--kind", choices=kinds, required=True)
    sh.add_argument("--candidates", action="store_true")
    a = p.parse_args()
    try:
        {"balance": cmd_balance, "fetch": cmd_fetch, "image": cmd_image, "edit": cmd_edit, "mesh-image": cmd_mesh_image,
         "mesh-text": cmd_mesh_text, "status": cmd_status, "batch-images": cmd_batch_images, "pick": cmd_pick,
         "batch-meshes": cmd_batch_meshes, "sheet": cmd_sheet}[a.cmd](a)
    except TaskFailed as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
