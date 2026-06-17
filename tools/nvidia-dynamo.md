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

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
