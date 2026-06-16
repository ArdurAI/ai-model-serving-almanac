# Architecture: Model Serving & Inference Engines

How the model serving & inference engines landscape is shaped, and how the Quest tests it.

## The landscape at a glance

| Tool | Tier | License | Focus | Notes |
|------|------|---------|-------|-------|
| vLLM | A | Apache-2.0 | Inference Engine | 73.7K+ stars; PagedAttention; 200+ models; multi-GPU (NVIDIA |
| SGLang | A | Apache-2.0 | Inference Engine | ~20K+ stars; RadixAttention; 29% throughput advantage on RAG |
| TensorRT-LLM | A | Apache-2.0 + closed | Inference Engine | NVIDIA-backed; highest throughput; 30-60% faster than vLLM o |
| llama.cpp | A | MIT | Inference Engine | 100K+ stars; GGUF format; Metal/CUDA/Vulkan/ROCm; ARM, Raspb |
| NVIDIA Dynamo | A | Open source | Orchestration | GTC 2026; disaggregated serving; KV-aware routing; 7x Blackw |
| KServe | A | Apache-2.0 | K8s Model Serving | CNCF Incubating; InferenceService CRD; scale-to-zero; canary |
| BentoML | A | Apache-2.0 | Model Serving | Python-first packaging; BentoCloud hosted; multi-framework |
| Ray Serve | A | Apache-2.0 | Distributed Serving | Multi-model serving graphs; online RAG; integration with Ray |
| Ollama | A | MIT | Local LLM Serving | 52M monthly downloads; on-premise; not for multi-tenant prod |
| LMDeploy | A | Apache-2.0 | Inference Engine | Shanghai AI Lab; TurboMind C++/CUDA; 1.5x vLLM on AWQ/MXFP4; |
| Fireworks AI | A | Commercial | Managed API | Per-token; FireAttention sub-100ms TTFT; low latency |
| Together AI | A | Commercial | Managed API | Per-token; broad model catalog; fine-tuned deployment; resea |
| RunPod | A | Commercial | GPU Cloud + Serverless | $0.34-2.69/hr; Pods + Serverless + Community Cloud; 30+ regi |
| Lambda Labs | A | Commercial | GPU Cloud | $3.78/hr H100 SXM; 99.9% SLA; 1-Click Clusters (16-2,000 GPU |
| LiteLLM | A | MIT | LLM Gateway | 18K+ stars; 100+ providers; OpenAI-compatible proxy; YC W23 |
| Portkey | A | Partially open | AI Gateway | 250+ models; 20-40ms latency; MCP Gateway; open source March |

## How the Quest tests a tool

Same harness for all entries; the judge was frozen before any tool ran:

```
Adapter[frozen CategoryAdapter contract]
  ├── setup()    → install, configure
  ├── load()     → ingest workload
  ├── await_ready() → async barrier
  ├── query()    → run test, get response
  └── teardown() → cleanup, measure
       ↓
Telemetry: latency · tokens · $ · ops notes
       ↓
Grading: deterministic + LLM judge (frozen prompts)
       ↓
Raw results JSON (published)
```

The `await_ready()` barrier is where async designs get their cost measured instead of hidden.

## License

Content is licensed CC BY 4.0 — share and adapt with attribution to **ArdurAI / Model Serving & Inference Engines Almanac**.
