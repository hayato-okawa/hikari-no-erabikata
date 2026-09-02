#!/usr/bin/env python3
"""
articles-queue/ にある未公開記事を1本だけ取り出し、
- articles/{slug}.html を生成
- index.html の一覧に先頭挿入
- sitemap.xml に追記
- 公開済みキューファイルを articles-queue/published/ へ移動
する。GitHub Actions から週1回呼び出される想定。

キューファイル形式 (articles-queue/0001-xxxx.html):
  title: ...
  tag: ...
  dek: ...
  slug: ...
  ---
  <p>本文HTML...</p>
"""
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE_DIR = ROOT / "articles-queue"
PUBLISHED_DIR = QUEUE_DIR / "published"
ARTICLES_DIR = ROOT / "articles"
TEMPLATE_PATH = ROOT / "templates" / "article-template.html"
INDEX_PATH = ROOT / "index.html"
SITEMAP_PATH = ROOT / "sitemap.xml"
SITE_URL = "https://example.github.io"  # README の手順に従って実際のURLに置き換えること


def parse_queue_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if "---" not in text:
        raise ValueError(f"front matter (---) not found in {path}")
    front, body = text.split("---", 1)
    meta = {}
    for line in front.strip().splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    for required in ("title", "tag", "dek", "slug"):
        if required not in meta:
            raise ValueError(f"missing '{required}' in front matter of {path}")
    meta["body"] = body.strip("\n")
    return meta


def render_article(meta: dict) -> str:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    return (
        template.replace("{{TITLE}}", meta["title"])
        .replace("{{DESC}}", meta["dek"])
        .replace("{{TAG}}", meta["tag"])
        .replace("{{SLUG}}", meta["slug"])
        .replace("{{SITE_URL}}", SITE_URL)
        .replace("{{BODY}}", meta["body"])
    )


def insert_into_index(meta: dict) -> None:
    index_html = INDEX_PATH.read_text(encoding="utf-8")
    row = (
        '\n  <div class="article-row">\n'
        '    <div class="title">\n'
        f'      <a href="articles/{meta["slug"]}.html">{meta["title"]}</a>\n'
        f'      <div class="dek">{meta["dek"]}</div>\n'
        "    </div>\n"
        f'    <div class="tag">{meta["tag"]}</div>\n'
        "  </div>\n"
    )
    marker = '<h2>選び方ガイド</h2>'
    if marker not in index_html:
        raise ValueError("could not find insertion marker in index.html")
    index_html = index_html.replace(marker, marker + row, 1)
    INDEX_PATH.write_text(index_html, encoding="utf-8")


def append_to_sitemap(meta: dict) -> None:
    if not SITEMAP_PATH.exists():
        SITEMAP_PATH.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            "</urlset>\n",
            encoding="utf-8",
        )
    sitemap = SITEMAP_PATH.read_text(encoding="utf-8")
    entry = (
        f"  <url>\n"
        f"    <loc>{SITE_URL}/articles/{meta['slug']}.html</loc>\n"
        f"    <lastmod>{date.today().isoformat()}</lastmod>\n"
        f"  </url>\n"
    )
    sitemap = sitemap.replace("</urlset>", entry + "</urlset>")
    SITEMAP_PATH.write_text(sitemap, encoding="utf-8")


def main() -> int:
    PUBLISHED_DIR.mkdir(exist_ok=True)
    candidates = sorted(
        p for p in QUEUE_DIR.glob("*.html") if p.is_file()
    )
    if not candidates:
        print("no queued articles found - nothing to publish this week")
        return 0

    next_file = candidates[0]
    meta = parse_queue_file(next_file)

    out_path = ARTICLES_DIR / f"{meta['slug']}.html"
    if out_path.exists():
        print(f"ERROR: {out_path} already exists, aborting to avoid overwrite", file=sys.stderr)
        return 1

    out_path.write_text(render_article(meta), encoding="utf-8")
    insert_into_index(meta)
    append_to_sitemap(meta)

    next_file.rename(PUBLISHED_DIR / next_file.name)
    print(f"published: {meta['slug']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
