# Kueue

- **Category**: Model Serving & Inference Engines
- **Type**: GPU Scheduling
- **License**: Apache-2.0
- **Region**: Global
- **Tier**: B
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-06-16

> CNCF; multi-tenant GPU queueing; fair-share; preemption; GPU util 25-35% → 60-85%

---

## Overview

Kueue is a gpu scheduling in the model serving and inference engines category.

**Supported model formats**: N/A

**Supported quantization**: N/A

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

Kueue is a Kubernetes-native job queueing system (CNCF project) that manages batch workloads including AI/ML training and inference. It provides fair-share scheduling, preemption, priority queues, and multi-tenant resource management. Organizations report improving GPU utilization from 25-35% to 60-85% by using Kueue for GPU batch scheduling.

### 2. Gotchas of Using This Tool

Kueue has 496 open issues, reflecting the complexity of Kubernetes scheduling. The fair-share and preemption policies require careful configuration to avoid starving low-priority workloads. Kueue manages Kubernetes Jobs — it doesn't handle real-time inference scaling (use KServe or HPA for that).

### 3. Limitations

Kueue is specifically for batch job scheduling, not real-time serving. Integration with existing CI/CD pipelines requires understanding Kueue's admission webhooks and resource flavors. The project is evolving rapidly, with API changes between minor versions.

### 4. How Secure Is This Tool?

No published security advisories. As a Kubernetes SIGs project, it follows Kubernetes security practices. Runs with elevated permissions (webhook admission), so RBAC configuration is important. Integrates with Kubernetes audit logging.

### 5. Usefulness to General Public and Non-Technical Users

**Rating: 2/10**

Kueue uniquely provides fair-share GPU queueing on Kubernetes — multiple teams can share a GPU cluster with guaranteed resource quotas and preemption policies. No other Kubernetes-native tool offers this level of multi-tenant batch scheduling for AI workloads. The 25-35% → 60-85% GPU utilization improvement is a major cost saver.

### 6. What Does This Tool Solve That Others Don't?

Kueue uniquely provides fair-share GPU queueing on Kubernetes — multiple teams can share a GPU cluster with guaranteed resource quotas and preemption policies. No other Kubernetes-native tool offers this level of multi-tenant batch scheduling for AI workloads. The 25-35% → 60-85% GPU utilization improvement is a major cost saver.

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

Development is very active (pushed July 2026) with 673 forks. Improvement areas include better documentation for multi-cluster setups, visualization tools for queue status, simpler configuration for common scheduling patterns, and tighter integration with inference frameworks.

### 9. Official Maintainer Contacts

Kubernetes SIGs project. Contact via GitHub Issues at kubernetes-sigs/kueue, the CNCF Slack (#kueue channel), or the Kubernetes mailing list. Maintainers include engineers from Google, Red Hat, and NVIDIA.

### 10. General Usage Guidance

Best for organizations sharing GPU clusters across multiple teams or projects. Pair with KServe for inference workloads and Kubeflow for training. Start with a single ClusterQueue and expand to multi-tenant setups as you learn the model.

---

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
