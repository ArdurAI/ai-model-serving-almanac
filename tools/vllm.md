# vLLM


[![Infrastructure](https://img.shields.io/badge/Also_in-Infrastructure-blue)](https://github.com/ArdurAI/ai-infrastructure-almanac)

- **Category**: Model Serving & Inference Engines
- **Type**: Inference Engine
- **License**: Apache-2.0
- **Region**: Global
- **Tier**: A
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-07-12

> 86K+ stars; Model Runner V2; continuous batching; 200+ models; multi-GPU (NVIDIA, AMD, Intel, TPU)

---

## Overview

vLLM is a inference engine in the model serving and inference engines category.

**Supported model formats**: safetensors, gguf, pytorch, awq, gptq

**Supported quantization**: fp16, bf16, fp8, int8, awq, gptq, marlin, gguf

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
# Recommended: install with uv
uv venv --python 3.12 --seed
source .venv/bin/activate
uv pip install vllm --torch-backend=auto

# Alternative: pip-only
pip install vllm --torch-backend=auto

# Start the OpenAI-compatible server
vllm serve meta-llama/Meta-Llama-3.1-8B-Instruct --port 8000

# Offline batch inference (Python)
from vllm import LLM, SamplingParams
llm = LLM(model="meta-llama/Meta-Llama-3.1-8B-Instruct")
params = SamplingParams(temperature=0.7, max_tokens=512)
outputs = llm.generate(["Hello world"], params)
```

### Known sharp edges (from community / docs)
1. **OOM during sampler warmup with large models** — DeepSeek-V3.2 and similar large MoE models can crash during the `_dummy_sampler_run` warmup phase even when model loading appears to succeed. Mitigation: lower `--gpu-memory-utilization` or `--max-num-batched-tokens`.
2. **GPU memory leaks in model forward** — Repeated `llm.generate()` calls can leak GPU memory because PyTorch's allocator retains cached memory between steps that isn't fully reused. Workaround: insert `torch.cuda.empty_cache()` between batches.
3. **PyTorch version sensitivity with CUDA graphs** — Upgrading PyTorch can silently increase internal memory overhead, causing CUDA graph-enabled runs to OOM even when non-graph runs work fine.
4. **New NVIDIA driver / CUDA compatibility issues** — vLLM's loader may fail on very new driver stacks because it hardcodes library search paths under `/usr/`. Requires pinning or environment overrides.
5. **V1 Engine experimental instability** — The newer V1 engine (default in recent nightlies) has higher memory overhead and different tuning knobs; production users often pin to `VLLM_USE_V1=0` for stability.

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

> Raw results JSON: `benchmarks/vllm-<date>.json`

---

## Bug Notes

### Smoke gate findings
- ⏳ Not yet tested

### Known issues (from community / docs)
1. **OOM during sampler warmup with large models** — DeepSeek-V3.2 and similar large MoE models can crash during the `_dummy_sampler_run` warmup phase even when model loading appears to succeed. Mitigation: lower `--gpu-memory-utilization` or `--max-num-batched-tokens`.
2. **GPU memory leaks in model forward** — Repeated `llm.generate()` calls can leak GPU memory because PyTorch's allocator retains cached memory between steps that isn't fully reused. Workaround: insert `torch.cuda.empty_cache()` between batches.
3. **PyTorch version sensitivity with CUDA graphs** — Upgrading PyTorch can silently increase internal memory overhead, causing CUDA graph-enabled runs to OOM even when non-graph runs work fine.
4. **New NVIDIA driver / CUDA compatibility issues** — vLLM's loader may fail on very new driver stacks because it hardcodes library search paths under `/usr/`. Requires pinning or environment overrides.
5. **V1 Engine experimental instability** — The newer V1 engine (default in recent nightlies) has higher memory overhead and different tuning knobs; production users often pin to `VLLM_USE_V1=0` for stability.

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
- [SGLang](sglang.md)
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

- Official site: https://vllm.ai
- GitHub: https://github.com/vllm-project/vllm
- Documentation: https://docs.vllm.ai
- Community / Discord: - User Forum: https://github.com/vllm-project/vllm/discussions
- Developer Slack: linked from README (invite via vllm.ai)
- Twitter/X: @vllm_project
- Blog: https://blog.vllm.ai
- Benchmark adapter: ⏳ (link to harness repo when available)

---

## Changelog

| Date | Event | Notes |
|------|-------|-------|
| 2026-06-16 | First triaged | Added to roster, deep-dive template created |
| 2026-06-17 | Research enriched | Official links, setup commands, sharp edges populated from community research |


---

## Deep Analysis

### Daily monitoring update — 2026-07-12

- **Latest release:** `v0.25.0` (2026-07-11): 558-commit release that makes Model Runner V2 the default for dense models, removes legacy PagedAttention, brings the Transformers backend to native-vLLM performance, adds new model support (LLaVA-OneVision-2, Unlimited OCR, MOSS-Transcribe-Diarize, openai/privacy-filter, Hy3, GLM-5/DeepSeek-V3.2, MiniMax-M3 improvements), introduces a unified streaming parser engine, and expands heterogeneous-vocabulary speculative decoding.
- **Community health:** Open issues increased from 5,639 to 5,705 (+66). This is a material support-load increase; watch MRv2 migration regressions and model-zoo churn.

### Daily monitoring update — 2026-07-09

- **Community health:** Open issues increased from 5,549 to 5,629 (+80). This is a notable issue-load increase; keep an eye on community support pressure.

### 1. How Is This Tool Useful?

vLLM is the dominant open-source LLM inference engine with 86K+ GitHub stars, now centered on Model Runner V2, continuous batching, and support for 200+ model architectures across NVIDIA, AMD, Intel, and TPU hardware. It pioneered PagedAttention, but v0.25.0 retires the legacy implementation as the V1/MRv2 backend becomes standard. It has become the de facto standard for LLM serving, powering inference at companies like Anthropic, Cohere, and many others. The OpenAI-compatible server makes deployment trivial.

### 2. Gotchas of Using This Tool

vLLM has 5,705 open issues — the highest raw count in the ecosystem, reflecting its massive user base and complex multi-hardware support. 30 published security advisories mean production deployments must track CVEs carefully. GPU memory leaks in model forward passes can occur with repeated batch inference. OOM during sampler warmup with large MoE models requires careful memory tuning.

### 3. Limitations

Not the fastest on single-GPU NVIDIA (TensorRT-LLM is 30-60% faster). Memory management can be unpredictable with large models. Multi-GPU tensor parallelism requires careful configuration. AMD/Intel/TPU support lags behind NVIDIA in both features and performance. The project's rapid growth means some features are less tested.

### 4. How Secure Is This Tool?

30 published GitHub security advisories — the highest in this category, indicating both active security maintenance and a large attack surface. The project participates in responsible disclosure and publishes CVE fixes regularly. Production deployments should pin to stable versions and monitor for security advisories. The OpenAI-compatible server should be secured with authentication.

### 5. Usefulness to General Public and Non-Technical Users

**Rating: 5/10**

vLLM pioneered PagedAttention — treating KV cache like virtual memory with page-based allocation — which eliminated the memory fragmentation that limited early LLM serving. This innovation, combined with continuous batching, made vLLM 2-4x more efficient than previous serving approaches and established it as the standard.

### 6. What Does This Tool Solve That Others Don't?

vLLM pioneered PagedAttention — treating KV cache like virtual memory with page-based allocation — which eliminated the memory fragmentation that limited early LLM serving. This innovation, combined with continuous batching, made vLLM 2-4x more efficient than previous serving approaches and established it as the standard.

### 7. How Does This Tool Rank Compared to Others?

| Rank | Tool | Stars | Key Advantage |
|------|------|-------|---------------|
| 1 | vLLM | 86K+ | Largest community, broadest hardware support |
| 2 | SGLang | 30K | RadixAttention, best for RAG workloads |
| 3 | TensorRT-LLM | 14K | Highest single-GPU throughput on NVIDIA |
| 4 | llama.cpp | 119K | Best for CPU/consumer hardware |
| 5 | Ollama | 175K | Easiest local deployment |

*See [tools/README.md](README.md) for the full ranking table.*

### 8. How Can This Tool Be Improved? How Active Is Development?

Development is extremely active (pushed July 2026) with 18,841 forks — the most actively developed LLM inference project. Improvement areas include reducing the issue backlog, improving multi-hardware support consistency, reducing memory management issues, better documentation for edge cases, and stabilizing APIs for production use.

### 9. Official Maintainer Contacts

Maintained by the vLLM Project (originated from UC Berkeley Sky Computing). Contact via GitHub Issues at vllm-project/vllm, their Discord (invite via vllm.ai), or discussions on GitHub. Core maintainers include researchers from Sky Computing and engineers from multiple companies.

### 10. General Usage Guidance

Best as the default LLM serving engine for most use cases. Use `vllm serve model_name` for quick deployment. For NVIDIA-only maximum throughput, consider TensorRT-LLM. For RAG workloads, consider SGLang. Always test with your specific model and hardware — performance characteristics vary significantly.

---

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
