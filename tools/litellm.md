# LiteLLM


[![Observability](https://img.shields.io/badge/Also_in-Observability-blue)](https://github.com/ArdurAI/ai-observability-almanac) [![Infrastructure](https://img.shields.io/badge/Also_in-Infrastructure-blue)](https://github.com/ArdurAI/ai-infrastructure-almanac)

- **Category**: Model Serving & Inference Engines
- **Type**: LLM Gateway
- **License**: MIT
- **Region**: US
- **Tier**: A
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-07-17

> 53.8K+ stars; 100+ providers; OpenAI-compatible proxy; YC W23

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

## Deep Analysis

### Daily monitoring update — 2026-07-17

- **Adoption signal:** GitHub stars moved from 53,298 to 53,831 (+533). Track 53,831 as the current monitoring baseline because this crossed the >500 daily-change threshold.
- **Community health:** Open issues moved from 3,918 to 3,981 (+63). This is a material backlog increase; watch maintainer triage capacity, support load, and regression risk.

### Daily monitoring update — 2026-07-12

- **Latest release:** `v1.92.0` (2026-07-12): reiterates cosign verification for Docker image signatures and includes proxy fixes for team passthrough-route admin gating, Bedrock/Cohere embedding-type serialization, OpenAI responses cache-hit streaming, DeepSeek Anthropic-endpoint/tool sanitization, Bedrock batch metadata validation, plus Prometheus user budget metrics and test stabilization.
- **Community health:** Open issues increased from 3,841 to 3,918 (+77). This is a material backlog increase for a security-critical gateway component.

### Daily monitoring update — 2026-07-09

- **Latest release:** `v1.91.1` (2026-07-08): foregrounds Docker image signature verification with cosign and reiterates the release signing key; operators should verify images as part of supply-chain hygiene.
- **Community health:** Open issues increased from 3,641 to 3,828 (+187). This is a material backlog increase; monitor regression volume and maintainer response time.

### 1. How Is This Tool Useful?

LiteLLM is the most popular LLM gateway/proxy, providing a unified OpenAI-compatible API to call 100+ LLM providers (OpenAI, Anthropic, Bedrock, Azure, Cohere, VertexAI, vLLM, and more). It handles cost tracking, rate limiting, load balancing, fallbacks, caching, guardrails, and logging across all providers. The proxy server can be deployed as a gateway in front of any LLM infrastructure, making it the de facto standard for multi-provider LLM routing.

### 2. Gotchas of Using This Tool

LiteLLM has 3,981 open issues — one of the highest in the ecosystem — reflecting the challenge of maintaining 100+ provider integrations. The 12 published security advisories mean production deployments must track CVEs. Configuration for all 100+ providers is complex, and provider API changes frequently break integrations. The proxy adds ~20-50ms latency overhead.

### 3. Limitations

Not an inference engine — it routes to other providers/engines. The sheer number of provider integrations means some are poorly maintained. Enterprise features (SSO, RBAC, budget tracking UI) are in the paid version. The Python SDK has a large dependency footprint.

### 4. How Secure Is This Tool?

12 published GitHub security advisories as of mid-2026, indicating active security maintenance and responsible disclosure. The proxy handles API keys for all providers, making it a security-critical component — key management via environment variables or vault integration is essential. Enterprise version adds audit logging and PII redaction.

### 5. Usefulness to General Public and Non-Technical Users

**Rating: 5/10**

LiteLLM uniquely provides a single unified API for 100+ LLM providers with automatic fallback, load balancing, and cost tracking — no other gateway covers as many providers. This solves the multi-provider lock-in problem and enables cost optimization by routing to the cheapest capable provider per request.

### 6. What Does This Tool Solve That Others Don't?

LiteLLM uniquely provides a single unified API for 100+ LLM providers with automatic fallback, load balancing, and cost tracking — no other gateway covers as many providers. This solves the multi-provider lock-in problem and enables cost optimization by routing to the cheapest capable provider per request.

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

Development is extremely active (pushed July 2026) with 9,398 forks — one of the most actively developed projects in this category. Improvement areas include reducing the issue backlog, stabilizing provider integrations, reducing latency overhead, and improving documentation for the proxy configuration.

### 9. Official Maintainer Contacts

Maintained by BerriAI (YC W23). Contact via GitHub Issues at BerriAI/litellm, their Discord community, or the enterprise contact form at litellm.ai. Founded by Ishaan Jaff and Krithik Rao.

### 10. General Usage Guidance

Best as an LLM gateway/proxy in front of any inference setup. Pair with vLLM or SGLang for self-hosted models, or use it to route across managed APIs (OpenAI, Anthropic, Fireworks, etc.). Start with the proxy server for production deployments.

---

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.

---

*Authored by Team Ardur · CC BY 4.0*
