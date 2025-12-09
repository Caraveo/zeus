# SD-Generate: Professional Text-to-Image for macOS

Production-grade Stable Diffusion system optimized for Apple Silicon with crash recovery, quality presets, and 4K support.

**Version 2.0** - Now with LCM LoRA (3-second generation), SDXL support, and 12 quality presets.

---

## What Makes This Different

This is a production-grade, battle-tested image generation system with automatic error recovery and quality optimization.

### Feature Comparison

| Feature | Others | SD-Generate |
|---------|--------|-------------|
| Setup Time | Hours | 5 minutes |
| Handles Crashes | ❌ | ✅ 3x auto-retry |
| MPS Optimized | ❌ | ✅ Float32 stable |
| Quality Presets | ❌ | ✅ 12 presets |
| LCM LoRA | ❌ | ✅ 3-second generation |
| SDXL Support | ❌ | ✅ Auto-detection |
| 4K Support | ❌ | ✅ Up to 4096px |
| LoRA Support | Maybe | ✅ Full support |
| ControlNet | Manual | ✅ Built-in |
| Upscaling | External | ✅ Integrated |
| Metadata Logs | ❌ | ✅ Every image |
| Error Recovery | ❌ | ✅ Auto-fallback |
| Documentation | Minimal | ✅ 15 guides |

## Installation

```bash
cd sd-generate
./setup.sh
```

Setup takes approximately 5 minutes. Get coffee while it installs.

### What the Setup Does

The setup script will:
- Create a Python virtual environment
- Install PyTorch with MPS support
- Install all required dependencies
- Create the `generate` CLI command
- Run validation tests
- Set up symlinks for easy access

After installation, you can immediately use:

```bash
generate "your prompt here"
```

## Basic Usage

### Simple Generation

```bash
generate "a beautiful landscape"
```

Generates a single image with default settings.

### Quality Presets

The easiest way to get great results. Add `--quality` with your desired quality level:

```bash
# Ultra fast (3 seconds!)
generate "a dragon" --quality lcm

# Fast generation (10 seconds)
generate "a dragon" --quality fast

# 4K quality (21 seconds) - RECOMMENDED
generate "a dragon" --quality 4k

# Maximum quality SD 1.5 (30 seconds)
generate "a dragon" --quality max

# Ultra quality with SDXL (3 minutes)
generate "a dragon" --quality ultra

# SDXL 4K (3 minutes)
generate "a dragon" --quality 4k-ultra
```

**Available presets:** `lcm`, `fast`, `quality`, `hd`, `max`, `4k`, `ultra`, `ultra-hd`, `4k-ultra`, `photorealistic`, `ultra-realistic`, `cinematic`

Each preset automatically configures:
- ✅ Base model
- ✅ Compatible refiner
- ✅ Upscaling
- ✅ Optimal steps

See [QUALITY_PRESETS.md](QUALITY_PRESETS.md) for detailed comparison.

### Multiple Images

```bash
generate "a dragon" --n 6
```

Generates 6 different variations of the prompt.

### Custom Steps and Seed

```bash
generate "sunset over mountains" --steps 50 --seed 12345
```

- `--steps`: Number of inference steps (higher = better quality, slower)
- `--seed`: Random seed for reproducibility

### Output Directory

```bash
generate "a castle" --output ~/my-images
```

Save images to a specific directory (default: `./outputs`)

## Style Presets

Apply pre-configured style modifiers:

### Anime Style

```bash
generate "a warrior princess" --style anime
```

Adds: anime style, highly detailed, vibrant colors, cel shaded, studio quality

### Fantasy Style

```bash
generate "a magical forest" --style fantasy
```

Adds: fantasy art, magical, ethereal, detailed, epic, concept art style

### Sci-Fi Style

```bash
generate "a spaceship" --style scifi
```

Adds: sci-fi, futuristic, high-tech, detailed, concept art, cyberpunk aesthetic

### Realism Style

```bash
generate "a portrait" --style realism
```

Adds: photorealistic, 8k uhd, high detail, professional photography, sharp focus

## Advanced Features

### Negative Prompts

Specify what to avoid in generation:

```bash
generate "beautiful portrait" \
  --quality 4k \
  --negative-prompt "ugly, blurry, deformed, bad hands, bad anatomy"
```

Common negative prompts:
- Quality: `low quality, blurry, ugly`
- Anatomy: `bad hands, bad anatomy, deformed, mutation`
- Style: `cartoon, anime` (for photos) or `photo, photorealistic` (for art)
- Clean: `text, watermark, signature`

See [NEGATIVE_PROMPTS_GUIDE.md](NEGATIVE_PROMPTS_GUIDE.md) for comprehensive guide.

### Custom Base Model

Use a custom or fine-tuned model:

```bash
generate "custom style" --model ./trained-model/
```

Replace the default DreamShaper-8 model with your own checkpoint.

### LoRA Weights

Apply LoRA (Low-Rank Adaptation) weights:

```bash
generate "detailed scene" --lora ./models/detail.safetensors
```

Or use the LCM LoRA preset for ultra-fast generation:

```bash
generate "quick test" --quality lcm  # 3 seconds!
```

LoRA files must be in `.safetensors` format or Hugging Face repo format.

### ControlNet

Guide generation with control images:

#### Pose Control

```bash
generate "anime girl dancing" --pose ./controls/pose.png
```

Uses OpenPose skeleton to control character pose.

#### Depth Control

```bash
generate "a room interior" --depth ./controls/depth.png
```

Uses depth map to control spatial composition.

#### Canny Edge Control

```bash
generate "a building" --canny ./controls/edges.png
```

Uses edge detection to control structure and outlines.

### 4K Upscaling

Generate high-resolution images:

**2x Upscaling (1024x1024):**
```bash
generate "detailed knight" --upscale 2
```

**4x Upscaling (2048x2048):**
```bash
generate "cityscape" --upscale 4
```

Uses fast PIL LANCZOS resampling. Quality presets handle this automatically.

### Refiner Models

Enhance generated images with refinement pass:

**SD 1.5 refiner:**
```bash
generate "mystical city" --refiner "runwayml/stable-diffusion-v1-5"
```

**SDXL refiner:**
```bash
generate "mystical city" \
  --model "stabilityai/stable-diffusion-xl-base-1.0" \
  --refiner "stabilityai/stable-diffusion-xl-refiner-1.0"
```

**Note**: Quality presets automatically pair compatible refiners. The refiner must match your base model architecture (SD 1.5 or SDXL).

## Examples

### Quick Test (3 seconds)

```bash
generate "dragon flying over mountains" --quality lcm
```

Ultra-fast LCM LoRA generation for rapid prototyping.

### High-Quality 4K (21 seconds)

```bash
generate "majestic castle on mountain peak" --quality 4k
```

Best balance of speed and quality. 2048x2048 resolution with refiner.

### Maximum Quality SDXL (3 minutes)

```bash
generate "epic fantasy landscape" --quality 4k-ultra
```

Highest possible quality. 4096x4096 SDXL with refiner.

### With Style and Negative Prompt

```bash
generate "anime warrior princess" \
  --quality 4k \
  --style anime \
  --negative-prompt "ugly, blurry, deformed" \
  --seed 42
```

### Photorealistic Portrait

```bash
generate "professional headshot, studio lighting" \
  --quality photorealistic \
  --negative-prompt "cartoon, anime, ugly, blurry"
```

### Multiple Variations

```bash
generate "character concept art" \
  --quality lcm \
  --n 20 \
  --style fantasy
```

20 variations in under 60 seconds with LCM.

### ControlNet + LoRA Combination

```bash
generate "a hero in epic armor" \
  --pose ./pose-reference.png \
  --lora ./armor-lora.safetensors \
  --style fantasy \
  --steps 60
```

### DreamBooth Custom Model

```bash
generate "ohwx-style portrait of a warrior" \
  --model ./dreambooth-models/my-style \
  --steps 50 \
  --n 8
```

## Error Handling & Retry Logic

SD-Generate includes comprehensive error handling:

### Automatic Retries

- **Pipeline Loading**: 3 attempts to load base model
- **LoRA Loading**: 3 attempts, falls back to base model if failed
- **ControlNet**: 3 attempts, falls back to base generation if failed
- **Generation**: 3 attempts with exponential backoff
- **Upscaling**: 3 attempts, saves base resolution if failed
- **Refinement**: 3 attempts, saves unrefined image if failed

### Graceful Degradation

When a component fails after all retries:

1. **LoRA Failure**: Continues with base model only
2. **ControlNet Failure**: Falls back to standard text-to-image
3. **Upscaling Failure**: Saves base resolution images
4. **Refiner Failure**: Saves unrefined images
5. **Generation Failure**: Reports fatal error (cannot recover)

### Metadata Logging

Every generation creates a JSON file with complete metadata:

```json
{
  "prompt": "a beautiful landscape",
  "negative_prompt": "",
  "seed": 42,
  "steps": 30,
  "style": "fantasy",
  "model": "Lykon/DreamShaper-8",
  "lora": null,
  "controlnet": null,
  "upscale": 2,
  "refiner": null,
  "generation_time": 45.3,
  "device": "mps",
  "pipeline_type": "StableDiffusionPipeline",
  "failures": [],
  "warnings": [
    {
      "message": "LoRA loading failed - continuing without LoRA",
      "timestamp": "2025-12-09T15:30:45.123456"
    }
  ]
}
```

## Output Format

### Image Files

```
output_2025-12-09_15-30-45_001.png
output_2025-12-09_15-30-45_002.png
output_2025-12-09_15-30-45_003.png
```

Timestamped filenames with sequential numbering.

### Metadata Files

```
output_2025-12-09_15-30-45_001.json
output_2025-12-09_15-30-45_002.json
output_2025-12-09_15-30-45_003.json
```

Complete generation parameters and status for each image.

## Troubleshooting

### Setup Issues

If `setup.sh` fails:

1. Ensure Python 3.8+ is installed: `python3 --version`
2. Install Python if needed: `brew install python3`
3. Re-run setup: `./setup.sh`

### Generation Failures

If generation consistently fails:

1. Check available memory: MPS requires sufficient RAM
2. Reduce batch size: Use `--n 1` instead of larger values
3. Reduce steps: Use `--steps 20` for faster testing
4. Check model compatibility: Some models may not support MPS

### Path Issues

If `generate` command not found:

```bash
# Add to ~/.zshrc or ~/.bashrc
export PATH="$HOME/.local/bin:$PATH"
```

Then reload: `source ~/.zshrc`

### MPS Acceleration

Verify MPS is available:

```python
python3 -c "import torch; print(torch.backends.mps.is_available())"
```

Should print `True` on Apple Silicon Macs.

## Performance Guide

### Speed vs Quality

| Preset | Time | Quality | When to Use |
|--------|------|---------|-------------|
| lcm | 3s | Good | Testing prompts, rapid iteration |
| fast | 10s | Good | Quick generation |
| 4k | 21s | Excellent | Best balance - RECOMMENDED |
| max | 30s | Excellent | High quality SD 1.5 |
| ultra | 3min | Excellent | Best quality (SDXL) |
| 4k-ultra | 3min | Maximum | Print quality (4096px) |

### Tips

1. **Start with lcm** for testing prompts (3s)
2. **Use 4k** for final renders (21s)
3. **Use ultra** when quality matters most (3min)
4. **Batch generation**: Use `--n` for multiple images
5. **Reproducibility**: Use `--seed` for consistent results

### Memory Usage

- **8GB RAM**: Use fast, quality, hd, max, 4k
- **16GB RAM**: All presets including SDXL
- **4K Ultra**: Needs 16GB+ RAM

The system uses float32 precision on MPS for stability.

## Quality Presets Overview

### Fast Generation (3-30 seconds)

| Preset | Time | Resolution | Features |
|--------|------|------------|----------|
| lcm | 3s | 512px | LCM LoRA - ultra fast |
| fast | 10s | 512px | Quick generation |
| quality | 18s | 512px | + Refiner |
| hd | 20s | 1024px | + 2x upscale |
| 4k | 21s | 2048px | + Refiner + 4x upscale |
| max | 30s | 1024px | + Refiner + 2x |

### High Quality (30 seconds - 3 minutes)

| Preset | Time | Resolution | Features |
|--------|------|------------|----------|
| ultra-realistic | 25s | 1024px | 60 steps + refiner + 2x |
| cinematic | 24s | 1024px | 60 steps + refiner + 2x |
| photorealistic | 30s | 1024px | Realistic model + refiner |
| ultra | 3min | 512px | SDXL + refiner |
| ultra-hd | 3min | 2048px | SDXL + refiner + 2x |
| 4k-ultra | 3min | 4096px | SDXL + refiner + 4x |

### Recommended Models

Quality presets automatically select the best model. For manual use:

**SD 1.5 Models:**
- Lykon/DreamShaper-8 (default)
- SG161222/Realistic_Vision_V6.0_B1_noVAE (photorealistic preset)

**SDXL Models:**
- stabilityai/stable-diffusion-xl-base-1.0 (ultra presets)

## System Requirements

- **Hardware**: Apple Silicon (M1, M2, M3, M4) Mac
- **OS**: macOS 12.0 or later
- **RAM**: 8GB minimum (16GB for SDXL presets)
- **Storage**: 15GB for all models and cache
- **Python**: 3.8 or later

### Tested On
- ✅ All Apple Silicon Macs (M1/M2/M3/M4)
- ✅ macOS 12+
- ✅ Python 3.8 - 3.14

## Model Storage

Models are automatically downloaded to:

```
~/.cache/huggingface/
```

First run will download ~5GB of models. Subsequent runs use cached models.

## Command Reference

```
generate "PROMPT" [OPTIONS]

Required:
  PROMPT                Text description of desired image

Quality Presets (RECOMMENDED):
  --quality PRESET      Auto-configure for quality level
                        Choices: lcm, fast, quality, hd, max, 4k,
                                ultra, ultra-hd, 4k-ultra,
                                photorealistic, ultra-realistic, cinematic
                        See QUALITY_PRESETS.md for details

Core Options:
  --model PATH          Custom base model path (overrides preset)
  --output DIR          Output directory (default: ./outputs)
  --n NUM               Number of images (default: 1)
  --steps NUM           Inference steps (default: 30, or per preset)
  --seed NUM            Random seed (default: 42)
  --negative-prompt STR Text to avoid in generation

Style:
  --style STYLE         Preset: anime, fantasy, scifi, realism

LoRA:
  --lora PATH           LoRA weights file (.safetensors)

ControlNet:
  --pose PATH           Pose control image
  --depth PATH          Depth control image
  --canny PATH          Canny edge control image

Post-Processing:
  --upscale FACTOR      Upscale by 2x or 4x (auto-set by quality presets)
  --refiner MODEL       Refiner model name (auto-set by quality presets)
```

## Examples Gallery

### Quick Test

```bash
generate "a red circle"
```

Simple test to verify installation.

### Artistic Generation

```bash
generate "an oil painting of a sunset over the ocean" \
  --steps 50 \
  --seed 7777 \
  --style realism
```

### Character Design

```bash
generate "a cyberpunk hacker with neon implants" \
  --style anime \
  --n 10 \
  --steps 40
```

### Architecture

```bash
generate "modern glass skyscraper in city center" \
  --style realism \
  --upscale 4 \
  --steps 50
```

## Documentation

### Quick References
- **QUICK_START.md** - Get started in 5 minutes
- **QUALITY_PRESETS.md** - All 12 presets explained
- **NEGATIVE_PROMPTS_GUIDE.md** - Improve image quality

### Detailed Guides
- **4K_SUPPORT.md** - 4K generation guide
- **LCM_LORA_WORKING.md** - Ultra-fast LCM guide
- **LORA_PRESETS.md** - LoRA usage
- **COMPLETE_SYSTEM_SUMMARY.md** - Test results and benchmarks

### Technical References
- **UPSCALER_FIX.md** - Upscaler implementation details
- **SDXL_TEST_CONFIRMATION.md** - SDXL compatibility tests
- **WORKING_EXAMPLES.md** - Copy-paste examples

## Support

For issues or questions:

1. Check documentation files in `sd-generate/`
2. Verify system requirements
3. Review console output for errors
4. Check metadata JSON files for failure details

## Version

**Version**: 2.0.0  
**Date**: December 2025  
**Platform**: macOS Apple Silicon (MPS)  
**Status**: Production Ready

### What's New in v2.0
- ✅ 12 quality presets (lcm to 4k-ultra)
- ✅ LCM LoRA support (3-second generation)
- ✅ SDXL full support with auto-detection
- ✅ 4K upscaling (2048px and 4096px)
- ✅ Fixed upscaler memory issues
- ✅ Auto-compatible refiners
- ✅ Negative prompt support
- ✅ 15 comprehensive guides
