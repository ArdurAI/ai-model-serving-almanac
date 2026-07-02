# Fireworks AI

- **Category**: Model Serving & Inference Engines
- **Type**: Managed API
- **License**: Commercial
- **Region**: US
- **Tier**: A
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-06-16

> Per-token; FireAttention sub-100ms TTFT; low latency

---

## Overview

Fireworks AI is a managed api in the model serving and inference engines category.

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
# Python SDK
pip install fireworks-ai
# Or with uv
uv add fireworks-ai
```
```python
from fireworks import Fireworks
import os
client = Fireworks(api_key=os.environ["FIREWORKS_API_KEY"])
response = client.chat.completions.create(
    model="accounts/fireworks/models/llama-v3p1-405b-instruct",
    messages=[{"role": "user", "content": "Hello!"}]
)
```
API key: generate at https://fireworks.ai/account/api-keys

### Known sharp edges (from community / docs)
1. **Model listing bug** — `get_models()` queries by default only dedicated deployments (often 0 for most users). Must use `accounts/fireworks/models?filter=supports_serverless=true` for serverless catalog.
2. **Pricing complexity** — Per-model pricing varies widely; cached input is 50% off only for "text and vision language models unless otherwise specified," making cost estimation non-trivial.
3. **Rate limits** — Usage-based tiers; new accounts hit caps quickly. Enterprise tier required for higher rate limits and priority routing.
4. **Cold-start on dedicated** — On-demand GPU deployments bill per GPU-second but still incur startup initialization time that is not discounted.
5. **Fine-tuning token counting with reasoning traces** — Multi-turn conversations are unrolled into user, assistant, and thinking traces, inflating billed training tokens unexpectedly.

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

> Raw results JSON: `benchmarks/fireworks-ai-<date>.json`

---

## Bug Notes

### Smoke gate findings
- ⏳ Not yet tested

### Known issues (from community / docs)
1. **Model listing bug** — `get_models()` queries by default only dedicated deployments (often 0 for most users). Must use `accounts/fireworks/models?filter=supports_serverless=true` for serverless catalog.
2. **Pricing complexity** — Per-model pricing varies widely; cached input is 50% off only for "text and vision language models unless otherwise specified," making cost estimation non-trivial.
3. **Rate limits** — Usage-based tiers; new accounts hit caps quickly. Enterprise tier required for higher rate limits and priority routing.
4. **Cold-start on dedicated** — On-demand GPU deployments bill per GPU-second but still incur startup initialization time that is not discounted.
5. **Fine-tuning token counting with reasoning traces** — Multi-turn conversations are unrolled into user, assistant, and thinking traces, inflating billed training tokens unexpectedly.

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

- Official site: https://fireworks.ai
- GitHub: https://github.com/fw-ai-external/python-sdk
- Documentation: https://docs.fireworks.ai
- Community / Discord: - Discord: https://discord.gg/fireworks-ai (community Discord)
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

Fireworks AI is a managed inference platform known for its FireAttention technology achieving sub-100ms time-to-first-token (TTFT) on large models. It offers per-token pricing, a broad model catalog, and fine-tuning APIs. The platform is backed by $570M+ in funding (Sequoia, Andreessen Horowitz) and is valued at $3B+.

### 2. Gotchas of Using This Tool

Fireworks is a closed-source commercial platform with no self-hosting option. Per-token pricing can become expensive at scale compared to renting GPUs and self-serving. The platform's performance claims (FireAttention, sub-100ms TTFT) are difficult to independently verify.

### 3. Limitations

Limited to US-based inference regions. Custom model hosting requires engaging Fireworks' team — you can't bring arbitrary custom architectures. The fine-tuning API supports LoRA but full fine-tuning requires enterprise engagement.

### 4. How Secure Is This Tool?

Fireworks AI is SOC 2 Type II compliant and offers enterprise security features including SSO, data isolation, and audit logging. Customer data and model weights are not used for training. The platform provides data residency guarantees for enterprise customers.

### 5. Usefulness to General Public and Non-Technical Users

**Rating: 6/10**

Fireworks' key differentiator is FireAttention, a proprietary attention implementation that delivers industry-leading latency (sub-100ms TTFT) for large models. This makes it the platform of choice for real-time, user-facing applications where latency is critical — voice assistants, coding assistants, and chatbots.

### 6. What Does This Tool Solve That Others Don't?

Fireworks' key differentiator is FireAttention, a proprietary attention implementation that delivers industry-leading latency (sub-100ms TTFT) for large models. This makes it the platform of choice for real-time, user-facing applications where latency is critical — voice assistants, coding assistants, and chatbots.

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

Fireworks is well-funded and actively developed with regular model additions. Improvement areas include transparent benchmark data, self-hosted options, international regions, and more flexible custom model support. The platform should publish FireAttention performance comparisons.

### 9. Official Maintainer Contacts

Fireworks AI Inc. — contact via their website fireworks.ai, support channels, or enterprise sales. Valued at $3B+, backed by Sequoia, a16z, and others.

### 10. General Usage Guidance

Best for latency-critical, user-facing applications that need sub-100ms TTFT. Compare with Together AI for model catalog breadth, and with self-served vLLM on Lambda Labs for cost optimization. Use the free tier to benchmark latency for your specific models.

---

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
