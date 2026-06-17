import json

roster = json.load(open('/Users/gnutakki16/Documents/kimi/workspace/ai-model-serving-almanac/data/roster.json'))

enrichment = {
    "vLLM": {
        "region": "Global",
        "supported_formats": ["safetensors", "gguf", "pytorch", "awq", "gptq"],
        "supported_quantization": ["fp16", "bf16", "fp8", "int8", "awq", "gptq", "marlin", "gguf"],
        "hardware_target": "GPU"
    },
    "SGLang": {
        "region": "Global",
        "supported_formats": ["safetensors", "pytorch", "gguf"],
        "supported_quantization": ["fp16", "bf16", "fp8", "int8", "awq", "gptq"],
        "hardware_target": "GPU"
    },
    "TensorRT-LLM": {
        "region": "US",
        "supported_formats": ["safetensors", "pytorch", "onnx", "tensorrt"],
        "supported_quantization": ["fp16", "bf16", "fp8", "int8", "int4", "awq"],
        "hardware_target": "GPU"
    },
    "llama.cpp": {
        "region": "Global",
        "supported_formats": ["gguf", "ggml"],
        "supported_quantization": ["q4_0", "q4_1", "q5_0", "q5_1", "q8_0", "q2_k", "q3_k", "q4_k", "q5_k", "q6_k", "q8_k", "f16", "f32"],
        "hardware_target": "CPU|GPU|Edge"
    },
    "NVIDIA Dynamo": {
        "region": "US",
        "supported_formats": ["safetensors", "pytorch", "tensorrt"],
        "supported_quantization": ["fp16", "bf16", "fp8", "int8"],
        "hardware_target": "Multi-node"
    },
    "KServe": {
        "region": "Global",
        "supported_formats": ["safetensors", "pytorch", "onnx", "tensorrt"],
        "supported_quantization": ["fp16", "bf16", "fp8", "int8"],
        "hardware_target": "Multi-node"
    },
    "BentoML": {
        "region": "Global",
        "supported_formats": ["safetensors", "pytorch", "onnx", "pickle"],
        "supported_quantization": ["fp16", "bf16", "fp8", "int8"],
        "hardware_target": "GPU|Multi-node"
    },
    "Ray Serve": {
        "region": "US",
        "supported_formats": ["safetensors", "pytorch", "onnx", "tensorrt"],
        "supported_quantization": ["fp16", "bf16", "fp8", "int8"],
        "hardware_target": "Multi-node"
    },
    "Ollama": {
        "region": "Global",
        "supported_formats": ["gguf"],
        "supported_quantization": ["q4_0", "q4_1", "q5_0", "q5_1", "q8_0", "q2_k", "q3_k", "q4_k", "q5_k", "q6_k", "q8_k", "f16", "f32"],
        "hardware_target": "CPU|GPU|Edge"
    },
    "LMDeploy": {
        "region": "China",
        "supported_formats": ["safetensors", "pytorch", "awq", "gptq"],
        "supported_quantization": ["fp16", "bf16", "fp8", "int8", "awq", "gptq", "w4a16"],
        "hardware_target": "GPU"
    },
    "TGI (Text Generation Inference)": {
        "region": "Global",
        "supported_formats": ["safetensors", "pytorch", "gguf"],
        "supported_quantization": ["fp16", "bf16", "fp8", "int8", "awq", "gptq", "eetq", "marlin"],
        "hardware_target": "GPU"
    },
    "DeepSpeed-MII": {
        "region": "US",
        "supported_formats": ["safetensors", "pytorch"],
        "supported_quantization": ["fp16", "bf16", "int8"],
        "hardware_target": "GPU|Multi-node"
    },
    "Aphrodite Engine": {
        "region": "Global",
        "supported_formats": ["safetensors", "pytorch", "gguf", "exl2"],
        "supported_quantization": ["fp16", "bf16", "fp8", "fp4", "fp2", "int8", "awq", "gptq", "exl2", "gguf", "marlin"],
        "hardware_target": "GPU"
    },
    "MLX": {
        "region": "US",
        "supported_formats": ["safetensors", "gguf", "npz"],
        "supported_quantization": ["fp16", "bf16", "int8", "q4", "q8"],
        "hardware_target": "Edge"
    },
    "ExLlamaV2": {
        "region": "Global",
        "supported_formats": ["safetensors", "exl2"],
        "supported_quantization": ["fp16", "exl2", "gptq"],
        "hardware_target": "GPU"
    },
    "CTranslate2": {
        "region": "Global",
        "supported_formats": ["safetensors", "pytorch", "onnx"],
        "supported_quantization": ["fp16", "int8", "int16", "fp32"],
        "hardware_target": "CPU|GPU"
    },
    "TensorRT Edge-LLM": {
        "region": "US",
        "supported_formats": ["onnx", "tensorrt"],
        "supported_quantization": ["fp16", "int8", "fp8", "nvfp4"],
        "hardware_target": "Edge"
    },
    "MindIE": {
        "region": "China",
        "supported_formats": ["safetensors", "pytorch"],
        "supported_quantization": ["fp16", "bf16", "int8"],
        "hardware_target": "GPU"
    },
    "RTP-LLM": {
        "region": "China",
        "supported_formats": ["safetensors", "pytorch"],
        "supported_quantization": ["fp16", "bf16", "fp8", "int8"],
        "hardware_target": "GPU|Multi-node"
    },
    "NVIDIA Nim": {
        "region": "US",
        "supported_formats": ["safetensors", "tensorrt"],
        "supported_quantization": ["fp16", "bf16", "fp8", "int8"],
        "hardware_target": "GPU|Multi-node|Cloud"
    },
    "Triton Inference Server": {
        "region": "US",
        "supported_formats": ["onnx", "tensorrt", "pytorch", "tensorflow"],
        "supported_quantization": ["fp16", "bf16", "fp8", "int8"],
        "hardware_target": "GPU|Multi-node"
    },
    "Seldon Core v2": {
        "region": "Global",
        "supported_formats": ["safetensors", "pytorch", "onnx", "tensorflow", "sklearn"],
        "supported_quantization": ["fp16", "bf16", "int8"],
        "hardware_target": "Multi-node"
    },
    "llm-d": {
        "region": "Global",
        "supported_formats": ["safetensors", "pytorch"],
        "supported_quantization": ["fp16", "bf16", "fp8", "int8"],
        "hardware_target": "Multi-node"
    },
    "KAITO": {
        "region": "US",
        "supported_formats": ["safetensors", "pytorch", "onnx", "gguf"],
        "supported_quantization": ["fp16", "bf16", "fp8", "int8"],
        "hardware_target": "Multi-node"
    },
    "Kueue": {
        "region": "Global",
        "supported_formats": ["N/A"],
        "supported_quantization": ["N/A"],
        "hardware_target": "Multi-node"
    },
    "NVIDIA GPU Operator": {
        "region": "US",
        "supported_formats": ["N/A"],
        "supported_quantization": ["N/A"],
        "hardware_target": "Multi-node"
    },
    "TorchServe": {
        "region": "US",
        "supported_formats": ["pytorch", "torchscript", "onnx"],
        "supported_quantization": ["fp16", "bf16", "int8"],
        "hardware_target": "GPU|Multi-node"
    },
    "TensorFlow Serving": {
        "region": "US",
        "supported_formats": ["tensorflow", "onnx"],
        "supported_quantization": ["fp16", "int8"],
        "hardware_target": "GPU|Multi-node"
    },
    "Fireworks AI": {
        "region": "US",
        "supported_formats": ["N/A"],
        "supported_quantization": ["N/A"],
        "hardware_target": "Cloud"
    },
    "Together AI": {
        "region": "US",
        "supported_formats": ["N/A"],
        "supported_quantization": ["N/A"],
        "hardware_target": "Cloud"
    },
    "Replicate": {
        "region": "US",
        "supported_formats": ["N/A"],
        "supported_quantization": ["N/A"],
        "hardware_target": "Cloud"
    },
    "Modal": {
        "region": "US",
        "supported_formats": ["N/A"],
        "supported_quantization": ["N/A"],
        "hardware_target": "Cloud"
    },
    "Baseten": {
        "region": "US",
        "supported_formats": ["N/A"],
        "supported_quantization": ["N/A"],
        "hardware_target": "Cloud"
    },
    "Deep Infra": {
        "region": "US",
        "supported_formats": ["N/A"],
        "supported_quantization": ["N/A"],
        "hardware_target": "Cloud"
    },
    "RunPod": {
        "region": "US",
        "supported_formats": ["N/A"],
        "supported_quantization": ["N/A"],
        "hardware_target": "Cloud"
    },
    "Lambda Labs": {
        "region": "US",
        "supported_formats": ["N/A"],
        "supported_quantization": ["N/A"],
        "hardware_target": "Cloud"
    },
    "Vast.ai": {
        "region": "US",
        "supported_formats": ["N/A"],
        "supported_quantization": ["N/A"],
        "hardware_target": "Cloud"
    },
    "CoreWeave": {
        "region": "US",
        "supported_formats": ["N/A"],
        "supported_quantization": ["N/A"],
        "hardware_target": "Cloud"
    },
    "Nebius": {
        "region": "EU",
        "supported_formats": ["N/A"],
        "supported_quantization": ["N/A"],
        "hardware_target": "Cloud"
    },
    "Crusoe": {
        "region": "US",
        "supported_formats": ["N/A"],
        "supported_quantization": ["N/A"],
        "hardware_target": "Cloud"
    },
    "GMI Cloud": {
        "region": "US",
        "supported_formats": ["N/A"],
        "supported_quantization": ["N/A"],
        "hardware_target": "Cloud"
    },
    "LiteLLM": {
        "region": "US",
        "supported_formats": ["N/A"],
        "supported_quantization": ["N/A"],
        "hardware_target": "Cloud|Multi-node"
    },
    "Portkey": {
        "region": "Global",
        "supported_formats": ["N/A"],
        "supported_quantization": ["N/A"],
        "hardware_target": "Cloud|Multi-node"
    },
    "Bifrost": {
        "region": "Global",
        "supported_formats": ["N/A"],
        "supported_quantization": ["N/A"],
        "hardware_target": "Cloud|Multi-node"
    },
    "TensorZero": {
        "region": "Global",
        "supported_formats": ["N/A"],
        "supported_quantization": ["N/A"],
        "hardware_target": "Cloud|Multi-node"
    },
    "ExecuTorch": {
        "region": "US",
        "supported_formats": ["pte", "pytorch"],
        "supported_quantization": ["fp16", "bf16", "int8", "int4"],
        "hardware_target": "Edge"
    },
    "MLC-LLM": {
        "region": "Global",
        "supported_formats": ["safetensors", "pytorch"],
        "supported_quantization": ["fp16", "int8", "int4", "q4f16", "q4f32"],
        "hardware_target": "Edge"
    }
}

for tool in roster['tools']:
    name = tool['name']
    if name in enrichment:
        for key, value in enrichment[name].items():
            tool[key] = value

with open('/Users/gnutakki16/Documents/kimi/workspace/ai-model-serving-almanac/data/roster.json', 'w') as f:
    json.dump(roster, f, indent=2)

print("Enriched roster.json written successfully")
print(f"Total tools: {len(roster['tools'])}")

# Verify all recommended fields now present
missing_any = 0
for tool in roster['tools']:
    for key in ['region', 'supported_formats', 'supported_quantization', 'hardware_target']:
        if key not in tool or not tool[key]:
            print(f"WARNING: {tool['name']} missing {key}")
            missing_any += 1

if missing_any == 0:
    print("All tools have complete recommended fields!")
