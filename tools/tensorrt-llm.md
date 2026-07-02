# TensorRT-LLM

- **Category**: Model Serving & Inference Engines
- **Type**: Inference Engine
- **License**: Apache-2.0 + closed
- **Region**: US
- **Tier**: A
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-06-16

> NVIDIA-backed; highest throughput; 30-60% faster than vLLM on H100; per-model compile

---

## Overview

TensorRT-LLM is a inference engine in the model serving and inference engines category.

**Supported model formats**: safetensors, pytorch, onnx, tensorrt

**Supported quantization**: fp16, bf16, fp8, int8, int4, awq

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
# Native pip install (Ubuntu 24.04 recommended)
sudo apt-get -y install libopenmpi-dev
pip3 install --upgrade pip setuptools
pip3 install tensorrt_llm -U --extra-index-url https://pypi.nvidia.com

# Verify
python3 -c "import tensorrt_llm; print(tensorrt_llm.__version__)"

# Or use pre-built Docker (recommended for reproducibility)
docker run --rm --runtime=nvidia --gpus all \
  --entrypoint /bin/bash -it \
  nvcr.io/nvidia/cuda:12.1.0-devel-ubuntu22.04

# Inside container:
apt-get update && apt-get -y install python3.10 python3-pip openmpi-bin libopenmpi-dev
pip3 install tensorrt_llm -U --extra-index-url https://pypi.nvidia.com

# Serve via the new LLM API (v1.0+)
python -c "
from tensorrt_llm import LLM
llm = LLM(model='meta-llama/Meta-Llama-3.1-8B-Instruct')
for output in llm.generate(['Hi, how are you?']):
    print(output.text)
"
```

### Known sharp edges (from community / docs)
1. **Installation fragility on newer drivers** — The `pip install tensorrt_llm` path can fail on newer NVIDIA drivers because the wheel tries to load CUDA libraries from hardcoded `/usr/` paths. Docker-based installs are more reliable.
2. **Segmentation fault on multimodal batch inference** — Batch inference with 2+ images on Qwen2-VL-7B can crash with SIGSEGV in the vision engine (`promptTuningBuffers`). Single-image inference often works fine.
3. **Windows support deprecated** — As of v0.18.0, Windows is officially deprecated and will be fully removed in future releases. Windows users must use WSL2.
4. **SBSA PyTorch workflow incompatibility** — The PyTorch-native workflow on ARM SBSA platforms fails on bare-metal Ubuntu 24.04; NVIDIA mandates using the PyTorch NGC container for ARM.
5. **Complex model build / compilation step** — Unlike vLLM/SGLang, TensorRT-LLM historically requires an explicit "engine build" step. The newer PyTorch-native LLM API mitigates this, but advanced features still require manual build tuning.

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

> Raw results JSON: `benchmarks/tensorrt-llm-<date>.json`

---

## Bug Notes

### Smoke gate findings
- ⏳ Not yet tested

### Known issues (from community / docs)
1. **Installation fragility on newer drivers** — The `pip install tensorrt_llm` path can fail on newer NVIDIA drivers because the wheel tries to load CUDA libraries from hardcoded `/usr/` paths. Docker-based installs are more reliable.
2. **Segmentation fault on multimodal batch inference** — Batch inference with 2+ images on Qwen2-VL-7B can crash with SIGSEGV in the vision engine (`promptTuningBuffers`). Single-image inference often works fine.
3. **Windows support deprecated** — As of v0.18.0, Windows is officially deprecated and will be fully removed in future releases. Windows users must use WSL2.
4. **SBSA PyTorch workflow incompatibility** — The PyTorch-native workflow on ARM SBSA platforms fails on bare-metal Ubuntu 24.04; NVIDIA mandates using the PyTorch NGC container for ARM.
5. **Complex model build / compilation step** — Unlike vLLM/SGLang, TensorRT-LLM historically requires an explicit "engine build" step. The newer PyTorch-native LLM API mitigates this, but advanced features still require manual build tuning.

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
| Open source | Yes | License: Apache-2.0 + closed |
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

- Official site: https://nvidia.github.io/TensorRT-LLM/
- GitHub: https://github.com/NVIDIA/TensorRT-LLM
- Documentation: https://nvidia.github.io/TensorRT-LLM/
- Community / Discord: - WeChat Discussion Group (linked in README for real-time Q&A)
- NVIDIA Developer Forums: https://forums.developer.nvidia.com/c/ai-data-science/tensorrt/18
- Tech blogs on NVIDIA developer blog
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

TensorRT-LLM is NVIDIA's flagship LLM inference engine, achieving the highest throughput on NVIDIA GPUs — typically 30-60% faster than vLLM on H100/H200. It supports FP8/FP4 quantization, in-flight batching, speculative decoding, and per-model graph optimization. TensorRT-LLM is the engine behind NVIDIA NIM and many commercial inference providers (Together AI, Fireworks AI use it for optimization).

### 2. Gotchas of Using This Tool

TensorRT-LLM has 1,471 open issues. Per-model compilation is required — each model must be compiled for specific GPU architecture, which takes time and creates deployment complexity. NVIDIA-only (no AMD/Intel support). The build process can be challenging with many dependencies. Documentation for advanced features is sparse.

### 3. Limitations

Locked to NVIDIA GPUs. Per-model, per-GPU compilation creates large engine artifacts and slow iteration cycles. Source code includes proprietary NVIDIA components alongside open-source Apache-2.0 code. Not as flexible as vLLM for rapid model experimentation.

### 4. How Secure Is This Tool?

No published security advisories. The license is complex — some components are Apache-2.0, others are NVIDIA proprietary. Compiled engines are binary artifacts that can't be easily audited. NVIDIA provides security updates through TensorRT releases.

### 5. Usefulness to General Public and Non-Technical Users

**Rating: 3/10**

TensorRT-LLM achieves the highest raw throughput on NVIDIA GPUs through deep kernel-level optimization — the per-model graph compilation enables optimizations that JIT-based engines like vLLM can't perform. For latency-critical, maximum-throughput NVIDIA deployments, nothing else matches it.

### 6. What Does This Tool Solve That Others Don't?

TensorRT-LLM achieves the highest raw throughput on NVIDIA GPUs through deep kernel-level optimization — the per-model graph compilation enables optimizations that JIT-based engines like vLLM can't perform. For latency-critical, maximum-throughput NVIDIA deployments, nothing else matches it.

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

Development is very active (pushed July 2026) with 2,512 forks. Improvement areas include simplifying the compilation process, reducing engine build times, better documentation, broader model support, and reducing the dependency complexity. The open-source/community engagement could be improved.

### 9. Official Maintainer Contacts

Maintained by NVIDIA (TensorRT team). Contact via GitHub Issues at NVIDIA/TensorRT-LLM or NVIDIA developer forums. Enterprise support through NVIDIA support contracts.

### 10. General Usage Guidance

Best for maximum-throughput NVIDIA GPU deployments where per-model compilation is acceptable. Compare with vLLM (easier to use, broader hardware) and SGLang (RAG optimization). Use TensorRT-LLM when raw throughput on NVIDIA is the priority. Pre-built Docker images simplify deployment.

---

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
