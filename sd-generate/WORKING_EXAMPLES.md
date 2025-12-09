# Working Examples - Copy & Paste Ready

## ⭐ NEW: Quality Presets (Easiest Way!)

**No more compatibility worries!** Just use `--quality` presets:

### Your Cat Prompt - Now With Easy Presets!

**Fast (5-10 seconds):**
```bash
generate "(masterpiece, best quality, ultra-detailed, cinematic lighting), a cat, sharp focus, intricate details" --quality fast
```

**High Quality (30 seconds):**
```bash
generate "(masterpiece, best quality, ultra-detailed, cinematic lighting), a cat, sharp focus, intricate details" --quality max
```

**Ultra Quality SDXL (60+ seconds):**
```bash
generate "(masterpiece, best quality, ultra-detailed, cinematic lighting), a cat, sharp focus, intricate details" --quality ultra
```

**Maximum Possible Quality (90+ seconds):**
```bash
generate "(masterpiece, best quality, ultra-detailed, cinematic lighting), a cat, sharp focus, intricate details" --quality ultra-hd
```

**All presets:** `fast`, `quality`, `hd`, `max`, `ultra`, `ultra-hd`, `photorealistic`

See [QUALITY_PRESETS.md](QUALITY_PRESETS.md) for full details!

---

## Problem You Had
You tried to use the SDXL refiner with a SD 1.5 base model (DreamShaper-8), which caused a component mismatch error.

## Solution
1. **Easy way:** Use `--quality` presets (recommended!)
2. **Manual way:** The script now auto-detects SDXL models and uses the correct pipeline, but you still need to match refiner architecture to your base model.

---

## Working Commands (Manual Configuration)

### 1. Default Model (DreamShaper-8) with Compatible Refiner
```bash
generate "(masterpiece, best quality, ultra-detailed, cinematic lighting), a cat, sharp focus, intricate details, 8k ultra-resolution, hyperrealistic skin, subsurface scattering, perfect eyes with reflections, volumetric rim light, dynamic shadows, depth-of-field, bokeh, vivid color grading, highly detailed textures, beautiful composition, award-winning photo" --refiner "runwayml/stable-diffusion-v1-5"
```

### 2. Default Model with 2x Upscaler (Works!)
```bash
generate "(masterpiece, best quality, ultra-detailed, cinematic lighting), a cat, sharp focus, intricate details" --upscale 2
```

### 3. Default Model with Both Refiner AND Upscaler
```bash
generate "(masterpiece, best quality, ultra-detailed, cinematic lighting), a cat, sharp focus, intricate details" --refiner "runwayml/stable-diffusion-v1-5" --upscale 2
```

### 4. SDXL Base with SDXL Refiner (Correct Pairing)
```bash
generate "(masterpiece, best quality, ultra-detailed, cinematic lighting), a cat, sharp focus, intricate details" --model "stabilityai/stable-diffusion-xl-base-1.0" --refiner "stabilityai/stable-diffusion-xl-refiner-1.0"
```

### 5. Photorealistic Model with Refiner
```bash
generate "professional photograph of a cat, studio lighting, 8k, sharp focus" --model "SG161222/Realistic_Vision_V6.0_B1_noVAE" --refiner "runwayml/stable-diffusion-v1-5" --style realism
```

---

## Why Your Command Failed

**Your command:**
```bash
generate "..." --refiner "stabilityai/stable-diffusion-xl-refiner-1.0"
```

**Problem:** 
- Base model: DreamShaper-8 (SD 1.5 architecture)
- Refiner: SDXL architecture
- These are incompatible!

**The Fix:**
Either use a compatible SD 1.5 refiner:
```bash
--refiner "runwayml/stable-diffusion-v1-5"
```

Or switch to an SDXL base model:
```bash
--model "stabilityai/stable-diffusion-xl-base-1.0" --refiner "stabilityai/stable-diffusion-xl-refiner-1.0"
```

---

## Quick Reference Table

| Base Model | Compatible Refiner | Works? |
|------------|-------------------|--------|
| DreamShaper-8 (default) | `runwayml/stable-diffusion-v1-5` | ✅ YES |
| DreamShaper-8 (default) | `stabilityai/stable-diffusion-xl-refiner-1.0` | ❌ NO |
| `stabilityai/stable-diffusion-xl-base-1.0` | `stabilityai/stable-diffusion-xl-refiner-1.0` | ✅ YES |
| `stabilityai/stable-diffusion-xl-base-1.0` | `runwayml/stable-diffusion-v1-5` | ❌ NO |
| ANY MODEL | `--upscale 2` or `--upscale 4` | ✅ YES |

---

## Recommended Starting Point

**For best results with your cat prompt:**

```bash
generate "(masterpiece, best quality, ultra-detailed, cinematic lighting), a cat, sharp focus, intricate details, 8k ultra-resolution, hyperrealistic skin, subsurface scattering, perfect eyes with reflections, volumetric rim light, dynamic shadows, depth-of-field, bokeh, vivid color grading, highly detailed textures, beautiful composition, award-winning photo" --refiner "runwayml/stable-diffusion-v1-5" --upscale 2 --steps 40 --seed 12345
```

This will:
1. Generate with DreamShaper-8 (default)
2. Refine with a compatible SD 1.5 refiner
3. Upscale 2x for higher resolution
4. Use 40 steps for better quality

**Estimated time:** 30-60 seconds depending on your Mac
**Estimated memory:** ~10-12GB RAM

---

## Testing

Run the test script to verify everything works:
```bash
cd sd-generate
./test-refiner-upscale.sh
```

This will test all combinations and save results to `./test-outputs/`

---

## Need Help?

1. **Read:** `QUICK_REFERENCE.md` - Model compatibility guide
2. **Read:** `README.md` - Full documentation
3. **Check:** Output JSON files contain detailed error info
