# llama.cpp

- **Category**: Model Serving & Inference Engines
- **Type**: Inference Engine
- **License**: MIT
- **Region**: Global
- **Tier**: A
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-06-16

> 100K+ stars; GGUF format; Metal/CUDA/Vulkan/ROCm; ARM, Raspberry Pi, WASM

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

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
