#!/usr/bin/env python3
"""Build the static project website (GitHub Pages) from the catalogs.

Usage: python scripts/build_site.py <output_dir> [--labels LIT_A1,LIT_A2,...]
Reads catalog/P2_*_catalog.csv and work/OA_RESOLVE/oa_manifest.csv; writes <output_dir>/index.html, design.html,
literature.html, about.html, assets/style.css, assets/literature.js, data/papers.json and .nojekyll.
No external fonts, scripts or trackers. Light mode only.
"""
import csv
import datetime
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

TOPICS = {
    "LIT_A1": ("appearance", "Object appearance: patches, stickers, camouflage"),
    "LIT_A2": ("shadows", "Shadows"),
    "LIT_A3": ("reflections", "Reflections, lasers and infrared"),
    "LIT_A4": ("lighting", "Lighting: projection, exposure, flicker"),
    "LIT_A5": ("frames", "Changes across video frames"),
    "LIT_X1": ("surveys", "Surveys and systematizations"),
    "LIT_X2": ("datasets", "Datasets and benchmarks"),
    "LIT_X3": ("code", "Open code and small models"),
    "LIT_X4": ("explain", "Explainable attack detection"),
    "LIT_X5": ("light", "Lightweight and embedded detection"),
    "LIT_X6": ("calib", "Calibration and abstention"),
    "LIT_X7": ("night", "Night, low visibility, adverse weather"),
    "LIT_X8": ("evaluation", "Evaluation methodology"),
    "LIT_X9": ("system", "System-level impact and simulation"),
    "LIT_X10": ("context", "Cross-sensor and context consistency"),
    "LIT_X11": ("phantom", "Phantom and fabricated objects"),
    "LIT_X12": ("signs", "Traffic-sign priors and sign-specific defenses"),
    "LIT_X13": ("monitor", "Runtime monitoring of perception"),
    "LIT_X14": ("targets", "Lanes, traffic lights, pedestrians, vehicles"),
    "DECK_SRC": ("background", "Background sources"),
    "LIT_IEEE": ("ieee", "IEEE Xplore search pass"),
    "EMBED_1": ("embedded", "Vehicle computing platforms and latency budgets"),
}

CLOSEST = {
    "appearance": [],
    "shadows": ["P2-P228", "P2-P230", "P2-P208"],
    "reflections": ["P2-P338", "P2-P309"],
    "lighting": ["P2-P431", "P2-P403", "P2-P406"],
    "frames": ["P2-P511", "P2-P512", "P2-P501"],
    "explain": ["P2-P1301", "P2-P1302"],
    "calib": ["P2-P1502"],
}

DESIGNS = [
    {
        "key": "appearance", "n": 1, "name": "Object appearance",
        "title": "Viewpoint-aware structural disagreement",
        "idea": "Low-cost evidence that an object's geometry and the detector's output disagree, without rebuilding the whole image.",
        "cue": "Contour, edges, sign shape, local colour and texture of the object region",
        "check": "Align the object region, track viewpoint and scale, compare the contour with the box and the label",
        "module": "Viewpoint-conditioned shape and detector mismatch with calibrated uncertainty",
        "open": ["Does class-specific contour consistency add signal against natural-looking patches, beyond texture?",
                 "Can a tiny head generalize across viewing angles?"],
        "limit": "Severe occlusion or artistic signs may destroy the geometric evidence; abstentions must be reported.",
    },
    {
        "key": "shadows", "n": 2, "name": "Shadows",
        "title": "Physics-gated temporal shadow evidence",
        "idea": "Check whether shadow movement is physically plausible before treating a detector failure as an attack.",
        "cue": "Shadow mask and edges, motion and a light-direction proxy",
        "check": "Align the shadow to the sign, correct for camera motion, estimate the plausible change",
        "module": "Shadow and geometry consistency residual with a reliability gate",
        "open": ["Can a physical reliability gate lower false positives on tree and cloud shadows?",
                 "Can it detect temporally coherent attack shadows?"],
        "limit": "Physically plausible malicious shadows may be indistinguishable from benign ones in RGB alone.",
    },
    {
        "key": "reflections", "n": 3, "name": "Reflections",
        "title": "View-conditioned light consistency",
        "idea": "Detect suspicious object responses to changing view and illumination without assuming every reflection is malicious.",
        "cue": "Specular regions and saturation, camera motion and a light proxy",
        "check": "Track the reflected region, contrast it with the nearby surface, estimate exposure drift",
        "module": "View-conditioned reflection residual with a confidence or abstain output",
        "open": ["Do low-cost view and illumination constraints reject natural highlights while detecting visible reflected-light attacks?"],
        "limit": "An RGB camera with an infrared-cut filter may not see an infrared attack; sensor assumptions must be stated.",
    },
    {
        "key": "lighting", "n": 4, "name": "Lighting",
        "title": "Global-local exposure and flicker test",
        "idea": "Combine local-versus-global illumination residuals with temporal flicker patterns under a fixed compute budget.",
        "cue": "Global luminance trend, local residuals and stripe cues",
        "check": "Normalize exposure drift, track local light change, estimate flicker consistency",
        "module": "Exposure-aware local light anomaly score with a temporal flicker gate",
        "open": ["Can a tiny exposure-flicker detector identify projected attacks without flagging normal headlight and auto-exposure changes?"],
        "limit": "Rolling-shutter and frame-rate aliasing can hide or imitate flicker; tests must cover several sensors.",
    },
    {
        "key": "frames", "n": 5, "name": "Changes across video frames",
        "title": "Bounded causal multi-cue evidence",
        "idea": "Lightweight sequential disagreement scoring with measured latency and an explicit insufficient-evidence state.",
        "cue": "Optical flow, local light and appearance consistency across recent frames",
        "check": "Align recent frames, extract trajectory and cue gaps, check quality and occlusion",
        "module": "Causal evidence accumulation with bounded frame memory",
        "open": ["Can bounded multi-cue evidence improve recall or warning time for unseen attacks while keeping a fixed false-alarm rate?"],
        "limit": "Prior work already uses temporal and physical consistency; any gain has to be shown as a controlled increment.",
    },
]

ABSTRACT = ("Autonomous vehicles rely on cameras and AI models to recognize road signs, pedestrians, cars, and obstacles. "
            "However, attackers can manipulate visual information using altered signs, stickers, patterns, or lighting to "
            "confuse these models. As a result, vehicles may fail to recognize dangerous objects, classify them incorrectly, "
            "or detect obstacles that are not actually there. These attacks can become more challenging to detect at night "
            "or in poor weather, when visibility is already limited. Existing defenses may struggle with unfamiliar attacks "
            "or require significant computing power.")
APPROACH = ("The plan is to develop a lightweight and explainable AI model that identifies suspicious changes in visual "
            "information and object detection results, by analyzing object appearance, shadows, reflections, lighting, "
            "and changes across video frames.")
CONTRIBUTIONS = [
    "Detect possible adversarial attacks targeting object detection models.",
    "Identify objects that are hidden, missed, or misclassified because of visual manipulation.",
    "Distinguish suspicious visual changes from normal lighting and weather conditions.",
    "Improve detection reliability under nighttime and low-visibility conditions.",
    "Develop a lightweight model suitable for vehicles with limited computing resources.",
    "Explain which visual inconsistencies caused the system to flag a possible attack.",
    "Evaluate detection accuracy, false alarms, processing time, and robustness using public datasets.",
]

CSS = """
:root{--bg:#ffffff;--ink:#1d2433;--muted:#5b6475;--line:#e3e7ee;--soft:#f5f7fb;--accent:#1f5fae;--accent-soft:#e8f0fb;--warn:#8a5a00;--warn-soft:#fff6e0;--ok:#1d6b3a;--ok-soft:#e7f5ec}
*{box-sizing:border-box}
html{color-scheme:light}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent)}
header.site{border-bottom:1px solid var(--line);background:#fff;position:sticky;top:0;z-index:5}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
header.site .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:60px;flex-wrap:wrap}
.brand{font-weight:700;color:var(--ink);text-decoration:none}
nav a{margin-left:18px;text-decoration:none;color:var(--muted);font-weight:500}
nav a.on,nav a:hover{color:var(--accent)}
.hero{padding:44px 0 18px}
.kicker{text-transform:uppercase;letter-spacing:.08em;font-size:12px;color:var(--muted);font-weight:600}
h1{font-size:30px;line-height:1.25;margin:8px 0 12px}
h2{font-size:22px;margin:36px 0 12px}
h3{font-size:17px;margin:0 0 6px}
.lead{font-size:18px;color:var(--muted);max-width:820px}
.notice{background:var(--warn-soft);border:1px solid #f0dca6;color:var(--warn);border-radius:8px;padding:12px 14px;margin:18px 0;font-size:14.5px}
.grid{display:grid;gap:16px}
.g2{grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}
.g3{grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}
.card{border:1px solid var(--line);border-radius:10px;padding:16px 18px;background:#fff}
.card.soft{background:var(--soft)}
.card .tag{display:inline-block;font-size:12px;font-weight:600;color:var(--accent);background:var(--accent-soft);border-radius:999px;padding:2px 10px;margin-bottom:8px}
.stat{font-size:28px;font-weight:700}
.muted{color:var(--muted)}
.small{font-size:14px}
ol.contrib li,ul.tight li{margin:4px 0}
.flow{display:flex;flex-wrap:wrap;align-items:stretch;gap:8px;margin:12px 0}
.flow .step{flex:1 1 150px;border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:var(--soft);font-size:14px}
.flow .step b{display:block;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:4px}
.flow .arrow{align-self:center;color:var(--muted);font-weight:700}
dl.kv{display:grid;grid-template-columns:150px 1fr;gap:6px 14px;margin:10px 0}
dl.kv dt{color:var(--muted);font-size:14px}
dl.kv dd{margin:0}
.limit{border-left:3px solid #d9a441;padding:6px 12px;background:var(--warn-soft);font-size:14.5px;margin-top:10px}
.controls{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0}
.controls input,.controls select{font:inherit;font-size:14.5px;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:#fff;color:var(--ink)}
.controls input{flex:1 1 260px}
table.papers{width:100%;border-collapse:collapse;font-size:14.5px}
table.papers th{position:sticky;top:60px;background:#fff;text-align:left;border-bottom:2px solid var(--line);padding:8px 6px;font-size:13px;color:var(--muted);cursor:pointer;white-space:nowrap}
table.papers td{border-bottom:1px solid var(--line);padding:9px 6px;vertical-align:top}
.title{font-weight:600}
.badge{display:inline-block;font-size:11.5px;border-radius:999px;padding:1px 8px;margin:2px 4px 2px 0;white-space:nowrap;border:1px solid var(--line);color:var(--muted)}
.badge.ok{color:var(--ok);background:var(--ok-soft);border-color:#bfe3cb}
.badge.pre{color:var(--warn);background:var(--warn-soft);border-color:#f0dca6}
.badge.topic{color:var(--accent);background:var(--accent-soft);border-color:#c9dbf3}
.links a{margin-right:10px;white-space:nowrap}
footer{border-top:1px solid var(--line);margin-top:48px;padding:22px 0 40px;color:var(--muted);font-size:14px}
@media (max-width:640px){h1{font-size:24px}dl.kv{grid-template-columns:1fr}nav a{margin-left:12px}}
"""

JS = r"""
(function(){
  const state={q:'',topic:'',role:'',ver:'',oa:'',sort:'year',dir:-1};
  const byId=id=>document.getElementById(id);
  const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let papers=[],topics={};
  function verBadge(v){
    if(v==='VERIFIED')return '<span class="badge ok" title="Crossref record matches title, first author and year">verified (Crossref)</span>';
    if(v==='ARXIV_API_VERIFIED')return '<span class="badge ok" title="arXiv record matches title, first author and year">verified (arXiv)</span>';
    return '<span class="badge pre" title="Not yet matched to a primary metadata record">'+esc(v.toLowerCase().replace(/_/g,' '))+'</span>';
  }
  function row(p){
    const links=[];
    if(p.doi)links.push('<a href="https://doi.org/'+esc(p.doi)+'" rel="noopener">DOI</a>');
    if(p.arxiv)links.push('<a href="https://arxiv.org/abs/'+esc(p.arxiv)+'" rel="noopener">arXiv</a>');
    if(p.oa_pdf)links.push('<a href="'+esc(p.oa_pdf)+'" rel="noopener">open PDF</a>');
    if(!links.length&&p.url)links.push('<a href="'+esc(p.url)+'" rel="noopener">page</a>');
    const tps=p.topics.map(t=>'<span class="badge topic">'+esc(topics[t]||t)+'</span>').join('');
    return '<tr><td><div class="title">'+esc(p.title)+'</div><div class="muted small">'+esc(p.first_author)+(p.venue?' &middot; '+esc(p.venue):'')+'</div>'+
      (p.key_idea?'<div class="small" style="margin-top:4px">'+esc(p.key_idea)+'</div>':'')+
      '<div>'+tps+'<span class="badge">'+esc(p.role.toLowerCase())+'</span>'+(p.peer_review==='preprint'?'<span class="badge pre">preprint</span>':'')+verBadge(p.verification)+'</div></td>'+
      '<td>'+esc(p.year)+'</td><td class="links">'+links.join('')+'</td></tr>';
  }
  function render(){
    const q=state.q.toLowerCase();
    let list=papers.filter(p=>(!state.topic||p.topics.includes(state.topic))&&(!state.role||p.role===state.role)&&
      (!state.ver||(state.ver==='verified'?/VERIFIED$/.test(p.verification):!/VERIFIED$/.test(p.verification)))&&
      (!state.oa||(state.oa==='yes'?!!p.oa_pdf:!p.oa_pdf))&&
      (!q||(p.title+' '+p.first_author+' '+p.venue+' '+p.key_idea+' '+p.method).toLowerCase().includes(q)));
    const k=state.sort;
    list.sort((a,b)=>{const x=k==='year'?(+a.year||0)-(+b.year||0):String(a[k]).localeCompare(String(b[k]));return x*state.dir;});
    byId('count').textContent=list.length+' of '+papers.length+' papers';
    byId('rows').innerHTML=list.map(row).join('');
  }
  function opt(sel,values,label){sel.innerHTML='<option value="">'+label+'</option>'+values.map(v=>'<option value="'+esc(v[0])+'">'+esc(v[1])+'</option>').join('');}
  fetch('data/papers.json').then(r=>r.json()).then(d=>{
    papers=d.papers;topics=d.topics;
    opt(byId('topic'),Object.entries(topics).filter(([k])=>papers.some(p=>p.topics.includes(k))),'All topics');
    opt(byId('role'),[...new Set(papers.map(p=>p.role))].sort().map(r=>[r,r.toLowerCase()]),'All roles');
    const h=new URLSearchParams(location.hash.slice(1));if(h.get('topic')){state.topic=h.get('topic');byId('topic').value=state.topic;}
    ['q','topic','role','ver','oa'].forEach(id=>byId(id).addEventListener('input',e=>{state[id]=e.target.value;render();}));
    document.querySelectorAll('th[data-k]').forEach(th=>th.addEventListener('click',()=>{const k=th.dataset.k;state.dir=state.sort===k?-state.dir:(k==='year'?-1:1);state.sort=k;render();}));
    byId('built').textContent=d.built;render();
  }).catch(()=>{byId('count').textContent='The paper list could not be loaded.';});
})();
"""


def esc(text):
    return html.escape(str(text), quote=True)


def norm(text):
    return re.sub(r"[^a-z0-9]+", "", str(text or "").lower())


def load_papers(labels=None):
    manifest = {}
    path = ROOT / "work" / "OA_RESOLVE" / "oa_manifest.csv"
    if path.exists():
        with open(path, encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                if row.get("pdf_url"):
                    manifest[row["paper_id"]] = row["pdf_url"]
    merged, order = {}, []
    for csv_path in sorted((ROOT / "catalog").glob("P2_*_catalog.csv")):
        label = csv_path.stem[3:-8]
        if label not in TOPICS or (labels and label not in labels):
            continue
        topic = TOPICS[label][0]
        with open(csv_path, encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                doi = (row.get("doi") or "").strip().lower()
                arxiv = (row.get("arxiv_id") or "").strip()
                key = "doi:" + doi if doi else ("arxiv:" + arxiv if arxiv else "title:" + norm(row.get("title")))
                relation = re.sub(r"\b(?:design )?slide 0?(\d)\b", r"design \1", row.get("relation_to_project", ""), flags=re.I)
                if key in merged:
                    item = merged[key]
                    if topic not in item["topics"]:
                        item["topics"].append(topic)
                    item["ids"].append(row["paper_id"])
                    if not item["oa_pdf"] and manifest.get(row["paper_id"]):
                        item["oa_pdf"] = manifest[row["paper_id"]]
                    if item["verification"] not in ("VERIFIED", "ARXIV_API_VERIFIED") and row.get("verification_status", "").endswith("VERIFIED") and not row.get("verification_status", "").startswith("UN"):
                        item["verification"] = row["verification_status"]
                    continue
                merged[key] = {
                    "id": row["paper_id"], "ids": [row["paper_id"]], "topics": [topic],
                    "title": row.get("title", ""), "first_author": row.get("first_author", ""), "venue": row.get("venue", ""),
                    "year": row.get("year", ""), "role": row.get("role", ""), "relevance": row.get("relevance", ""),
                    "key_idea": row.get("key_idea", ""), "method": row.get("method", ""), "relation": relation,
                    "peer_review": row.get("peer_review", ""), "verification": row.get("verification_status", "UNVERIFIED"),
                    "doi": doi, "arxiv": arxiv, "url": row.get("url", ""), "oa_pdf": manifest.get(row["paper_id"], ""),
                    "code_or_data": row.get("code_or_data", ""),
                }
                order.append(key)
    return [merged[k] for k in order]


def page(title, active, body, built):
    nav = [("index.html", "Overview"), ("design.html", "Research design"), ("literature.html", "Literature map"), ("about.html", "About")]
    links = "".join(f'<a href="{href}"{" class=\"on\"" if href == active else ""}>{name}</a>' for href, name in nav)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | Physical visual attacks on AV perception</title>
<meta name="description" content="PhD research: lightweight and explainable detection of physical visual adversarial attacks on object detection in autonomous vehicles. Work in progress.">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="site"><div class="wrap"><a class="brand" href="index.html">AV visual-attack detection research</a><nav>{links}</nav></div></header>
<main class="wrap">
{body}
</main>
<footer><div class="wrap">Work in progress, PhD thesis research. Nothing on this site is peer reviewed or independently audited. Built {esc(built)} from the repository <a href="https://github.com/ilkimaydar/phdthesisproject">ilkimaydar/phdthesisproject</a>.</div></footer>
</body>
</html>
"""


def build(out, labels=None):
    papers = load_papers(labels)
    built = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    by_id = {}
    for p in papers:
        for pid in p["ids"]:
            by_id[pid] = p
    counts = {}
    for p in papers:
        for t in p["topics"]:
            counts[t] = counts.get(t, 0) + 1
    verified = sum(1 for p in papers if p["verification"] in ("VERIFIED", "ARXIV_API_VERIFIED"))
    with_pdf = sum(1 for p in papers if p["oa_pdf"])
    topic_names = {v[0]: v[1] for v in TOPICS.values()}

    (out / "assets").mkdir(parents=True, exist_ok=True)
    (out / "data").mkdir(parents=True, exist_ok=True)
    (out / ".nojekyll").write_text("", encoding="utf-8")
    (out / "assets" / "style.css").write_text(CSS.strip() + "\n", encoding="utf-8", newline="\n")
    (out / "assets" / "literature.js").write_text(JS.strip() + "\n", encoding="utf-8", newline="\n")
    public = [{k: p[k] for k in ("id", "topics", "title", "first_author", "venue", "year", "role", "relevance", "key_idea",
                                 "method", "peer_review", "verification", "doi", "arxiv", "url", "oa_pdf")} for p in papers]
    (out / "data" / "papers.json").write_text(json.dumps({"built": built, "topics": topic_names, "papers": public},
                                                         ensure_ascii=False, separators=(",", ":")), encoding="utf-8", newline="\n")

    flow = ('<div class="flow"><div class="step"><b>Input</b>Camera frames with or without a physical attack</div><div class="arrow">&rarr;</div>'
            '<div class="step"><b>Existing detector</b>Frozen object or sign detector: boxes, labels, confidence</div><div class="arrow">+</div>'
            '<div class="step"><b>Independent cue</b>Cheap physical evidence: shape, shadow, reflection, light, motion</div><div class="arrow">&rarr;</div>'
            '<div class="step"><b>Consistency check</b>Do the cue and the detector output agree?</div><div class="arrow">&rarr;</div>'
            '<div class="step"><b>Decision</b>Flag with the region and cue that caused it, or no alarm or abstain</div></div>')
    cards = "".join(
        f'<div class="card"><span class="tag">{d["n"]}. {esc(d["name"])}</span><h3>{esc(d["title"])}</h3>'
        f'<p class="small">{esc(d["idea"])}</p><p class="small muted"><a href="literature.html#topic={d["key"]}">{counts.get(d["key"], 0)} papers in the literature map</a></p></div>'
        for d in DESIGNS)
    topic_cards = "".join(
        f'<div class="card soft"><div class="stat">{counts.get(k, 0)}</div><a href="literature.html#topic={k}">{esc(name)}</a></div>'
        for k, name in topic_names.items() if counts.get(k))
    index_body = f"""
<section class="hero">
<div class="kicker">PhD thesis research &middot; work in progress</div>
<h1>Lightweight and Explainable AI for Detecting Adversarial Attacks on Object Detection in Autonomous Vehicles</h1>
<p class="lead">Working title. The project studies physical attacks on the camera side of autonomous driving (altered signs, stickers, shadows, reflected or projected light, manipulations that unfold over video frames) and asks whether cheap, explainable consistency checks can flag them without slowing the vehicle down.</p>
<div class="notice">Current phase: literature mapping and research design. No experiment has been run yet, so this site reports no results. The design below is a set of hypotheses, not a proven method.</div>
</section>
<h2>Problem</h2>
<p>{esc(ABSTRACT)}</p>
<h2>Approach</h2>
<p>{esc(APPROACH)}</p>
{flow}
<h2>Planned contributions</h2>
<ol class="contrib">{"".join(f"<li>{esc(c)}</li>" for c in CONTRIBUTIONS)}</ol>
<h2>Five cue families</h2>
<div class="grid g3">{cards}</div>
<p class="small muted"><a href="design.html">Full research design</a>, with the open questions and the known weak point of each cue.</p>
<h2>Literature map so far</h2>
<p>{len(papers)} distinct papers, of which {verified} are matched to a Crossref or arXiv record (title, first author and year) and {with_pdf} have a known open-access PDF location. Summaries were written with AI assistance and are not yet independently audited.</p>
<div class="grid g3">{topic_cards}</div>
"""
    design_sections = []
    for d in DESIGNS:
        closest = [by_id[i] for i in CLOSEST.get(d["key"], []) if i in by_id]
        closest_html = ""
        if closest:
            items = "".join(f'<li><span class="title">{esc(p["title"])}</span> <span class="muted small">({esc(p["first_author"])}, {esc(p["year"])})</span></li>' for p in closest)
            closest_html = f'<p class="small muted" style="margin-bottom:2px">Closest prior work flagged by the literature pass (not yet audited):</p><ul class="tight small">{items}</ul>'
        design_sections.append(f"""
<div class="card" id="{d["key"]}"><span class="tag">{d["n"]}. {esc(d["name"])}</span><h3>{esc(d["title"])}</h3>
<p>{esc(d["idea"])}</p>
<dl class="kv"><dt>Independent cue</dt><dd>{esc(d["cue"])}</dd><dt>Consistency check</dt><dd>{esc(d["check"])}</dd><dt>Proposed module</dt><dd>{esc(d["module"])}</dd>
<dt>Open questions</dt><dd><ul class="tight">{"".join(f"<li>{esc(q)}</li>" for q in d["open"])}</ul></dd></dl>
{closest_html}
<div class="limit"><b>Known weak point.</b> {esc(d["limit"])}</div>
<p class="small"><a href="literature.html#topic={d["key"]}">{counts.get(d["key"], 0)} papers on this cue</a></p></div>""")
    design_body = f"""
<section class="hero"><div class="kicker">Research design &middot; hypotheses</div><h1>Five consistency checks around a frozen detector</h1>
<p class="lead">Every design keeps the existing detector unchanged, adds one cheap physical cue, and turns their disagreement into a calibrated decision that can also say "not enough evidence".</p></section>
{flow}
<div class="notice">Shared evaluation stance: compare methods at matched false-alarm operating points, on held-out recordings, and report processing time per frame. None of these designs has been implemented or tested yet.</div>
<div class="grid">{"".join(design_sections)}</div>
"""
    lit_body = """
<section class="hero"><div class="kicker">Literature map</div><h1>Papers collected so far</h1>
<p class="lead">Search and filter the catalog. A green badge means the bibliographic record was matched automatically against Crossref or the arXiv API. One-line summaries are paraphrases written with AI assistance and are not yet audited: read the paper before relying on one.</p></section>
<div class="controls">
<input id="q" type="search" placeholder="Search title, author, venue, summary" aria-label="Search">
<select id="topic" aria-label="Topic"></select>
<select id="role" aria-label="Role"></select>
<select id="ver" aria-label="Verification"><option value="">Any verification</option><option value="verified">Verified record</option><option value="other">Not yet verified</option></select>
<select id="oa" aria-label="Open access"><option value="">Any access</option><option value="yes">Open PDF known</option><option value="no">No open PDF known</option></select>
</div>
<p class="muted small"><span id="count">Loading...</span> &middot; data built <span id="built"></span></p>
<table class="papers"><thead><tr><th data-k="title">Paper</th><th data-k="year">Year</th><th>Links</th></tr></thead><tbody id="rows"></tbody></table>
<script src="assets/literature.js"></script>
"""
    about_body = """
<section class="hero"><div class="kicker">About</div><h1>How this site is made</h1></section>
<h2>Status</h2>
<p>This is a PhD research project in its first phase. The site shows the research question, the research design and a literature map. It contains no experimental results. Drafts and results will appear here only after they exist and have been checked.</p>
<h2>How papers enter the map</h2>
<ul class="tight">
<li>Candidate papers are found by topic-specific searches.</li>
<li>Each paper is looked up by DOI in Crossref or by identifier in the arXiv API. A paper counts as verified only when the title, first author and year of that record match the catalog row. The lookup is logged with its time.</li>
<li>Summaries are short paraphrases. They are not copied abstracts and they have not yet been audited by an independent reviewer.</li>
<li>Open-access PDF locations come from OpenAlex and arXiv. PDFs are not hosted on this site; follow the links to the publisher or the preprint server.</li>
</ul>
<h2>Use of AI</h2>
<p>The literature search, the verification scripts, the summaries and this site were produced with assistance from AI models (Anthropic Claude, run through the OpenCode agent tool) under the direction of the project owner. Every catalog entry carries its verification state, and nothing is presented as a finding before an independent check.</p>
<h2>Licence</h2>
<p>The repository is under the MIT License, chosen by the owner (LICENSE file in the repository). Paper titles and bibliographic data belong to their publishers and authors.</p>
<h2>Repository and mirrors</h2>
<p>Source of this site, the catalogs and the scripts: <a href="https://github.com/ilkimaydar/phdthesisproject">github.com/ilkimaydar/phdthesisproject</a>. Corrections are welcome through GitHub issues. The same site is mirrored as a Hugging Face Space: <a href="https://huggingface.co/spaces/ilkimaydar/phdthesisproject">huggingface.co/spaces/ilkimaydar/phdthesisproject</a>.</p>
"""
    for name, title, body in (("index.html", "Overview", index_body), ("design.html", "Research design", design_body),
                              ("literature.html", "Literature map", lit_body), ("about.html", "About", about_body)):
        (out / name).write_text(page(title, name, body, built), encoding="utf-8", newline="\n")
    return {"papers": len(papers), "verified": verified, "with_pdf": with_pdf, "topics": len(counts)}


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = sys.argv[1:]
    labels = None
    if "--labels" in args:
        position = args.index("--labels")
        labels = set(filter(None, args[position + 1].split(","))) if position + 1 < len(args) else set()
        args = args[:position] + args[position + 2:]
    if len(args) != 1:
        print(__doc__)
        return 2
    out = pathlib.Path(args[0]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    stats = build(out, labels)
    print("site built: " + ", ".join(f"{k} {v}" for k, v in stats.items()) + f" -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
