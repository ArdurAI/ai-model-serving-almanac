# LMDeploy


[![Infrastructure](https://img.shields.io/badge/Also_in-Infrastructure-blue)](https://github.com/ArdurAI/ai-infrastructure-almanac)

- **Category**: Model Serving & Inference Engines
- **Type**: Inference Engine
- **License**: Apache-2.0
- **Region**: China
- **Tier**: A
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-06-16

> Shanghai AI Lab; TurboMind C++/CUDA; 1.5x vLLM on AWQ/MXFP4; DeepSeek/Qwen/InternLM

---

## Overview

LMDeploy is a inference engine in the model serving and inference engines category.

**Supported model formats**: safetensors, pytorch, awq, gptq

**Supported quantization**: fp16, bf16, fp8, int8, awq, gptq, w4a16

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
# Create conda environment (recommended)
conda create -n lmdeploy python=3.12 -y
conda activate lmdeploy

# Install from PyPI (CUDA 12.8 wheels by default for v0.13.0+)
pip install lmdeploy

# Offline batch inference (Python)
import lmdeploy
with lmdeploy.pipeline("internlm/internlm3-8b-instruct") as pipe:
    response = pipe(["Hi, pls intro yourself", "Shanghai is"])
    print(response)

# OpenAI-compatible server
lmdeploy serve api_server internlm/internlm2-chat-1_8b --server-port 23333

# Gradio Web UI
pip install lmdeploy[serve]
lmdeploy serve gradio internlm/internlm-chat-7b
```

### Known sharp edges (from community / docs)
1. **CUDA misaligned address on large models** — Serving GPT-OSS-120B on 4×V100 with prefix caching enabled crashes with `misaligned address` after the first request. Related to alignment of CUDA buffers when prefix caching + quantization are combined.
2. **TurboMind OOM during weight creation** — `_create_weight` → `create_shared_weights` can hit `CUDA runtime error: out of memory`, especially on GPUs with < 40GB VRAM when loading unquantized large models.
3. **Illegal memory access under stress** — Benchmark/stress tests can trigger `OverflowError` followed by cascading `CUDA runtime error: an illegal memory access was encountered` in `core/stream.h`.
4. **Triton compilation failure on GCC version mismatch** — Flash Attention/Triton kernels may fail to compile at runtime if system GCC doesn't match expected version. Requires `std=gnu99` or GCC pinning.
5. **Engine capability confusion** — TurboMind (C++/CUDA) and PyTorchEngine have different supported model lists and dtypes. Users frequently try to run models on TurboMind that only work on PyTorchEngine, causing cryptic errors.

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

> Raw results JSON: `benchmarks/lmdeploy-<date>.json`

---

## Bug Notes

### Smoke gate findings
- ⏳ Not yet tested

### Known issues (from community / docs)
1. **CUDA misaligned address on large models** — Serving GPT-OSS-120B on 4×V100 with prefix caching enabled crashes with `misaligned address` after the first request. Related to alignment of CUDA buffers when prefix caching + quantization are combined.
2. **TurboMind OOM during weight creation** — `_create_weight` → `create_shared_weights` can hit `CUDA runtime error: out of memory`, especially on GPUs with < 40GB VRAM when loading unquantized large models.
3. **Illegal memory access under stress** — Benchmark/stress tests can trigger `OverflowError` followed by cascading `CUDA runtime error: an illegal memory access was encountered` in `core/stream.h`.
4. **Triton compilation failure on GCC version mismatch** — Flash Attention/Triton kernels may fail to compile at runtime if system GCC doesn't match expected version. Requires `std=gnu99` or GCC pinning.
5. **Engine capability confusion** — TurboMind (C++/CUDA) and PyTorchEngine have different supported model lists and dtypes. Users frequently try to run models on TurboMind that only work on PyTorchEngine, causing cryptic errors.

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
- [SGLang](sglang.md)
- [TensorRT-LLM](tensorrt-llm.md)
- [llama.cpp](llamacpp.md)
- [NVIDIA Dynamo](nvidia-dynamo.md)
- [KServe](kserve.md)
- [BentoML](bentoml.md)
- [Ray Serve](ray-serve.md)
- [Ollama](ollama.md)
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

- Official site: https://github.com/InternLM/lmdeploy
- GitHub: https://github.com/InternLM/lmdeploy
- Documentation: https://lmdeploy.readthedocs.io/
- Community / Discord: - GitHub Discussions and Issues (primary)
- No official Discord or Slack found in current README/docs
- InternLM ecosystem community (Chinese and international)
- Benchmark adapter: ⏳ (link to harness repo when available)

---

## Changelog

| Date | Event | Notes |
|------|-------|-------|
| 2026-06-16 | First triaged | Added to roster, deep-dive template created |
| 2026-06-17 | Research enriched | Official links, setup commands, sharp edges populated from community research |


---

## Deep Analysis

### 1. How Is This Tool Useful?

LMDeploy is a high-performance LLM deployment toolkit from Shanghai AI Lab, featuring the TurboMind C++/CUDA inference engine that achieves 1.5x vLLM throughput on AWQ/MXFP4 quantized models. It provides model compression, serving, and pipeline tools with excellent support for Chinese LLMs (InternLM, Qwen, DeepSeek). The project is a top choice for teams deploying Chinese open-source models.

### 2. Gotchas of Using This Tool

LMDeploy has 597 open issues and 4 published security advisories. The TurboMind engine is tightly coupled to specific model architectures — support for new models requires manual integration. Documentation is primarily in Chinese, creating a language barrier for international users. The project is less well-known outside the Chinese AI ecosystem.

### 3. Limitations

TurboMind's per-model optimization means new model architectures may not be immediately supported. International community and documentation are limited compared to vLLM or SGLang. Some advanced features (W4A16, KV cache quantization) require specific hardware configurations.

### 4. How Secure Is This Tool?

4 published GitHub security advisories indicate some security maintenance. Apache-2.0 license is business-friendly. The project is developed in China, which may raise data sovereignty concerns for some organizations — though the code itself is open-source and auditable.

### 5. Usefulness to General Public and Non-Technical Users

**Rating: 4/10**

LMDeploy's TurboMind engine uniquely achieves 1.5x vLLM throughput on AWQ and MXFP4 quantized models through optimized CUDA kernels. For teams heavily invested in AWQ quantization (common in the Chinese AI ecosystem), this provides a meaningful performance advantage. Its tight integration with InternLM models is also unique.

### 6. What Does This Tool Solve That Others Don't?

LMDeploy's TurboMind engine uniquely achieves 1.5x vLLM throughput on AWQ and MXFP4 quantized models through optimized CUDA kernels. For teams heavily invested in AWQ quantization (common in the Chinese AI ecosystem), this provides a meaningful performance advantage. Its tight integration with InternLM models is also unique.

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

Development is active (pushed July 2026) with 701 forks. Improvement areas include English documentation, broader model architecture support, international community building, and reducing the issue backlog. Better integration with Western model formats would expand adoption.

### 9. Official Maintainer Contacts

Maintained by Shanghai AI Laboratory (InternLM team). Contact via GitHub Issues at InternLM/lmdeploy or their community channels. The project is part of the OpenInternLM ecosystem.

### 10. General Usage Guidance

Best for deploying Chinese LLMs (InternLM, Qwen, DeepSeek) with AWQ quantization. Compare with vLLM for broader model support and SGLang for RAG workloads. For international teams, be prepared for Chinese-language documentation and community.

---

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
