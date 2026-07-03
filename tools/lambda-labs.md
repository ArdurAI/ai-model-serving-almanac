# Lambda Labs


[![Infrastructure](https://img.shields.io/badge/Also_in-Infrastructure-blue)](https://github.com/ArdurAI/ai-infrastructure-almanac)

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

## Deep Analysis

### 1. How Is This Tool Useful?

Lambda Labs offers GPU cloud instances at industry-leading prices ($3.78/hr for H100 SXM) with transparent pricing, no egress fees, and a 99.9% SLA. Their 1-Click Clusters can provision 16-2,000 GPUs for distributed training and inference. Lambda is the simplest and most cost-effective way to get raw GPU compute for AI workloads.

### 2. Gotchas of Using This Tool

GPU availability can be limited — H100s and H200s are often sold out or have long wait times. Lambda offers only bare-metal instances (no managed services, no auto-scaling, no serverless). The platform is US-only, limiting options for international data residency requirements.

### 3. Limitations

No managed services — you get a GPU instance and must set up everything else (serving framework, monitoring, load balancing). No spot/preemptible instances for cost savings. The product is infrastructure-only — no model serving APIs, no fine-tuning APIs, just raw GPUs.

### 4. How Secure Is This Tool?

Lambda provides standard cloud security including SSH key management, VPC networking, and firewall rules. SOC 2 compliance status should be verified. Security maturity is less documented than AWS or GCP. Data is encrypted at rest and in transit.

### 5. Usefulness to General Public and Non-Technical Users

**Rating: 4/10**

Lambda Labs' key differentiator is transparent, no-nonsense pricing — $3.78/hr for H100 SXM is one of the lowest rates available, with no hidden egress fees or complex pricing tiers. The 1-Click Clusters feature makes provisioning large GPU clusters (up to 2,000 GPUs) trivially easy, which is unique.

### 6. What Does This Tool Solve That Others Don't?

Lambda Labs' key differentiator is transparent, no-nonsense pricing — $3.78/hr for H100 SXM is one of the lowest rates available, with no hidden egress fees or complex pricing tiers. The 1-Click Clusters feature makes provisioning large GPU clusters (up to 2,000 GPUs) trivially easy, which is unique.

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

Lambda is expanding rapidly with significant funding. Improvement areas include managed services (serving, monitoring), spot instances, international regions, auto-scaling, and a richer API. GPU availability remains the biggest customer pain point.

### 9. Official Maintainer Contacts

Lambda Inc. — contact via lambdalabs.com, support@lambdalabs.com, or their community Discord. The company is backed by Gradient Ventures, Google's AI fund.

### 10. General Usage Guidance

Best for teams that want raw GPU compute at the lowest prices and can manage their own serving infrastructure. Compare with RunPod (serverless option, community cloud) and CoreWeave (Kubernetes-native). Use vLLM or SGLang on Lambda instances for self-managed LLM serving.

---

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
