# RunPod

- **Category**: Model Serving & Inference Engines
- **Type**: GPU Cloud + Serverless
- **License**: Commercial
- **Region**: US
- **Tier**: A
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-06-16

> $0.34-2.69/hr; Pods + Serverless + Community Cloud; 30+ regions; cost leader

---

## Overview

RunPod is a gpu cloud + serverless in the model serving and inference engines category.

**Supported model formats**: N/A

**Supported quantization**: N/A

**Hardware target**: Cloud

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
# CLI (optional, for pod management)
pip install runpodctl
# Serverless deployment is template-based via web UI or API
```
```python
# Serverless API example
import requests
response = requests.post(
    "https://api.runpod.ai/v2/{endpoint-id}/run",
    headers={"Authorization": f"Bearer {RUNPOD_API_KEY}"},
    json={"input": {"prompt": "Hello"}}
)
```
API key: generate at https://www.runpod.io/console/settings

### Known sharp edges (from community / docs)
1. **Dual-cloud confusion** — Community Cloud (third-party hosts, cheaper, inconsistent) vs. Secure Cloud (Tier 3/4 DCs, SOC-2). First-time users often deploy on the wrong tier.
2. **Serverless cold-start variance** — FlashBoot claims sub-200ms, but during peak demand cold starts can stretch to 5+ minutes. ~48% hit sub-200ms according to third-party tracking.
3. **Stopped pod storage double-billing** — Volume disks on stopped pods charge 2× the active rate ($0.20/GB/month vs. $0.10/GB/month). Migrate to Network Volumes to avoid this.
4. **Non-refundable credits** — Account deposits cannot be withdrawn; only spent on RunPod services. Over-depositing locks capital.
5. **New account fraud cap** — $80/hour default spend limit. Large training jobs require a support ticket to raise.
6. **Community Cloud outages** — 151+ outages tracked over six months on the community tier by StatusGator.

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

> Raw results JSON: `benchmarks/runpod-<date>.json`

---

## Bug Notes

### Smoke gate findings
- ⏳ Not yet tested

### Known issues (from community / docs)
1. **Dual-cloud confusion** — Community Cloud (third-party hosts, cheaper, inconsistent) vs. Secure Cloud (Tier 3/4 DCs, SOC-2). First-time users often deploy on the wrong tier.
2. **Serverless cold-start variance** — FlashBoot claims sub-200ms, but during peak demand cold starts can stretch to 5+ minutes. ~48% hit sub-200ms according to third-party tracking.
3. **Stopped pod storage double-billing** — Volume disks on stopped pods charge 2× the active rate ($0.20/GB/month vs. $0.10/GB/month). Migrate to Network Volumes to avoid this.
4. **Non-refundable credits** — Account deposits cannot be withdrawn; only spent on RunPod services. Over-depositing locks capital.
5. **New account fraud cap** — $80/hour default spend limit. Large training jobs require a support ticket to raise.
6. **Community Cloud outages** — 151+ outages tracked over six months on the community tier by StatusGator.

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
| Self-hostable | No | |
| Open source | No | License: Commercial |
| Audit trail | ⏳ TBD | |
| Data residency controls | ⏳ TBD | |
| On-premise deployment | No | |
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
- [Lambda Labs](lambda-labs.md)
- [LiteLLM](litellm.md)
- [Portkey](portkey.md)

### Complementary tools
- ⏳ TBD (tools commonly used together)

### Alternatives to consider
- ⏳ TBD (when this tool is not the right fit)

---

## Links

- Official site: https://www.runpod.io
- GitHub: N/A (commercial platform; some utility repos exist)
- Documentation: https://docs.runpod.io
- Community / Discord: - Discord: https://discord.gg/runpod (active developer community)
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
