# Zeus - AI Toolkit for Apple Silicon

**Got a Mac? Mac Silicon? Infer like God-Mode!**

A collection of AI tools optimized for Apple Silicon Macs, leveraging MPS (Metal Performance Shaders) acceleration for blazing-fast inference without CUDA.

## Projects

### 🎨 SD-Generate - Text-to-Image Generation

Complete Stable Diffusion pipeline for macOS with Apple Silicon optimization.

**Features:**
- One-command installation and setup
- Robust retry logic and fault tolerance
- Support for LoRA, ControlNet, refiners, and upscaling
- Built-in style presets (anime, fantasy, scifi, realism)
- Complete metadata logging
- MPS-optimized with float32 precision

**Quick Start:**
```bash
cd sd-generate
./setup.sh

# Generate images
generate "a beautiful landscape"
generate "cyberpunk city" --style scifi --n 4
generate "anime warrior" --style anime --steps 50
```

**[Full Documentation →](sd-generate/README.md)**

## System Requirements

- **Hardware**: Apple Silicon (M1, M2, M3, M4) Mac
- **OS**: macOS 12.0 or later
- **RAM**: 8GB minimum, 16GB recommended
- **Python**: 3.8+

## Why Zeus?

Traditional AI tools are built for CUDA/NVIDIA GPUs. Zeus brings that power to Mac users by:

1. **Native MPS Support**: Leverages Apple's Metal Performance Shaders
2. **Float32 Stability**: Avoids common MPS precision issues
3. **Fault Tolerance**: Automatic retries and graceful degradation
4. **Zero Configuration**: One script to rule them all
5. **Production Ready**: Battle-tested error handling

## Performance

| Task | Steps | Resolution | Time (M1 Pro) |
|------|-------|-----------|---------------|
| Basic Generation | 25 | 512x512 | ~8-12s |
| High Quality | 50 | 512x512 | ~15-20s |
| Batch (4 images) | 25 | 512x512 | ~30-35s |
| With Upscale 2x | 25 | 1024x1024 | ~25-30s |

## Coming Soon

- 🎭 Face restoration and enhancement
- 🎬 Video generation (Stable Video Diffusion)
- 🗣️ Local LLM inference (Llama, Mistral)
- 🎵 Audio generation and processing
- 🔍 Image analysis and captioning

## Contributing

Contributions welcome! This is an evolving toolkit focused on bringing enterprise-grade AI to Mac users.

## License

See individual project directories for licensing information.

---

**Built with ⚡ by developers who believe Macs can be AI powerhouses too.**
