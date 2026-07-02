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

## Deep Analysis

### 1. How Is This Tool Useful?

KServe is a CNCF Incubating project that standardizes model serving on Kubernetes through the InferenceService CRD. It supports scale-to-zero, canary rollouts, traffic splitting, and multiple runtimes (vLLM, TGI, HuggingFace TGI, custom). KServe is widely adopted in enterprise MLOps platforms including IBM Cloud, Red Hat OpenShift AI, and Kubeflow.

### 2. Gotchas of Using This Tool

KServe has 633 open issues, many related to the complexity of Kubernetes-native serving. The CRD-based approach adds abstraction layers that can make debugging harder. v2 (the latest architecture) introduces significant changes from v1, and migration can be non-trivial. Requires solid Kubernetes knowledge.

### 3. Limitations

Performance is bounded by the underlying inference runtime — KServe is an orchestration layer, not an inference engine. Scale-to-zero cold starts can take 30+ seconds for large models. The project's multi-framework support means some features are runtime-specific and not uniformly available.

### 4. How Secure Is This Tool?

No published security advisories, but the project benefits from CNCF security scanning. KServe integrates with Kubernetes RBAC, network policies, and service mesh (Istio) for mTLS. Enterprise features include token-based auth and request-level authorization.

### 5. Usefulness to General Public and Non-Technical Users

**Rating: 3/10**

KServe standardizes the model serving API on Kubernetes — the InferenceService CRD provides a vendor-neutral way to deploy models that works across clouds and runtimes. This standardization is unique; no other project provides this level of K8s-native serving abstraction with CNCF backing.

### 6. What Does This Tool Solve That Others Don't?

KServe standardizes the model serving API on Kubernetes — the InferenceService CRD provides a vendor-neutral way to deploy models that works across clouds and runtimes. This standardization is unique; no other project provides this level of K8s-native serving abstraction with CNCF backing.

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

Development is active (pushed July 2026) with 1,551 forks — one of the most actively contributed K8s ML projects. Improvement areas include reducing cold start times, better documentation for v2 migration, simplifying the CRD model, and deeper integration with modern inference engines.

### 9. Official Maintainer Contacts

CNCF Incubating project. Contact via GitHub Issues at kserve/kserve, the CNCF Slack (#kserve channel), or the KServe mailing list. Governing board includes representatives from Google, IBM, Bloomberg, and Nvidia.

### 10. General Usage Guidance

Best for enterprise teams running Kubernetes who need standardized, multi-runtime model serving. Pair with vLLM or TensorRT-LLM as the inference backend. For simpler setups, use BentoML or Modal. Migrate from Seldon Core if you want a CNCF-backed standard.

---

## License

Content for this page is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
