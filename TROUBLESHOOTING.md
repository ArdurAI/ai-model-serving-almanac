# Troubleshooting & Debugging

How to understand the model serving almanac codebase, debug issues, and resolve common problems when working with the almanac or reproducing benchmarks.

## Table of Contents

1. [Understanding the Codebase](#understanding-the-codebase)
2. [Common Issues](#common-issues)
3. [Debugging the Data Pipeline](#debugging-the-data-pipeline)
4. [Debugging Benchmark Runs](#debugging-benchmark-runs)
5. [FAQ](#faq)
6. [Getting Help](#getting-help)

---

## Understanding the Codebase

### High-level flow

```
Research Agents → Research Output (Markdown) →
  Python Script → roster.json (Structured Data) →
    Manual Review → Edition Markdown →
      Git Commit → GitHub Publication
```

### Key files and their roles

| File | Role | When to read it |
|------|------|-----------------|
| `README.md` | Project overview, quick reference, roster at a glance | First thing you read |
| `INTENT.md` | Philosophy, why we do things this way, core principles | When you disagree with a decision or need context on methodology |
| `IMPLEMENTATION.md` | How things are built, how to add engines, adapter patterns | When you want to contribute or add an engine |
| `TESTING.md` | Benchmark methodology, scoring rubrics, failure taxonomy | When you want to reproduce or challenge a result |
| `TROUBLESHOOTING.md` | This file | When something is broken or you need to debug |
| `architecture.md` | Serving stack architecture diagram | When you want to understand the big picture |
| `editions/YYYY-MM.md` | Monthly snapshot of the inference landscape | When you want historical data or trend analysis |
| `data/roster.json` | Machine-readable catalog of engines | When you want to query or analyze the engine data |
| `methodology/benchmark-harness.md` | Harness specification for serving workloads | When you want to build an adapter or run benchmarks |
| `benchmarks/*.json` | Raw benchmark results per engine per suite | When you want to re-analyze or challenge a score |

### The data model

The almanac is fundamentally a **directed graph** of data:

```
Research findings → Engine metadata → Roster JSON → Edition Markdown → README
                                      ↓
                               Benchmark results → Per-engine pages
```

- **Research findings** are the raw output of the research swarm. They're saved in `research/` (not in the public repo).
- **Engine metadata** is extracted from research and stored in `data/roster.json`.
- **Roster JSON** is the single source of truth. Everything else derives from it.
- **Edition markdown** is human-written based on the roster and research.
- **README** is auto-generated from the roster and the latest edition.
- **Benchmark results** are machine-generated and stored in `benchmarks/`; they are never overwritten, only appended.

### Understanding `data/roster.json`

This is the most important file in the repo. It is the single source of truth.

**Structure**:
```json
{
  "meta": { ... },
  "categories": {
    "model-serving": {
      "name": "Model Serving & Inference Engines",
      "description": "...",
      "estimated_total": N,
      "tools": [
        { "name": "...", "type": "...", "license": "...", "tier": "A|B|C", "supported_formats": [...], "supported_quantization": [...], "hardware_target": "...", "notes": "..." }
      ]
    }
  }
}
```

**How to query it**:
```bash
# Find all Tier A engines
jq '.categories."model-serving".tools[] | select(.tier == "A") | .name' data/roster.json

# Count engines by tier
jq '.categories."model-serving".tools | group_by(.tier) | map({tier: .[0].tier, count: length})' data/roster.json

# Find all engines that support FP8
jq '.categories."model-serving".tools[] | select(.supported_quantization[] | contains("fp8")) | .name' data/roster.json

# Find all GPU-targeted engines
jq '.categories."model-serving".tools[] | select(.hardware_target == "GPU") | .name' data/roster.json
```

### The edition markdown

Editions are **human-written** summaries, not machine-generated. They are based on the roster but include analysis, interpretation, and narrative that a machine can't produce.

**How editions are structured**:
1. Front matter: date, research method, hardware context (GPU class used for benchmarks this month)
2. Landscape at a glance: summary table by tier
3. Per-tier sections: findings, roster, analysis, notable releases
4. Hardware-specific notes: A100 vs H100 results, single-node vs multi-node observations
5. Quest diary: what was tested this month, which engines, which regressions found
6. Cross-category findings: patterns that span categories (e.g., "all engines added FP8 this month")

### The benchmark harness (separate repo)

The actual benchmark code lives in a separate repository. The almanac repo contains:
- The methodology specification
- The results (JSON + markdown)
- The adapter interface definitions

The harness repo contains:
- The runner code
- The adapter implementations (LLMPerf, AnyScale, custom)
- The GPU telemetry collector (nvidia-smi / pynvml integration)
- The judge model integration (for accuracy/quality scoring)
- The perplexity and logits divergence graders

**Why separate?** Because the harness is code that runs on GPU machines, and the almanac is data that is published. They have different lifecycles, different audiences, and different hardware requirements (the harness needs GPUs; the almanac repo does not).

## Common Issues

### Issue: `roster.json` is invalid JSON

**Symptoms**:
- `jq` fails to parse it
- GitHub Actions fails on JSON validation
- Python `json.load()` raises `JSONDecodeError`

**Diagnosis**:
```bash
python3 -c "import json; json.load(open('data/roster.json'))"
```

**Resolution**:
1. Find the line with the error: `python3 -m json.tool data/roster.json`
2. Common causes: trailing commas, unescaped quotes in engine names, incorrect nesting of `supported_formats` or `supported_quantization` arrays
3. Fix the JSON and re-validate
4. Consider using a JSON linter in your editor

### Issue: Edition markdown has broken links

**Symptoms**:
- Links to per-engine pages return 404
- Links to benchmark JSON files don't exist yet
- Relative links work locally but break on GitHub

**Diagnosis**:
```bash
# Check all links in the repo
find . -name "*.md" -exec grep -oP '\[.*?\]\(.*?\)' {} + | grep -v "http" | grep -v "mailto"
```

**Resolution**:
1. For internal links, use relative paths: `../benchmarks/llmperf-vllm-2026-06.json`
2. For external links, verify the URL is correct (engine homepages, GitHub repos, benchmark suites)
3. For engines without a per-engine page yet, link to their GitHub repo or homepage
4. Run a link checker as part of CI

### Issue: Tier assignment is wrong

**Symptoms**:
- An engine is Tier A but has no production serving references
- An engine is Tier C but is widely adopted in production (e.g., at a major cloud provider)
- An engine's tier changed without explanation in the edition notes

**Diagnosis**:
1. Check the tier assignment rules in `IMPLEMENTATION.md`
2. Verify the engine's adoption, activity, and community health (GitHub stars, last push, Discord activity, production references)
3. Check the edition notes for the rationale

**Resolution**:
1. File an issue with evidence (GitHub stars, last push, production references, benchmark results)
2. The tier will be reviewed in the next edition cycle
3. Tiers are not changed mid-edition; they are updated at edition boundaries

### Issue: Benchmark results can't be reproduced

**Symptoms**:
- Running the harness produces different TTFT/TPOT numbers
- The adapter fails with a different engine version or CUDA version
- The GPU class doesn't match the published results (e.g., A100 vs H100)
- The model checkpoint SHA-256 doesn't match

**Diagnosis**:
1. Check the `results.json` metadata for the exact commit, seed, hardware, CUDA version, PyTorch version, and model checkpoint SHA-256
2. Check if the engine version has changed since the published run (engine versions are the #1 source of variance)
3. Check if the CUDA/PyTorch version matches (e.g., vLLM 0.6.x requires CUDA 12.1, not 11.8)
4. Verify the GPU class matches (A100 vs H100 results are **not comparable** due to different memory bandwidth and SM counts)

**Resolution**:
1. Use the exact commit, dependencies, and model checkpoint from the results metadata
2. If the engine version changed, the results are for a different version — this is expected and documented
3. If the CUDA version changed, that's an environment issue — use the documented CUDA version
4. If the GPU class changed, compare only within the same GPU class (results are hardware-specific)

### Issue: Adapter fails on GPU setup

**Symptoms**:
- `setup()` crashes with `CUDA not available`
- `load()` throws `RuntimeError: CUDA out of memory` during model loading
- The engine starts but uses CPU instead of GPU (silent fallback)
- `NCCL` errors on multi-GPU setups

**Diagnosis**:
1. Check `nvidia-smi` output: is the GPU visible? Is memory already occupied by a zombie process?
2. Check `CUDA_VISIBLE_DEVICES` is set correctly in the adapter
3. Check the engine's CUDA version requirement matches the host CUDA version
4. Check if another engine's adapter left a zombie process holding GPU memory

**Resolution**:
- Missing GPU → Check driver installation, run `nvidia-smi`
- CUDA version mismatch → Install the correct CUDA version or use the engine's Docker image
- OOM during load → Use a smaller model, enable quantization, or use a GPU with more memory
- CPU fallback → Check if the engine was compiled with CUDA support; reinstall with CUDA-enabled wheels
- Zombie process → Kill orphaned processes: `nvidia-smi | grep python` and `kill -9` if needed; always run `teardown()`
- NCCL error → Set `NCCL_P2P_DISABLE=1` or `NCCL_IB_DISABLE=1` for problematic GPU topologies; check the engine docs

### Issue: Benchmark results inconsistent due to hardware differences

**Symptoms**:
- Same engine, same test, different results across runs on different machines
- TTFT varies by 20%+ between A100 and H100 (expected, but confusing)
- Throughput varies based on GPU temperature / thermal throttling
- Results differ between single-node and multi-node runs

**Diagnosis**:
1. Check GPU class (A100, H100, RTX 4090) — results are **not comparable across classes**
2. Check if GPU was thermally throttling during the run (`nvidia-smi` shows temperature and clock throttling)
3. Check if other processes were using the GPU during the benchmark
4. Check if the engine uses non-deterministic features (e.g., FlashAttention with `torch.compile` may have variance)

**Resolution**:
1. Always tag results with GPU class; never merge A100 and H100 results
2. Allow GPU to cool between runs; run a warm-up period before measurement
3. Ensure exclusive GPU access during benchmarks (no other processes)
4. Set `temperature=0.0` and fixed seeds for all generation; disable non-deterministic optimizations if variance is excessive

### Issue: Quantization configuration mismatches

**Symptoms**:
- Engine loads quantized weights but accuracy is far worse than expected
- Quantized model loads but silently falls back to fp16 (no memory savings)
- Engine claims FP8 support but requires specific hardware (H100) and fails on A100
- `quantization_config` in the checkpoint doesn't match the engine's expected format

**Diagnosis**:
1. Check the exact quantization scheme used: AWQ, GPTQ, FP8, INT8, Marlin, etc.
2. Check if the engine supports the quantization scheme natively or requires a conversion step
3. Check GPU compatibility: FP8 requires Hopper (H100); some INT8 kernels require Ampere or newer
4. Check if the model checkpoint was quantized with the same scheme the engine expects

**Resolution**:
- Mismatched quantization scheme → Re-quantize with the engine's recommended recipe or use a different engine
- Silent fallback to fp16 → Check engine logs for warnings; verify quantization config is passed correctly
- Hardware-incompatible quantization → Use a GPU that supports the quantization scheme or switch to a compatible scheme
- Accuracy loss → Run the accuracy benchmark (MMLU/GSM8K) to quantify the loss; compare against the reference fp16 result

### Issue: Research agent missed an engine

**Symptoms**:
- A well-known inference engine is not in the roster
- An engine from a specific region (e.g., China) is missing
- A newly launched engine is not in the latest edition

**Diagnosis**:
1. Check if the engine meets triage criteria in `IMPLEMENTATION.md`
2. Check if it was added in a previous edition and later removed (dead/abandoned)
3. Check if it falls outside the search scope (e.g., not a serving engine but a training framework)

**Resolution**:
1. File an issue with the engine name, URL, evidence of adoption/activity, and hardware targets
2. The engine will be triaged for the next edition
3. If it meets criteria, it will be added and smoke-gated

### Issue: Monthly update cron failed

**Symptoms**:
- No new edition was published on the 15th
- The cron job is missing from the scheduler
- The research agent timed out during GPU benchmark runs

**Diagnosis**:
```bash
# Check cron status
cron status

# Check the cron job list
# (use the Kimi Work cron interface)
```

**Resolution**:
1. Check if the cron job is still registered
2. Check if the research agent timed out (GPU benchmarks can take hours; increase timeout if needed)
3. Manually trigger the update if the cron missed a cycle
4. Check the workspace path in the cron job configuration

### Issue: GitHub push fails

**Symptoms**:
- `git push` returns 403 or 401
- The remote is not configured
- The branch is behind origin

**Diagnosis**:
```bash
git remote -v
git status
git log --oneline -5
```

**Resolution**:
1. Verify the remote URL is correct: `git remote set-url origin https://github.com/ArdurAI/...`
2. Verify GitHub CLI auth: `gh auth status`
3. If behind origin, pull first: `git pull origin main`
4. If there are conflicts, resolve them manually

## Debugging the Data Pipeline

### Research output → roster.json

**Problem**: Research agents produce markdown, but the roster JSON is incomplete or wrong.

**Debug steps**:
1. Read the research output files in `research/` (local workspace, not in the repo)
2. Check if the Python extraction script correctly parsed the engine tables
3. Check if engines were dropped during triage (check the triage log)
4. Verify the JSON schema is correct (including `supported_formats`, `supported_quantization`, `hardware_target`)

**Common bugs**:
- Engine names with special characters break JSON parsing → Escape them properly
- Engines with no tier get dropped → Default to Tier C if unsure
- Engines with no `supported_formats` get empty arrays → Add the formats from the engine docs
- Engines with no `hardware_target` get blank → Infer from docs (GPU/CPU/Edge/Multi-node)

### roster.json → edition markdown

**Problem**: The edition doesn't reflect the roster.

**Debug steps**:
1. Compare the engine counts in the roster vs. the edition
2. Check if the edition was written before the roster was updated
3. Check if engines were manually edited in the edition but not in the roster

**Resolution**:
1. The edition should be derived from the roster, not the other way around
2. If the edition has manual additions, ensure they are also in the roster
3. The edition is a human-readable summary; the roster is the source of truth

### Edition markdown → README

**Problem**: The README roster-at-a-glance doesn't match the latest edition.

**Debug steps**:
1. Check which edition is referenced in the README
2. Check if the README was updated after the edition was published

**Resolution**:
1. The README should always reference the latest edition
2. Update the README when a new edition is published
3. Consider automating README updates from the roster JSON

## Debugging Benchmark Runs

### The adapter fails

**Symptoms**:
- `setup()` crashes with CUDA or dependency errors
- `load()` throws an exception during model weight loading
- `query()` returns empty responses or non-JSON output
- `batch_query()` causes a deadlock or OOM

**Debug steps**:
1. Run the adapter in isolation (without the harness) on a single request
2. Check the engine's documentation for GPU requirements and setup steps
3. Check if environment variables are set (`CUDA_VISIBLE_DEVICES`, `NCCL_P2P_DISABLE`, etc.)
4. Check if the engine version matches what the adapter expects
5. Check `nvidia-smi` for GPU availability and memory state

**Common fixes**:
- Missing CUDA / wrong CUDA version → Use the engine's Docker image or reinstall with correct CUDA
- Missing API key → For cloud endpoints, set the environment variable; for self-hosted, use a dummy key
- Wrong engine version → Update the adapter or pin the version in the adapter's `setup()`
- Dependency conflict → Use a virtual environment or container per engine; do not mix engines in the same env
- Model format mismatch → Convert weights to the format the engine expects (e.g., `trtllm-build` for TensorRT-LLM)
- GPU OOM → Reduce batch size, enable quantization, or use a smaller model for testing

### The canary fails

**Symptoms**:
- The naive `transformers` baseline scores better than expected on throughput (suspicious)
- The naive baseline shows impossible latency improvements
- GPU telemetry shows no utilization during the canary run (indicates CPU-only execution)

**Debug steps**:
1. Check if the harness accidentally enabled optimizations for the canary
2. Check if the model was cached or pre-warmed outside the measurement window
3. Check if the GPU was already warm from a previous run
4. Check if the naive baseline was accidentally configured with FlashAttention or another optimization

**Resolution**:
1. The canary must use raw `AutoModelForCausalLM` with no optimizations, no FlashAttention, no quantization
2. Ensure a cold start: reboot the GPU process or clear caches between runs
3. If the canary is biased, the entire batch is invalid — fix the harness and rerun all tests

### Results are inconsistent

**Symptoms**:
- Same engine, same test, different TTFT/TPOT across runs
- Scores vary by more than the confidence interval
- Throughput drops on the second run (thermal throttling or memory leak)

**Debug steps**:
1. Check if the engine has non-deterministic behavior (e.g., `torch.compile` with different kernels, dynamic batching decisions)
2. Check if the hardware was different between runs (GPU class, driver version)
3. Check if the engine version changed between runs
4. Check GPU temperature and clock speed across runs (`nvidia-smi` logs)

**Resolution**:
1. Set `temperature=0.0` and fixed seeds for all generation; disable non-deterministic features if possible
2. Record hardware specs (GPU class, driver version, CUDA version) in the results metadata
3. Pin engine versions and record them; re-run with identical versions for reproduction
4. Allow GPU cool-down between runs; monitor for thermal throttling
5. Check for memory leaks between runs (KV cache not released, GPU memory not freed)

## FAQ

### Q: Why is engine X not in the roster?

A: Either it doesn't meet triage criteria (seriousness, activity, documentation, accessibility, scope), it hasn't been discovered yet, or it was removed for inactivity. File an issue with evidence (GitHub repo, release history, production references) and we'll triage it.

### Q: Why did engine X's score change?

A: Either the engine was updated (new version), the methodology was refined (new benchmark or weight adjustment), we found a bug in our previous test, or the hardware changed. All four are valid reasons. Check the edition notes for the rationale. Engine version changes are the most common cause.

### Q: Can I run the benchmarks myself?

A: Yes. The harness is published separately. Clone it, install dependencies (matching CUDA and PyTorch versions), download the exact model weights, and run the adapter for the engine you want to test. See `TESTING.md` for reproducibility instructions. You will need a GPU (A100 or H100 recommended for comparable results).

### Q: How do I challenge a ranking?

A: File an issue with specific evidence. Check the raw results JSON (per-request TTFT/TPOT), the adapter code, and the harness configuration. If you find a real problem (e.g., "adapter used wrong batching flag"), we'll re-run or update the methodology.

### Q: Can I add an engine to the roster?

A: Yes. See `CONTRIBUTING.md` for instructions. The engine must meet triage criteria and pass the smoke gate (deploy model → send request → verify response + GPU utilization).

### Q: Why are results hardware-specific?

A: Inference performance is fundamentally tied to GPU memory bandwidth, SM count, and architecture (Ampere vs Hopper). A100 and H100 results differ significantly and are never merged. Always check the hardware class before comparing results.

### Q: Why are there separate category almanacs?

A: Each category is deep enough to warrant its own dedicated repo with per-tool pages, category-specific benchmarks, and focused community. The parent almanac (`ai-infrastructure-almanac`) is the master catalog that cross-references all categories.

### Q: How often are benchmarks re-run?

A: Standard: every quarter for each engine tier. Stress: annually. Integration: quarterly. If an engine releases a major version (e.g., vLLM 0.5 → 0.6), we may re-run early. If CUDA or PyTorch has a major release, we may re-run the full roster.

### Q: What's the difference between Tier A, B, and C?

A: Tier A = market leader in throughput/adoption or strongest technical merit with proven production serving. Tier B = solid option, actively maintained, good for specific use cases (e.g., edge, specific quantization). Tier C = niche, early-stage, or highly specialized. See `IMPLEMENTATION.md` for full rules.

### Q: Can vendors sponsor the almanac?

A: No. The almanac is independently funded. Sponsorship would compromise the core mission. Vendors can improve their scores by actually improving their engines or fixing the bugs we document.

### Q: Why do you test on both A100 and H100?

A: Different GPU classes have different strengths. H100 has FP8 Tensor Cores and much higher memory bandwidth; A100 is the most common production GPU. Testing on both gives a complete picture of where an engine excels or struggles.

### Q: How do you handle quantization accuracy?

A: Every quantized run is compared against a reference fp16 run on the same engine (or naive baseline). We measure perplexity delta on WikiText-2 / C4, exact-match drop on MMLU / GSM8K, and logits KL divergence. A quantization scheme that saves 50% memory but drops 10% accuracy is documented as a trade-off, not a win.

## Getting Help

### File an issue

GitHub issues are the primary support channel. Use the appropriate template:

- **Engine request**: "Add [Engine Name] to Model Serving roster"
- **Data correction**: "[Engine Name] metadata is wrong: [what's wrong]"
- **Benchmark challenge**: "Challenge [Engine Name] ranking on [Dimension]: [evidence]"
- **Bug report**: "[Bug description] in [file/process]"
- **Feature request**: "[Feature description] for [use case]"

### Discussion

GitHub Discussions are for:
- General questions about the almanac
- Sharing experiences with engines on the roster
- Proposing methodology changes
- Community announcements
- Hardware-specific tips and tricks

### Email

For private or sensitive inquiries: Use the contact info in the ArdurAI org profile.

## License

Content: CC BY 4.0
