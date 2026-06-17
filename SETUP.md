# Setup Guide

How to push the AI Model Serving Almanac to GitHub and set up the development environment.

## Prerequisites

- Git
- GitHub CLI (`gh`) or a GitHub account with SSH keys configured
- Python 3.10+ (for scripts)
- `jq` (optional, for querying `roster.json`)

## Initial Setup

```bash
# Clone the repo (if you haven't already)
git clone https://github.com/ArdurAI/ai-model-serving-almanac.git
cd ai-model-serving-almanac

# Verify the roster JSON is valid
python3 -c "import json; json.load(open('data/roster.json'))"

# Verify all tool pages exist
ls tools/ | wc -l
# Expected: 47
```

## GitHub Repository Configuration

```bash
# Set the remote (if not already set)
git remote add origin https://github.com/ArdurAI/ai-model-serving-almanac.git

# Or via SSH
git remote add origin git@github.com:ArdurAI/ai-model-serving-almanac.git

# Verify
 git remote -v
```

## Making Changes

```bash
# Edit files, then commit
git add -A
git commit -m "Update: description of changes"

# Push to GitHub
git push origin main
```

## Monthly Update Workflow

1. Run the roster enrichment script if needed:
   ```bash
   python3 scripts/enrich_roster.py
   ```
2. Update `data/roster.json` with new metadata (stars, last push, releases).
3. Create a new edition in `editions/YYYY-MM.md`.
4. Update `README.md` with the latest roster-at-a-glance.
5. Commit and push.

## CI / GitHub Actions (Optional)

A GitHub Actions workflow can be configured for automatic metadata refresh. See `IMPLEMENTATION.md` for the workflow template.

## License

Content: CC BY 4.0
