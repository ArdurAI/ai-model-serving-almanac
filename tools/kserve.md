# KServe

- **Category**: Model Serving & Inference Engines
- **Type**: K8s Model Serving
- **License**: Apache-2.0
- **Region**: Global
- **Tier**: A
- **First Triaged**: 2026-06-16
- **Last Updated**: 2026-06-16

> CNCF Incubating; InferenceService CRD; scale-to-zero; canary; vLLM/TGI runtimes

---

## Overview

KServe is a k8s model serving in the model serving and inference engines category.

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
# Quick install (standalone, without Knative scale-to-zero)
curl -s "https://raw.githubusercontent.com/kserve/kserve/release-0.18/hack/quick_install.sh" | bash

# Or Helm / OCI for production
helm install kserve-crd oci://ghcr.io/kserve/charts/kserve-crd --version v0.18.0
helm install kserve-resources oci://ghcr.io/kserve/charts/kserve-resources --version v0.18.0

# Deploy a model
cat <<EOF | kubectl apply -f -
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: llama-service
spec:
  predictor:
    model:
      modelFormat:
        name: huggingface
      storageUri: "hf://meta-llama/Llama-3.1-8B-Instruct"
      resources:
        limits:
          nvidia.com/gpu: "1"
EOF
```

### Known sharp edges (from community / docs)
1. **CRD ordering failures** — `error: no matches for kind "InferenceService"` occurs if CRDs are not applied before the InferenceService resource. Always verify `kserve-crd` is installed first.
2. **Knative webhook conflicts** — Setting `terminationGracePeriodSeconds` in InferenceService YAML causes validation webhook denials (`validation.webhook.serving.knative.dev` rejects the field).
3. **Missing `storageInitializer` initContainer** — In some installs, the init container that downloads models from S3/GCS/HF is absent, causing `Unknown` status and `Readiness probe failed: 503` because `/mnt/models` is empty.
4. **Strict `podSpec` decoding** — Adding `podSpec` fields under `predictor` can trigger `strict decoding error: unknown field` in newer API versions.
5. **Air-gapped image pull policy ignored** — `imagePullPolicy: "Never"` is not always respected by Knative reconciler, causing offline deployments to fail trying to resolve image digests.

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

> Raw results JSON: `benchmarks/kserve-<date>.json`

---

## Bug Notes

### Smoke gate findings
- ⏳ Not yet tested

### Known issues (from community / docs)
1. **CRD ordering failures** — `error: no matches for kind "InferenceService"` occurs if CRDs are not applied before the InferenceService resource. Always verify `kserve-crd` is installed first.
2. **Knative webhook conflicts** — Setting `terminationGracePeriodSeconds` in InferenceService YAML causes validation webhook denials (`validation.webhook.serving.knative.dev` rejects the field).
3. **Missing `storageInitializer` initContainer** — In some installs, the init container that downloads models from S3/GCS/HF is absent, causing `Unknown` status and `Readiness probe failed: 503` because `/mnt/models` is empty.
4. **Strict `podSpec` decoding** — Adding `podSpec` fields under `predictor` can trigger `strict decoding error: unknown field` in newer API versions.
5. **Air-gapped image pull policy ignored** — `imagePullPolicy: "Never"` is not always respected by Knative reconciler, causing offline deployments to fail trying to resolve image digests.

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
- [BentoML](bentoml.md)
- [Ray Serve](ray-serve.md)
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

- Official site: https://kserve.github.io/website/
- GitHub: https://github.com/kserve/kserve
- Documentation: https://kserve.github.io/website/docs/
- Community / Discord: - CNCF Slack: `#kserve`, `#kserve-contributors`, `#kserve-oip-collaboration`
- GitHub Discussions: https://github.com/kserve/kserve/discussions
- Community Meetings: Monthly public meetings (calendar + recordings available)
- Mailing list: kserve-discuss@lists.lfaidata.foundation
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
