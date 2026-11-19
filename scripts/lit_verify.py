#!/usr/bin/env python3
"""Read-only metadata checks against open scholarly APIs, with a verification ledger.

Usage (LABEL = your task label, for example LIT_A1):
  python scripts/lit_verify.py LABEL crossref <doi> [<doi> ...]
  python scripts/lit_verify.py LABEL arxiv <arxiv_id> [<arxiv_id> ...]
  python scripts/lit_verify.py LABEL dblp "<paper title>" [rows]
  python scripts/lit_verify.py LABEL openalex <doi> [<doi> ...]     one batch call, at most 50 DOIs (citation counts)
  python scripts/lit_verify.py LABEL search-crossref "<free text>" [rows]
  python scripts/lit_verify.py LABEL search-arxiv "<free text>" [rows]
Add --abstract to print the abstract when the record carries one.

Every record returned is appended as one JSON line to work/LABEL/verify_ledger.jsonl (stamp from the system
clock). Every search is appended to work/LABEL/query_log.tsv. The catalog builder trusts only the ledger.

Built-in rules (AGENTS.md 3.2 Tier 4, docs/playbook/11_literature.md): one request at a time, a pause after
each request, no file downloads, no personal data in URLs or headers. HTTP 404 on a single DOI is the result
NOT_FOUND. Any other 4xx prints STOP_HOST and exits 3: do not call that host again in this run. A 5xx or a
network error prints RETRY_LATER and exits 4: move on to other work, do not loop.
"""
import datetime
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = "P2-lit-verify/0.1 (academic literature check; python urllib)"
PAUSE = {"api.crossref.org": 1.0, "export.arxiv.org": 3.0, "dblp.org": 2.0, "api.openalex.org": 1.0}
ATOM = "{http://www.w3.org/2005/Atom}"
ARX = "{http://arxiv.org/schemas/atom}"
CR_SELECT = "DOI,title,author,issued,published-print,published-online,container-title,type,is-referenced-by-count"


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def norm_doi(text):
    text = re.sub(r"^https?://(dx\.)?doi\.org/", "", text.strip(), flags=re.I)
    return re.sub(r"^doi:\s*", "", text, flags=re.I).lower()


def norm_arxiv(text):
    text = re.sub(r"^https?://arxiv\.org/(abs|pdf)/", "", text.strip(), flags=re.I)
    text = re.sub(r"^arxiv:\s*", "", text, flags=re.I)
    text = re.sub(r"\.pdf$", "", text, flags=re.I)
    return re.sub(r"v\d+$", "", text)


def clean(text):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", __import__("html").unescape(text or ""))).strip()


class Run:
    def __init__(self, label):
        if not re.match(r"^[A-Za-z0-9_.-]+$", label):
            sys.exit("lit_verify: bad label")
        self.dir = ROOT / "work" / label
        self.dir.mkdir(parents=True, exist_ok=True)

    def append(self, name, line):
        with open(self.dir / name, "a", encoding="utf-8", newline="\n") as handle:
            handle.write(line + "\n")

    def ledger(self, record):
        record = {"at": now(), **record}
        self.append("verify_ledger.jsonl", json.dumps(record, ensure_ascii=False))
        return record

    def qlog(self, source, query, count):
        self.append("query_log.tsv", "\t".join([now(), source, query.replace("\t", " "), str(count)]))


GAP = {"api.crossref.org": 1.5, "export.arxiv.org": 3.5, "api.openalex.org": 1.5}


def wait_turn(host):
    """Space requests to one host across all agents on this computer (shared stamp file in the local temp folder)."""
    try:
        import msvcrt
        import os
        import tempfile
        folder = pathlib.Path(os.environ.get("TEMP") or tempfile.gettempdir()) / "opencode" / "p2_throttle"
        folder.mkdir(parents=True, exist_ok=True)
        fd = os.open(str(folder / (re.sub(r"[^A-Za-z0-9.-]", "_", host) + ".txt")), os.O_RDWR | os.O_CREAT)
    except (ImportError, OSError):
        return
    try:
        locked = False
        for _ in range(2400):
            try:
                os.lseek(fd, 1000000, 0)
                msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
                locked = True
                break
            except OSError:
                time.sleep(0.25)
        os.lseek(fd, 0, 0)
        text = os.read(fd, 32).decode("ascii", "ignore").strip()
        try:
            wait = float(text) + GAP.get(host, 1.5) - time.time()
        except ValueError:
            wait = 0.0
        if 0 < wait <= 10:
            time.sleep(wait)
        os.lseek(fd, 0, 0)
        os.write(fd, ("%-32s" % repr(time.time())).encode("ascii"))
        if locked:
            os.lseek(fd, 1000000, 0)
            msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
    except OSError:
        pass
    finally:
        os.close(fd)


STOP_SECONDS = 1800
TAB = chr(9)


def stop_file(host):
    import os
    import tempfile
    folder = pathlib.Path(os.environ.get("TEMP") or tempfile.gettempdir()) / "opencode" / "p2_throttle"
    folder.mkdir(parents=True, exist_ok=True)
    return folder / (re.sub(r"[^A-Za-z0-9.-]", "_", host) + ".stop")


def host_stopped(host):
    """True while a shared stop set after a 4xx or a bot-check answer is in force (AGENTS.md 3.2 Tier 4)."""
    try:
        until = float(stop_file(host).read_text(encoding="ascii").split()[0])
    except (OSError, ValueError, IndexError):
        return False
    return until > time.time()


def stop_host(host, reason):
    """Record a shared stop for every agent on this computer, then end this call with exit code 3."""
    try:
        stop_file(host).write_text("%d %s%s" % (time.time() + STOP_SECONDS, reason, chr(10)), encoding="ascii")
    except OSError:
        pass
    print(TAB.join(["STOP_HOST", host, str(reason), "shared stop for all agents for %d min" % (STOP_SECONDS // 60)]))
    sys.exit(3)


def get(url, single_lookup=False):
    host = urllib.parse.urlsplit(url).netloc
    if host_stopped(host):
        print(TAB.join(["STOP_HOST", host, "shared stop in force after an earlier 4xx or bot check; do not call this host again in this run"]))
        sys.exit(3)
    wait_turn(host)
    request = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json, application/atom+xml;q=0.9, */*;q=0.1"})
    try:
        with urllib.request.urlopen(request, timeout=40) as response:
            body = response.read()
            if "html" in response.headers.get("Content-Type", "").lower():
                stop_host(host, "HTML body, possible bot check")
    except urllib.error.HTTPError as error:
        if error.code == 404 and single_lookup:
            time.sleep(PAUSE.get(host, 1.0))
            return None
        if 400 <= error.code < 500:
            stop_host(host, error.code)
            print(f"STOP_HOST\t{host}\t{error.code}")
            sys.exit(3)
        print(f"RETRY_LATER\t{host}\t{error.code}")
        sys.exit(4)
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        print(f"RETRY_LATER\t{host}\t{type(error).__name__}")
        sys.exit(4)
    time.sleep(PAUSE.get(host, 1.0))
    return body


def show(record, abstract=""):
    print("\t".join([
        record["status"], record["source"], record["key"], "/".join(record.get("years", [])),
        record.get("first_author", ""), record.get("venue", ""), record.get("type", ""),
        "cited_by=" + str(record.get("cited_by", "")), record.get("title", ""), record["at"],
    ]))
    if abstract:
        print("ABSTRACT\t" + abstract[:1800])


def crossref_fields(message):
    author = (message.get("author") or [{}])[0]
    years = []
    for key in ("published-print", "issued", "published-online"):
        parts = (message.get(key) or {}).get("date-parts") or [[None]]
        if parts and parts[0] and parts[0][0] and str(parts[0][0]) not in years:
            years.append(str(parts[0][0]))
    return {
        "title": clean((message.get("title") or [""])[0]),
        "first_author": author.get("family") or author.get("name") or "",
        "years": years,
        "venue": clean((message.get("container-title") or [""])[0]),
        "type": message.get("type", ""),
        "cited_by": message.get("is-referenced-by-count"),
    }


def cmd_crossref(run, dois, abstract):
    for raw in dois:
        doi = norm_doi(raw)
        body = get("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/"), single_lookup=True)
        if body is None:
            record = run.ledger({"source": "crossref", "key": doi, "status": "NOT_FOUND"})
            print(f"NOT_FOUND\tcrossref\t{doi}\t{record['at']}")
            continue
        message = json.loads(body)["message"]
        record = run.ledger({"source": "crossref", "key": doi, "status": "FOUND", **crossref_fields(message)})
        show(record, clean(message.get("abstract", "")) if abstract else "")


def cmd_search_crossref(run, query, rows):
    url = f"https://api.crossref.org/works?rows={rows}&select={CR_SELECT}&query.bibliographic=" + urllib.parse.quote(query)
    items = json.loads(get(url))["message"].get("items", [])
    run.qlog("crossref", query, len(items))
    for message in items:
        record = run.ledger({"source": "crossref", "key": norm_doi(message.get("DOI", "")), "status": "FOUND", **crossref_fields(message)})
        show(record)
    if not items:
        print("NO_HITS\tcrossref\t" + query)


def arxiv_entries(body):
    entries = []
    for entry in ET.fromstring(body).findall(ATOM + "entry"):
        ident = entry.findtext(ATOM + "id") or ""
        if "arxiv.org/abs/" not in ident:
            continue
        authors = [clean(a.findtext(ATOM + "name")) for a in entry.findall(ATOM + "author")]
        first = authors[0] if authors else ""
        entries.append({
            "key": norm_arxiv(ident),
            "title": clean(entry.findtext(ATOM + "title")),
            "first_author": first.split()[-1] if first else "",
            "years": [(entry.findtext(ATOM + "published") or "")[:4]],
            "venue": clean(entry.findtext(ARX + "journal_ref") or "") or "arXiv preprint",
            "type": "preprint",
            "doi": (entry.findtext(ARX + "doi") or "").lower(),
            "abstract": clean(entry.findtext(ATOM + "summary")),
        })
    return entries


def cmd_arxiv(run, idents, abstract):
    idents = [norm_arxiv(i) for i in idents]
    url = "https://export.arxiv.org/api/query?max_results=" + str(len(idents)) + "&id_list=" + urllib.parse.quote(",".join(idents), safe=",/")
    found = {entry["key"]: entry for entry in arxiv_entries(get(url))}
    for ident in idents:
        entry = found.get(ident)
        if entry is None:
            record = run.ledger({"source": "arxiv", "key": ident, "status": "NOT_FOUND"})
            print(f"NOT_FOUND\tarxiv\t{ident}\t{record['at']}")
            continue
        text = entry.pop("abstract")
        record = run.ledger({"source": "arxiv", "status": "FOUND", **entry})
        show(record, text if abstract else "")


def cmd_search_arxiv(run, query, rows, abstract):
    words = re.findall(r"[A-Za-z0-9\-]+", query)[:10]
    search = " AND ".join("all:" + word for word in words)
    url = f"https://export.arxiv.org/api/query?max_results={rows}&sortBy=relevance&search_query=" + urllib.parse.quote(search)
    entries = arxiv_entries(get(url))
    run.qlog("arxiv", query, len(entries))
    for entry in entries:
        text = entry.pop("abstract")
        record = run.ledger({"source": "arxiv", "status": "FOUND", **entry})
        show(record, text if abstract else "")
    if not entries:
        print("NO_HITS\tarxiv\t" + query)


def cmd_dblp(run, title, rows):
    url = f"https://dblp.org/search/publ/api?format=json&h={rows}&q=" + urllib.parse.quote(title)
    hits = ((json.loads(get(url)).get("result") or {}).get("hits") or {}).get("hit") or []
    run.qlog("dblp", title, len(hits))
    for hit in hits:
        info = hit.get("info", {})
        authors = (info.get("authors") or {}).get("author") or []
        if isinstance(authors, dict):
            authors = [authors]
        first = re.sub(r"\s+\d{4}$", "", authors[0].get("text", "")) if authors else ""
        venue = info.get("venue", "")
        if isinstance(venue, list):
            venue = ", ".join(venue)
        record = run.ledger({
            "source": "dblp", "key": "dblp:" + info.get("key", ""), "status": "FOUND",
            "title": clean(info.get("title", "")).rstrip("."),
            "first_author": first.split()[-1] if first else "",
            "years": [str(info.get("year", ""))], "venue": venue, "type": info.get("type", ""),
            "doi": (info.get("doi") or "").lower(), "ee": info.get("ee", "") if isinstance(info.get("ee", ""), str) else "",
        })
        show(record)
    if not hits:
        print("NO_HITS\tdblp\t" + title)


def cmd_openalex(run, dois):
    dois = [norm_doi(d) for d in dois][:50]
    flt = "|".join("https://doi.org/" + d for d in dois)
    url = "https://api.openalex.org/works?per-page=50&select=doi,cited_by_count,publication_year,title&filter=doi:" + urllib.parse.quote(flt, safe=":/|")
    seen = set()
    for work in json.loads(get(url)).get("results", []):
        doi = norm_doi(work.get("doi") or "")
        seen.add(doi)
        record = run.ledger({"source": "openalex", "key": doi, "status": "FOUND", "cited_by": work.get("cited_by_count"),
                             "years": [str(work.get("publication_year") or "")], "title": clean(work.get("title") or "")})
        print(f"CITED_BY\t{doi}\t{record['cited_by']}\t{record['at']}")
    for doi in dois:
        if doi not in seen:
            print(f"NO_RECORD\topenalex\t{doi}")


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    abstract = "--abstract" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--abstract"]
    if len(args) < 3:
        print(__doc__)
        return 2
    run, command, rest = Run(args[0]), args[1], args[2:]
    rows = 5
    if command in ("dblp", "search-crossref", "search-arxiv") and len(rest) > 1 and rest[-1].isdigit():
        rows = max(1, min(10, int(rest[-1])))
        rest = rest[:-1]
    text = " ".join(rest)
    if command == "crossref":
        cmd_crossref(run, rest, abstract)
    elif command == "arxiv":
        cmd_arxiv(run, rest, abstract)
    elif command == "dblp":
        print("DISABLED\tdblp\tdblp.org answered with a bot-check page at kickoff; host stopped (AGENTS.md 3.2 Tier 4)")
        return 3
    elif command == "openalex":
        cmd_openalex(run, rest)
    elif command == "search-crossref":
        cmd_search_crossref(run, text, rows)
    elif command == "search-arxiv":
        cmd_search_arxiv(run, text, rows, abstract)
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, ET.ParseError):
        print("STOP_HOST\t" + (sys.argv[2] if len(sys.argv) > 2 else "?") + "\tunparseable body (possible bot check); stop this source")
        sys.exit(3)
