#!/usr/bin/env python3
"""Assemble the playbook HTML from curated JSON (run: python3 build.py, then wrap.py).

Inputs (relative to scratchpad):
  curated/<CAT>.json   {"id","name","intro_html","principles":[...],"plays":[...]}
  extract/<show>/*.json  episode summaries (episodes[] of each batch file)
  build/front.json     {"subtitle","how_html","method_html"}
Output:
  build/five-houses.html
"""
import json, glob, os, re, sys, html

ROOT = os.path.dirname(os.path.abspath(__file__))
CAT_ORDER = ["INT","LEV","PSY","NEG","DEC","TRAP","ALLY","TIME","RISK","POW","REP","RULE","LEAD","DEF","WAR"]

SHOWS = [
  {"id":"billions","name":"Billions","short":"Billions","span":"2016 to 2023 · 7 seasons · 84 episodes",
   "blurb":"Hedge fund king Bobby Axelrod and US Attorney Chuck Rhoades wage a war of leverage, law and money in New York."},
  {"id":"peaky-blinders","name":"Peaky Blinders","short":"Peaky","span":"2013 to 2022 · 6 series · 36 episodes",
   "blurb":"Tommy Shelby turns a Birmingham street gang into an empire, playing police, rivals, unions and Parliament against each other."},
  {"id":"vikings","name":"Vikings","short":"Vikings","span":"2013 to 2020 · 6 seasons · 89 episodes",
   "blurb":"Ragnar Lothbrok and his sons rise from farmers to kings through raids, alliances, betrayals and sieges."},
  {"id":"house-of-cards","name":"House of Cards","short":"HoC","span":"2013 to 2018 · 6 seasons · 73 episodes",
   "blurb":"Frank and Claire Underwood climb from House Majority Whip to the Oval Office by any means that work."},
  {"id":"suits","name":"Suits","short":"Suits","span":"2011 to 2019 · 9 seasons · 134 episodes",
   "blurb":"Closer Harvey Specter and fraud-genius associate Mike Ross win cases and firm wars through leverage and nerve."},
]
DASH = re.compile("[—–]")

def clean(s):
    if isinstance(s, str):
        s = DASH.sub(", ", s).replace(" ,", ",").replace(",,", ",")
        return s
    if isinstance(s, list): return [clean(x) for x in s]
    if isinstance(s, dict): return {k: clean(v) for k, v in s.items()}
    return s

def main():
    eps = json.load(open(os.path.join(ROOT, "episodes.json")))
    cats, plays = [], []
    seen = set()
    chapters = {}
    for cid in CAT_ORDER:
        f = os.path.join(ROOT, "curated", f"{cid}.json")
        if os.path.exists(f): chapters[cid] = json.load(open(f))
        else: print("missing chapter", cid, file=sys.stderr)
    # plays borrowed into another chapter are removed from their home chapter
    borrowed = {}
    for cid, c in chapters.items():
        for p in c["plays"]:
            if p.get("borrowed_from"): borrowed[p["borrowed_from"]] = cid
    for cid, c in chapters.items():
        keep = []
        for p in c["plays"]:
            ids = p.get("pool_ids") or []
            if ids and all(i in borrowed and borrowed[i] != cid for i in ids):
                print(f"drop {cid}:{p['title']} (borrowed by {borrowed[ids[0]]})", file=sys.stderr); continue
            keep.append(p)
        c["plays"] = keep
    # cross-chapter duplicate check on shared pool ids
    owner = {}
    for cid, c in chapters.items():
        for p in c["plays"]:
            for i in p.get("pool_ids") or []:
                if i in owner and owner[i][0] != cid:
                    print(f"shared pool id {i}: {owner[i]} and {cid}:{p['title']}", file=sys.stderr)
                owner[i] = (cid, p["title"])
    for f in sorted(glob.glob(os.path.join(ROOT, "curated_extra", "*.json"))):
        for p in json.load(open(f)).get("plays", []):
            if p.get("category") in chapters: chapters[p["category"]]["plays"].append(p)
            else: print("extra play with unknown category", p.get("title"), file=sys.stderr)
    for cid in CAT_ORDER:
        if cid not in chapters: continue
        c = chapters[cid]
        cats.append({"id": cid, "name": c["name"], "intro_html": c.get("intro_html",""), "principles": c.get("principles", [])})
        for p in c["plays"]:
            p["category"] = cid
            base = re.sub(r"[^a-z0-9]+", "-", (p["show"][:3] + " " + p["title"]).lower()).strip("-")[:48]
            pid, n = base, 2
            while pid in seen: pid, n = f"{base}-{n}", n + 1
            seen.add(pid); p["id"] = pid
            p["strength"] = int(p.get("strength", 3))
            p["episodes"] = [e for e in p.get("episodes", []) if re.match(r"^S\d\dE\d\d$", e)] or ["S01E01"]
            p["episodes"] = sorted(dict.fromkeys(p["episodes"]))
            for k in ("pool_ids","pool_id","batch","origin","absorbs","absorbed_by","dup_of","fix","borrowed_from","borrowed_category"):
                p.pop(k, None)
            plays.append(p)
    front = json.load(open(os.path.join(ROOT, "front.json")))
    data = clean({"meta": front, "shows": SHOWS, "categories": cats, "plays": plays, "episodes": eps})
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    tpl = open(os.path.join(ROOT, "template.html")).read()
    out = tpl.replace("/*__DATA__*/", blob)
    dst = os.path.join(ROOT, "five-houses.fragment.html")
    open(dst, "w").write(out)
    print(f"wrote {dst}: {len(plays)} plays, {len(cats)} chapters, {len(eps)} episodes, {len(out)//1024} KB")
    by = {}
    for p in plays: by[p["show"]] = by.get(p["show"], 0) + 1
    print(by)

if __name__ == "__main__":
    main()
