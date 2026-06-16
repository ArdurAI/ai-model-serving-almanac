# Project Intent & Philosophy

## Why this almanac exists

The model serving and inference landscape is a fog of war. Every vendor publishes their own benchmark claiming "fastest TTFT in the industry" or "2x throughput versus vLLM." But **nobody independently reproduces these claims on identical hardware**, and nobody evaluates serving engines the way a platform engineer actually lives with them: GPU topology nightmares, batching heuristics that silently break accuracy, quantization recipes that trade perplexity for speed without documenting the loss, and the 3 AM pager when concurrent load spikes OOM your inference nodes.

This almanac is the **public record of independent verification for inference engines and model serving platforms**. It exists because ML platform engineers need a single source of truth that answers:

- Does this inference engine actually hit the throughput numbers on my GPU class?
- What's the real TTFT and TPOT under concurrent load, not just the best-case single-request number?
- How does batching behave when request lengths vary wildly (prefill-decode imbalance)?
- Does quantization (AWQ, GPTQ, FP8, INT8) retain enough accuracy for my use case?
- What's the ops burden of deploying and scaling this serving stack?
- Can I trust the vendor's benchmark numbers when they used H100s and I have A100s?

## Core principles

### 1. Frozen methodology before results

The harness, judge model, prompts, batching configuration, and scoring rubric are **fixed and published before any engine is tested**. This prevents "cherry-picking" the methodology that favors a particular engine (e.g., testing only short prompts that hide prefill bottlenecks, or using a quantization scheme that a specific engine optimizes for). If an engine doesn't fit the harness, we adapt the adapter — not the rules.

### 2. Ops-first evaluation

Most serving benchmarks measure throughput on a synthetic dataset. We measure **what a platform engineer actually lives with**:
- Time from `docker pull` to a serving endpoint responding to a health check
- Dependency conflicts between CUDA versions, PyTorch builds, and TensorRT backends
- Time to debug when the engine silently OOMs under load instead of gracefully degrading
- Upgrade pain when vLLM 0.5.x → 0.6.x breaks the scheduling API
- Cost predictability at scale: cost per 1M tokens served, not just theoretical FLOPs
- GPU utilization under real request-mix (not just 100% identical prompts)

### 3. Raw data is always published

Every benchmark run produces a JSON file with every request, every TTFT, every TPOT, every token count, every GPU memory snapshot, every batching decision. These raw files are published alongside the summary. If you disagree with a ranking, you can re-analyze the data yourself — or rerun the harness on your own hardware.

### 4. No engine is above criticism

Every engine on the roster has been through a smoke gate. Every engine has bugs: batching fairness issues, KV cache memory leaks, scheduling starvation, quantization accuracy cliff. We document them honestly. A vendor relationship or sponsorship does not influence rankings. The only way an engine improves its score is by actually improving.

### 5. Living document, not a static snapshot

The almanac is updated monthly. Engines enter and exit the roster. Scores change as engines improve or degrade. The "founding edition" is a snapshot; the current edition is the truth. CUDA versions change, PyTorch versions change, and what was true in June may not be true in September.

## Design philosophy

### The two-bar test

Every engine must clear two bars to justify its existence as infrastructure:
1. **Beat the naive baseline** on latency/throughput/accuracy (e.g., naive `transformers` pipeline, or unoptimized PyTorch inference)
2. **Beat the full-capability baseline** on ops burden/cost/complexity (e.g., does it justify itself over vLLM or SGLang?)

If an engine can't do both, it has no reason to exist as infrastructure. An engine that is 5% faster on TTFT but requires a custom CUDA kernel compilation step and undocumented environment variables is not worth adopting over a well-tuned default.

### The seven dimensions

We score every engine on seven dimensions because no single number (like "throughput") captures "good model serving":

| Dimension | Why it matters for model serving |
|-----------|---------------|
| **Accuracy** | Does the engine produce the same distribution as reference? Perplexity retention under quantization, exact-match drift on benchmark suites, logits divergence. |
| **Latency** | TTFT (time to first token), TPOT (time per output token), end-to-end latency. Measured at p50, p95, p99 under load. |
| **Token economics** | Cost per 1M tokens served (inference-time cost), GPU cost per hour, pricing predictability for cloud-hosted endpoints. |
| **Scale behavior** | What happens when you 10x concurrent requests? Batch saturation, KV cache exhaustion, scheduling fairness, throughput plateau. |
| **Ops burden** | Deployment complexity: Docker setup, GPU driver alignment, model format conversion, multi-node orchestration, upgrade stability. |
| **Developer experience** | API compatibility (OpenAI, TGI, custom), documentation quality, error messages when batching fails, community responsiveness. |
| **Data sovereignty** | Can you run it yourself? Self-hosted weights, on-prem GPU clusters, air-gapped deployments, auditability of the serving binary. |

### The adapter pattern

Every engine is tested through a **ModelServingAdapter** — a frozen interface that the engine must satisfy. The adapter handles model loading, serving startup, request formatting, and teardown. This means:
- Engines are tested identically (same prompts, same concurrency levels, same measurement hooks)
- The adapter is the only thing that changes per engine
- New engines can be added without changing the harness
- The adapter is published and open for review

Model serving adapters typically wrap:
- The engine's CLI or Docker entrypoint (e.g., `vllm serve`, `python -m sglang.launch_server`)
- The HTTP/gRPC client used to send requests
- The model format conversion (if the engine requires a specific checkpoint format)
- The GPU readiness check (CUDA_VISIBLE_DEVICES, NCCL setup for multi-node)

### The canary

Every benchmark batch starts with a **no-engine baseline** (the "canary") — typically a naive `transformers` pipeline with no optimization. If the benchmark leaked answers or the measurement pipeline is biased, the canary would show impossible improvements. The canary must score exactly at the naive baseline — this is a hard invariant. If it doesn't, the entire batch is invalid.

## Who this is for

- **ML Platform Engineers** evaluating which inference engine to deploy in production
- **CTOs/CIOs** making build-vs-buy decisions for model serving infrastructure
- **Open-source maintainers** who want independent benchmarking of their serving project
- **Researchers** studying the inference engine landscape and trade-offs
- **Vendors** who want to improve their engines based on real evidence, not marketing claims

## What this is NOT

- Not a marketing site for any inference engine vendor
- Not a "best of" list based on GitHub stars or funding rounds
- Not a tutorial on how to quantize a model or set up a vLLM server
- Not a replacement for your own due diligence on your specific hardware and model
- Not a static document that never changes

## The "Quest"

The "Inference Engineer's Quest for the Best" is the ongoing effort to test, measure, and rank every engine on the roster. It's not a one-time effort. It's a continuous process of:
1. **Discovery** — finding new engines via research, community, and submissions
2. **Triage** — deciding if an engine is serious enough to enter the roster
3. **Smoke gate** — running every engine through an identical 3-turn scenario: deploy model → send request → verify response
4. **Benchmark** — running standard benchmarks (LLMPerf, AnyScale) + custom throughput tests + stress suite
5. **Publication** — publishing raw data + summary + per-engine deep-dives
6. **Iteration** — re-testing as engines update, as CUDA/PyTorch versions change, as new benchmarks emerge

## How to challenge a result

If you believe a ranking or score is wrong:
1. Check the **raw results JSON** — the data is public, including per-request TTFT/TPOT and GPU telemetry
2. Check the **adapter implementation** — the adapter code is public
3. Check the **harness configuration** — batching settings, concurrency levels, and model checkpoints are frozen and published
4. File an issue with a specific claim and evidence (e.g., "I reran on A100 and got different TTFT")
5. We'll re-run the test or update the methodology if warranted

## Governance

- **ArdurAI** maintains the almanac and runs the Quest
- **Methodology changes** require a public RFC and at least one edition cycle of notice
- **Engine additions/removals** are decided by the triage criteria (stars, last push, community activity, seriousness)
- **Benchmark results** are machine-generated; summaries are human-reviewed for fairness
- **Conflicts of interest** are disclosed (e.g., ArdurAI contributes to some engines on the roster); mitigation is identical harness for all

## License

Content: CC BY 4.0  
Harness code: MIT  
Raw data: CC BY 4.0
