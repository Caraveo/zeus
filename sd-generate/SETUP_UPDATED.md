# setup.sh Updated for v2.1.1

## Summary

The setup.sh script has been updated to reflect the new SD 3.5 Large Turbo support and improved features in v2.1.1.

---

## Changes Made

### 1. Version Number
```bash
# Old
SD-Generate Setup v2.1 (MPS/Apple Silicon)

# New
SD-Generate Setup v2.1.1 (MPS/Apple Silicon)
```

### 2. Features List
**Added highlights:**
- SD 3.5 Large Turbo (--pro flag, 8 steps, 2-5 min)
- Updated from "SD 3.5" to "SD 3.5 Turbo"
- Expanded memory management details
- Added speed benefits (4-6x faster)
- Added RAM requirements (20GB+ vs 36GB+)

### 3. Pro Mode Section
**Old:**
```bash
Pro mode (SD 3.5 - Requires auth + 36GB RAM + Max/Ultra chip):
  generate "dragon" --pro    # Best quality (5-20min)
  Note: Requires ./login-hf.sh first + 36GB+ RAM
```

**New:**
```bash
Pro mode (SD 3.5 Large Turbo - NEW! Much faster!):
  generate "dragon" --pro    # Best quality (2-5min)
  Note: Requires ./login-hf.sh + 20GB+ RAM (works on all Apple Silicon)
  Model: stabilityai/stable-diffusion-3.5-large-turbo
  Steps: 8 (optimized for turbo model)
```

### 4. Documentation List
**Updated from 18 to 20 guides:**
- Added: PRO_MODE_UPDATE.md
- Added: CHANGES_V2.1.md
- Reordered for better organization

### 5. Final Setup Message
**Old:**
```bash
For SD 3.5 (best quality, requires auth + 36GB RAM + Max/Ultra chip):
  1. Accept license: https://huggingface.co/stabilityai/stable-diffusion-3.5-large
  2. Run: ./login-hf.sh
  3. Generate: generate "prompt" --model "stabilityai/stable-diffusion-3.5-large"
```

**New:**
```bash
For SD 3.5 Large Turbo (best quality, fast, NEW!):
  1. Accept license: https://huggingface.co/stabilityai/stable-diffusion-3.5-large-turbo
  2. Run: ./login-hf.sh (if not already authenticated)
  3. Generate: generate "prompt" --pro

The --pro flag now uses:
  • Model: stabilityai/stable-diffusion-3.5-large-turbo
  • Steps: 8 (optimized for turbo)
  • Time: 2-5 min (vs 15-20 min for regular SD 3.5)
  • RAM: 20GB+ (works on all Apple Silicon)

See PRO_MODE_UPDATE.md for complete guide.
```

---

## What Users Will See

When running `./setup.sh`, users will see:

```
======================================================================
  SD-Generate Setup v2.1.1 (MPS/Apple Silicon)
======================================================================

Features:
  • SD 3.5 Large Turbo (--pro flag, 8 steps, 2-5 min)
  • Advanced memory management for SD 3.5
  • 12 quality presets (lcm → 4k-ultra)
  • SD 1.5 + SDXL + SD 3.5 Turbo support
  • LCM LoRA (3 second generation)
  • 4K upscaling (2048px & 4096px)
  • Auto-compatible refiners
  • Gated model support (SD 3.5 Turbo)
  • Style presets + ControlNet ready
```

And at the end:

```
Features available:
  • SD 3.5 Large Turbo with --pro flag (NEW!)
    - 4-6x faster than SD 3.5 Large (2-5 min vs 15-20 min)
    - Only 8 steps needed for excellent quality
    - Works on all Apple Silicon (20GB+ RAM)
  • Advanced memory management for SD 3.5
    - Aggressive cleanup between stages
    - Real-time memory monitoring
    - Pipeline unloading before refiner
    - Attention & VAE slicing
  [... other features ...]
```

---

## Key Messages Updated

### Speed Improvement
- **Old:** 5-20 minutes
- **New:** 2-5 minutes (4-6x faster)

### RAM Requirements
- **Old:** 36GB+ (Max/Ultra only)
- **New:** 20GB+ (all Apple Silicon)

### Model Name
- **Old:** stabilityai/stable-diffusion-3.5-large
- **New:** stabilityai/stable-diffusion-3.5-large-turbo

### Steps
- **Old:** 28 steps
- **New:** 8 steps

---

## Benefits Highlighted

The setup script now emphasizes:

1. ⚡ **Speed**: 4-6x faster generation
2. 💻 **Compatibility**: Works on all Apple Silicon (not just Max/Ultra)
3. 💾 **Memory**: Lower RAM requirement (20GB vs 36GB)
4. 🎯 **Simplicity**: Just use `--pro` flag
5. 📚 **Documentation**: 20 comprehensive guides

---

## Running the Updated Setup

### New Installation
```bash
cd sd-generate
./setup.sh
```

### Updating Existing Installation
```bash
cd sd-generate
./setup.sh
```

The setup script will:
1. Install/update all dependencies (including psutil)
2. Configure MPS environment
3. Run validation tests
4. Show updated usage instructions

---

## Post-Setup Instructions

After running setup, users are guided to:

1. **Accept SD 3.5 Large Turbo license** (one-time):
   https://huggingface.co/stabilityai/stable-diffusion-3.5-large-turbo

2. **Authenticate** (if needed):
   ```bash
   ./login-hf.sh
   ```

3. **Start generating**:
   ```bash
   generate "your prompt" --pro
   ```

---

## Dependencies

Setup now installs:
- PyTorch with MPS support
- diffusers, transformers, accelerate
- safetensors, pillow, sentencepiece
- opencv-python, datasets
- huggingface_hub, peft
- protobuf (for SD 3.5)
- **psutil** (for memory management)

---

## Validation Tests

Setup runs 3 validation tests:
1. Basic image generation (10 steps)
2. Style preset test (anime style, 10 steps)
3. Multiple images test (2 images, 5 steps)

All tests use SD 1.5 (fast) to verify installation.

---

## Version History

- **v2.0.0**: Initial stable release
- **v2.1.0**: Added memory management for SD 3.5
- **v2.1.1**: Updated to SD 3.5 Large Turbo (this update)

---

## Complete Feature List

Setup configures:

✅ **Models:**
- SD 1.5 (DreamShaper-8, Realistic Vision)
- SDXL (base + refiner)
- SD 3.5 Large Turbo (--pro flag)

✅ **Quality Presets:**
- lcm (3s), fast (10s), quality (18s)
- hd (20s), max (30s), 4k (21s)
- ultra (3min), ultra-hd (3min), 4k-ultra (3min)
- photorealistic, ultra-realistic, cinematic
- sd3.5, sd3.5-4k (with turbo model)

✅ **Features:**
- 4K upscaling (2x, 4x)
- LCM LoRA support
- Style presets (4 styles)
- ControlNet ready
- Negative prompts
- Memory management
- Crash recovery
- Real-time monitoring

---

## File Location

**Path:** `/Users/caraveo/Projects/Zues/sd-generate/setup.sh`
**Lines:** 789
**Version:** 2.1.1

---

## Summary

The setup.sh now properly reflects:
- ✅ SD 3.5 Large Turbo as default for --pro
- ✅ Faster generation times (2-5 min)
- ✅ Lower requirements (20GB RAM)
- ✅ All Apple Silicon support
- ✅ Updated documentation (20 guides)
- ✅ Clear usage instructions

**Users get the best experience right from setup!** 🚀
