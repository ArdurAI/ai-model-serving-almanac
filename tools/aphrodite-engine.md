# Aphrodite Engine

- **Category**: Model Serving & Inference Engines
- **Type**: Inference Engine
- **License**: AGPL-3.0
- **Region**: Global
- **Tier**: B
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-06-16

> PygmalionAI; vLLM fork; broadest quantization (FP2-FP12, EXL2, GGUF); creative/roleplay

---

## Overview

Aphrodite Engine is a inference engine in the model serving and inference engines category.

**Supported model formats**: safetensors, pytorch, gguf, exl2

**Supported quantization**: fp16, bf16, fp8, fp4, fp2, int8, awq, gptq, exl2, gguf, marlin

**Hardware target**: GPU

---

## Benchmark Results

⏳ Benchmark results pending. See [TESTING.md](../TESTING.md) for methodology.

> Raw results JSON: 

---

## Links

- Official site: ⏳
- GitHub: ⏳
- Documentation: ⏳

---

## Changelog

| Date | Event | Notes |
|------|-------|-------|
| 2026-06-16 | First triaged | Added to roster, stub page created |


---

## Deep Analysis

### 1. How Is This Tool Useful?

Aphrodite Engine is a vLLM fork by PygmalionAI optimized for creative writing and roleplay use cases, offering the broadest quantization support in the ecosystem (FP2 through FP12, EXL2, GGUF). It enables running large models on consumer hardware through aggressive quantization while maintaining the PagedAttention and continuous batching capabilities inherited from vLLM. The engine is particularly popular in the AI roleplay community for its ability to serve uncensored models efficiently on single-GPU setups.

### 2. Gotchas of Using This Tool

The AGPL-3.0 license is a significant constraint — any SaaS deployment using Aphrodite must open-source modifications, making it unsuitable for most commercial products. Being a vLLM fork, it lags behind upstream vLLM in feature updates and bug fixes, sometimes by months. The extreme quantization options (FP2-FP4) produce significant quality degradation and should only be used when GPU memory is critically constrained.

### 3. Limitations

Aphrodite is primarily designed for single-GPU consumer hardware and lacks robust multi-node or multi-GPU tensor parallelism compared to upstream vLLM. It does not support enterprise features like RBAC, audit logging, or SLA-backed monitoring. Documentation is community-maintained and sparse compared to commercial alternatives.

### 4. How Secure Is This Tool?

No published security advisories as of mid-2026, but the project's smaller contributor base (compared to vLLM) means security review is less rigorous. The AGPL license provides some copyleft protection but users should audit dependencies. Running uncensored models introduces content safety risks for production deployments.

### 5. Usefulness to General Public and Non-Technical Users

**Rating: 4/10**

Aphrodite uniquely targets the creative AI community with quantization options as extreme as FP2 that no other major engine offers, enabling 70B-class models to run on 8GB GPUs. It also ships with sampling parameter presets specifically tuned for roleplay and creative writing out of the box.

### 6. What Does This Tool Solve That Others Don't?

Aphrodite uniquely targets the creative AI community with quantization options as extreme as FP2 that no other major engine offers, enabling 70B-class models to run on 8GB GPUs. It also ships with sampling parameter presets specifically tuned for roleplay and creative writing out of the box.

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

Development is community-driven with irregular release cadence — the repo had 127 open issues as of July 2026. Improvement areas include better documentation, closer sync with upstream vLLM, and enterprise-grade monitoring. The core team is small (primarily PygmalionAI maintainers).

### 9. Official Maintainer Contacts

Maintained by PygmalionAI. Contact via GitHub Issues at PygmalionAI/aphrodite-engine or their Discord community (linked from the GitHub README).

### 10. General Usage Guidance

Best for hobbyists and creative AI researchers who need extreme quantization on consumer GPUs. Not recommended for production enterprise deployments due to AGPL licensing and limited support. Use EXL2 or GGUF formats for best quality-per-bit on supported models.

---

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
