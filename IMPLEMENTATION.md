# Implementation Guide

How the model serving almanac is built, how to add an inference engine, how to update an edition, and how the data pipeline works.

## Table of Contents

1. [Repository Structure](#repository-structure)
2. [The Data Pipeline](#the-data-pipeline)
3. [Adding a New Engine](#adding-a-new-engine)
4. [Updating an Edition](#updating-an-edition)
5. [The Roster JSON Schema](#the-roster-json-schema)
6. [Directory Conventions](#directory-conventions)
7. [Building the Adapter](#building-the-adapter)
8. [Automation](#automation)

---

## Repository Structure

```
ai-model-serving-almanac/
├── README.md                          # Project overview + roster at a glance
├── INTENT.md                          # Philosophy, design principles, governance
├── IMPLEMENTATION.md                  # This file
├── TESTING.md                         # Benchmark methodology, harness details
├── TROUBLESHOOTING.md                 # Common issues, debugging, FAQ
├── CONTRIBUTING.md                    # How to contribute
├── architecture.md                    # Serving stack architecture + test philosophy
├── SETUP.md                           # How to push to GitHub
├── .gitignore
│
├── editions/                          # Monthly editions
│   └── 2026-06.md                   # Founding edition
│
├── benchmarks/                        # Benchmark results (rolling)
│   └── (populated as results land)
│       ├── llmperf-<engine>-<date>.json
│       ├── anyscale-<engine>-<date>.json
│       └── throughput-<engine>-<date>.json
│
├── methodology/
│   └── benchmark-harness.md         # Detailed harness spec for serving workloads
│
├── data/
│   └── roster.json                  # Machine-readable catalog (47+ engines)
│
├── tools/                             # Per-engine deep-dive pages (placeholder)
│   └── (populated as deep-dives are written)
│       ├── vllm.md
│       ├── sglang.md
│       └── ...
│
└── assets/                            # Charts, diagrams, GPU telemetry screenshots
    └── (populated by editions)
        ├── ttft-p50-2026-06.png
        ├── throughput-vs-concurrency-2026-06.png
        └── gpu-memory-heatmap-2026-06.png
```

## The Data Pipeline

The almanac data flows through four stages:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Discovery      │────▶│  Triage         │────▶│  Research       │────▶│  Publication    │
│  (find engines) │     │  (decide entry) │     │  (deep dive)    │     │  (write edition)│
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Stage 1: Discovery

Engines are discovered through:
- **Monthly research swarm**: Parallel agents search for new inference engines, serving platforms, and deployment tools
- **Community submissions**: Issues, PRs, email, social media (e.g., "Have you tested X?")
- **Vendor announcements**: NVIDIA, AnyScale, Hugging Face, major releases (e.g., TensorRT-LLM 0.10, vLLM 0.6)
- **GitHub trending**: New repos with significant star growth in the LLM serving space
- **Conference talks**: MLSys, NeurIPS Datasets & Benchmarks, papers on serving systems
- **Upstream ecosystem changes**: New CUDA versions, new PyTorch releases, new quantization formats (e.g., FP8, Marlin)

### Stage 2: Triage

An engine enters the roster if it meets ALL of these criteria:
1. **Seriousness**: Not a toy/demo. Must have real throughput/latency claims, real users, or real backing (company, academic lab, or major cloud provider).
2. **Activity**: Last push or release within 6 months. Exceptions for "stable/mature" engines with proven production usage (e.g., TensorRT-LLM may have slower release cadence but is widely deployed).
3. **Documentation**: Must have a README, docs, or at least a landing page explaining how to serve a model and what hardware it supports.
4. **Accessibility**: Must be accessible to test (open source, free tier, or evaluation license available). Must support at least one publicly available model (e.g., Llama 3, Mistral, Qwen).
5. **Scope**: Must fit the model serving category. A general-purpose ML framework (e.g., raw PyTorch) doesn't enter unless it includes a dedicated serving layer.

An engine is **excluded** if:
- It's a fork of another engine with no meaningful divergence in serving behavior
- It's a thin wrapper around another engine with no added value (e.g., a CLI that just calls `vllm serve`)
- It has no evidence of real-world inference usage (no users, no community, no production references)
- It requires an enterprise-only license with no evaluation path for independent benchmarking
- It only supports proprietary models with no open weights available for testing

### Stage 3: Research

For each new engine, we collect:
- Name, type (Inference Engine, Serving Platform, Edge Runtime), license, language, GitHub URL, stars
- Last push date, release cadence, CUDA/PyTorch version requirements
- Supported model formats (Safetensors, GGUF, ONNX, TensorRT engine, etc.)
- Supported quantization schemes (AWQ, GPTQ, FP8, INT8, INT4, Marlin, etc.)
- Key features and differentiators (continuous batching, speculative decoding, prefix caching, PD-disaggregation)
- Known bugs and sharp edges (from smoke gate): OOM behavior, batching fairness, scheduling bugs
- Community health (issues, PRs, maintainer responsiveness, Discord/Slack activity)
- GPU requirements and multi-node support

This data is stored in `data/roster.json` and summarized in the edition.

### Stage 4: Publication

The edition is a markdown file that includes:
- Landscape at a glance table (engines by tier, throughput class, hardware target)
- Per-tier findings and trends (e.g., "Tier A engines all added FP8 support this month")
- New engines added and engines removed
- Notable releases and acquisitions (e.g., NVIDIA Dynamo launch, major vLLM release)
- Quest diary (what was tested this month: which engines, which benchmarks, which hardware)
- Hardware-specific notes (results on A100 vs H100, single-node vs multi-node)

## Adding a New Engine

### Step 1: Verify the engine meets triage criteria

Check: seriousness, activity, documentation, accessibility, scope.

### Step 2: Add to the roster JSON

Edit `data/roster.json` and add the engine to the `model-serving` category:

```json
{
  "name": "EngineName",
  "type": "Inference Engine|Serving Platform|Edge Runtime",
  "license": "License",
  "region": "Region",
  "tier": "A|B|C",
  "supported_formats": ["safetensors", "gguf", "onnx"],
  "supported_quantization": ["fp16", "fp8", "awq", "gptq"],
  "hardware_target": "GPU|CPU|Edge|Multi-node",
  "notes": "One-line description and key differentiators"
}
```

**Tier assignment rules**:
- **Tier A**: Market leader in throughput or adoption, or strongest technical merit with proven production usage at scale. Must be actively maintained and have real multi-user serving references.
- **Tier B**: Solid option, actively maintained, but not the market leader. Good for specific use cases (e.g., edge deployment, specific quantization scheme, specific model family).
- **Tier C**: Niche, early-stage, or highly specialized. Worth knowing about but not a default choice for general model serving.

### Step 3: Update the edition

Add the engine to the model serving section in `editions/YYYY-MM.md`. If the engine is Tier A, add it to the roster-at-a-glance table in the README.

### Step 4: Update the per-engine deep-dive (if applicable)

If the engine is Tier A or has significant differentiation, create a stub in `tools/<engine-name>.md` with:
- Setup experience notes
- Supported model formats and quantization
- Known sharp edges from the smoke gate
- Links to benchmark results

### Step 5: Run the smoke gate

Before the engine is officially "in," it must pass the smoke gate (see TESTING.md). The smoke gate for model serving is:
1. **Deploy**: Start the engine with a standard model (e.g., Llama-3.1-8B-Instruct)
2. **Request**: Send a standard chat completion request via the engine's API
3. **Verify**: Confirm the response is non-empty, the JSON format matches the expected schema, and the GPU was actually utilized

If it fails, document the failure in the edition and assign it to Tier C with a note about the blocker.

### Step 6: Build the adapter

If the engine passes the smoke gate, build a `ModelServingAdapter` (see Building the Adapter below) so it can enter the standard benchmark pipeline.

## Updating an Edition

### Monthly update checklist

```
□ Check for new engines (discovery phase)
□ Triage new engines (add to roster or reject)
□ Update metadata for existing engines (stars, last push, releases, CUDA reqs)
□ Flag engines for removal (dead/abandoned, no longer maintained)
□ Run smoke gate for new engines
□ Run benchmark updates for re-tested engines (new versions, new CUDA)
□ Draft the edition markdown
□ Update README roster-at-a-glance
□ Update per-engine deep-dive stubs if needed
□ Commit and push
```

### Edition markdown template

```markdown
# Edition YYYY-MM — [Title]

*Research conducted YYYY-MM-DD. Hardware: [GPU class]. [Context about this month].*

## The landscape at a glance

| Tier | Engine Count | New This Month | Notable Changes |
|------|-------------|----------------|-----------------|
| A    | N           | ±N             | ...             |
| B    | N           | ±N             | ...             |
| C    | N           | ±N             | ...             |

## Model Serving — [Theme]

### Tier A roster
[table: name, type, throughput class, key differentiator, last release]

### Findings
[bullets: trends observed across engines this month]

### Hardware-specific notes
[bullets: A100 vs H100 results, single-node vs multi-node]

## Quest diary — [Month] [Year]

- [Engine tested, benchmark suite, key result, hardware used]
- [Regression found: e.g., "vLLM 0.6.x TTFT regression on long prefill"]

## Coming next month

[what's planned: new engines, new benchmarks, hardware changes]

## License
Content is licensed CC BY 4.0.
```

## The Roster JSON Schema

```json
{
  "meta": {
    "name": "Model Serving & Inference Engines Almanac Roster",
    "version": "YYYY-MM",
    "generated_at": "ISO-8601 timestamp",
    "total_engines": number,
    "categories": 1,
    "research_method": "description",
    "hardware_tested": ["A100-80GB", "H100-80GB", "RTX-4090"]
  },
  "categories": {
    "model-serving": {
      "name": "Model Serving & Inference Engines",
      "description": "Inference engines, model serving platforms, and deployment tools for LLMs and generative AI models",
      "estimated_total": number,
      "tools": [
        {
          "name": "Engine Name",
          "type": "Inference Engine|Serving Platform|Edge Runtime",
          "license": "License",
          "region": "Region",
          "tier": "A|B|C",
          "supported_formats": ["safetensors", "gguf", "onnx", "tensorrt"],
          "supported_quantization": ["fp16", "fp8", "awq", "gptq", "int8", "int4"],
          "hardware_target": "GPU|CPU|Edge|Multi-node",
          "notes": "Description"
        }
      ]
    }
  }
}
```

**Field definitions**:
- `name`: The engine's common name. Use the name the engine calls itself.
- `type`: What kind of serving tool is it? (e.g., "Inference Engine", "Serving Platform", "Edge Runtime")
- `license`: The primary license. Use SPDX identifiers where possible.
- `region`: Where the engine is primarily developed (US, EU, China, Global, etc.)
- `tier`: A, B, or C (see tier rules above)
- `supported_formats`: Model checkpoint formats the engine can load directly
- `supported_quantization`: Quantization schemes supported natively
- `hardware_target`: Primary deployment target (GPU server, CPU, edge device, multi-node cluster)
- `notes`: One-line description with key differentiators. Keep under 100 chars.

## Directory Conventions

### `editions/`
- One file per month: `YYYY-MM.md`
- Never delete old editions. The history is part of the record.
- New editions are appended; old editions are never rewritten.
- Hardware notes are included in every edition (what GPU class results were collected on).

### `data/`
- `roster.json` is the single source of truth for the engine catalog.
- It is machine-generated from the research process.
- It should be valid JSON at all times.

### `benchmarks/`
- One file per benchmark run: `<suite>-<engine>-<date>.json`
- Raw JSON files alongside summary markdown: `<suite>-<engine>-<date>.md`
- Raw data is never deleted. It is the audit trail.
- Naming convention: `llmperf-vllm-2026-06.json`, `anyscale-sglang-2026-06.json`, `throughput-tensorrt-llm-2026-06.json`

### `tools/`
- One file per engine: `<name>.md`
- Contains deep-dive analysis: setup experience, benchmark results, bug notes, comparison with peers, GPU requirements, quantization notes
- Populated as deep-dives are written (not all engines have a page immediately)

### `assets/`
- Images, charts, GPU telemetry screenshots referenced by editions and benchmarks
- Named descriptively: `ttft-p50-2026-06.png`, `throughput-vs-concurrency-2026-06.png`, `gpu-memory-heatmap-2026-06.png`

### `methodology/`
- The benchmark harness specification for serving workloads
- Frozen before any results are generated
- Changes require an RFC and a public announcement
- Includes: prompt mix, concurrency levels, model weights used, measurement hooks, GPU telemetry collection method

## Building the Adapter

When a new engine is added to the roster and is ready for benchmarking, an adapter must be built. The adapter is the bridge between the engine's serving API and the harness's fixed interface.

### The ModelServingAdapter contract

```python
class ModelServingAdapter:
    def setup(self, model_id: str, gpu_devices: List[int]) -> None:
        """Install, configure, and start the serving engine."""
        pass
    
    def load(self, model_path: str, quantization: Optional[str] = None) -> None:
        """Load the model weights into the engine."""
        pass
    
    def await_ready(self, timeout: float = 300.0) -> None:
        """Wait for the engine to report ready (health check passes)."""
        pass
    
    def query(self, prompt: str, max_tokens: int, temperature: float = 0.0) -> Response:
        """Send a completion request and return the response."""
        pass
    
    def batch_query(self, prompts: List[str], max_tokens: int) -> List[Response]:
        """Send concurrent requests and return responses."""
        pass
    
    def teardown(self) -> None:
        """Clean up, stop the server, release GPU memory."""
        pass
    
    def get_telemetry(self) -> Dict[str, Any]:
        """Return GPU telemetry: memory used, utilization, temperature."""
        pass
```

### Adapter types

Depending on the engine, the adapter may be one of three patterns:

**1. LLMPerf-compatible adapter**
For engines that already support an OpenAI-compatible API (vLLM, SGLang, TGI, etc.). The adapter uses the `llmperf` client to send requests and measure TTFT/TPOT.

```python
class LLMPerfAdapter(ModelServingAdapter):
    def __init__(self, engine_name, base_url, api_key=None):
        self.engine = engine_name
        self.client = OpenAI(base_url=base_url, api_key=api_key or "dummy")
    
    def query(self, prompt, max_tokens, temperature=0.0):
        return self.client.completions.create(
            model="default",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
    
    def batch_query(self, prompts, max_tokens):
        # Use concurrent.futures or asyncio to send parallel requests
        # llmperf measures inter-token latency and TTFT per request
        pass
```

**2. AnyScale serving benchmark adapter**
For engines that we test via the AnyScale serving benchmark suite. This adapter focuses on sustained throughput and goodput under load.

```python
class AnyScaleAdapter(ModelServingAdapter):
    def __init__(self, engine_name, base_url):
        self.engine = engine_name
        self.base_url = base_url
    
    def run_sustained_load(self, duration_sec: int, concurrency: int):
        # Send requests at fixed concurrency for N seconds
        # Measure goodput, throughput, and error rate
        pass
```

**3. Custom serving adapter**
For engines that do not expose an OpenAI-compatible API or require custom request formats (e.g., TensorRT-LLM with gRPC, llama.cpp with its own HTTP API, custom C++ engines). The adapter must handle the request formatting and response parsing.

```python
class CustomServingAdapter(ModelServingAdapter):
    def __init__(self, engine_name, config):
        self.engine = engine_name
        self.config = config
    
    def setup(self, model_id, gpu_devices):
        if self.engine == "tensorrt-llm":
            # Build TensorRT engine from checkpoint
            subprocess.run(["trtllm-build", "--checkpoint", model_id, ...])
            # Start Triton server or standalone gRPC server
            self.server = subprocess.Popen(["trtllm-serve", ...])
        elif self.engine == "llama-cpp":
            self.server = subprocess.Popen(["./server", "-m", model_id, ...])
    
    def query(self, prompt, max_tokens, temperature=0.0):
        # Custom HTTP/gRPC request format
        if self.engine == "tensorrt-llm":
            return self.grpc_client.generate(prompt, max_tokens, temperature)
        elif self.engine == "llama-cpp":
            return requests.post(self.base_url + "/completion", json={...})
```

### Adapter rules

1. The adapter must be **pure** — it should not modify the engine's behavior (batching, scheduling, quantization), only interface with it.
2. The adapter must be **documented** — every step should be explainable in plain English (e.g., "We set `--tensor-parallel-size` to match the GPU count because vLLM requires it").
3. The adapter must be **reproducible** — running it twice on the same machine with the same model should produce the same serving endpoint.
4. The adapter must be **isolated** — it should not depend on other engines' adapters. Each engine gets its own container or virtual env.
5. The adapter code is **published** in the benchmark harness repo (separate from the almanac repo).
6. The adapter must handle **GPU cleanup** — after teardown, `nvidia-smi` should show no remaining processes from the engine.

## Automation

### Monthly update cron

The monthly update is run by a scheduled job:
- **Trigger**: `cron` expression `0 7 15 * *` (monthly, 15th at 7:00 AM)
- **Action**: Runs a research agent to discover new engines, update metadata, and draft the next edition
- **Output**: Commits to the repo with the updated roster and new edition

### GitHub Actions (optional)

For automatic metadata refresh (GitHub stars, last push dates, release tags), a GitHub Actions workflow can be configured:

```yaml
name: Monthly Metadata Refresh
on:
  schedule:
    - cron: '0 7 1 * *'
  workflow_dispatch:
jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Refresh metadata
        run: python scripts/refresh_metadata.py
      - name: Commit and push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add -A
          git commit -m "Monthly metadata refresh: $(date +%Y-%m)" || echo "No changes"
          git push
```

## License

Content: CC BY 4.0  
Code: MIT
