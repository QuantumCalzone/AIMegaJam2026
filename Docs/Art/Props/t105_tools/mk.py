import json,sys
# mk.py out.json date "prop id sig" ...
out, date = sys.argv[1], sys.argv[2]
rows=[]
for s in sys.argv[3:]:
    p,i,g = s.split()
    rows.append([p,i,f"https://file.hyper3d.com/custom-upload/{i}/incoming?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Content-Sha256=UNSIGNED-PAYLOAD&X-Tos-Credential=<the X-Tos-Credential from a signed URL>.hyper3d.com%2Ftos%2Frequest&X-Tos-Date={date}&X-Tos-Expires=3600&X-Tos-SignedHeaders=host&X-Tos-Signature={g}"])
json.dump(rows,open(out,"w"))
