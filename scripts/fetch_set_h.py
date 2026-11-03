#!/usr/bin/env python3
"""
Fetch Set H, the ten pre-ChatGPT human texts the criteria name.  (unit 8, M3)

    python scripts/fetch_set_h.py --out set_h.json

The calibration set (samples/calibration.json) used r/rutgers, simple and
English Wikipedia, and one arXiv abstract. criteria.md asks for sources it
never touched, so Set H comes from three new places:

  casual (5)  Hacker News comments posted 2019-03-01 00:00-01:00 UTC
  formal (2)  Stanford Encyclopedia of Philosophy, Fall 2021 archive, entry preambles
  formal (3)  PubMed abstracts with publication date 2018-06-01

The picks are mechanical, so nothing about the detector can steer them:

  HN       oldest first; skip any comment with a link, code, or a quoted line
  SEP      walk the alphabetical contents from the one-third and two-thirds
           marks; take the first preamble at or after each mark
  PubMed   in the order esearch returns them; unstructured abstracts only
           (one paragraph, no BACKGROUND/METHODS labels)

Every pick must be 80 to 300 words (whitespace split). Everything here was
published before 30 November 2022. The script prints what it picked, and it
never scores anything.
"""

import argparse
import html
import json
import re
import sys
import xml.etree.ElementTree as ET

import requests

HEADERS = {"User-Agent": "provenance-guard-eval/1.0 (course project test set)"}
MIN_WORDS, MAX_WORDS = 80, 300

HN_WINDOW = (1551398400, 1551402000)  # 2019-03-01 00:00 to 01:00 UTC
SEP_ARCHIVE = "https://plato.stanford.edu/archives/fall2021"
PUBMED_DATE = "2018/06/01"


def words(text):
    return len(text.split())


def strip_tags(fragment):
    fragment = re.sub(r"</p>\s*<p[^>]*>|<p[^>]*>", "\n\n", fragment)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    text = html.unescape(fragment)
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)  # source line wraps, not paragraphs
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fetch_hn(n=5):
    url = ("https://hn.algolia.com/api/v1/search_by_date?tags=comment"
           f"&numericFilters=created_at_i>={HN_WINDOW[0]},created_at_i<{HN_WINDOW[1]}"
           "&hitsPerPage=1000")
    hits = requests.get(url, headers=HEADERS, timeout=30).json()["hits"]
    hits.sort(key=lambda h: (h["created_at_i"], int(h["objectID"])))
    picks = []
    for hit in hits:
        raw = hit.get("comment_text") or ""
        if re.search(r"<a |https?://|<pre>|<code>", raw):
            continue
        text = strip_tags(raw)
        if any(line.lstrip().startswith(">") for line in text.splitlines()):
            continue
        if not MIN_WORDS <= words(text) <= MAX_WORDS:
            continue
        picks.append({
            "id": f"hn_{hit['objectID']}",
            "group": "human_casual",
            "source": f"Hacker News comment on '{hit.get('story_title') or 'a thread'}'",
            "url": f"https://news.ycombinator.com/item?id={hit['objectID']}",
            "date": hit["created_at"],
            "text": text,
        })
        if len(picks) == n:
            break
    return picks


def sep_slugs():
    page = requests.get(f"{SEP_ARCHIVE}/contents.html", headers=HEADERS, timeout=60).text
    seen, slugs = set(), []
    for slug in re.findall(r'href="entries/([a-z0-9-]+)/"', page):
        if slug not in seen:
            seen.add(slug)
            slugs.append(slug)
    return slugs


def sep_preamble(slug):
    page = requests.get(f"{SEP_ARCHIVE}/entries/{slug}/", headers=HEADERS, timeout=60).text
    match = re.search(r'<div id="preamble">(.*?)</div>', page, re.S)
    if not match or re.search(r'class="math|\\\(|<img', match.group(1)):
        return None
    return strip_tags(match.group(1))


def fetch_sep():
    slugs = sep_slugs()
    picks = []
    for start in (len(slugs) // 3, 2 * len(slugs) // 3):
        for slug in slugs[start:start + 40]:
            text = sep_preamble(slug)
            if text and MIN_WORDS <= words(text) <= MAX_WORDS:
                picks.append({
                    "id": f"sep_{slug}",
                    "group": "human_formal",
                    "source": f"Stanford Encyclopedia of Philosophy, entry '{slug}', preamble",
                    "url": f"{SEP_ARCHIVE}/entries/{slug}/",
                    "date": "Fall 2021 archive edition",
                    "text": text,
                })
                break
    return picks


def fetch_pubmed(n=3):
    search = requests.get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
        params={"db": "pubmed", "retmode": "json", "retmax": 60,
                "term": f"{PUBMED_DATE}[pdat] AND hasabstract AND english[lang] "
                        "AND journal article[pt]"},
        headers=HEADERS, timeout=30).json()
    ids = search["esearchresult"]["idlist"]
    xml = requests.get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
        params={"db": "pubmed", "retmode": "xml", "id": ",".join(ids)},
        headers=HEADERS, timeout=60).text
    articles = {a.findtext(".//PMID"): a for a in ET.fromstring(xml).iter("PubmedArticle")}
    picks = []
    for pmid in ids:
        article = articles.get(pmid)
        if article is None:
            continue
        parts = article.findall(".//Abstract/AbstractText")
        if len(parts) != 1 or parts[0].get("Label"):
            continue
        text = re.sub(r"\s+", " ", "".join(parts[0].itertext())).strip()
        if not MIN_WORDS <= words(text) <= MAX_WORDS:
            continue
        picks.append({
            "id": f"pubmed_{pmid}",
            "group": "human_formal",
            "source": f"PubMed abstract {pmid}: {article.findtext('.//ArticleTitle')}",
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "date": PUBMED_DATE.replace("/", "-"),
            "text": text,
        })
        if len(picks) == n:
            break
    return picks


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", required=True, help="where to write the picks as JSON")
    args = parser.parse_args()

    picks = fetch_hn() + fetch_sep() + fetch_pubmed()
    for p in picks:
        print(f"{p['id']:<24} {words(p['text']):>4} words  {p['source'][:70]}")
    if len(picks) != 10:
        print(f"!! expected 10 picks, got {len(picks)}", file=sys.stderr)
        sys.exit(1)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(picks, f, indent=2, ensure_ascii=False)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
