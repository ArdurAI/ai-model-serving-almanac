# SGLang


[![Infrastructure](https://img.shields.io/badge/Also_in-Infrastructure-blue)](https://github.com/ArdurAI/ai-infrastructure-almanac)

- **Category**: Model Serving & Inference Engines
- **Type**: Inference Engine
- **License**: Apache-2.0
- **Region**: Global
- **Tier**: A
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-07-09

> ~20K+ stars; RadixAttention; 29% throughput advantage on RAG workloads

---

## Overview

SGLang is a inference engine in the model serving and inference engines category.

**Supported model formats**: safetensors, pytorch, gguf

**Supported quantization**: fp16, bf16, fp8, int8, awq, gptq

**Hardware target**: GPU

---

## Setup Experience

| Step | Metric | Value | Notes |
|------|--------|-------|-------|
| Time to first result | `git clone` to working | ⏳ TBD | To be measured in Quest smoke gate |
| Dependency count | Direct + transitive | ⏳ TBD | |
| Docker required? | Yes / No | ⏳ TBD | |
| Language runtime | Required version | ⏳ TBD | |
| Auth complexity | API key / OAuth / None | ⏳ TBD | |
| First-run failure rate | Smoke gate pass/fail | ⏳ TBD | |

### Setup commands (from official docs)
```bash
# Install with pip (recommended)
pip install --upgrade pip
pip install uv
uv pip install sglang

# For AMD ROCm
pip install "sglang[all]" --index-url https://download.pytorch.org/whl/rocm6.2

# Start the server
python -m sglang.launch_server \
  --model-path meta-llama/Meta-Llama-3.1-8B-Instruct \
  --port 30000

# Or using the CLI shorthand
sglang serve meta-llama/Meta-Llama-3.1-8B-Instruct --port 30000

# Docker (NVIDIA, CUDA 13 default; use -cu12 suffix for CUDA 12)
docker run --gpus all \
  --shm-size 32g -p 30000:30000 \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  --env "HF_TOKEN=<token>" --ipc=host \
  lmsysorg/sglang:latest \
  python3 -m sglang.launch_server \
    --model-path meta-llama/Meta-Llama-3.1-8B-Instruct \
    --host 0.0.0.0 --port 30000
```

### Known sharp edges (from community / docs)
1. **OOM during benchmarking with large models** — Running `bench_serving` with 6000 prompts on 70B-parameter FP8 models can hit OOM in the logits processor during decode, even with TP8. Requires tuning `--mem-fraction-static` down.
2. **Alignment errors when disabling RadixAttention** — Disabling prefix caching (`--disable-radix-cache`) while enabling chunked prefill can trigger `AlignedAllocator` failures in `batch_prefill_tmp_v`.
3. **Concurrent long-request OOM** — 20 concurrent requests each with 1k tokens on Llama-3-8B can exceed KV pool capacity during prefill, even with A100 80GB. Needs `--chunked-prefill-size` reduction or `--max-running-requests` caps.
4. **Decode OOM with speculative decoding + retract** — EAGLE speculative decoding combined with request retraction can exhaust token allocation pools mid-verify, causing `RuntimeError: Out of memory` during draft verification.
5. **Batch-size-dependent result drift** — Different concurrency levels (1 vs 2 requests) can produce measurably different outputs on Mixtral-8x7B, causing evaluation score deltas of 5–10 points when benchmarked.

---

## Benchmark Results

### Standard benchmarks
| Benchmark | Tool Score | Baseline | Published Claim | Verified | Notes |
|-----------|-----------|----------|-----------------|----------|-------|
| LLMPerf | ⏳ TBD | | | | |
| AnyScale serving benchmark | ⏳ TBD | | | | |
| MMLU (exact match) | ⏳ TBD | | | | |
| GSM8K (exact match) | ⏳ TBD | | | | |
| Perplexity (WikiText-2) | ⏳ TBD | | | | |
| Logits divergence | ⏳ TBD | | | | |

### Custom PlatformOps benchmarks
| Dimension | Score (0-100) | Raw Value | Notes |
|-----------|-------------|-----------|-------|
| Accuracy | ⏳ TBD | | |
| Latency | ⏳ TBD | | |
| Token economics | ⏳ TBD | | |
| Scale behavior | ⏳ TBD | | |
| Ops burden | ⏳ TBD | | |
| Developer experience | ⏳ TBD | | |
| Data sovereignty | ⏳ TBD | | |

### Stress suite results
| Stress Test | Result | Notes |
|-------------|--------|-------|
| Prefill-decode imbalance | ⏳ TBD | |
| Concurrent request flood | ⏳ TBD | |
| KV cache exhaustion | ⏳ TBD | |
| Kill-the-GPU | ⏳ TBD | |
| Quantization stress | ⏳ TBD | |
| Cost-runaway | ⏳ TBD | |
| Warm-up deception | ⏳ TBD | |

> Raw results JSON: `benchmarks/sglang-<date>.json`

---

## Bug Notes

### Smoke gate findings
- ⏳ Not yet tested

### Known issues (from community / docs)
1. **OOM during benchmarking with large models** — Running `bench_serving` with 6000 prompts on 70B-parameter FP8 models can hit OOM in the logits processor during decode, even with TP8. Requires tuning `--mem-fraction-static` down.
2. **Alignment errors when disabling RadixAttention** — Disabling prefix caching (`--disable-radix-cache`) while enabling chunked prefill can trigger `AlignedAllocator` failures in `batch_prefill_tmp_v`.
3. **Concurrent long-request OOM** — 20 concurrent requests each with 1k tokens on Llama-3-8B can exceed KV pool capacity during prefill, even with A100 80GB. Needs `--chunked-prefill-size` reduction or `--max-running-requests` caps.
4. **Decode OOM with speculative decoding + retract** — EAGLE speculative decoding combined with request retraction can exhaust token allocation pools mid-verify, causing `RuntimeError: Out of memory` during draft verification.
5. **Batch-size-dependent result drift** — Different concurrency levels (1 vs 2 requests) can produce measurably different outputs on Mixtral-8x7B, causing evaluation score deltas of 5–10 points when benchmarked.

### Workarounds documented
- ⏳ To be validated

---

## Comparison with Peers

| Dimension | This Tool | Peer A | Peer B | Notes |
|-----------|-----------|--------|--------|-------|
| Accuracy | ⏳ | ⏳ | ⏳ | |
| Latency | ⏳ | ⏳ | ⏳ | |
| Cost | ⏳ | ⏳ | ⏳ | |
| Ops burden | ⏳ | ⏳ | ⏳ | |
| Scale ceiling | ⏳ | ⏳ | ⏳ | |
| Community | ⏳ | ⏳ | ⏳ | |

---

## Cost Analysis

### Pricing model
- ⏳ TBD

### Cost at scale
| Scale | Estimated Cost | Notes |
|-------|---------------|-------|
| Small (1-10 users) | ⏳ TBD | |
| Medium (10-100 users) | ⏳ TBD | |
| Large (100+ users) | ⏳ TBD | |
| Enterprise | ⏳ TBD | |

### Hidden costs
- ⏳ TBD (infrastructure, ops time, training, support)

---

## Data Sovereignty

| Property | Status | Notes |
|----------|--------|-------|
| Self-hostable | Yes | |
| Open source | Yes | License: Apache-2.0 |
| Audit trail | ⏳ TBD | |
| Data residency controls | ⏳ TBD | |
| On-premise deployment | Yes | |
| Export format | ⏳ TBD | |

---

## Security & Compliance

| Standard | Status | Notes |
|----------|--------|-------|
| SOC 2 | ⏳ TBD | |
| GDPR | ⏳ TBD | |
| HIPAA | ⏳ TBD | |
| ISO 27001 | ⏳ TBD | |
| EU AI Act | ⏳ TBD | |
| FedRAMP | ⏳ TBD | |

---

## Related Tools

### Tier A peers in same category
- [vLLM](vllm.md)
- [TensorRT-LLM](tensorrt-llm.md)
- [llama.cpp](llamacpp.md)
- [NVIDIA Dynamo](nvidia-dynamo.md)
- [KServe](kserve.md)
- [BentoML](bentoml.md)
- [Ray Serve](ray-serve.md)
- [Ollama](ollama.md)
- [LMDeploy](lmdeploy.md)
- [Fireworks AI](fireworks-ai.md)
- [Together AI](together-ai.md)
- [RunPod](runpod.md)
- [Lambda Labs](lambda-labs.md)
- [LiteLLM](litellm.md)
- [Portkey](portkey.md)

### Complementary tools
- ⏳ TBD (tools commonly used together)

### Alternatives to consider
- ⏳ TBD (when this tool is not the right fit)

---

## Links

- Official site: https://sgl-project.github.io/sglang/
- GitHub: https://github.com/sgl-project/sglang
- Documentation: https://docs.sglang.ai / https://sgl-project.github.io/references/
- Community / Discord: - Slack: https://slack.sglang.ai/ (linked from README)
- Weekly Dev Meeting: linked from README
- Blog: https://blog.sglang.ai/
- Roadmap: public GitHub projects
- Hosted under non-profit LMSYS (https://lmsys.org)
- Benchmark adapter: ⏳ (link to harness repo when available)

---

## Changelog

| Date | Event | Notes |
|------|-------|-------|
| 2026-06-16 | First triaged | Added to roster, deep-dive template created |
| 2026-06-17 | Research enriched | Official links, setup commands, sharp edges populated from community research |


---

## Deep Analysis

### Daily monitoring update — 2026-07-09

- **Community health:** Open issues increased from 3,917 to 4,095 (+178). This is a material backlog increase; monitor regression volume and maintainer response time.

### 1. How Is This Tool Useful?

SGLang is a high-performance LLM serving framework featuring RadixAttention (automatic prefix caching via radix tree), which provides up to 29% throughput advantage on RAG workloads with shared system prompts. It supports 200+ model architectures, constrained decoding (JSON/regex), multi-modal models, and speculative decoding. SGLang has rapidly grown to 30K+ stars and is considered the second-most-popular LLM engine after vLLM.

### 2. Gotchas of Using This Tool

SGLang has 3,880 open issues — very high, reflecting rapid growth and broad feature development. RadixAttention benefits depend on workload characteristics — pure single-turn workloads see minimal benefit. The project moves fast with frequent API changes. Documentation sometimes lags behind features.

### 3. Limitations

While SGLang supports many models, vLLM still has broader hardware support (TPU, Intel Gaudi). RadixAttention's cache management can lead to unexpected memory usage patterns. The project's rapid growth means some features are less battle-tested than vLLM's equivalents.

### 4. How Secure Is This Tool?

No published GitHub security advisories. Apache-2.0 license. The project is relatively young, so security maturity is still developing. Constrained decoding features (JSON/regex) could have edge cases that lead to unexpected behavior.

### 5. Usefulness to General Public and Non-Technical Users

**Rating: 5/10**

SGLang's RadixAttention is a unique innovation — automatic prefix caching using a radix tree data structure that eliminates redundant computation for shared prefixes (common system prompts, few-shot examples). For RAG workloads where many requests share context, this provides up to 29% throughput improvement that no other engine matches.

### 6. What Does This Tool Solve That Others Don't?

SGLang's RadixAttention is a unique innovation — automatic prefix caching using a radix tree data structure that eliminates redundant computation for shared prefixes (common system prompts, few-shot examples). For RAG workloads where many requests share context, this provides up to 29% throughput improvement that no other engine matches.

### 7. How Does This Tool Rank Compared to Others?

| Rank | Tool | Stars | Key Advantage |
|------|------|-------|---------------|
| 1 | vLLM | 85K+ | Largest community, broadest hardware support |
| 2 | SGLang | 30K | RadixAttention, best for RAG workloads |
| 3 | TensorRT-LLM | 14K | Highest single-GPU throughput on NVIDIA |
| 4 | llama.cpp | 119K | Best for CPU/consumer hardware |
| 5 | Ollama | 175K | Easiest local deployment |

*See [tools/README.md](README.md) for the full ranking table.*

### 8. How Can This Tool Be Improved? How Active Is Development?

Development is extremely active (pushed July 2026) with 6,882 forks — one of the fastest-growing AI projects. Improvement areas include reducing the issue backlog, stabilizing APIs, broader hardware support, better documentation, and production hardening.

### 9. Official Maintainer Contacts

Maintained by the SGL Project (originated from LMSYS/UC Berkeley). Contact via GitHub Issues at sgl-project/sglang or their Discord. Core contributors include researchers from LMSYS Org and UC Berkeley.

### 10. General Usage Guidance

Best for RAG workloads and any serving scenario with shared prefixes (system prompts, few-shot examples). Compare with vLLM (broader hardware support) and TensorRT-LLM (higher single-GPU throughput on NVIDIA). Use SGLang's structured output (JSON mode) for reliable tool use.

---

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
