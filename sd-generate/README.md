# 🎨 SD-Generate: Professional Text-to-Image for macOS

<div align="center">

### **Got a Mac? Mac Silicon? Infer like God-Mode!** 🔥

*The ONLY Stable Diffusion setup you need for Apple Silicon*

</div>

---

## 💎 What Makes This Different?

**THIS ISN'T JUST ANOTHER STABLE DIFFUSION WRAPPER.**

This is a **PRODUCTION-GRADE**, **BATTLE-TESTED**, **CRASH-PROOF** image generation system that treats your Mac like the powerhouse it is.

### 🚀 The Complete Package

| Feature | Others | SD-Generate |
|---------|--------|-------------|
| **Setup Time** | Hours of pain | **5 minutes** ☕ |
| **Handles Crashes** | ❌ | ✅ **3x auto-retry** |
| **MPS Optimized** | ⚠️ Broken | ✅ **Float32 stable** |
| **LoRA Support** | Maybe | ✅ **Full support** |
| **ControlNet** | "Install yourself" | ✅ **Built-in** |
| **Upscaling** | Extra tools | ✅ **Integrated** |
| **Metadata Logs** | ❌ | ✅ **Every image** |
| **Error Recovery** | Crash & lose work | ✅ **Auto-fallback** |
| **Documentation** | "Read the code" | ✅ **Complete guide** |

**Translation:** We built what we wish existed.

## ⚡ Installation - Stupidly Simple

**Seriously, this is ALL you need:**

```bash
cd sd-generate
./setup.sh
```

**That's it.** Go get coffee. Come back. You're a wizard now. 🧙‍♂️

### What Just Happened? (Magic, Basically)

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

### 🎯 Quality Presets (NEW! - Easy Mode)

**The easiest way to get great results!** Just add `--quality` with your desired quality level:

```bash
# Fast generation (5-10 seconds)
generate "a dragon" --quality fast

# Maximum quality SD 1.5 (30 seconds)
generate "a dragon" --quality max

# Ultra quality with SDXL (60 seconds)
generate "a dragon" --quality ultra

# Photorealistic (specialized model)
generate "a portrait" --quality photorealistic
```

**Available presets:** `fast`, `quality`, `hd`, `max`, `ultra`, `ultra-hd`, `photorealistic`

Each preset automatically configures the perfect combination of:
- ✅ Base model
- ✅ Compatible refiner
- ✅ Upscaling (if applicable)
- ✅ Optimal steps

**See [QUALITY_PRESETS.md](QUALITY_PRESETS.md) for detailed comparison and examples.**

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

### Custom Base Model

Use a custom or fine-tuned model:

```bash
generate "jon-style hero" --model ./trained-model/
```

Replace the default DreamShaper-8 model with your own checkpoint.

### LoRA Weights

Apply LoRA (Low-Rank Adaptation) weights:

```bash
generate "an elf archer" --lora ./models/elf-face.safetensors
```

LoRA files must be in `.safetensors` format.

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

### Upscaling

Enhance resolution with AI upscaling:

**2x Upscaling (faster):**
```bash
generate "a detailed knight" --upscale 2
```

**4x Upscaling (highest quality):**
```bash
generate "a cityscape" --upscale 4
```

Uses **stabilityai/stable-diffusion-x4-upscaler** for high-quality enlargement.

**Note**: Upscaling is memory-intensive. On 8GB RAM systems, use `--upscale 2` instead of 4. The upscaler works with any base model (SD 1.5 or SDXL) since it operates on the generated image.

### Refiner Models

Enhance generated images with a refiner pass:

**For SD 1.5 models (like DreamShaper-8):**
```bash
generate "a mystical city" --refiner "runwayml/stable-diffusion-v1-5"
```

**For SDXL base models:**
```bash
generate "a mystical city" --model "stabilityai/stable-diffusion-xl-base-1.0" --refiner "stabilityai/stable-diffusion-xl-refiner-1.0"
```

**Important**: The refiner must match your base model architecture:
- SD 1.5 base → SD 1.5 refiner
- SDXL base → SDXL refiner

The refiner applies an additional img2img pass at 30% strength to improve details and fix small artifacts.

### Negative Prompts

Specify what to avoid:

```bash
generate "a serene lake" --negative-prompt "people, buildings, cars, modern"
```

## Complex Examples

### High-Quality Anime Portrait

```bash
generate "a beautiful sorceress with flowing hair" \
  --style anime \
  --steps 50 \
  --seed 42 \
  --n 4 \
  --output ~/anime-art
```

### Sci-Fi Scene with Upscaling

```bash
generate "a futuristic cyberpunk street at night" \
  --style scifi \
  --steps 40 \
  --upscale 2 \
  --seed 9999
```

### High-Quality with Refiner

```bash
generate "a mystical forest with ancient ruins" \
  --style fantasy \
  --steps 40 \
  --refiner "runwayml/stable-diffusion-v1-5" \
  --seed 12345
```

### Maximum Quality (Refiner + Upscaler)

```bash
generate "a majestic dragon perched on a mountain" \
  --style fantasy \
  --steps 50 \
  --refiner "runwayml/stable-diffusion-v1-5" \
  --upscale 2 \
  --seed 8888
```

**Warning**: Using both refiner and upscaler significantly increases generation time and memory usage.

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

## Performance Tips

1. **Precision**: Uses float32 on MPS for stability (automatic)
2. **Attention Slicing**: Already enabled (reduces memory)
3. **Batch Size**: Larger `--n` values are more efficient than multiple runs
4. **Steps**: 20-30 steps usually sufficient; 50+ for high quality
5. **Resolution**: Default 512x512 is fastest; upscale after if needed

**Note**: The system uses float32 precision on MPS to avoid VAE decode issues that can cause NaN values and black images. This provides better stability at a slight performance cost compared to float16.

## Recommended Models

### Base Models (SD 1.5)
- **Lykon/DreamShaper-8** (default) - Great all-around quality
- **runwayml/stable-diffusion-v1-5** - Original SD 1.5
- **SG161222/Realistic_Vision_V6.0_B1_noVAE** - Photorealistic images
- **prompthero/openjourney-v4** - Midjourney-style art

### Base Models (SDXL)
- **stabilityai/stable-diffusion-xl-base-1.0** - High quality, slower
- **stablediffusionapi/newdream-sdxl-20** - Artistic SDXL

### Refiners
- **SD 1.5**: `runwayml/stable-diffusion-v1-5`
- **SDXL**: `stabilityai/stable-diffusion-xl-refiner-1.0`

### Upscalers
- **stabilityai/stable-diffusion-x4-upscaler** (auto-used with `--upscale`)

### Quick Start Examples

**Photorealistic:**
```bash
generate "professional photo of a coffee cup, studio lighting" \
  --model "SG161222/Realistic_Vision_V6.0_B1_noVAE" \
  --steps 40
```

**Artistic (Midjourney-style):**
```bash
generate "fantasy landscape, epic composition" \
  --model "prompthero/openjourney-v4" \
  --style fantasy \
  --steps 40
```

**Maximum Quality SDXL:**
```bash
generate "ultra detailed portrait of a wizard" \
  --model "stabilityai/stable-diffusion-xl-base-1.0" \
  --refiner "stabilityai/stable-diffusion-xl-refiner-1.0" \
  --steps 50
```

## System Requirements

- **Hardware**: Apple Silicon (M1, M2, M3, M4) Mac
- **OS**: macOS 12.0 or later
- **RAM**: 8GB minimum, 16GB recommended for SDXL
- **Storage**: 10GB+ for models and cache
- **Python**: 3.8 or later

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

Quality Presets (⭐ RECOMMENDED - Easy Mode):
  --quality PRESET      Auto-configure for quality level
                        Choices: fast, quality, hd, max, ultra, ultra-hd, photorealistic
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

## License

This tool uses open-source models from Hugging Face. Check individual model licenses:

- DreamShaper-8: https://huggingface.co/Lykon/DreamShaper-8
- ControlNet: https://huggingface.co/lllyasviel
- SD Upscaler: https://huggingface.co/stabilityai

## Support

For issues or questions:

1. Check this README for solutions
2. Verify system requirements
3. Check console output for specific errors
4. Review metadata JSON files for failure details

## Version

**Version**: 1.0.0  
**Date**: December 2025  
**Platform**: macOS Apple Silicon (MPS)
