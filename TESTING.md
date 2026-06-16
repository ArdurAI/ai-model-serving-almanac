# Testing & Benchmarking

How the model serving almanac tests inference engines, what the harness does, how scoring works, and how to reproduce results.

## Table of Contents

1. [The Three Benchmark Types](#the-three-benchmark-types)
2. [The Seven Dimensions](#the-seven-dimensions)
3. [The Harness Architecture](#the-harness-architecture)
4. [The Canary](#the-canary)
5. [Standard Benchmarks](#standard-benchmarks)
6. [PlatformOps Custom Benchmarks](#platformops-custom-benchmarks)
7. [Stress Suite](#stress-suite)
8. [Cross-Category Integration Tests](#cross-category-integration-tests)
9. [Scoring](#scoring)
10. [Reproducibility](#reproducibility)
11. [Failure Mode Taxonomy](#failure-mode-taxonomy)

---

## The Three Benchmark Types

Every engine is tested across three types of benchmarks:

| Type | Purpose | Frequency |
|------|---------|-----------|
| **Standard benchmarks** | Verify vendor claims with published test suites (LLMPerf, AnyScale) | Every benchmark run |
| **PlatformOps custom benchmarks** | Test ops reality: setup, throughput, GPU utilization, failure modes | Every benchmark run |
| **Cross-category integration tests** | Test how engines work with guardrails, vector DBs, and agent frameworks in a full stack | Quarterly |

## The Seven Dimensions

Every engine is scored 0-100 on each dimension. The final score is a weighted average, but the per-dimension scores are always published.

| Dimension | Weight | What it measures for model serving | How it's tested |
|-----------|--------|-----------------------------------|-----------------|
| **Accuracy / Quality** | 25% | Does the engine produce the same output distribution as the reference (fp16)? Perplexity retention under quantization, logits divergence, exact-match drift on benchmark suites. | Perplexity comparison on WikiText-2 / C4; exact-match on MMLU / GSM8K; logits divergence vs. reference fp16; LLM-as-judge for response quality |
| **Latency** | 15% | TTFT (time to first token), TPOT (time per output token), end-to-end latency under load. | Instrumented measurements via `llmperf`; p50, p95, p99 across prompt lengths (short/medium/long) |
| **Token Economics** | 15% | Cost per 1M tokens served (inference-time cost), GPU cost per hour, pricing predictability for cloud endpoints. | Standardized workloads; $/1M tokens for self-hosted (GPU cost amortized); published cloud pricing vs. measured throughput |
| **Scale Behavior** | 15% | What happens at 2x, 10x concurrent requests? Batch saturation, KV cache exhaustion, throughput plateau, scheduling fairness. | Load tests with concurrency sweeps (1, 2, 4, 8, 16, 32, 64); throughput-vs-concurrency curves; degradation points |
| **Ops Burden** | 15% | Deployment complexity: time to first serving endpoint, dependency conflicts (CUDA/PyTorch), model format conversion, multi-node setup, upgrade pain. | Measured setup time; smoke-gate sweep; dependency matrix; upgrade test (N → N+1) |
| **Developer Experience** | 10% | API compatibility (OpenAI, TGI, custom), documentation quality, error messages when batching fails, community responsiveness, quantization UX. | Structured rubric; API compatibility matrix; community health metrics (issue response time) |
| **Data Sovereignty** | 5% | Self-hosting viability: on-prem GPU clusters, air-gapped deployments, auditability of serving binary, weights ownership. | Feature matrix; self-hosting checklist; EU AI Act / GDPR alignment for cloud endpoints |

### Why these weights?

The weights reflect what a platform engineer actually cares about when choosing an inference engine. Accuracy is the most important — an engine that silently degrades output quality under quantization is worse than a slow engine. Latency and scale behavior are nearly as important because an engine that collapses under concurrent load or has unpredictable TTFT spikes is not production-ready. Ops burden is the hidden tax: an engine that requires a PhD in CUDA to deploy is not worth a 10% throughput gain.

Weights are reviewed annually. Changes require an RFC and a public comment period.

## The Harness Architecture

```
┌─────────────────────────────────────────┐
│  ModelServingAdapter (frozen contract)   │
│  ├── setup()   → install, configure GPU │
│  ├── load()    → load model weights      │
│  ├── await_ready() → health check passes │
│  ├── query()   → single request, TTFT/TPOT│
│  ├── batch_query() → concurrent requests  │
│  ├── get_telemetry() → GPU mem/util     │
│  └── teardown() → cleanup, release GPU  │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Telemetry Collector                    │
│  ├── TTFT (p50/p95/p99)                │
│  ├── TPOT (p50/p95/p99)                │
│  ├── token count & throughput            │
│  ├── GPU memory & utilization           │
│  ├── batch size distribution            │
│  ├── error rate & failure mode taxonomy │
│  └── ops notes (setup time, CUDA, bugs) │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Grading Pipeline                       │
│  ├── Perplexity grader (vs. reference)  │
│  ├── Exact-match grader (MMLU/GSM8K)    │
│  ├── Logits divergence grader          │
│  ├── LLM judge (frozen prompts, SHA-256)│
│  ├── Second pass (confidence < 0.7)     │
│  └── Failure mode taxonomy             │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  Results Publisher                      │
│  ├── Raw JSON (per request, per run)   │
│  ├── Summary tables (per engine)        │
│  ├── Cross-verification analysis        │
│  └── Insight extraction                 │
└─────────────────────────────────────────┘
```

### The `await_ready()` barrier

This is where async model-loading and engine warm-up get their cost measured instead of hidden. Many engines claim "fast" serving because the model loading happens in the background, but the first request after "ready" still incurs graph compilation or JIT overhead. The `await_ready()` barrier waits for the engine to report healthy (HTTP 200 on `/health`) and then sends a warm-up request, ensuring the true cold-start-to-first-token latency is measured.

### The Telemetry Collector

Every adapter call is instrumented:
- **TTFT**: Time from request send to first response token; measured via `llmperf` or custom HTTP client with streaming
- **TPOT**: Inter-token latency measured from the stream; p50, p95, p99 computed across all tokens and all requests
- **Throughput**: Total tokens generated / total wall-clock time (including both prefill and decode)
- **GPU Memory**: `nvidia-smi` or `pynvml` snapshots during the run; peak memory, memory at steady state
- **GPU Utilization**: Compute utilization percentage during decode phase (prefill typically maxes GPU, decode is the bottleneck)
- **Batch Size Distribution**: If the engine exposes batch size metrics, we capture them; otherwise we infer from request timing
- **Errors**: Every timeout, CUDA OOM, batching error, or unexpected result is logged with full traceback and GPU state snapshot
- **Ops notes**: Human observations about setup friction, CUDA version conflicts, model conversion pain, undocumented flags

## The Canary

The first run of every batch is the **no-engine baseline** (the "canary") — a naive `transformers` pipeline with no optimization (no FlashAttention, no continuous batching, no quantization). If the benchmark leaked favorable conditions or the measurement pipeline is biased, the canary would show impossible improvements.

**Canary rules**:
- The canary must score exactly at the **naive baseline** on all metrics (no better, no worse than unoptimized PyTorch)
- If the canary scores above the naive baseline on throughput or below on latency, something is wrong with the harness
- If the canary fails, the entire batch is invalid and must be rerun
- The canary run is published alongside the real results
- The canary adapter is a minimal `transformers` pipeline: `AutoModelForCausalLM` + `AutoTokenizer`, no optimizations

## Standard Benchmarks

### By category (model serving)

| Benchmark | What it tests | Source | Adapter used |
|-----------|-------------|--------|-------------|
| **LLMPerf** | TTFT, TPOT, throughput, inter-token latency under load | [LLMPerf](https://github.com/ray-project/llmperf) | LLMPerf-compatible adapter |
| **AnyScale serving benchmark** | Sustained throughput, goodput, error rate under sustained load | [AnyScale](https://github.com/anyscale/llmperf) | AnyScale adapter |
| **MMLU (exact match)** | Accuracy retention under quantization vs. reference fp16 | [MMLU](https://github.com/hendrycks/test) | Custom adapter |
| **GSM8K (exact match)** | Math reasoning accuracy retention under quantization | [GSM8K](https://github.com/openai/grade-school-math) | Custom adapter |
| **Perplexity (WikiText-2 / C4)** | Perplexity delta vs. reference fp16 after quantization | Custom | Custom adapter |
| **Logits divergence** | KL divergence of output distributions vs. reference fp16 | Custom | Custom adapter |

### Published vs. reproduced

Every standard benchmark ranking ships a table:

| Engine | Published Claim | Our Result | Delta | Verdict |
|--------|----------------|------------|-------|---------|
| Engine A | "2x throughput vs. vLLM" | 1.4x vs. vLLM on identical hardware | -0.6x | ⚠️ Overstated |
| Engine B | "<10ms TTFT on Llama-3-8B" | 12ms TTFT p50 | +2ms | ✅ Close |
| Engine C | "Zero accuracy loss with FP8" | 0.3% MMLU drop vs. fp16 | -0.3% | ✅ Close |
| Engine D | No claim | 3rd of 8 on throughput | N/A | — |

## PlatformOps Custom Benchmarks

### Setup experience

**Measured**:
- Time from `docker pull` (or `git clone`) to first working `/health` response
- Number of CUDA/PyTorch dependency conflicts when installing alongside other roster engines
- Time to resolve dependency conflicts (e.g., "vLLM requires CUDA 12.1 but TensorRT-LLM requires 12.4")
- Number of undocumented steps required (e.g., "you must set `NCCL_P2P_DISABLE=1` on this GPU topology")
- Time to find the answer in the docs when stuck (e.g., "how do I enable FP8 on this engine?")
- Model conversion time: if the engine requires converting Safetensors to a proprietary format

**Scored on**:
- Sub-5 minutes: 90-100
- 5-30 minutes: 70-89
- 30-60 minutes: 50-69
- 60+ minutes or unresolved: 0-49

### Smoke gate

Every engine must pass an identical 3-turn scenario before entering the roster:

```
Turn 1: Deploy the engine with a standard model (Llama-3.1-8B-Instruct)
Turn 2: Send a standard chat completion request (mixed prompt: short + medium + long)
Turn 3: Verify the response is non-empty, JSON-schema-compliant, and GPU was utilized
```

**Pass criteria**:
- No crashes, no silent failures, no CUDA OOM during the basic test
- Response must be non-empty and structurally valid (has `choices[0].text` or `choices[0].message.content`)
- GPU must show utilization > 0% during generation (verifies the engine actually used the GPU, not CPU fallback)
- Engine must handle the basic case without workarounds or undocumented flags

**What the smoke gate surfaced** (from the model serving almanac, as example):
- **GPU topology bugs**: Engine fails on multi-GPU unless `NCCL_P2P_DISABLE=1` is set, but this is undocumented
- **Quantization cliff**: Engine loads FP8 model but silently falls back to fp16, doubling memory usage without warning
- **Batching starvation**: Engine accepts concurrent requests but serializes them, making TPOT identical to single-request mode
- **API incompatibility**: Engine claims OpenAI compatibility but returns non-standard JSON (missing `usage` field)
- **Memory leaks**: KV cache not released between requests, causing OOM after 10 sequential requests
- **Cold-start deception**: Engine reports `/health` as ready but first request triggers 30-second JIT compilation

### Stress suite

| Test | What it does | What it reveals |
|------|-------------|---------------|
| **Prefill-decode imbalance** | Send a mix of very long prefill prompts and short decode prompts simultaneously | How the scheduler handles imbalanced batching; does short-decode get starved by long-prefill? |
| **Concurrent request flood** | Ramp from 1 to 64 concurrent requests over 60 seconds | Batch saturation point, throughput plateau, scheduling fairness, error rate curve |
| **KV cache exhaustion** | Send requests until GPU memory is nearly full | How the engine handles memory pressure: graceful queueing, OOM, or silent eviction? |
| **Kill-the-GPU** | Simulate GPU failure (CUDA error injection) mid-request | Recovery, error handling, request retry behavior, data integrity |
| **Quantization stress** | Run identical workloads on fp16, fp8, int8, awq, gptq variants | Accuracy retention, throughput gain vs. accuracy loss, memory savings |
| **Cost-runaway** | Run the engine at maximum throughput for 1 hour | GPU cost per hour, thermal throttling, sustained performance degradation, memory leaks |
| **Warm-up deception** | Measure first-request TTFT vs. steady-state TTFT | Does the engine hide compilation/warm-up overhead in published benchmarks? |

### Upgrade path

**Tested**:
- Can you upgrade from version N to N+1 without rebuilding model engines or rewriting configs?
- Are there breaking changes in the serving API (e.g., OpenAI compatibility removed)?
- Is there a migration guide for CUDA version or PyTorch version bumps?
- Does the engine maintain backward compatibility for model formats (e.g., old TensorRT engines still load)?

### Debugging experience

**Tested**:
- When the engine fails (OOM, batching error, model load failure), can you find out why in <5 minutes?
- Are error messages clear and actionable (e.g., "CUDA OOM: KV cache exceeded, try reducing `max_num_seqs`" vs. "RuntimeError")?
- Is there a debug mode or verbose logging that shows batching decisions, scheduling queue, and GPU telemetry?
- Are there known issues documented for common GPU topologies (e.g., "P2P doesn't work on these cards")?
- Can you trace the request path (API → scheduler → GPU kernel) for a single request?

## Cross-Category Integration Tests

These tests run quarterly and check how engines work with tools from other categories in a realistic stack:

| Integration | What it tests | Tools involved |
|-------------|-------------|----------------|
| **Engine + Security Guardrails** | Do guardrails add <50ms latency to TTFT? Does batching behavior change when guardrails pre-process prompts? | Inference engine, security guardrail framework |
| **Engine + Vector DB** | Full RAG stack: vector DB retrieves context, engine generates response with retrieved context in prompt | Inference engine, vector database, agent framework |
| **Engine + Agent Framework** | Can the agent framework call the engine's API? Does the engine's streaming behavior work with the agent's event loop? | Agent framework, inference engine |
| **Engine + Observability** | Can you trace per-request TTFT/TPOT and GPU metrics to an observability platform? | Inference engine, observability tool |
| **Protocol + Engine** | Does the engine expose an MCP server for model serving? Does it support A2A for multi-agent orchestration? | Protocol implementation, inference engine |

## Scoring

### Per-dimension scoring

Each dimension is scored 0-100 using a rubric. The rubric is published before any scoring happens.

**Example: Accuracy rubric**

| Score | Criteria |
|-------|----------|
| 90-100 | ≤0.5% perplexity delta vs. fp16; ≤0.5% MMLU/GSM8K drop; no critical failures in quantization stress suite |
| 80-89 | 0.5-1.5% perplexity delta; 0.5-2% MMLU/GSM8K drop; minor failures in stress suite |
| 70-79 | 1.5-3% perplexity delta; 2-4% MMLU/GSM8K drop; some stress suite failures |
| 60-69 | 3-5% perplexity delta; 4-7% MMLU/GSM8K drop; frequent stress suite failures |
| 50-59 | 5-8% perplexity delta; 7-10% MMLU/GSM8K drop; significant reliability issues |
| 0-49 | >8% perplexity delta or >10% MMLU/GSM8K drop; fundamentally unreliable |

**Example: Latency rubric**

| Score | Criteria |
|-------|----------|
| 90-100 | TTFT p95 <20ms for 8B model; TPOT p95 <15ms; excellent tail latency |
| 80-89 | TTFT p95 20-50ms; TPOT p95 15-30ms; good tail latency |
| 70-79 | TTFT p95 50-100ms; TPOT p95 30-60ms; acceptable tail latency |
| 60-69 | TTFT p95 100-200ms; TPOT p95 60-120ms; noticeable lag |
| 50-59 | TTFT p95 200-500ms; TPOT p95 120-250ms; poor latency |
| 0-49 | TTFT p95 >500ms or TPOT p95 >250ms; unacceptable for real-time use |

### Composite score

The composite score is a weighted average of the seven dimensions:

```
Composite = (Accuracy × 0.25) + (Latency × 0.15) + (TokenEconomics × 0.15) +
            (ScaleBehavior × 0.15) + (OpsBurden × 0.15) + (DevEx × 0.10) +
            (DataSovereignty × 0.05)
```

The composite is used for ranking, but the per-dimension scores are always published. A tool with a high composite but low accuracy score is a warning sign (fast but wrong). A tool with a high composite but low ops burden score is a warning sign (fast but you'll hate your life deploying it).

### Confidence intervals

Every score is reported with a confidence interval computed from the standard error across runs. If the intervals overlap between two engines, the difference is not statistically significant. Hardware variation is the dominant source of variance: results from A100 and H100 are reported separately and never merged.

## Reproducibility

### How to reproduce a benchmark

1. Clone the benchmark harness repo (published separately)
2. Check out the exact commit used for the run (recorded in the results JSON)
3. Install the exact dependencies (lockfile is published, including CUDA version and PyTorch version)
4. Provision the same GPU class (A100-80GB, H100-80GB, etc.) — results are hardware-specific
5. Download the same model weights (checkpoint SHA-256 is recorded)
6. Run the harness with the same adapter, same seed, same batching config
7. Compare your results to the published results

### What is frozen

| Element | How it's frozen | Where to find it |
|---------|---------------|------------------|
| Model weights | Pinned model name, checkpoint SHA-256 | `results.json` metadata |
| Prompt mix | Published JSON files with exact prompts | `benchmarks/` directory |
| Concurrency levels | Documented values | `methodology/benchmark-harness.md` |
| Judge prompts | SHA-256 hash | `methodology/benchmark-harness.md` |
| Control variables | Documented values | `results.json` metadata |
| Random seeds | Published integer | `results.json` metadata |
| Adapter code | Published in harness repo | Separate repo |
| GPU driver/CUDA version | Recorded in metadata | `results.json` metadata |
| Batching config | Documented flags | `methodology/benchmark-harness.md` |

### What is NOT frozen (and why)

| Element | Why it changes | How we handle it |
|---------|---------------|------------------|
| Engine versions | Engines update | We re-run benchmarks for new versions; old results are archived with version tags |
| CUDA/PyTorch versions | Ecosystem updates | Recorded in metadata; results are tagged with CUDA version |
| GPU hardware | We may upgrade machines | Hardware spec is recorded in `results.json`; results are hardware-specific and never merged across GPU classes |
| Cloud pricing | GPU cloud pricing changes | Cost is computed at runtime using current pricing; historical results are annotated |

## Failure Mode Taxonomy

Every failure is classified into a taxonomy. This helps identify patterns across engines and categories.

| Category | Failure Modes |
|----------|--------------|
| **Setup** | `install_failed`, `cuda_version_mismatch`, `dependency_conflict`, `config_error`, `missing_env_var`, `docs_incomplete`, `model_conversion_failed` |
| **Model Loading** | `oom_load`, `format_unsupported`, `quantization_mismatch`, `checkpoint_corrupt`, `weights_download_failed` |
| **Serving** | `batching_bug`, `scheduling_starvation`, `kv_cache_leak`, `prefill_decode_imbalance`, `request_timeout`, `api_incompatible` |
| **Accuracy** | `quantization_accuracy_loss`, `logits_divergence`, `fp8_clipping`, `awq_degradation`, `greedy_mismatch` |
| **Performance** | `throughput_degradation`, `ttft_spike`, `tpot_increase`, `memory_leak`, `gpu_underutilization`, `thermal_throttle` |
| **Scale** | `oom_under_load`, `connection_pool_exhaustion`, `request_queue_overflow`, `rate_limit_hit`, `nccl_failure` |
| **Ops** | `upgrade_breaking`, `undocumented_behavior`, `debug_opacity`, `community_unresponsive`, `multi_node_unsupported` |
| **Security** | `prompt_injection`, `model_extraction`, `unauthorized_access`, `side_channel_leak` |
| **Integration** | `mcp_noncompliant`, `a2a_noncompliant`, `openai_api_mismatch`, `streaming_failure` |

## License

Content: CC BY 4.0  
Code: MIT
