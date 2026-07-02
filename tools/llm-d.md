# llm-d

- **Category**: Model Serving & Inference Engines
- **Type**: Distributed Inference
- **License**: Open source
- **Region**: Global
- **Tier**: B
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-06-16

> Community; multi-node, multi-GPU for 70B+; disaggregated serving; KV cache offloading

---

## Overview

llm-d is a distributed inference in the model serving and inference engines category.

**Supported model formats**: safetensors, pytorch

**Supported quantization**: fp16, bf16, fp8, int8

**Hardware target**: Multi-node

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

llm-d is a community-driven distributed inference framework designed for multi-node, multi-GPU serving of large models (70B+). It implements disaggregated serving (separating prefill from decode) and KV cache offloading for efficient resource utilization. The project targets Kubernetes-native deployments and is gaining traction as an alternative to Ray Serve for distributed LLM inference.

### 2. Gotchas of Using This Tool

llm-d is relatively new (3,665 stars) compared to established alternatives like vLLM (85K+) — production readiness is still being proven. The 182 open issues suggest active but early-stage development. Multi-node setup requires significant Kubernetes and networking expertise. Documentation for complex topologies is still maturing.

### 3. Limitations

The project is newer than competitors and has fewer battle-tested production deployments. The disaggregated serving architecture adds complexity that may not benefit smaller models or single-GPU setups. The community is smaller, meaning less community support and fewer third-party integrations.

### 4. How Secure Is This Tool?

No published security advisories. Apache-2.0 license. As a Kubernetes-native project, it inherits K8s security model (RBAC, network policies). However, the project's newness means security hardening is still in progress.

### 5. Usefulness to General Public and Non-Technical Users

**Rating: 3/10**

llm-d uniquely implements disaggregated serving with KV cache offloading in a Kubernetes-native package — separating prefill and decode onto different GPU pools for better resource utilization. This is particularly valuable for large MoE models where prefill and decode have very different compute profiles.

### 6. What Does This Tool Solve That Others Don't?

llm-d uniquely implements disaggregated serving with KV cache offloading in a Kubernetes-native package — separating prefill and decode onto different GPU pools for better resource utilization. This is particularly valuable for large MoE models where prefill and decode have very different compute profiles.

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

Development is very active (pushed July 2026) with growing community (574 forks). Improvement areas include production hardening, better documentation, simplified deployment, more inference engine integrations, and benchmark comparisons against Ray Serve and NVIDIA Dynamo.

### 9. Official Maintainer Contacts

Community-driven project. Contact via GitHub Issues at llm-d/llm-d or their community channels (linked from README). The project has contributions from engineers across multiple organizations.

### 10. General Usage Guidance

Best for teams needing distributed multi-node LLM serving on Kubernetes, especially for large 70B+ models. Compare with NVIDIA Dynamo (commercial backing) and Ray Serve (more mature). Start with the single-node deployment before scaling to multi-node.

---

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
