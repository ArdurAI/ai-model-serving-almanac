# Contributing to the Model Serving Almanac

How to add inference engines, fix data, challenge rankings, and improve the methodology for model serving evaluation.

## Table of Contents

1. [Ways to Contribute](#ways-to-contribute)
2. [Adding a New Engine](#adding-a-new-engine)
3. [Fixing Data](#fixing-data)
4. [Challenging a Ranking](#challenging-a-ranking)
5. [Improving the Methodology](#improving-the-methodology)
6. [Code of Conduct](#code-of-conduct)
7. [License](#license)

---

## Ways to Contribute

You can contribute to the almanac in several ways:

| Contribution Type | What you do | Impact |
|-------------------|-------------|--------|
| **Add an engine** | File an issue with a new inference engine | Expands the roster |
| **Fix data** | Correct incorrect metadata (e.g., wrong quantization support, wrong hardware target) | Improves accuracy |
| **Challenge a ranking** | Provide evidence that a score is wrong (e.g., reran on same GPU and got different TTFT) | Drives quality |
| **Share experience** | Write about deploying an engine in production (GPU topology, batching behavior, OOM patterns) | Adds real-world context |
| **Improve methodology** | Propose a better benchmark or scoring rubric for model serving | Improves fairness |
| **Build an adapter** | Implement the `ModelServingAdapter` for a new engine | Enables testing |
| **Review an edition** | Proofread, fact-check, suggest improvements | Improves quality |
| **Spread the word** | Share the almanac with your ML platform community | Grows the ecosystem |

## Adding a New Engine

### Before you submit

Check if the engine meets the triage criteria:

1. **Seriousness**: Is it a real serving engine with real throughput claims, real users, or real backing? Not a toy/demo.
2. **Activity**: Has it had a push or release in the last 6 months?
3. **Documentation**: Does it have a README or docs explaining how to serve a model and what hardware it supports?
4. **Accessibility**: Is it testable (open source, free tier, or evaluation license)? Must support at least one open-weight model (Llama, Mistral, Qwen, etc.).
5. **Scope**: Does it fit the model serving category? A general training framework doesn't enter unless it has a dedicated serving layer.

### How to submit

**Option 1: GitHub Issue (preferred)**

File an issue with this template:

```markdown
## Engine Request: [Engine Name]

### Category
Model Serving & Inference Engines

### Engine URL
[GitHub repo or homepage URL]

### License
[e.g., MIT, Apache-2.0, Proprietary]

### Description
[What does it do? One paragraph. Key differentiators: continuous batching, speculative decoding, edge deployment, etc.]

### Why it should be on the roster
[Evidence of adoption, production usage, or technical merit.]

### Evidence
- GitHub stars: [N]
- Last release: [date]
- Notable users: [companies, cloud providers, if known]
- Funding: [amount, if known]
- Hardware targets: [GPU / CPU / Edge / Multi-node]
- Supported quantization: [FP16, FP8, AWQ, GPTQ, etc.]

### Tier suggestion
[A, B, or C — and why]
```

**Option 2: Pull Request**

If you want to add the engine directly:

1. Fork the repo
2. Edit `data/roster.json` to add the engine (include `supported_formats`, `supported_quantization`, `hardware_target`)
3. Update the README if the engine is Tier A
4. Submit a PR with the same template as above

### What happens after submission

1. **Triage**: We check if the engine meets criteria (within 7 days)
2. **Smoke gate**: We run the engine through the 3-turn scenario (within 14 days): deploy model → send request → verify response + GPU utilization
3. **Decision**: Accepted, rejected, or deferred with a note
4. **Publication**: If accepted, it appears in the next edition
5. **Adapter build**: If accepted, we (or a contributor) build the `ModelServingAdapter` for standard benchmarking

## Fixing Data

### If you find incorrect metadata

File an issue with:

```markdown
## Data Correction: [Engine Name]

### Current (incorrect) data
[What does the roster say?]

### Correct data
[What should it say?]

### Evidence
[Link to the source that proves the correct data.]
```

### Common corrections for model serving

| Field | Common errors | How to verify |
|-------|--------------|---------------|
| License | Wrong SPDX identifier | Check the repo's LICENSE file |
| Stars | Out of date | Check the GitHub API |
| Last push | Wrong date | Check the GitHub repo |
| Tier | Wrong tier | Check the tier rules in IMPLEMENTATION.md |
| Notes | Outdated description | Check the engine's homepage/docs |
| `supported_formats` | Missing formats | Check the engine's docs for supported checkpoint formats (Safetensors, GGUF, ONNX, etc.) |
| `supported_quantization` | Missing or wrong quantization | Check the engine's quantization docs; test loading a quantized model |
| `hardware_target` | Wrong target | Check if the engine is GPU-only, CPU-only, edge-focused, or multi-node |

### What happens after submission

Data corrections are reviewed and applied in the next edition cycle. We don't edit editions retroactively; we correct the data and note it in the next edition.

## Challenging a Ranking

### If you believe a score is wrong

File an issue with:

```markdown
## Challenge: [Engine Name] on [Dimension]

### Current score
[What does the almanac say?]

### Your evidence
[What data do you have?]

### Hardware used
[GPU class, CUDA version, engine version — must match or be comparable]

### What you did to verify
[Steps you took to reproduce or verify.]

### Suggested resolution
[What should change? Re-run? Different score? Methodology update?]
```

### What evidence is valid

| Evidence Type | Strength | Example |
|---------------|----------|---------|
| Raw results JSON analysis | Strong | "I re-analyzed the JSON and found the TTFT measurement was biased by warm-up" |
| Independent reproduction on same hardware | Strong | "I ran the harness on A100-80GB with identical CUDA version and got 15% different throughput" |
| Documentation of a known engine bug | Medium | "The engine has a known batching bug that affects this test, fixed in v0.6.1" |
| Vendor claim | Weak | "The vendor says Z" — but we already test vendor claims independently |
| Anecdote | Weak | "It worked for me" — not reproducible without hardware and version details |
| Different hardware result | Weak | "I got different numbers on my RTX 4090" — results are hardware-specific and not comparable |

### What happens after submission

1. **Review**: We review the evidence (within 7 days)
2. **Reproduction**: If the claim is reproducible on the same hardware class, we re-run the test
3. **Update**: If the re-run confirms the challenge, we update the score
4. **Publication**: The update appears in the next edition

## Improving the Methodology

### If you want to propose a methodology change

File an issue with:

```markdown
## Methodology Proposal: [Title]

### Current state
[What does the methodology say now?]

### Proposed change
[What should it say?]

### Rationale
[Why is this better? What problem does it solve?]

### Impact
[Which engines/dimensions would be affected?]

### Backward compatibility
[Can old results be re-scored with the new method?]
```

### Methodology change process

1. **RFC**: The proposal is posted as an RFC for public comment (30 days)
2. **Discussion**: Community feedback is collected
3. **Decision**: ArdurAI makes the final decision based on feedback
4. **Announcement**: If accepted, a public announcement is made with a transition plan
5. **Implementation**: The change is implemented in the next edition cycle
6. **Re-run**: Affected benchmarks are re-run with the new methodology

### What kinds of changes are accepted for model serving

| Change Type | Likelihood | Example |
|-------------|------------|---------|
| Bug fix in harness | High | "The adapter incorrectly measures TTFT by including connection establishment time" |
| New benchmark suite | Medium | "Add a prefix-caching benchmark to measure reuse efficiency" |
| New accuracy metric | Medium | "Add a long-context perplexity benchmark (e.g., RULER or needle-in-haystack)" |
| Weight adjustment | Medium | "Increase ops burden weight from 15% to 20% for multi-node engines" |
| New dimension | Low | "Add a 'sustainability' dimension measuring energy per 1M tokens" |
| Remove dimension | Very low | "Remove latency as a dimension" |

### What kinds of changes are rejected

- Changes that favor a specific vendor or engine
- Changes that reduce reproducibility (e.g., removing hardware-specific tagging)
- Changes that increase complexity without clear benefit to platform engineers
- Changes that are not backward-compatible without a migration plan
- Changes that ignore the hardware-specific nature of inference benchmarking

## Code of Conduct

### Be respectful

This is a collaborative project. Treat others with respect, even when you disagree about which engine is "best."

### Be evidence-based

Claims should be backed by evidence. "I think X is faster" is not enough. "I measured TTFT on A100 and found Y" is. Include hardware class, CUDA version, engine version, and model used.

### Be constructive

Criticism is welcome if it's constructive. "This engine sucks" is not helpful. "This engine has a batching starvation bug under concurrent load, and here's the reproduction" is.

### Be patient

The almanac is maintained by a small team. GPU benchmark runs take hours. Responses may take time. Repeated pings are not helpful.

### No spam

Don't submit the same engine multiple times. Don't submit engines that clearly don't meet criteria (e.g., a training framework with no serving layer). Don't use the almanac for marketing.

## License

By contributing to the almanac, you agree that your contributions are licensed under CC BY 4.0 for content and MIT for code.

## Attribution

Contributors are recognized in the edition notes. If you make a significant contribution (e.g., adding 5+ engines, fixing major data issues, improving methodology, building adapters), you will be listed as a contributor in the next edition.

## License

Content: CC BY 4.0  
Code: MIT
