# BentoML

- **Category**: Model Serving & Inference Engines
- **Type**: Model Serving
- **License**: Apache-2.0
- **Region**: Global
- **Tier**: A
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-06-16

> Python-first packaging; BentoCloud hosted; multi-framework

---

## Overview

BentoML is a model serving in the model serving and inference engines category.

**Supported model formats**: safetensors, pytorch, onnx, pickle

**Supported quantization**: fp16, bf16, fp8, int8

**Hardware target**: GPU|Multi-node

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
# Install
pip install -U bentoml   # Requires Python >= 3.9

# Create service.py (example pattern), then:
bentoml serve            # Local dev server at http://localhost:3000

# Build reproducible artifact ("Bento")
bentoml build

# Containerize (requires Docker running)
bentoml containerize summarization:latest

# Run container
docker run --rm -p 3000:3000 summarization:latest

# Deploy to BentoCloud
bentoml cloud login
bentoml deploy
```

### Known sharp edges (from community / docs)
1. **Dependency ordering in containerize** — `bentoml containerize` can fail when packages have build-time cross-dependencies (e.g., Detectron2 requires `torch` at `setup.py` time, but pip installs alphabetically).
2. **`--output` CLI flag bug** — `bentoml containerize --opt output=type=registry` causes duplicate `--output` flags and crashes with both `docker` and `buildctl` backends.
3. **Config env var FileNotFound in containers** — Setting `BENTOML_CONFIG=./config/default.yaml` in `bentofile.yaml` `env` section causes startup failure inside Docker because the path does not exist in the generated image.
4. **`serve` works but `containerize` fails** — Local development may succeed while container builds fail due to Docker daemon detection issues or backend health checks.
5. **Yatai/BentoCRD deployment opacity** — Deploying to Kubernetes via BentoRequest/Bento CRD can result in no pods spinning up with minimal error feedback, requiring deep event-log inspection.

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

> Raw results JSON: `benchmarks/bentoml-<date>.json`

---

## Bug Notes

### Smoke gate findings
- ⏳ Not yet tested

### Known issues (from community / docs)
1. **Dependency ordering in containerize** — `bentoml containerize` can fail when packages have build-time cross-dependencies (e.g., Detectron2 requires `torch` at `setup.py` time, but pip installs alphabetically).
2. **`--output` CLI flag bug** — `bentoml containerize --opt output=type=registry` causes duplicate `--output` flags and crashes with both `docker` and `buildctl` backends.
3. **Config env var FileNotFound in containers** — Setting `BENTOML_CONFIG=./config/default.yaml` in `bentofile.yaml` `env` section causes startup failure inside Docker because the path does not exist in the generated image.
4. **`serve` works but `containerize` fails** — Local development may succeed while container builds fail due to Docker daemon detection issues or backend health checks.
5. **Yatai/BentoCRD deployment opacity** — Deploying to Kubernetes via BentoRequest/Bento CRD can result in no pods spinning up with minimal error feedback, requiring deep event-log inspection.

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
| Open source | Yes | License: Apache-2.0 |
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
- [NVIDIA Dynamo](nvidia-dynamo.md)
- [KServe](kserve.md)
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

- Official site: https://bentoml.com
- GitHub: https://github.com/bentoml/BentoML
- Documentation: https://docs.bentoml.com
- Community / Discord: - Slack: https://l.bentoml.com/join-slack
- Twitter / X: @bentomlai
- GitHub Issues & Discussions: https://github.com/bentoml/BentoML/issues
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

BentoML is a Python-first model serving framework that handles the full lifecycle from packaging to deployment, supporting multi-framework models (PyTorch, TensorFlow, scikit-learn, Hugging Face) with a unified API. Its Bento packaging format creates reproducible, Docker-ready model artifacts that can run anywhere. BentoCloud provides a managed deployment option for teams wanting zero-infra serving.

### 2. Gotchas of Using This Tool

BentoML has 11 published security advisories, so production deployments must track CVEs carefully. The framework adds overhead compared to bare inference engines like vLLM — it's a serving layer, not an inference optimizer. Building Bentos for complex multi-model pipelines can be tricky with dependency conflicts across model requirements.

### 3. Limitations

BentoML is not an inference engine itself — it wraps other engines, so throughput is bounded by the underlying engine. The Python-centric design means it's less suitable for ultra-low-latency edge deployments. BentoCloud (managed offering) is a separate commercial product with its own pricing.

### 4. How Secure Is This Tool?

11 published GitHub security advisories as of mid-2026 indicates active security maintenance. The project participates in responsible disclosure. BentoML supports OCI artifact signing and supply chain security features. Enterprise BentoCloud adds SSO, RBAC, and audit logging.

### 5. Usefulness to General Public and Non-Technical Users

**Rating: 5/10**

BentoML solves the model packaging problem better than any other tool — its Bento format creates self-contained, versioned, deployable artifacts that work identically across local, cloud, and edge environments. No other serving framework offers this level of packaging portability combined with multi-framework support.

### 6. What Does This Tool Solve That Others Don't?

BentoML solves the model packaging problem better than any other tool — its Bento format creates self-contained, versioned, deployable artifacts that work identically across local, cloud, and edge environments. No other serving framework offers this level of packaging portability combined with multi-framework support.

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

Development is very active — the repo was pushed to in June 2026 with 979 forks. The team regularly ships releases. Improvement areas include better native LLM inference engine integrations (deeper vLLM/SGLang support), reduced packaging overhead, and more Kubernetes-native features.

### 9. Official Maintainer Contacts

Maintained by BentoML Inc. Contact via GitHub Issues at bentoml/BentoML, community Slack (invite at bentoml.com), or email hello@bentoml.com. Founders are active in the community.

### 10. General Usage Guidance

Best for teams that need to serve diverse model types (not just LLMs) with strong packaging and portability. Pair with vLLM or SGLang for LLM-specific serving. Use BentoCloud for managed deployment, or deploy Bentos to any Kubernetes cluster.

---

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
