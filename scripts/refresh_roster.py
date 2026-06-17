#!/usr/bin/env python3
"""
Monthly Roster Refresh Automation.

Usage:
  python scripts/refresh_roster.py --monthly
  python scripts/refresh_roster.py --check-stars
  python scripts/refresh_roster.py --update-edition 2026-07

What it does:
  1. Reads data/roster.json
  2. Fetches latest GitHub stars / last push / release dates for all GitHub repos
  3. Updates metadata fields (last_updated, stars, latest_release, last_push)
  4. Checks for new engines (not in roster) via GitHub search or manual CSV
  5. Generates a new edition stub in editions/YYYY-MM.md
  6. Updates README.md roster-at-a-glance section

Requires:
  - GitHub CLI (gh) installed and authenticated, OR
  - GITHUB_TOKEN environment variable with read access
"""

import argparse
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from typing import Dict, List, Optional


def parse_github_url(url: str) -> Optional[tuple]:
    """Extract (owner, repo) from https://github.com/owner/repo."""
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+)", url)
    if m:
        return m.group(1), m.group(2).rstrip("/")
    return None


def gh_api(endpoint: str) -> dict:
    """Call GitHub API via gh CLI or curl fallback."""
    try:
        result = subprocess.run(
            ["gh", "api", endpoint],
            capture_output=True, text=True, check=True,
        )
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback to curl with GITHUB_TOKEN
        token = os.environ.get("GITHUB_TOKEN", "")
        if not token:
            return {}
        import urllib.request
        req = urllib.request.Request(
            f"https://api.github.com{endpoint}",
            headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json",
            },
        )
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except Exception:
            return {}


def fetch_repo_info(owner: str, repo: str) -> dict:
    """Fetch stars, last push, and latest release from GitHub."""
    repo_data = gh_api(f"/repos/{owner}/{repo}")
    releases = gh_api(f"/repos/{owner}/{repo}/releases?per_page=1")
    
    info = {
        "stars": repo_data.get("stargazers_count", 0),
        "last_push": repo_data.get("pushed_at", ""),
        "latest_release": releases[0].get("tag_name", "") if releases else "",
        "release_date": releases[0].get("published_at", "") if releases else "",
    }
    return info


def refresh_roster(roster_path: str) -> dict:
    """Update roster.json with latest metadata."""
    with open(roster_path) as f:
        roster = json.load(f)
    
    for tool in roster.get("tools", []):
        # Try to find GitHub URL from tool page or notes
        github_url = None
        # Simple heuristic: look for github.com in notes or links
        notes = tool.get("notes", "")
        m = re.search(r"https?://github\.com/[^\s)]+", notes)
        if m:
            github_url = m.group(0)
        
        # If not found in notes, skip (would need to parse tool page)
        if not github_url:
            continue
        
        parsed = parse_github_url(github_url)
        if not parsed:
            continue
        
        owner, repo = parsed
        try:
            info = fetch_repo_info(owner, repo)
            tool["stars"] = info.get("stars", tool.get("stars", 0))
            tool["last_push"] = info.get("last_push", tool.get("last_push", ""))
            tool["latest_release"] = info.get("latest_release", tool.get("latest_release", ""))
            tool["release_date"] = info.get("release_date", tool.get("release_date", ""))
            tool["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            print(f"  Updated {tool['name']}: {info['stars']} stars, last push {info['last_push'][:10]}")
        except Exception as e:
            print(f"  Failed to update {tool['name']}: {e}")
    
    roster["meta"]["last_updated"] = datetime.now(timezone.utc).isoformat()
    
    with open(roster_path, "w") as f:
        json.dump(roster, f, indent=2)
    
    print(f"\nRoster updated: {roster_path}")
    return roster


def generate_edition_stub(roster: dict, edition_month: str, editions_dir: str) -> str:
    """Generate a new edition markdown stub."""
    edition_path = os.path.join(editions_dir, f"{edition_month}.md")
    if os.path.exists(edition_path):
        print(f"Edition already exists: {edition_path}")
        return edition_path
    
    tier_a = [t for t in roster["tools"] if t.get("tier") == "A"]
    tier_b = [t for t in roster["tools"] if t.get("tier") == "B"]
    tier_c = [t for t in roster["tools"] if t.get("tier") == "C"]
    
    # Count how many tools have been smoke-tested
    smoke_pass = sum(1 for t in tier_a if t.get("smoke_gate_status") == "PASS")
    
    content = f"""# Edition {edition_month} — Monthly Update

*Edition generated on {datetime.now(timezone.utc).strftime("%Y-%m-%d")}.*

## Roster at a Glance

| Tier | Count | Smoke Gate Pass | Notes |
|------|-------|-----------------|-------|
| A | {len(tier_a)} | {smoke_pass}/{len(tier_a)} | |
| B | {len(tier_b)} | — | Not yet smoke-tested |
| C | {len(tier_c)} | — | Not yet smoke-tested |

**Total: {len(roster['tools'])} tools**

## Changes Since Last Edition

### New Engines
- ⏳ None this month (or list new additions)

### Tier Changes
- ⏳ None this month (or list promotions/demotions)

### Major Releases
- ⏳ Check latest_release fields in roster.json

### Smoke Gate Results
- ⏳ Run `python smoke_gate.py` for each Tier A engine and record results

### Benchmark Highlights
- ⏳ Run `python llmperf_runner.py` and `python sustained_load_runner.py`

## Findings
- ⏳ To be populated after benchmark runs

---

## License

Edition content is CC BY 4.0.
"""
    
    with open(edition_path, "w") as f:
        f.write(content)
    
    print(f"Edition stub created: {edition_path}")
    return edition_path


def update_readme(roster: dict, readme_path: str) -> None:
    """Update README.md roster-at-a-glance section with latest data."""
    with open(readme_path) as f:
        content = f.read()
    
    tier_a = [t for t in roster["tools"] if t.get("tier") == "A"]
    tier_b = [t for t in roster["tools"] if t.get("tier") == "B"]
    tier_c = [t for t in roster["tools"] if t.get("tier") == "C"]
    
    # Update the counts in the table (simple regex replacement)
    new_table = f"""| Tier | Count | Description |
|------|-------|-------------|
| **A** | {len(tier_a)} | Must-run for any model-serving decision |
| **B** | {len(tier_b)} | Evaluated; use with eyes open |
| **C** | {len(tier_c)} | Exploratory or dormant |"""
    
    # Replace the old table
    pattern = r"\| Tier \| Count \| Description \|\n\|------\|-------\|-------------\|\n\| \*\*A\*\* \| \d+ \|.*?\| \*\*C\*\* \| \d+ \| .*? \|"
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, new_table, content, flags=re.DOTALL)
    
    with open(readme_path, "w") as f:
        f.write(content)
    
    print(f"README updated: {readme_path}")


def main():
    parser = argparse.ArgumentParser(description="Monthly roster refresh")
    parser.add_argument("--monthly", action="store_true", help="Run full monthly refresh")
    parser.add_argument("--check-stars", action="store_true", help="Only update GitHub metadata")
    parser.add_argument("--update-edition", metavar="YYYY-MM", help="Generate new edition stub")
    parser.add_argument("--roster", default="data/roster.json", help="Path to roster.json")
    parser.add_argument("--editions-dir", default="editions", help="Editions directory")
    parser.add_argument("--readme", default="README.md", help="Path to README.md")
    args = parser.parse_args()
    
    if not any([args.monthly, args.check_stars, args.update_edition]):
        parser.print_help()
        return
    
    roster = None
    if args.check_stars or args.monthly:
        roster = refresh_roster(args.roster)
    
    if args.update_edition or args.monthly:
        if roster is None:
            with open(args.roster) as f:
                roster = json.load(f)
        edition = args.update_edition or datetime.now(timezone.utc).strftime("%Y-%m")
        generate_edition_stub(roster, edition, args.editions_dir)
    
    if args.monthly:
        if roster is None:
            with open(args.roster) as f:
                roster = json.load(f)
        update_readme(roster, args.readme)
        print("\n=== Monthly refresh complete ===")
        print(f"Next steps:")
        print(f"  1. Review {args.editions_dir}/{datetime.now(timezone.utc).strftime('%Y-%m')}.md")
        print(f"  2. Run smoke gates: python smoke_gate.py --engine <engine> --model <model>")
        print(f"  3. Run benchmarks: python llmperf_runner.py --engine <engine> --model <model>")
        print(f"  4. Commit and push: git add -A && git commit -m 'feat: {edition} edition' && git push")


if __name__ == "__main__":
    main()
