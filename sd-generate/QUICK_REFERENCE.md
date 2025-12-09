# Quick Reference: Working Model Combinations

## ✅ Compatible Combinations

### SD 1.5 Base Models
**DreamShaper-8** (default):
```bash
generate "prompt" --refiner "runwayml/stable-diffusion-v1-5"
generate "prompt" --upscale 2
generate "prompt" --refiner "runwayml/stable-diffusion-v1-5" --upscale 2
```

**Realistic Vision**:
```bash
generate "prompt" --model "SG161222/Realistic_Vision_V6.0_B1_noVAE" --refiner "runwayml/stable-diffusion-v1-5"
generate "prompt" --model "SG161222/Realistic_Vision_V6.0_B1_noVAE" --upscale 4
```

### SDXL Base Models
**Stable Diffusion XL**:
```bash
generate "prompt" --model "stabilityai/stable-diffusion-xl-base-1.0" --refiner "stabilityai/stable-diffusion-xl-refiner-1.0"
generate "prompt" --model "stabilityai/stable-diffusion-xl-base-1.0" --upscale 2
```

## ❌ Incompatible Combinations (Will Fail)

**DON'T mix SD 1.5 with SDXL refiner:**
```bash
# ❌ WRONG - Will fail
generate "prompt" --refiner "stabilityai/stable-diffusion-xl-refiner-1.0"
```

**DON'T mix SDXL with SD 1.5 refiner:**
```bash
# ❌ WRONG - Will fail
generate "prompt" --model "stabilityai/stable-diffusion-xl-base-1.0" --refiner "runwayml/stable-diffusion-v1-5"
```

## Memory Considerations

| Configuration | RAM Required | Speed |
|--------------|--------------|-------|
| SD 1.5 Base | 6GB | Fast |
| SD 1.5 + Refiner | 8GB | Medium |
| SD 1.5 + Upscale 2x | 10GB | Medium |
| SD 1.5 + Upscale 4x | 12GB | Slow |
| SDXL Base | 12GB | Slow |
| SDXL + Refiner | 16GB+ | Very Slow |

## Recommended Workflows

### Quick Generation (8GB RAM)
```bash
generate "a beautiful landscape" --steps 30
```

### High Quality (16GB RAM)
```bash
generate "a beautiful landscape" --steps 50 --refiner "runwayml/stable-diffusion-v1-5"
```

### Maximum Quality (16GB+ RAM)
```bash
generate "a beautiful landscape" --steps 50 --refiner "runwayml/stable-diffusion-v1-5" --upscale 2
```

### Photorealistic (16GB RAM)
```bash
generate "professional photo of a mountain lake" \
  --model "SG161222/Realistic_Vision_V6.0_B1_noVAE" \
  --steps 40 \
  --refiner "runwayml/stable-diffusion-v1-5" \
  --style realism
```

### Ultra High-Res (16GB+ RAM, Slow)
```bash
generate "detailed fantasy scene" \
  --model "stabilityai/stable-diffusion-xl-base-1.0" \
  --refiner "stabilityai/stable-diffusion-xl-refiner-1.0" \
  --steps 50
```

## Tips

1. **Upscaler works with everything**: The upscaler (`--upscale`) works with any base model
2. **Refiner must match**: SD 1.5 base needs SD 1.5 refiner, SDXL base needs SDXL refiner
3. **Start simple**: Test without refiner/upscaler first, then add them if needed
4. **Memory errors**: If you get OOM errors, remove upscaler first, then refiner
5. **Speed vs Quality**: More steps = better quality but slower (30-50 is good range)

## Error Messages

**"Pipeline expected [...] but only {...} were passed"**
- You're using an incompatible refiner
- Solution: Match refiner architecture to base model

**"MPS backend out of memory"**
- Not enough RAM
- Solution: Remove `--upscale` or reduce `--n` count

**"CUDA is not available"**
- This is just a warning, ignore it
- The script uses MPS (Apple Silicon) not CUDA

## Command Templates

Copy and modify these:

```bash
# Template: Basic
generate "YOUR_PROMPT" --steps 30 --seed 42

# Template: With Style
generate "YOUR_PROMPT" --style anime --steps 40 --n 4

# Template: High Quality SD 1.5
generate "YOUR_PROMPT" \
  --steps 50 \
  --refiner "runwayml/stable-diffusion-v1-5" \
  --seed 42

# Template: High Quality SDXL
generate "YOUR_PROMPT" \
  --model "stabilityai/stable-diffusion-xl-base-1.0" \
  --refiner "stabilityai/stable-diffusion-xl-refiner-1.0" \
  --steps 50 \
  --seed 42

# Template: Maximum Quality with Upscale
generate "YOUR_PROMPT" \
  --steps 50 \
  --refiner "runwayml/stable-diffusion-v1-5" \
  --upscale 2 \
  --seed 42
```
