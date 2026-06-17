# Lambda Labs

- **Category**: Model Serving & Inference Engines
- **Type**: GPU Cloud
- **License**: Commercial
- **Region**: US
- **Tier**: A
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-06-16

> $3.78/hr H100 SXM; 99.9% SLA; 1-Click Clusters (16-2,000 GPUs); no egress fees

---

## Overview

Lambda Labs is a gpu cloud in the model serving and inference engines category.

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
# No proprietary CLI required; standard SSH after launch
ssh ubuntu@<INSTANCE_IP> -i ~/.ssh/lambda_key
```
Account + API key: https://cloud.lambda.ai → Add payment method → Generate API key → Add SSH key (required before launching).

### Known sharp edges (from community / docs)
1. **No native serverless / auto-scaling** — Lambda is instance-based (like EC2). You must bring your own orchestration (Kubernetes, custom scripts) for scale-to-zero inference.
2. **Idle billing blind spot** — Lambda 'does not distinguish between idle and in use instance states.' One user reported a $583 bill for a forgotten idle instance running 16 days.
3. **Per-minute billing** — Stopping an instance mid-minute still rounds up; less granular than RunPod's per-second serverless tier.
4. **No spot instances** — All on-demand or reserved. No interruptible discount pricing for fault-tolerant training.
5. **GPU availability tightens** — H100 on-demand can sell out during peak demand. B200 instances have 1–2 week wait lists as of early 2026.
6. **Persistent filesystem billing continues unmounted** — If you create a persistent filesystem, it bills hourly (~$0.20/GiB/month) even when no instance is attached.

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

> Raw results JSON: `benchmarks/lambda-labs-<date>.json`

---

## Bug Notes

### Smoke gate findings
- ⏳ Not yet tested

### Known issues (from community / docs)
1. **No native serverless / auto-scaling** — Lambda is instance-based (like EC2). You must bring your own orchestration (Kubernetes, custom scripts) for scale-to-zero inference.
2. **Idle billing blind spot** — Lambda 'does not distinguish between idle and in use instance states.' One user reported a $583 bill for a forgotten idle instance running 16 days.
3. **Per-minute billing** — Stopping an instance mid-minute still rounds up; less granular than RunPod's per-second serverless tier.
4. **No spot instances** — All on-demand or reserved. No interruptible discount pricing for fault-tolerant training.
5. **GPU availability tightens** — H100 on-demand can sell out during peak demand. B200 instances have 1–2 week wait lists as of early 2026.
6. **Persistent filesystem billing continues unmounted** — If you create a persistent filesystem, it bills hourly (~$0.20/GiB/month) even when no instance is attached.

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
- [RunPod](runpod.md)
- [LiteLLM](litellm.md)
- [Portkey](portkey.md)

### Complementary tools
- ⏳ TBD (tools commonly used together)

### Alternatives to consider
- ⏳ TBD (when this tool is not the right fit)

---

## Links

- Official site: https://lambdalabs.com (console at https://cloud.lambda.ai)
- GitHub: N/A (commercial)
- Documentation: https://docs.lambdalabs.com
- Community / Discord: No public Discord widely promoted; support via https://lambdalabs.com/support
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
