# LiteLLM

- **Category**: Model Serving & Inference Engines
- **Type**: LLM Gateway
- **License**: MIT
- **Region**: US
- **Tier**: A
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-06-16

> 18K+ stars; 100+ providers; OpenAI-compatible proxy; YC W23

---

## Overview

LiteLLM is a llm gateway in the model serving and inference engines category.

**Supported model formats**: N/A

**Supported quantization**: N/A

**Hardware target**: Cloud|Multi-node

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
# Python SDK (call 100+ LLMs from Python code)
uv add litellm
# Or with pip
pip install litellm

# AI Gateway / Proxy Server (self-hosted OpenAI-compatible endpoint)
uv tool install 'litellm[proxy]'
# Or with pip
pip install 'litellm[proxy]'

# Start the proxy (simplest mode)
litellm --model gpt-4o
# Proxy now running on http://0.0.0.0:4000
```
```python
# Using the proxy with any OpenAI-compatible client
import openai
client = openai.OpenAI(api_key="anything", base_url="http://0.0.0.0:4000")
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```
```python
# Using the Python SDK directly
from litellm import completion
import os
os.environ["OPENAI_API_KEY"] = "sk-..."
response = completion(model="openai/gpt-4o", messages=[...])
response = completion(model="anthropic/claude-sonnet-4-20250514", messages=[...])
```
**Docker / production proxy:**
```bash
docker pull ghcr.io/berriai/litellm:latest-stable
# Or with docker-compose for Postgres + Redis backend
docker-compose up db prometheus
```

### Known sharp edges (from community / docs)
1. **PyPI supply chain incident (March 2026)** — A compromise occurred; maintainers responded with Sigstore signing and commit-pinning. You must pin to `v1.83.0+` and verify cosign signatures for production installs.
2. **Enterprise feature gating** — SSO, audit logs, and advanced RBAC require a BerriAI Enterprise License (commercial). Core proxy is MIT, but 'enterprise' folder is under a separate commercial license.
3. **DevOps overhead at scale** — Self-hosted proxy requires Postgres, Redis, and Prometheus for full feature parity. Managed alternative is 'LiteLLM Cloud' (BerriAI-hosted).
4. **Credential sprawl** — To use 100+ providers, you must manage API keys for each provider in environment variables or the proxy config. No built-in secret vault beyond `.env`.
5. **Rapid release velocity** — 1,300+ releases; `-stable` Docker tag is recommended over `latest` for production.

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

> Raw results JSON: `benchmarks/litellm-<date>.json`

---

## Bug Notes

### Smoke gate findings
- ⏳ Not yet tested

### Known issues (from community / docs)
1. **PyPI supply chain incident (March 2026)** — A compromise occurred; maintainers responded with Sigstore signing and commit-pinning. You must pin to `v1.83.0+` and verify cosign signatures for production installs.
2. **Enterprise feature gating** — SSO, audit logs, and advanced RBAC require a BerriAI Enterprise License (commercial). Core proxy is MIT, but 'enterprise' folder is under a separate commercial license.
3. **DevOps overhead at scale** — Self-hosted proxy requires Postgres, Redis, and Prometheus for full feature parity. Managed alternative is 'LiteLLM Cloud' (BerriAI-hosted).
4. **Credential sprawl** — To use 100+ providers, you must manage API keys for each provider in environment variables or the proxy config. No built-in secret vault beyond `.env`.
5. **Rapid release velocity** — 1,300+ releases; `-stable` Docker tag is recommended over `latest` for production.

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
- [Ollama](ollama.md)
- [LMDeploy](lmdeploy.md)
- [Fireworks AI](fireworks-ai.md)
- [Together AI](together-ai.md)
- [RunPod](runpod.md)
- [Lambda Labs](lambda-labs.md)
- [Portkey](portkey.md)

### Complementary tools
- ⏳ TBD (tools commonly used together)

### Alternatives to consider
- ⏳ TBD (when this tool is not the right fit)

---

## Links

- Official site: https://litellm.ai
- GitHub: https://github.com/BerriAI/litellm
- Documentation: https://docs.litellm.ai
- Community / Discord: - Community Discord: https://discord.gg/litellm
- Community Slack: linked via GitHub README
- Email: ishaan@berri.ai / krrish@berri.ai
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
