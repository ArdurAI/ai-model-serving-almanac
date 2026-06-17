# Model Serving & Inference Engines Almanac

A living encyclopedia of LLM inference engines, model serving platforms, and deployment tools. Updated monthly with fresh repo metadata, releases, landscape shifts, and independent benchmark results.

> Vendors publish their own benchmark numbers. Nobody reproduces them independently, and nobody evaluates tools the way a platform engineer has to live with them: ops burden, failure modes, scale curves, and cost. This almanac is the public record of that work.

## How to use this repo

| You want… | Go to |
|-----------|-------|
| The state of the landscape right now | The latest file in `editions/` |
| Everything we know about one tool | `tools/<name>.md` |
| Machine-readable roster + metadata | `data/roster.json` |
| Architecture diagrams | `architecture.md` |
| Benchmark results (rolling) | `benchmarks/` |
| How tools are tested and ranked | `methodology/benchmark-harness.md` |
| Project intent & philosophy | `INTENT.md` |
| Implementation guide & how to add tools | `IMPLEMENTATION.md` |
| Testing methodology & benchmarks | `TESTING.md` |
| Troubleshooting & debugging | `TROUBLESHOOTING.md` |
| How to contribute | `CONTRIBUTING.md` |

## The roster

**Tier A** — 16 tools with full deep-dive pages: [vLLM](tools/vllm.md), [SGLang](tools/sglang.md), [TensorRT-LLM](tools/tensorrt-llm.md), [llama.cpp](tools/llamacpp.md), [NVIDIA Dynamo](tools/nvidia-dynamo.md), [KServe](tools/kserve.md), [BentoML](tools/bentoml.md), [Ray Serve](tools/ray-serve.md), [Ollama](tools/ollama.md), [LMDeploy](tools/lmdeploy.md), [Fireworks AI](tools/fireworks-ai.md), [Together AI](tools/together-ai.md), [RunPod](tools/runpod.md), [Lambda Labs](tools/lambda-labs.md), [LiteLLM](tools/litellm.md), [Portkey](tools/portkey.md)

**Tier B** — 30 tools with stub pages: [TGI](tools/tgi-text-generation-inference.md), [DeepSpeed-MII](tools/deepspeed-mii.md), [Aphrodite Engine](tools/aphrodite-engine.md), [MLX](tools/mlx.md), [ExLlamaV2](tools/exllamav2.md), [CTranslate2](tools/ctranslate2.md), [TensorRT Edge-LLM](tools/tensorrt-edge-llm.md), [MindIE](tools/mindie.md), [RTP-LLM](tools/rtp-llm.md), [NVIDIA Nim](tools/nvidia-nim.md), [Triton Inference Server](tools/triton-inference-server.md), [Seldon Core v2](tools/seldon-core-v2.md), [llm-d](tools/llm-d.md), [KAITO](tools/kaito.md), [Kueue](tools/kueue.md), [NVIDIA GPU Operator](tools/nvidia-gpu-operator.md), [TorchServe](tools/torchserve.md), [TensorFlow Serving](tools/tensorflow-serving.md), [Replicate](tools/replicate.md), [Modal](tools/modal.md), [Baseten](tools/baseten.md), [Deep Infra](tools/deep-infra.md), [Vast.ai](tools/vastai.md), [CoreWeave](tools/coreweave.md), [Nebius](tools/nebius.md), [Crusoe](tools/crusoe.md), [GMI Cloud](tools/gmi-cloud.md), [Bifrost](tools/bifrost.md), [TensorZero](tools/tensorzero.md), [ExecuTorch](tools/executorch.md)

**Tier C** — 1 tool with stub page: [MLC-LLM](tools/mlc-llm.md)

**Total: 47 tools**

## Methodology

Results published here come from a frozen-before-results harness:
- Standard benchmarks for comparability with published claims — every ranking ships a _published vs. reproduced_ table.
- A custom PlatformOps benchmark: testing on infrastructure work — setup, reliability, scale, cost.
- A stress suite: contradiction storms, near-duplicate floods, concurrent writers, kill-the-backing-store chaos, cost-runaway measurement.
- Seven scored dimensions: accuracy, latency, token economics, scale behavior, **ops burden**, developer experience, data sovereignty.

The judge model, prompts (SHA-256-frozen), and control variables were fixed before any tool ran. Raw results JSON is published with every ranking.

## Update cadence

One edition per month under `editions/YYYY-MM.md`: refreshed metadata, notable releases, new entrants triaged in or out, and a diary of what was tested.

## License

Content is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
