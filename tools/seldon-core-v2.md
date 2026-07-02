# Seldon Core v2

- **Category**: Model Serving & Inference Engines
- **Type**: K8s Model Serving
- **License**: Apache-2.0
- **Region**: Global
- **Tier**: B
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-06-16

> Multi-step pipelines; drift detection; MLServer multi-model per GPU

---

## Overview

Seldon Core v2 is a k8s model serving in the model serving and inference engines category.

**Supported model formats**: safetensors, pytorch, onnx, tensorflow, sklearn

**Supported quantization**: fp16, bf16, int8

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

Seldon Core v2 is a Kubernetes-native MLOps framework for deploying, monitoring, and managing ML models at scale, featuring multi-step inference pipelines, drift detection, and the MLServer runtime for multi-model packing per GPU. Seldon Core is one of the most mature production ML serving platforms, widely used in financial services and enterprise environments. The v2 architecture introduces a cloud-native message bus and improved scaling.

### 2. Gotchas of Using This Tool

Seldon Core v2 is a significant architectural change from v1 — migration is non-trivial and some v1 features are not yet ported. The repo has 394 open issues. Last push was March 2026, raising concerns about development pace. The commercial Seldon Deploy product adds cost for enterprise features.

### 3. Limitations

v2 is still maturing compared to the battle-tested v1. Complex pipeline configurations require deep understanding of the Seldon architecture. Performance overhead is higher than bare inference engines. The project faces strong competition from KServe (CNCF-backed standard) which is gaining momentum.

### 4. How Secure Is This Tool?

Seldon Core supports Kubernetes RBAC, network policies, and integrates with OAuth2/OIDC for authentication. The v2 message bus architecture (based on Knative/CloudEvents) provides good security isolation. Enterprise Seldon Alibi (adversarial detection, drift monitoring) adds security for model integrity.

### 5. Usefulness to General Public and Non-Technical Users

**Rating: 3/10**

Seldon Core uniquely provides multi-step inference pipelines with drift detection and explainability built into the serving layer. The MLServer runtime enables packing multiple models per GPU for better utilization — a feature critical for cost optimization with expensive GPUs. Seldon Alibi adds production ML monitoring that no other serving tool provides natively.

### 6. What Does This Tool Solve That Others Don't?

Seldon Core uniquely provides multi-step inference pipelines with drift detection and explainability built into the serving layer. The MLServer runtime enables packing multiple models per GPU for better utilization — a feature critical for cost optimization with expensive GPUs. Seldon Alibi adds production ML monitoring that no other serving tool provides natively.

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

Development appears to have slowed (last push March 2026). The project needs to accelerate v2 development, improve migration tooling from v1, reduce complexity, and compete more effectively with KServe. Better documentation and community engagement are critical.

### 9. Official Maintainer Contacts

Maintained by Seldon Technologies Ltd. Contact via GitHub Issues at SeldonIO/seldon-core, their Slack community, or enterprise sales at seldon.io.

### 10. General Usage Guidance

Best for enterprise ML deployments needing inference pipelines, drift detection, and multi-model GPU packing. Compare with KServe (CNCF standard, simpler) and BentoML (Python-first, easier). Consider migration path carefully if already on Seldon Core v1.

---

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
