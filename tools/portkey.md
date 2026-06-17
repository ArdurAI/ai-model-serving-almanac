# Portkey

- **Category**: Model Serving & Inference Engines
- **Type**: AI Gateway
- **License**: Partially open
- **Region**: Global
- **Tier**: A
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-06-16

> 250+ models; 20-40ms latency; MCP Gateway; open source March 2026

---

## Overview

Portkey is a ai gateway in the model serving and inference engines category.

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
# Node.js / npx gateway (lightweight local gateway)
npx @portkey-ai/gateway
# Gateway runs on http://localhost:8787/v1

# Python SDK
pip install portkey-ai
```
```python
from portkey_ai import Portkey
client = Portkey(
    provider="openai",
    Authorization="sk-..."  # provider API key
)
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```
**Helm / Kubernetes self-host:**
```bash
helm repo add portkey-ai https://portkey-ai.github.io/helm
helm repo update
helm upgrade --install portkey-ai portkey-ai/gateway -f values.yaml -n portkey --create-namespace
```
**Docker self-host:**
```bash
docker run -p 8787:8787 portkeyai/gateway:latest
```
API key: create at https://app.portkey.ai → API Keys

### Known sharp edges (from community / docs)
1. **Log-based pricing limits observability** — Dev plan = 10K logs/month. Pro = 100K base + $9 per 100K additional (up to 3M). Exceeding the limit does not stop routing, but you lose dashboard visibility, cost tracking, and debugging data for excess requests.
2. **Short retention on Pro tier** — 30-day log retention only. Enterprise required for 90+ days. Many compliance regimes (SOX, healthcare) need longer retention.
3. **MCP support gaps** — As of early 2026, MCP gateway support is limited compared to competitors. Check current docs if agentic MCP is a hard requirement.
4. **Enterprise-only self-hosting for advanced governance** — VPC deployment, SSO, advanced RBAC, and air-gapped options are Enterprise-only. Pro tier does not offer private cloud.
5. **Provider cost + Portkey cost** — You pay Portkey for gateway/observability and you still pay OpenAI/Anthropic/etc. for actual tokens. TCO must be calculated as a surcharge, not a replacement.
6. **Scale cost inflection** — Above ~3M requests/month, self-hosted alternatives (LiteLLM OSS) or flat-fee competitors become cheaper than Portkey's per-log pricing.

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

> Raw results JSON: `benchmarks/portkey-<date>.json`

---

## Bug Notes

### Smoke gate findings
- ⏳ Not yet tested

### Known issues (from community / docs)
1. **Log-based pricing limits observability** — Dev plan = 10K logs/month. Pro = 100K base + $9 per 100K additional (up to 3M). Exceeding the limit does not stop routing, but you lose dashboard visibility, cost tracking, and debugging data for excess requests.
2. **Short retention on Pro tier** — 30-day log retention only. Enterprise required for 90+ days. Many compliance regimes (SOX, healthcare) need longer retention.
3. **MCP support gaps** — As of early 2026, MCP gateway support is limited compared to competitors. Check current docs if agentic MCP is a hard requirement.
4. **Enterprise-only self-hosting for advanced governance** — VPC deployment, SSO, advanced RBAC, and air-gapped options are Enterprise-only. Pro tier does not offer private cloud.
5. **Provider cost + Portkey cost** — You pay Portkey for gateway/observability and you still pay OpenAI/Anthropic/etc. for actual tokens. TCO must be calculated as a surcharge, not a replacement.
6. **Scale cost inflection** — Above ~3M requests/month, self-hosted alternatives (LiteLLM OSS) or flat-fee competitors become cheaper than Portkey's per-log pricing.

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
| Open source | Yes | License: Partially open |
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
- [LiteLLM](litellm.md)

### Complementary tools
- ⏳ TBD (tools commonly used together)

### Alternatives to consider
- ⏳ TBD (when this tool is not the right fit)

---

## Links

- Official site: https://portkey.ai
- GitHub: https://github.com/Portkey-AI/gateway
- Documentation: https://docs.portkey.ai
- Community / Discord: - Discord: https://discord.gg/portkey (community + `#portkey-docs`)
- Twitter / X: https://twitter.com/portkeyai
- LinkedIn: https://linkedin.com/company/portkey-ai
- YouTube: https://youtube.com/portkey
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
