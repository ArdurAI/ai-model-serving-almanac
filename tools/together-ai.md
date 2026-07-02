# Together AI

- **Category**: Model Serving & Inference Engines
- **Type**: Managed API
- **License**: Commercial
- **Region**: US
- **Tier**: A
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-06-16

> Per-token; broad model catalog; fine-tuned deployment; research focus

---

## Overview

Together AI is a managed api in the model serving and inference engines category.

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
pip install together
```
```python
from together import Together
import os
client = Together(api_key=os.environ["TOGETHER_API_KEY"])
response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)
```
API key: generate at https://api.together.ai/settings/api-keys

### Known sharp edges (from community / docs)
1. **Rate limits on free tier** — Aggressive request-per-minute caps; production workloads require paid tier upgrade.
2. **Model availability churn** — Broad catalog means some models are preview/beta and can be deprecated or rotated without long notice.
3. **Fine-tuning deployment latency** — Deploying a fine-tuned model to a dedicated endpoint can take several minutes, causing gap in service during updates.
4. **Cost ambiguity on media models** — Image/video generation pricing uses per-generation or per-pixel units that are harder to forecast than per-token text APIs.
5. **Queueing under burst** — Serverless endpoints can queue requests during traffic spikes; TTFT degrades noticeably.

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

> Raw results JSON: `benchmarks/together-ai-<date>.json`

---

## Bug Notes

### Smoke gate findings
- ⏳ Not yet tested

### Known issues (from community / docs)
1. **Rate limits on free tier** — Aggressive request-per-minute caps; production workloads require paid tier upgrade.
2. **Model availability churn** — Broad catalog means some models are preview/beta and can be deprecated or rotated without long notice.
3. **Fine-tuning deployment latency** — Deploying a fine-tuned model to a dedicated endpoint can take several minutes, causing gap in service during updates.
4. **Cost ambiguity on media models** — Image/video generation pricing uses per-generation or per-pixel units that are harder to forecast than per-token text APIs.
5. **Queueing under burst** — Serverless endpoints can queue requests during traffic spikes; TTFT degrades noticeably.

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

- Official site: https://www.together.ai
- GitHub: N/A (commercial platform; no primary open-source inference engine repo)
- Documentation: https://docs.together.ai
- Community / Discord: - Discord: https://discord.gg/together-ai (community Discord)
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

Together AI is a managed inference platform offering per-token pricing for 200+ open-source models, fine-tuned model deployment, and a broad research-focused model catalog. The company has raised $225M+ in funding and is known for its contributions to open-source AI research (RedPajama, OpenChat, etc.). Together AI provides both serverless APIs and dedicated endpoints.

### 2. Gotchas of Using This Tool

Together AI is a closed-source commercial platform — no self-hosting. Per-token pricing at scale is more expensive than self-serving on Lambda Labs or RunPod. Fine-tuned model hosting requires their enterprise tier. The togethercomputer GitHub org has limited public repos (the Python client has only 81 stars).

### 3. Limitations

Limited to US-based inference. Custom model hosting beyond their catalog requires enterprise engagement. No GPU passthrough or raw compute options — it's API-only. Rate limits on lower tiers can affect production workloads during peak demand.

### 4. How Secure Is This Tool?

Together AI is SOC 2 Type II compliant with enterprise security features including SSO, data isolation, and audit logging. Customer data is not used for training. The platform provides data residency options for enterprise customers.

### 5. Usefulness to General Public and Non-Technical Users

**Rating: 6/10**

Together AI uniquely combines a managed inference platform with active AI research — they contribute to open-source models (RedPajama, OpenChat) and publish research papers. For teams that want their inference provider to also advance the open-source ecosystem, Together AI is a natural choice.

### 6. What Does This Tool Solve That Others Don't?

Together AI uniquely combines a managed inference platform with active AI research — they contribute to open-source models (RedPajama, OpenChat) and publish research papers. For teams that want their inference provider to also advance the open-source ecosystem, Together AI is a natural choice.

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

Together AI is well-funded and actively developed with regular model additions. Improvement areas include transparent pricing, self-hosted options, international regions, more flexible custom model support, and open benchmarking data.

### 9. Official Maintainer Contacts

Together Computer Inc. — contact via their website together.ai, API support channels, or enterprise sales. The company is backed by Sequoia, Kleiner Perkins, and others.

### 10. General Usage Guidance

Best for managed inference of open-source models with per-token pricing. Compare with Fireworks AI (latency focus) and DeepInfra (cost focus). Use Together AI if you value their research contributions and model catalog breadth.

---

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
