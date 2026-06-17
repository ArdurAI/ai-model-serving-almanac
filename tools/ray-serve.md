# Ray Serve

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

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
