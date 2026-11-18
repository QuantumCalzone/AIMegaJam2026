import json, sys, subprocess
plan = {x["prop"]: x for x in json.load(open("plan.json"))}
ids = json.load(open("ids.json")) if __import__("os").path.exists("ids.json") else {}
for pid, uid, url in json.load(open(sys.argv[1])):
    r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "PUT", "-H", "Content-Type: application/octet-stream",
                        "--data-binary", "@" + plan[pid]["image"], url], capture_output=True, text=True)
    print(pid, r.stdout)
    ids[pid] = {"upload_id": uid}
json.dump(ids, open("ids.json", "w"), indent=1)
