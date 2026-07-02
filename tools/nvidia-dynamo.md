# NVIDIA Dynamo

- **Category**: Model Serving & Inference Engines
- **Type**: Orchestration
- **License**: Open source
- **Region**: US
- **Tier**: A
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-06-16

> GTC 2026; disaggregated serving; KV-aware routing; 7x Blackwell boost; replaces Triton

---

## Overview

NVIDIA Dynamo is a orchestration in the model serving and inference engines category.

**Supported model formats**: safetensors, pytorch, tensorrt

**Supported quantization**: fp16, bf16, fp8, int8

**Hardware target**: Multi-node

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
# Option A: Pre-built container (fastest)
docker run --gpus all --network host --rm -it \
  nvcr.io/nvidia/ai-dynamo/sglang-runtime:1.2.1

# Inside container — start frontend and worker
python3 -m dynamo.frontend --http-port 8000 --discovery-backend file > /dev/null 2>&1 &
python3 -m dynamo.sglang --model-path Qwen/Qwen3-0.6B --discovery-backend file &

# Send request
curl -s localhost:8000/v1/chat/completions -H "Content-Type: application/json" -d '{
  "model": "Qwen/Qwen3-0.6B",
  "messages": [{"role": "user", "content": "Hello!"}],
  "max_tokens": 100
}' | jq

# Option B: PyPI install (requires uv)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install --prerelease=allow "ai-dynamo[sglang]"   # or [vllm]

# Option C: Kubernetes zero-config deploy
cat <<EOF | kubectl apply -f -
apiVersion: nvidia.com/v1beta1
kind: DynamoGraphDeploymentRequest
metadata:
  name: my-model
spec:
  model: Qwen/Qwen3-0.6B
  backend: vllm
  sla:
    ttft: 200.0
    itl: 20.0
  autoApply: true
EOF
```

### Known sharp edges (from community / docs)
1. **Complex dev build dependencies** — Building from source requires Rust toolchain, `libhwloc-dev`, `libudev-dev`, `protobuf-compiler`, and `cmake` on Ubuntu 24.04 — not a simple `pip install`.
2. **Backend-specific CUDA/PyPI index friction** — TensorRT-LLM backend requires `--extra-index-url https://pypi.nvidia.com` and strict CUDA version compatibility. vLLM backend needs `--kv-events-config` for local file-based discovery without NATS/etcd.
3. **Rapid API evolution** — Open-sourced at GTC 2025; 1.0 released March 2026. Config keys and CRD schemas are still stabilizing between minor versions.
4. **Multi-node topology sensitivity** — Disaggregated prefill/decode requires careful NUMA/NVLink-aware placement. The `Grove` K8s operator is required for optimal GB200/NVL72 gang scheduling.
5. **NIXL transfer failures across subnets** — GPU-to-GPU weight streaming via NIXL assumes RDMA/NVLink connectivity; fallback TCP paths are slower and may timeout on large checkpoints.

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

> Raw results JSON: `benchmarks/nvidia-dynamo-<date>.json`

---

## Bug Notes

### Smoke gate findings
- ⏳ Not yet tested

### Known issues (from community / docs)
1. **Complex dev build dependencies** — Building from source requires Rust toolchain, `libhwloc-dev`, `libudev-dev`, `protobuf-compiler`, and `cmake` on Ubuntu 24.04 — not a simple `pip install`.
2. **Backend-specific CUDA/PyPI index friction** — TensorRT-LLM backend requires `--extra-index-url https://pypi.nvidia.com` and strict CUDA version compatibility. vLLM backend needs `--kv-events-config` for local file-based discovery without NATS/etcd.
3. **Rapid API evolution** — Open-sourced at GTC 2025; 1.0 released March 2026. Config keys and CRD schemas are still stabilizing between minor versions.
4. **Multi-node topology sensitivity** — Disaggregated prefill/decode requires careful NUMA/NVLink-aware placement. The `Grove` K8s operator is required for optimal GB200/NVL72 gang scheduling.
5. **NIXL transfer failures across subnets** — GPU-to-GPU weight streaming via NIXL assumes RDMA/NVLink connectivity; fallback TCP paths are slower and may timeout on large checkpoints.

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
| Open source | Yes | License: Open source |
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

- Official site: https://developer.nvidia.com/dynamo
- GitHub: https://github.com/ai-dynamo/dynamo
- Documentation: https://docs.nvidia.com/dynamo/latest/index.html
- Community / Discord: - Discord: https://discord.gg/D92uqZRjCZ
- Community Meetings: Weekly Wed 10:30 AM PT (YouTube recorded)
- Office Hours: Biweekly calls
- Design Proposals / RFCs: https://github.com/ai-dynamo/enhancements
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

NVIDIA Dynamo is a datacenter-scale distributed inference framework announced at GTC 2025/2026, designed to replace Triton Inference Server as NVIDIA's recommended LLM serving platform. It implements disaggregated serving (separating prefill from decode), KV-aware routing, and claims 7x throughput improvements on Blackwell GPUs. Dynamo supports multiple backend engines (TensorRT-LLM, vLLM, SGLang) and is rapidly becoming the standard for large-scale NVIDIA inference.

### 2. Gotchas of Using This Tool

Dynamo has 781 open issues, reflecting its ambitious scope and rapid development. The project is very new (announced 2025) — production deployments are still early-stage. The architecture (Rust-based microservices) requires understanding of distributed systems. Documentation for advanced configurations is still evolving.

### 3. Limitations

Optimized for NVIDIA GPUs only — no AMD or Intel support. The disaggregated serving architecture adds complexity that benefits large-scale deployments but may be overkill for smaller setups. Being new, it lacks the battle-tested maturity of vLLM or Triton.

### 4. How Secure Is This Tool?

No published security advisories yet, but the project is new. As an NVIDIA project, it follows NVIDIA's security practices. The Rust core provides memory safety advantages. The microservice architecture requires careful network security configuration.

### 5. Usefulness to General Public and Non-Technical Users

**Rating: 3/10**

Dynamo uniquely implements KV-aware routing — routing requests to the GPU that already has the relevant KV cache, avoiding recomputation. Combined with disaggregated serving, this provides dramatic throughput improvements for large-scale multi-GPU deployments. The 7x Blackwell claim, if accurate, represents a generational leap.

### 6. What Does This Tool Solve That Others Don't?

Dynamo uniquely implements KV-aware routing — routing requests to the GPU that already has the relevant KV cache, avoiding recomputation. Combined with disaggregated serving, this provides dramatic throughput improvements for large-scale multi-GPU deployments. The 7x Blackwell claim, if accurate, represents a generational leap.

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

Development is extremely active (pushed July 2026) with 1,298 forks — one of the fastest-growing projects in this category. Improvement areas include reducing complexity, better documentation, stabilizing APIs, broader backend engine support, and production hardening.

### 9. Official Maintainer Contacts

Maintained by NVIDIA (AI Dynamics team). Contact via GitHub Issues at ai-dynamo/dynamo or NVIDIA developer forums. The project is open-source under NVIDIA's governance.

### 10. General Usage Guidance

Best for large-scale NVIDIA GPU deployments that need maximum throughput. It's positioned as the successor to Triton Inference Server for LLM workloads. For smaller deployments, vLLM or SGLang are simpler. Start with the Dynamo Cloud-in-a-Box examples.

---

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
