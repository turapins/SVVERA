#!/usr/bin/env python3
"""
collect_daily_competitor_creatives.py

Daily competitor-creative collection for Vocal Image, via Atria's ad-library API.

Loads config/competitor_watchlist.yaml, searches each query, keeps only
watchlist-relevant brands, downloads the actual creative files, dedupes by
(brand, title), diffs against yesterday's manifest to flag what's new, and
writes:

    data/competitor_refs/<YYYY-MM-DD>/manifest.json
    data/competitor_refs/<YYYY-MM-DD>/daily_report.md
    data/competitor_refs/<YYYY-MM-DD>/<brand_slug>/<ad_id>.<ext>

Files land locally only — nothing is uploaded to Drive automatically.
Ivan reviews daily_report.md and uploads what he wants via a separate script.

Usage:
    python3 scripts/collect_daily_competitor_creatives.py [--date YYYY-MM-DD]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

import requests
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.tool_registry import registry  # noqa: E402

WATCHLIST_PATH = REPO_ROOT / "config" / "competitor_watchlist.yaml"
DATA_ROOT = REPO_ROOT / "data" / "competitor_refs"


def load_watchlist() -> dict:
    with open(WATCHLIST_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _slug(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text or "unknown_brand").strip("_")
    return text.lower() or "unknown_brand"


def _ext_from_url(url: str, default: str) -> str:
    suffix = Path(urlparse(url).path).suffix
    return suffix if suffix else default


def _download_ad_media(ad: dict, day_dir: Path) -> None:
    """Download an ad's first image/video into day_dir/<brand_slug>/<ad_id>.<ext>.

    Mirrors the download logic in tools/research/atria_ad_intel.py — kept
    separate here so this script only downloads media for ads that survive
    the watchlist filter, not every raw search hit.
    """
    brand_dir = day_dir / _slug(ad.get("brand_name"))
    ad_id = ad.get("id", "unknown")

    for media_key, local_key, default_ext in (
        ("images", "local_image_path", ".jpg"),
        ("videos", "local_video_path", ".mp4"),
    ):
        items = ad.get(media_key) or []
        if not items or not items[0].get("url"):
            continue
        url = items[0]["url"]
        dest = brand_dir / f"{ad_id}{_ext_from_url(url, default_ext)}"
        try:
            resp = requests.get(url, timeout=120)
            resp.raise_for_status()
        except Exception:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(resp.content)
        ad[local_key] = str(dest)


def collect(run_date: date) -> dict:
    watchlist = load_watchlist()
    relevant = {b.strip().lower() for b in watchlist.get("relevant_brands", [])}
    excluded = {b.strip().lower() for b in watchlist.get("exclude_brands", [])}

    registry.discover()
    tool = registry.get("atria_ad_intel")
    if tool is None:
        raise RuntimeError("atria_ad_intel tool not found in registry")
    if not tool.get_status().value == "available":
        raise RuntimeError("atria_ad_intel is UNAVAILABLE — check ATRIA_API_KEY in .env")

    day_dir = DATA_ROOT / run_date.isoformat()
    day_dir.mkdir(parents=True, exist_ok=True)

    seen_ads: dict[str, dict] = {}
    errors: list[str] = []

    # Pass 1: search only (no downloads yet) — the watchlist filter below
    # drops most brands, so downloading before filtering wastes bandwidth
    # and disk (Atria's broad-match search returns a lot of noise brands).
    for query in watchlist.get("queries", []):
        result = tool.execute(
            {
                "query": query,
                "platform": "facebook",
                "status": "active",
                "order": "best_match",
                "language": "en",
                "page_size": 25,
            }
        )
        if not result.success:
            errors.append(f"{query}: {result.error}")
            continue
        for ad in result.data["ads"]:
            brand = (ad.get("brand_name") or "").strip().lower()
            if brand in excluded or brand not in relevant:
                continue
            ad["_query"] = query
            seen_ads[ad["id"]] = ad

    # Dedupe by (brand, title), keep the longest-running variant.
    best_by_creative: dict[tuple[str, str], dict] = {}
    for ad in seen_ads.values():
        key = (ad.get("brand_name"), ad.get("title"))
        current = best_by_creative.get(key)
        if current is None or ad.get("running_days", 0) > current.get("running_days", 0):
            best_by_creative[key] = ad

    ads = sorted(best_by_creative.values(), key=lambda a: a.get("running_days", 0), reverse=True)

    # Pass 2: download creative bytes only for the final, filtered list.
    for ad in ads:
        _download_ad_media(ad, day_dir)

    manifest = {
        "date": run_date.isoformat(),
        "generated_at": datetime.now().isoformat(),
        "source": "atria",
        "errors": errors,
        "ads": ads,
    }
    (day_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return manifest


def load_previous_manifest(run_date: date) -> dict | None:
    for days_back in range(1, 8):
        prev_dir = DATA_ROOT / (run_date - timedelta(days=days_back)).isoformat()
        prev_manifest = prev_dir / "manifest.json"
        if prev_manifest.exists():
            return json.loads(prev_manifest.read_text(encoding="utf-8"))
    return None


def write_report(run_date: date, manifest: dict, previous: dict | None) -> Path:
    day_dir = DATA_ROOT / run_date.isoformat()
    prev_ids = {a["id"] for a in previous["ads"]} if previous else set()
    new_ads = [a for a in manifest["ads"] if a["id"] not in prev_ids]
    still_running = [a for a in manifest["ads"] if a["id"] in prev_ids]

    lines = [f"# Competitor creative report — {run_date.isoformat()}", ""]

    if manifest["errors"]:
        lines.append("## Query errors")
        for err in manifest["errors"]:
            lines.append(f"- {err}")
        lines.append("")

    lines.append(f"## New today ({len(new_ads)})")
    lines.append("")
    for ad in new_ads:
        lines.append(_ad_line(ad))
    if not new_ads:
        lines.append("_Nothing new since the last run._")
    lines.append("")

    lines.append(f"## Still running ({len(still_running)})")
    lines.append("")
    for ad in still_running:
        lines.append(_ad_line(ad))
    if not still_running:
        lines.append("_None._")
    lines.append("")

    lines.append("## Meta Ad Library cross-check")
    lines.append("")
    lines.append(
        "_Pending — run `ads_library_search` (Meta Ads MCP) per watchlist query "
        "and append results here manually or via the daily routine._"
    )
    lines.append("")

    report_path = day_dir / "daily_report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def _ad_line(ad: dict) -> str:
    local = ad.get("local_video_path") or ad.get("local_image_path") or "(download failed)"
    return (
        f"- **{ad.get('brand_name')}** — {ad.get('title') or '(no title)'} "
        f"— {ad.get('running_days', 0)}d running — `{local}`"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect daily competitor creatives via Atria")
    parser.add_argument("--date", help="Run date as YYYY-MM-DD (default: today)")
    args = parser.parse_args()

    run_date = date.fromisoformat(args.date) if args.date else date.today()

    manifest = collect(run_date)
    previous = load_previous_manifest(run_date)
    report_path = write_report(run_date, manifest, previous)

    print(f"Collected {len(manifest['ads'])} competitor creatives for {run_date.isoformat()}")
    if manifest["errors"]:
        print(f"  {len(manifest['errors'])} query error(s) — see manifest.json")
    print(f"  Report: {report_path}")


if __name__ == "__main__":
    main()
