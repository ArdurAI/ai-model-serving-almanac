# Ollama

- **Category**: Model Serving & Inference Engines
- **Type**: Local LLM Serving
- **License**: MIT
- **Region**: Global
- **Tier**: A
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-06-16

> 52M monthly downloads; on-premise; not for multi-tenant production (collapses under 5 concurrent)

---

## Overview

Ollama is a local llm serving in the model serving and inference engines category.

**Supported model formats**: gguf

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
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows (PowerShell)
irm https://ollama.com/install.ps1 | iex

# Docker
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# Pull and run a model
ollama pull gemma4
ollama run gemma4

# Start server (binds to localhost:11434 by default)
ollama serve

# API request
curl http://localhost:11434/api/chat -d '{
  "model": "gemma4",
  "messages": [{"role": "user", "content": "Why is the sky blue?"}],
  "stream": false
}'

# Python client
pip install ollama
python -c "import ollama; print(ollama.chat(model='gemma4', messages=[{'role': 'user', 'content': 'Hello'}]).message.content)"
```

### Known sharp edges (from community / docs)
1. **Not production-ready for multi-tenant** — No built-in authentication, per-user rate limiting, or fair-share scheduling. The concurrency knob (`OLLAMA_NUM_PARALLEL`, default 1) is global and the queue is unbounded. Multi-tenant use requires an external reverse proxy (Nginx, LiteLLM, Kong) or API gateway.
2. **GPU backend detection flakiness** — Ollama may fail to select ROCm/CUDA despite the GPU being visible, falling back to slow CPU inference. Logs often show `no nvidia devices detected` or `inference compute` confusion.
3. **Model download stalls** — `ollama pull` frequently hangs with `part X stalled; retrying` on certain networks/regions, leaving the model in a partially-downloaded, unusable state.
4. **VRAM allocation mysteries** — Even when `nvidia-smi` reports sufficient free VRAM, Ollama may refuse to load a model claiming insufficient memory, or offload layers to system RAM unpredictably.
5. **Security exposure risk** — CVE-2026-7482 demonstrated that exposing Ollama directly to the internet (`0.0.0.0:11434` without firewall) allows unauthenticated remote memory reads. Over 300,000 deployments were reportedly exposed.

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

> Raw results JSON: `benchmarks/ollama-<date>.json`

---

## Bug Notes

### Smoke gate findings
- ⏳ Not yet tested

### Known issues (from community / docs)
1. **Not production-ready for multi-tenant** — No built-in authentication, per-user rate limiting, or fair-share scheduling. The concurrency knob (`OLLAMA_NUM_PARALLEL`, default 1) is global and the queue is unbounded. Multi-tenant use requires an external reverse proxy (Nginx, LiteLLM, Kong) or API gateway.
2. **GPU backend detection flakiness** — Ollama may fail to select ROCm/CUDA despite the GPU being visible, falling back to slow CPU inference. Logs often show `no nvidia devices detected` or `inference compute` confusion.
3. **Model download stalls** — `ollama pull` frequently hangs with `part X stalled; retrying` on certain networks/regions, leaving the model in a partially-downloaded, unusable state.
4. **VRAM allocation mysteries** — Even when `nvidia-smi` reports sufficient free VRAM, Ollama may refuse to load a model claiming insufficient memory, or offload layers to system RAM unpredictably.
5. **Security exposure risk** — CVE-2026-7482 demonstrated that exposing Ollama directly to the internet (`0.0.0.0:11434` without firewall) allows unauthenticated remote memory reads. Over 300,000 deployments were reportedly exposed.

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
- [llama.cpp](llamacpp.md)
- [NVIDIA Dynamo](nvidia-dynamo.md)
- [KServe](kserve.md)
- [BentoML](bentoml.md)
- [Ray Serve](ray-serve.md)
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

- Official site: https://ollama.com
- GitHub: https://github.com/ollama/ollama
- Documentation: https://github.com/ollama/ollama/blob/main/docs/README.md
- Community / Discord: - Discord: https://discord.gg/ollama
- Reddit: r/ollama
- Twitter / X: @ollama
- GitHub Discussions: https://github.com/ollama/ollama/discussions
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

Ollama is the most popular local LLM runtime with 175K+ GitHub stars and 52M+ monthly downloads, providing the simplest way to run LLMs locally on macOS, Linux, and Windows. It wraps llama.cpp with a beautiful CLI and REST API, supports model pulling from a registry, and runs models with a single command (`ollama run llama3`). Ollama has become the standard for local AI development and prototyping.

### 2. Gotchas of Using This Tool

Ollama has 3,466 open issues — very high, reflecting the massive user base and diverse hardware configurations. The runtime collapses under concurrent load (5+ simultaneous requests) — it's designed for single-user local use, not multi-tenant production serving. No continuous batching means throughput is limited for concurrent requests.

### 3. Limitations

Not suitable for production multi-user serving — use vLLM, SGLang, or TGI instead. GPU memory management is opaque (users can't fine-tune memory allocation like vLLM's `--gpu-memory-utilization`). No multi-GPU tensor parallelism for large models. Model format is proprietary Modelfile (though based on GGUF).

### 4. How Secure Is This Tool?

No published GitHub security advisories despite 175K+ stars — either very secure or under-reported. The REST API server (when enabled) should not be exposed to the internet without authentication. Models are pulled from Ollama's registry — verify model integrity. MIT license is business-friendly.

### 5. Usefulness to General Public and Non-Technical Users

**Rating: 8/10**

Ollama uniquely provides zero-friction local LLM execution — `ollama run llama3` works on any platform with one command, no configuration, no GPU setup. For non-technical users, it's the only tool that makes local LLM running approachable. This simplicity has driven its massive adoption.

### 6. What Does This Tool Solve That Others Don't?

Ollama uniquely provides zero-friction local LLM execution — `ollama run llama3` works on any platform with one command, no configuration, no GPU setup. For non-technical users, it's the only tool that makes local LLM running approachable. This simplicity has driven its massive adoption.

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

Development is extremely active (pushed July 2026) with 16,798 forks. Improvement areas include concurrent request handling, multi-GPU support, better memory management controls, model provenance/verification, and a path from local prototyping to production serving.

### 9. Official Maintainer Contacts

Maintained by Ollama Inc. Contact via GitHub Issues at ollama/ollama, their Discord community, or email hello@ollama.com. The company is venture-backed.

### 10. General Usage Guidance

Best for local LLM development and prototyping. For production serving, use vLLM or SGLang. Start with `ollama run llama3.1` and explore the model library at ollama.com/library. Pair with Open WebUI for a ChatGPT-like interface.

---

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
