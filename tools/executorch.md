# ExecuTorch

- **Category**: Model Serving & Inference Engines
- **Type**: Edge Runtime
- **License**: Open source
- **Region**: US
- **Tier**: B
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-06-16

> Meta; 1.0 GA Oct 2025; 50KB footprint; 12+ hardware backends; billions of users

---

## Overview

ExecuTorch is a edge runtime in the model serving and inference engines category.

**Supported model formats**: pte, pytorch

**Supported quantization**: fp16, bf16, int8, int4

**Hardware target**: Edge

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

ExecuTorch is PyTorch's official edge AI runtime, enabling deployment of PyTorch models on mobile phones, embedded devices, and microcontrollers. It achieved 1.0 GA in October 2025 and supports 12+ hardware backends including Apple Silicon, Qualcomm, MediaTek, and Arm. The runtime has a ~50KB footprint and powers applications used by billions of users across Meta's apps.

### 2. Gotchas of Using This Tool

ExecuTorch has 1,341 open issues — the highest of any tool in this category — reflecting its ambitious scope and rapid development. Model export from PyTorch requires careful handling of operator coverage and backend-specific delegation. The API is still evolving post-1.0, meaning breaking changes can occur.

### 3. Limitations

LLM support on-device is still maturing — large model inference on phones is constrained by memory and compute. The 12+ backend support means each backend has varying levels of operator coverage and optimization. Documentation for advanced use cases (custom operators, custom backends) is still being built out.

### 4. How Secure Is This Tool?

No published security advisories. As a PyTorch Foundation project backed by Meta, it undergoes internal security review. Edge deployment introduces unique security considerations — models run on untrusted devices, requiring careful handling of model IP protection.

### 5. Usefulness to General Public and Non-Technical Users

**Rating: 6/10**

ExecuTorch is the only framework that provides a unified PyTorch-to-edge pipeline across mobile, embedded, and microcontroller targets. Its delegate system allows hardware-specific acceleration (CoreML, QNN, etc.) while maintaining a single export path from PyTorch training code.

### 6. What Does This Tool Solve That Others Don't?

ExecuTorch is the only framework that provides a unified PyTorch-to-edge pipeline across mobile, embedded, and microcontroller targets. Its delegate system allows hardware-specific acceleration (CoreML, QNN, etc.) while maintaining a single export path from PyTorch training code.

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

Development is extremely active (pushed July 2026) with 1,063 forks. The project needs to reduce the issue backlog (1,341 open), stabilize APIs post-1.0, improve documentation for custom backends, and expand LLM support for mobile devices. Community contributions are strong given the fork count.

### 9. Official Maintainer Contacts

Maintained by the PyTorch team at Meta. Contact via GitHub Issues at pytorch/executorch, PyTorch Discussion forums (discuss.pytorch.org), or the PyTorch Slack. Core maintainers include Meta engineers working on PyTorch mobile/edge.

### 10. General Usage Guidance

Best for deploying PyTorch models to mobile or edge devices, especially if you're already in the PyTorch ecosystem. For LLMs specifically, consider alongside MLC-LLM or MLX (Apple Silicon). Start with the tutorial models and verify operator coverage for your target backend.

---

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
