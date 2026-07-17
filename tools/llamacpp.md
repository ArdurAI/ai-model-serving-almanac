# llama.cpp


[![Infrastructure](https://img.shields.io/badge/Also_in-Infrastructure-blue)](https://github.com/ArdurAI/ai-infrastructure-almanac)

- **Category**: Model Serving & Inference Engines
- **Type**: Inference Engine
- **License**: MIT
- **Region**: Global
- **Tier**: A
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-07-17

> 120K+ stars; GGUF format; Metal/CUDA/Vulkan/ROCm; ARM, Raspberry Pi, WASM

---

## Overview

llama.cpp is a inference engine in the model serving and inference engines category.

**Supported model formats**: gguf, ggml

**Supported quantization**: q4_0, q4_1, q5_0, q5_1, q8_0, q2_k, q3_k, q4_k, q5_k, q6_k, q8_k, f16, f32

**Hardware target**: CPU|GPU|Edge

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
# macOS / Linux via Homebrew (simplest)
brew install llama.cpp

# Or build from source (Linux/macOS)
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp

# CPU-only build
make

# Or CMake (recommended for GPU backends)
cmake -B build
cmake --build build --config Release

# CUDA build
make GGML_CUDA=1
# or
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release

# Apple Metal build (default on macOS)
cmake -B build -DGGML_METAL=ON
cmake --build build --config Release

# Run CLI
./build/bin/llama-cli -m my_model.gguf -p "Hello, my name is"

# Run OpenAI-compatible server
./build/bin/llama-server -m my_model.gguf --port 8080

# Or download and run from HuggingFace directly
llama-cli -hf ggml-org/gemma-3-1b-it-GGUF
llama-server -hf ggml-org/gemma-3-1b-it-GGUF --port 8080
```

### Known sharp edges (from community / docs)
1. **Vulkan backend instability** — Multiple open issues report garbled/repetitive output, initialization bugs, shared memory overruns, and assertion failures on Linux, Windows, and Intel GPUs. Not production-ready for Vulkan.
2. **CUDA illegal memory access errors** — Crashes in `K-Shift` operations and other CUDA kernels on specific commits, especially on RTX 3090 and similar consumer cards. Often tied to kernel version or driver mismatch.
3. **ROCm/HIP performance regressions** — Significant slowdowns and system freezes on AMD GPUs with MoE models and unified KV cache changes. Prompt processing can become extremely slow.
4. **Quantization breakage for multimodal** — CLIP `mmproj` quantization has been broken since May 2025 (`unknown model architecture: 'clip'`). Blocks vision model quantization workflows.
5. **Build failures on newer toolchains** — Compilation fails on newer distributions with CUDA 12.8 + GCC 14 due to incompatibility between CUDA math headers and system headers. GCC version must often be pinned to match nvcc requirements.

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

> Raw results JSON: `benchmarks/llamacpp-<date>.json`

---

## Bug Notes

### Smoke gate findings
- ⏳ Not yet tested

### Known issues (from community / docs)
1. **Vulkan backend instability** — Multiple open issues report garbled/repetitive output, initialization bugs, shared memory overruns, and assertion failures on Linux, Windows, and Intel GPUs. Not production-ready for Vulkan.
2. **CUDA illegal memory access errors** — Crashes in `K-Shift` operations and other CUDA kernels on specific commits, especially on RTX 3090 and similar consumer cards. Often tied to kernel version or driver mismatch.
3. **ROCm/HIP performance regressions** — Significant slowdowns and system freezes on AMD GPUs with MoE models and unified KV cache changes. Prompt processing can become extremely slow.
4. **Quantization breakage for multimodal** — CLIP `mmproj` quantization has been broken since May 2025 (`unknown model architecture: 'clip'`). Blocks vision model quantization workflows.
5. **Build failures on newer toolchains** — Compilation fails on newer distributions with CUDA 12.8 + GCC 14 due to incompatibility between CUDA math headers and system headers. GCC version must often be pinned to match nvcc requirements.

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
| Open source | Yes | License: MIT |
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

- Official site: https://github.com/ggml-org/llama.cpp
- GitHub: https://github.com/ggml-org/llama.cpp
- Documentation: - Build guide: https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md
- Server docs: https://github.com/ggml-org/llama.cpp/blob/master/examples/server/README.md
- GBNF grammars: https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md
- Community / Discord: - GitHub Discussions: https://github.com/ggml-org/llama.cpp/discussions
- Very large ecosystem of downstream UIs and tools (Ollama, LM Studio, KoboldCpp, etc.)
- No official Discord; community is fragmented across GitHub, Reddit, and downstream projects.
- Benchmark adapter: ⏳ (link to harness repo when available)

---

## Changelog

| Date | Event | Notes |
|------|-------|-------|
| 2026-06-16 | First triaged | Added to roster, deep-dive template created |
| 2026-06-17 | Research enriched | Official links, setup commands, sharp edges populated from community research |


---

## Deep Analysis

### Daily monitoring update — 2026-07-17

- **Latest release:** `b10054` (2026-07-17): Adds documentation for using OpenCL with Adreno 810 and ships updated platform binaries, including macOS/iOS artifacts.
- **Adoption signal:** GitHub stars moved from 120,092 to 120,662 (+570). Track 120,662 as the current monitoring baseline because this crossed the >500 daily-change threshold.

### Daily monitoring update — 2026-07-12

- **Latest release:** `b9969` (2026-07-12): Vulkan routes large Adreno matmuls to medium tiles, fixing `llama-cli` failures on longer prompts with q4_0 quantized networks caused by insufficient shared memory; release artifacts were refreshed across macOS/iOS, Linux, Android, and Windows builds.

### Daily monitoring update — 2026-07-10

- **Latest release:** `b9948` (2026-07-10): reduces temporary CUDA memory usage by processing `ggml_top_k()` and `ggml_argsort()` in smaller chunks, allocates temporary buffers once per loop, and refreshes release artifacts across macOS/iOS/Linux backends.

### Daily monitoring update — 2026-07-09

- **Latest release:** `b9940` (2026-07-09): initializes offline parameters for `llama-bench` and refreshes release artifacts including macOS/iOS binaries.
- **Adoption signal:** GitHub stars moved from 119,244 to 119,779 (+535). Star references in this file now use the new 119,779 baseline.

### 1. How Is This Tool Useful?

llama.cpp is the most popular LLM inference engine by GitHub stars (120.7K+), providing C/C++ inference for GGUF-format models across CPU, GPU (CUDA, Metal, Vulkan, ROCm), and edge devices. It runs on everything from Raspberry Pi to multi-GPU servers and is the foundation for Ollama, LM Studio, and many other tools. The engine's broad hardware support and minimal dependencies make it the universal choice for local LLM inference.

### 2. Gotchas of Using This Tool

llama.cpp has 13 published security advisories — users must track CVEs. The GGUF format requires model conversion from safetensors/PyTorch. Performance tuning (thread count, batch size, GPU layers) requires experimentation for each hardware setup. The project moves fast with frequent breaking changes to the API and GGUF format.

### 3. Limitations

Not optimized for high-throughput multi-user serving — lacks continuous batching in the core library (though llama-server adds some concurrency support). Multi-GPU tensor parallelism is limited compared to vLLM or SGLang. The C/C++ codebase means extending it requires systems programming skills.

### 4. How Secure Is This Tool?

13 published GitHub security advisories indicate active security maintenance. Being a C/C++ project, memory safety is a concern — users should keep updated with the latest releases. The server mode exposes an API that should not be directly internet-facing without authentication.

### 5. Usefulness to General Public and Non-Technical Users

**Rating: 7/10**

llama.cpp uniquely provides universal LLM inference across the widest range of hardware — from ARM microcontrollers to datacenter GPUs — with a single codebase. Its GGUF format has become the de facto standard for quantized model distribution. No other engine matches its hardware breadth and portability.

### 6. What Does This Tool Solve That Others Don't?

llama.cpp uniquely provides universal LLM inference across the widest range of hardware — from ARM microcontrollers to datacenter GPUs — with a single codebase. Its GGUF format has become the de facto standard for quantized model distribution. No other engine matches its hardware breadth and portability.

### 7. How Does This Tool Rank Compared to Others?

| Rank | Tool | Stars | Key Advantage |
|------|------|-------|---------------|
| 1 | vLLM | 85K+ | Largest community, broadest hardware support |
| 2 | SGLang | 30K | RadixAttention, best for RAG workloads |
| 3 | TensorRT-LLM | 14K | Highest single-GPU throughput on NVIDIA |
| 4 | llama.cpp | 120K | Best for CPU/consumer hardware |
| 5 | Ollama | 175K | Easiest local deployment |

*See [tools/README.md](README.md) for the full ranking table.*

### 8. How Can This Tool Be Improved? How Active Is Development?

Development is extremely active (pushed July 2026) with 20,172 forks — one of the most actively developed open-source projects overall. Improvement areas include better multi-GPU support, continuous batching for serving, and stabilizing the GGUF format specification.

### 9. Official Maintainer Contacts

Maintained by Georgi Gerganov and a large community of contributors. Contact via GitHub Issues at ggml-org/llama.cpp or their IRC/Discord. The project is community-funded through GitHub Sponsors.

### 10. General Usage Guidance

Best for local LLM inference on any hardware. For production multi-user serving, wrap with Ollama or use vLLM/SGLang instead. Use GGUF Q4_K_M quantization for the best quality-speed tradeoff. Pair with a frontend like LM Studio or Text Generation WebUI for a GUI experience.

---

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.

---

*Authored by Team Ardur · CC BY 4.0*
