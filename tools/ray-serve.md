# Ray Serve


[![Infrastructure](https://img.shields.io/badge/Also_in-Infrastructure-blue)](https://github.com/ArdurAI/ai-infrastructure-almanac)

- **Category**: Model Serving & Inference Engines
- **Type**: Distributed Serving
- **License**: Apache-2.0
- **Region**: US
- **Tier**: A
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-06-16

> Multi-model serving graphs; online RAG; integration with Ray training

---

## Overview

Ray Serve is a distributed serving in the model serving and inference engines category.

**Supported model formats**: safetensors, pytorch, onnx, tensorrt

**Supported quantization**: fp16, bf16, fp8, int8

**Hardware target**: Multi-node

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
pip install "ray[serve]"

# Basic local deployment
python -c "
import requests
from ray import serve
from starlette.requests import Request

@serve.deployment
class MyModelDeployment:
    def __init__(self, msg: str):
        self._msg = msg
    def __call__(self, request: Request) -> dict:
        return {'result': self._msg}

app = MyModelDeployment.bind(msg='Hello world!')
serve.run(app, route_prefix='/')
print(requests.get('http://localhost:8000/').json())
"

# LLM serving (OpenAI-compatible)
python -c "
from ray import serve
from ray.serve.llm import LLMConfig, build_openai_app

llm_config = LLMConfig(
    model_loading_config={'model_id': 'deepseek', 'model_source': 'deepseek-ai/DeepSeek-R1'},
    deployment_config={'autoscaling_config': {'min_replicas': 1, 'max_replicas': 1}},
    accelerator_type='H100',
    engine_kwargs={'tensor_parallel_size': 8, 'pipeline_parallel_size': 2},
)
llm_app = build_openai_app({'llm_configs': [llm_config]})
serve.run(llm_app)
"
```

### Known sharp edges (from community / docs)
1. **3-strike deployment failure** — Since Ray 2.42+, a deployment that hits 3 retryable errors transitions to `DEPLOY_FAILED` permanently instead of retrying infinitely. The retry limit is hardcoded and not configurable.
2. **Constructor error loops** — If a model download or `__init__` fails, Ray Serve may enter a tight retry loop with unclear surface errors, making root cause diagnosis difficult.
3. **Multi-GPU allocation ambiguity** — There is no clean built-in way to pin a group of deployments to specific GPUs on the same node. Users must resort to `CUDA_VISIBLE_DEVICES` hacks or merge all models into one giant deployment.
4. **Whole-graph reload on updates** — In a single `RayService` CRD, changing one deployment can trigger a reload of the entire composition graph, causing temporary traffic disruption.
5. **Deployment graph anti-patterns** — Because graph topology is hidden in Python handle logic, it is easy to accidentally serialize requests sequentially rather than in parallel, killing throughput. Optimization requires manual code inspection.

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

> Raw results JSON: `benchmarks/ray-serve-<date>.json`

---

## Bug Notes

### Smoke gate findings
- ⏳ Not yet tested

### Known issues (from community / docs)
1. **3-strike deployment failure** — Since Ray 2.42+, a deployment that hits 3 retryable errors transitions to `DEPLOY_FAILED` permanently instead of retrying infinitely. The retry limit is hardcoded and not configurable.
2. **Constructor error loops** — If a model download or `__init__` fails, Ray Serve may enter a tight retry loop with unclear surface errors, making root cause diagnosis difficult.
3. **Multi-GPU allocation ambiguity** — There is no clean built-in way to pin a group of deployments to specific GPUs on the same node. Users must resort to `CUDA_VISIBLE_DEVICES` hacks or merge all models into one giant deployment.
4. **Whole-graph reload on updates** — In a single `RayService` CRD, changing one deployment can trigger a reload of the entire composition graph, causing temporary traffic disruption.
5. **Deployment graph anti-patterns** — Because graph topology is hidden in Python handle logic, it is easy to accidentally serialize requests sequentially rather than in parallel, killing throughput. Optimization requires manual code inspection.

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
- [BentoML](bentoml.md)
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

- Official site: https://www.ray.io/serve
- GitHub: https://github.com/ray-project/ray
- Documentation: https://docs.ray.io/en/latest/serve/index.html
- Community / Discord: - Discourse Forum: https://discuss.ray.io/
- Slack: Ray community Slack
- StackOverflow: `ray` tag
- GitHub Issues: https://github.com/ray-project/ray/issues
- Meetup Group: Monthly Ray meetups
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

Ray Serve is the model serving component of the Ray distributed computing framework, enabling multi-model serving graphs, online RAG pipelines, and seamless scaling from a single machine to a cluster. It integrates tightly with Ray's training and data processing capabilities, making it ideal for end-to-end ML pipelines. Ray Serve supports complex deployment topologies including multi-model routing, ensemble models, and pipeline stages.

### 2. Gotchas of Using This Tool

Ray has 3,473 open issues and 4 security advisories — the large issue count reflects the framework's broad scope. Ray Serve adds overhead compared to bare inference engines — it's a distributed serving layer, not an inference optimizer. Cluster setup and management is complex. Resource allocation across actors can be finicky.

### 3. Limitations

Ray Serve is part of the larger Ray ecosystem — adopting it means adopting Ray's runtime, which is heavy. Not optimized for raw LLM inference throughput (pair with vLLM as backend). Python-centric design limits multi-language use cases. Debugging distributed Ray applications can be challenging.

### 4. How Secure Is This Tool?

4 published GitHub security advisories. Apache-2.0 license. Ray's distributed architecture increases attack surface — Ray Dashboard and Ray Client should be secured. Anyscale (the company behind Ray) provides enterprise security features for managed deployments.

### 5. Usefulness to General Public and Non-Technical Users

**Rating: 4/10**

Ray Serve uniquely enables complex multi-model serving graphs — you can compose models into pipelines (e.g., embedding → retrieval → LLM → post-processing) with independent scaling per stage. Combined with Ray's training and data processing, it provides an end-to-end ML platform that no other serving tool matches.

### 6. What Does This Tool Solve That Others Don't?

Ray Serve uniquely enables complex multi-model serving graphs — you can compose models into pipelines (e.g., embedding → retrieval → LLM → post-processing) with independent scaling per stage. Combined with Ray's training and data processing, it provides an end-to-end ML platform that no other serving tool matches.

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

Development is very active (pushed July 2026) with 7,751 forks — one of the most actively developed distributed computing projects. Improvement areas include simplifying cluster setup, reducing overhead, better integration with modern inference engines, and improving documentation for serving-specific use cases.

### 9. Official Maintainer Contacts

Maintained by Anyscale Inc. and the Ray community. Contact via GitHub Issues at ray-project/ray, Ray Discuss (discuss.ray.io), or Ray Slack. Core contributors include Anyscale engineers and UC Berkeley RISELab researchers.

### 10. General Usage Guidance

Best for complex multi-model serving pipelines and teams already using Ray for training/data processing. Pair with vLLM as the LLM backend. For simpler single-model serving, use vLLM directly or BentoML. Use Anyscale for managed Ray if cluster management is a burden.

---

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
