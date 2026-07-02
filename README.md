# Model Serving & Inference Engines Almanac

A living encyclopedia of LLM inference engines, model serving platforms, and deployment tools. Updated **monthly** with fresh repo metadata, releases, landscape shifts, and independent benchmark results from the *"Platform Engineer's Quest for the Best"* series.

> Vendors publish their own benchmark numbers. Nobody reproduces them independently, and nobody evaluates tools the way a platform engineer has to live with them: ops burden, failure modes, scale curves, and cost. This almanac is the public record of that work.

**47 tools** — **Tier A**: 16 · **Tier B**: 30 · **Tier C**: 1

## Tool Catalogue

Every tool below has a full deep-dive page in [`tools/`](tools/). Sorted by tier (A → B → C), then alphabetically.

| Tool | Type | License | Stars | Tier | Description | Detail |
|------|------|---------|-------|------|-------------|--------|
| **BentoML** | Model Serving | Apache-2.0 | — | A | Python-first packaging; BentoCloud hosted; multi-framework | [`bentoml.md`](tools/bentoml.md) |
| **Fireworks AI** | Managed API | Commercial | — | A | Per-token; FireAttention sub-100ms TTFT; low latency | [`fireworks-ai.md`](tools/fireworks-ai.md) |
| **KServe** | K8s Model Serving | Apache-2.0 | — | A | CNCF Incubating; InferenceService CRD; scale-to-zero; canary; vLLM/TGI runtimes | [`kserve.md`](tools/kserve.md) |
| **Lambda Labs** | GPU Cloud | Commercial | — | A | $3.78/hr H100 SXM; 99.9% SLA; 1-Click Clusters (16-2,000 GPUs); no egress fees | [`lambda-labs.md`](tools/lambda-labs.md) |
| **LiteLLM** | LLM Gateway | MIT | 18K+ | A | 18K+ stars; 100+ providers; OpenAI-compatible proxy; YC W23 | [`litellm.md`](tools/litellm.md) |
| **llama.cpp** | Inference Engine | MIT | 100K+ | A | 100K+ stars; GGUF format; Metal/CUDA/Vulkan/ROCm; ARM, Raspberry Pi, WASM | [`llamacpp.md`](tools/llamacpp.md) |
| **LMDeploy** | Inference Engine | Apache-2.0 | — | A | Shanghai AI Lab; TurboMind C++/CUDA; 1.5x vLLM on AWQ/MXFP4; DeepSeek/Qwen/InternLM | [`lmdeploy.md`](tools/lmdeploy.md) |
| **NVIDIA Dynamo** | Orchestration | Open source | — | A | GTC 2026; disaggregated serving; KV-aware routing; 7x Blackwell boost; replaces Triton | [`nvidia-dynamo.md`](tools/nvidia-dynamo.md) |
| **Ollama** | Local LLM Serving | MIT | — | A | 52M monthly downloads; on-premise; not for multi-tenant production (collapses under 5 concurrent) | [`ollama.md`](tools/ollama.md) |
| **Portkey** | AI Gateway | Partially open | — | A | 250+ models; 20-40ms latency; MCP Gateway; open source March 2026 | [`portkey.md`](tools/portkey.md) |
| **Ray Serve** | Distributed Serving | Apache-2.0 | — | A | Multi-model serving graphs; online RAG; integration with Ray training | [`ray-serve.md`](tools/ray-serve.md) |
| **RunPod** | GPU Cloud + Serverless | Commercial | — | A | $0.34-2.69/hr; Pods + Serverless + Community Cloud; 30+ regions; cost leader | [`runpod.md`](tools/runpod.md) |
| **SGLang** | Inference Engine | Apache-2.0 | 20K+ | A | ~20K+ stars; RadixAttention; 29% throughput advantage on RAG workloads | [`sglang.md`](tools/sglang.md) |
| **TensorRT-LLM** | Inference Engine | Apache-2.0 + closed | — | A | NVIDIA-backed; highest throughput; 30-60% faster than vLLM on H100; per-model compile | [`tensorrt-llm.md`](tools/tensorrt-llm.md) |
| **Together AI** | Managed API | Commercial | — | A | Per-token; broad model catalog; fine-tuned deployment; research focus | [`together-ai.md`](tools/together-ai.md) |
| **vLLM** | Inference Engine | Apache-2.0 | 73.7K+ | A | 73.7K+ stars; PagedAttention; 200+ models; multi-GPU (NVIDIA, AMD, Intel, TPU) | [`vllm.md`](tools/vllm.md) |
| **Aphrodite Engine** | Inference Engine | AGPL-3.0 | — | B | PygmalionAI; vLLM fork; broadest quantization (FP2-FP12, EXL2, GGUF); creative/roleplay | [`aphrodite-engine.md`](tools/aphrodite-engine.md) |
| **Baseten** | Managed + Hybrid | Commercial | — | B | Free tier → Enterprise; multi-cloud capacity; TensorRT/SGLang/vLLM/TGI runtimes | [`baseten.md`](tools/baseten.md) |
| **Bifrost** | AI Gateway | Apache-2.0 | 52K+ | B | Go; ~11μs overhead; virtual keys; RBAC; SSO; vault integration; MCP tool filtering | [`bifrost.md`](tools/bifrost.md) |
| **CoreWeave** | GPU Cloud | Commercial | — | B | K8s-native; multi-region; NVIDIA partner; dedicated infra | [`coreweave.md`](tools/coreweave.md) |
| **Crusoe** | GPU Cloud | Commercial | — | B | Flared-gas powered data centers; NVIDIA partner | [`crusoe.md`](tools/crusoe.md) |
| **CTranslate2** | Inference Engine | MIT | — | B | OpenNMT; fast inference for Transformer models; C++ backend; Python bindings | [`ctranslate2.md`](tools/ctranslate2.md) |
| **Deep Infra** | Managed API | Commercial | — | B | Low-cost inference; integrates with Dynamo | [`deep-infra.md`](tools/deep-infra.md) |
| **DeepSpeed-MII** | Inference Engine | Apache-2.0 | — | B | Microsoft Research; Blocked KV caching; Dynamic SplitFuse; 37,000+ models | [`deepspeed-mii.md`](tools/deepspeed-mii.md) |
| **ExecuTorch** | Edge Runtime | Open source | — | B | Meta; 1.0 GA Oct 2025; 50KB footprint; 12+ hardware backends; billions of users | [`executorch.md`](tools/executorch.md) |
| **ExLlamaV2** | Inference Engine | MIT | — | B | EXL2 quantization; 2-3x faster than GGUF on GPU; single-card focus | [`exllamav2.md`](tools/exllamav2.md) |
| **GMI Cloud** | GPU Cloud | Commercial | — | B | H200 bare metal; 40% speed advantage over virtualized cloud | [`gmi-cloud.md`](tools/gmi-cloud.md) |
| **KAITO** | K8s Operator | Open source | — | B | Microsoft; AKS, K8s; automates GPU pool provisioning, model deployment, inference serving | [`kaito.md`](tools/kaito.md) |
| **Kueue** | GPU Scheduling | Apache-2.0 | — | B | CNCF; multi-tenant GPU queueing; fair-share; preemption; GPU util 25-35% → 60-85% | [`kueue.md`](tools/kueue.md) |
| **llm-d** | Distributed Inference | Open source | 3,665 | B | Community; multi-node, multi-GPU for 70B+; disaggregated serving; KV cache offloading | [`llm-d.md`](tools/llm-d.md) |
| **MindIE** | Inference Engine | Proprietary | — | B | Huawei Ascend NPU专用; 闭源商业 | [`mindie.md`](tools/mindie.md) |
| **MLX** | ML Framework + Inference | MIT | — | B | Apple; 24,600+ stars; unified memory; 4,255+ HF models; Apple Silicon only | [`mlx.md`](tools/mlx.md) |
| **Modal** | Serverless GPU | Commercial | — | B | Per-GPU-second; fast cold starts; vLLM native; pay-per-second for spiky workloads | [`modal.md`](tools/modal.md) |
| **Nebius** | GPU Cloud | Commercial | — | B | NVIDIA partner; Dynamo/TensorRT-LLM optimized | [`nebius.md`](tools/nebius.md) |
| **NVIDIA GPU Operator** | K8s GPU Management | Proprietary | — | B | Automates drivers, MIG, time-slicing, DCGM monitoring | [`nvidia-gpu-operator.md`](tools/nvidia-gpu-operator.md) |
| **NVIDIA Nim** | Containerized Serving | Proprietary | — | B | Containerized product on TensorRT-LLM; NGC distribution | [`nvidia-nim.md`](tools/nvidia-nim.md) |
| **Replicate** | Managed API | Commercial | — | B | Per-second billing; simple API; Cog container format; higher effective cost at volume | [`replicate.md`](tools/replicate.md) |
| **RTP-LLM** | Inference Engine | Open source | — | B | Alibaba's internal serving engine; MoE and long-context optimizations | [`rtp-llm.md`](tools/rtp-llm.md) |
| **Seldon Core v2** | K8s Model Serving | Apache-2.0 | — | B | Multi-step pipelines; drift detection; MLServer multi-model per GPU | [`seldon-core-v2.md`](tools/seldon-core-v2.md) |
| **TensorFlow Serving** | General Inference Server | Apache-2.0 | — | B | Google; TensorFlow-native; legacy for LLM workloads | [`tensorflow-serving.md`](tools/tensorflow-serving.md) |
| **TensorRT Edge-LLM** | Edge Engine | Proprietary | — | B | NVIDIA; C++ framework; EAGLE-3 speculative decoding; NVFP4; chunked prefill | [`tensorrt-edge-llm.md`](tools/tensorrt-edge-llm.md) |
| **TensorZero** | AI Gateway | Open source | 11K | B | Rust; ~0.3ms; LLM gateway, observability, optimization, evaluations, experimentation | [`tensorzero.md`](tools/tensorzero.md) |
| **TGI (Text Generation Inference)** | Inference Engine | Apache-2.0 | — | B | HuggingFace-backed; 800+ HF models; Rust HTTP server; maintenance mode as of late 2025 | [`tgi-text-generation-inference.md`](tools/tgi-text-generation-inference.md) |
| **TorchServe** | General Inference Server | Apache-2.0 | — | B | PyTorch/Amazon; PyTorch-native; less LLM-specific than vLLM | [`torchserve.md`](tools/torchserve.md) |
| **Triton Inference Server** | General Inference Server | Apache-2.0 | — | B | NVIDIA; multi-framework (LLM + CV + tabular); being displaced by Dynamo for LLMs | [`triton-inference-server.md`](tools/triton-inference-server.md) |
| **Vast.ai** | P2P GPU Marketplace | Commercial | — | B | ~$0.90/hr H100 (interruptible); cheapest verified rates; 68+ GPU classes | [`vastai.md`](tools/vastai.md) |
| **MLC-LLM** | Edge Runtime | Open source | 22K+ | C | On-device deployment; fragmented; Ollama emerged as winner in this niche | [`mlc-llm.md`](tools/mlc-llm.md) |

## Tool Categories

### AI Gateway (3)
**Bifrost** · **Portkey** · **TensorZero**

### Containerized Serving (1)
**NVIDIA Nim**

### Distributed Inference (1)
**llm-d**

### Distributed Serving (1)
**Ray Serve**

### Edge Engine (1)
**TensorRT Edge-LLM**

### Edge Runtime (2)
**ExecuTorch** · **MLC-LLM**

### GPU Cloud (5)
**CoreWeave** · **Crusoe** · **GMI Cloud** · **Lambda Labs** · **Nebius**

### GPU Cloud + Serverless (1)
**RunPod**

### GPU Scheduling (1)
**Kueue**

### General Inference Server (3)
**TensorFlow Serving** · **TorchServe** · **Triton Inference Server**

### Inference Engine (12)
**Aphrodite Engine** · **CTranslate2** · **DeepSpeed-MII** · **ExLlamaV2** · **llama.cpp** · **LMDeploy** · **MindIE** · **RTP-LLM** · **SGLang** · **TensorRT-LLM** · **TGI (Text Generation Inference)** · **vLLM**

### K8s GPU Management (1)
**NVIDIA GPU Operator**

### K8s Model Serving (2)
**KServe** · **Seldon Core v2**

### K8s Operator (1)
**KAITO**

### LLM Gateway (1)
**LiteLLM**

### Local LLM Serving (1)
**Ollama**

### ML Framework + Inference (1)
**MLX**

### Managed + Hybrid (1)
**Baseten**

### Managed API (4)
**Deep Infra** · **Fireworks AI** · **Replicate** · **Together AI**

### Model Serving (1)
**BentoML**

### Orchestration (1)
**NVIDIA Dynamo**

### P2P GPU Marketplace (1)
**Vast.ai**

### Serverless GPU (1)
**Modal**

## Quick Start

```bash
git clone https://github.com/ArdurAI/ai-model-serving-almanac.git
cd ai-model-serving-almanac
```

| You want… | Go to |
|-----------|-------|
| The state of the landscape right now | The latest file in [`editions/`](editions/) |
| Everything we know about one tool | [`tools/<name>.md`](tools/) |
| Machine-readable roster + metadata | [`data/`](data/) |
| Architecture diagrams | [`architecture.md`](architecture.md) |
| Benchmark results (rolling) | [`benchmarks/`](benchmarks/) |
| How tools are tested and ranked | [`methodology/benchmark-harness.md`](methodology/benchmark-harness.md) |
| Project intent & philosophy | [`INTENT.md`](INTENT.md) |
| Implementation guide | [`IMPLEMENTATION.md`](IMPLEMENTATION.md) |
| Testing methodology | [`TESTING.md`](TESTING.md) |
| Troubleshooting | [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) |

## Methodology

Results published here come from a frozen-before-results harness. Full details in [`methodology/benchmark-harness.md`](methodology/benchmark-harness.md):

- Standard benchmarks for comparability with published claims — every ranking ships a *published vs. reproduced* table.
- A custom **PlatformOps** benchmark: testing on infrastructure work — setup, reliability, scale, cost.
- A stress suite: contradiction storms, near-duplicate floods, concurrent writers, kill-the-backing-store chaos, cost-runaway measurement.
- Seven scored dimensions: accuracy, latency, token economics, scale behavior, **ops burden**, developer experience, data sovereignty.

The judge model, prompts (SHA-256-frozen), and control variables were fixed before any tool ran. Raw results JSON is published with every ranking.

## Contributing

We welcome contributions — new tools, data fixes, ranking challenges, and benchmark reproductions. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines on how to add a tool, fix data, or challenge a ranking.

## Recent Edition

📖 **[Read the latest edition →](editions/2026-06.md)**

One edition per month under `editions/YYYY-MM.md`: refreshed metadata, notable releases, new entrants triaged in or out, and a diary of what was tested.

---

## License

Content is licensed **CC BY 4.0** — share and adapt with attribution to **ArdurAI**.

---

**Authored by Team Ardur · CC BY 4.0**
