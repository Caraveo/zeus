# 4K Support Added! 🎨✨

## New Quality Presets

### 🎯 Standard Presets
| Preset | Resolution | Time | File Size | Use Case |
|--------|-----------|------|-----------|----------|
| `fast` | 512x512 | ~10s | ~300KB | Quick tests |
| `quality` | 512x512 | ~20s | ~400KB | High quality |
| `hd` | 1024x1024 | ~20s | ~1.4MB | Large prints |
| `max` | 1024x1024 | ~30s | ~1.4MB | Best SD 1.5 |

### 🚀 4K Presets (NEW!)
| Preset | Resolution | Time | File Size | Use Case |
|--------|-----------|------|-----------|----------|
| `4k` | 2048x2048 | ~21s | ~3.9MB | 4K displays |
| `4k-ultra` | 4096x4096 | ~200s | ~15MB | Print quality |
| `ultra-hd` | 2048x2048 | ~180s | ~4MB | SDXL 4K |

## Usage Examples

### 4K with SD 1.5 (Fast!)
```bash
generate "majestic mountain landscape" --quality 4k
```
- Resolution: 2048x2048
- Time: ~21 seconds
- Model: SD 1.5 + refiner
- Output: 3.9MB file

### 4K Ultra with SDXL (Best Quality!)
```bash
generate "majestic mountain landscape" --quality 4k-ultra
```
- Resolution: 4096x4096
- Time: ~3-4 minutes
- Model: SDXL + refiner
- Output: ~15MB file

### Ultra-HD SDXL
```bash
generate "portrait of a wizard" --quality ultra-hd
```
- Resolution: 2048x2048
- Time: ~3 minutes
- Model: SDXL + refiner
- Output: ~4MB file

## Resolution Comparison

| Preset | Size | Pixels | Aspect | Best For |
|--------|------|--------|--------|----------|
| `fast` | 512x512 | 262K | 1:1 | Testing |
| `hd` | 1024x1024 | 1.0M | 1:1 | HD displays |
| `4k` | 2048x2048 | 4.2M | 1:1 | 4K displays |
| `4k-ultra` | 4096x4096 | 16.8M | 1:1 | Large prints |

## Speed vs Quality

### Fast 4K (Recommended!)
```bash
generate "prompt" --quality 4k
```
✅ Fast (~21s)
✅ High quality with refiner
✅ 2048x2048 resolution
✅ 3.9MB file
✅ Perfect for 4K displays

### Ultimate 4K (Best Quality)
```bash
generate "prompt" --quality 4k-ultra
```
⚡ Slower (~3-4 min)
⭐ SDXL model
⭐ SDXL refiner
⭐ 4096x4096 resolution
⭐ ~15MB file
⭐ Perfect for printing

## Manual Upscaling

You can also manually specify upscale factor:

```bash
# 2x upscale (1024x1024)
generate "prompt" --upscale 2

# 4x upscale (2048x2048)
generate "prompt" --upscale 4

# With refiner
generate "prompt" --refiner "runwayml/stable-diffusion-v1-5" --upscale 4
```

## Performance Tips

### For Fast 4K
Use `--quality 4k`:
- SD 1.5 model (fast)
- Refiner (quality boost)
- 4x upscale (2048px)
- Total: ~21 seconds

### For Best 4K
Use `--quality 4k-ultra`:
- SDXL model (best)
- SDXL refiner (details)
- 4x upscale (4096px)
- Total: ~3-4 minutes

### For Balanced
Use `--quality ultra-hd`:
- SDXL model
- SDXL refiner
- 2x upscale (2048px)
- Total: ~3 minutes

## Test Results

### 4K Preset Test
**Command:**
```bash
generate "majestic mountain landscape" --quality 4k --seed 300
```

**Results:**
- ✅ Generation: 14.5s
- ✅ Refiner: 2.0s
- ✅ Upscale: 0.5s
- ✅ **Total: 21.0s**
- ✅ Resolution: **2048x2048**
- ✅ File size: **3.9MB**
- ✅ Quality: Excellent

## All Available Presets

```bash
# Quick tests
generate "prompt" --quality fast         # 512px, ~10s

# Standard quality
generate "prompt" --quality quality      # 512px + refiner, ~20s

# HD quality
generate "prompt" --quality hd           # 1024px, ~20s
generate "prompt" --quality max          # 1024px + refiner, ~30s

# 4K quality (NEW!)
generate "prompt" --quality 4k           # 2048px + refiner, ~21s ⭐

# Ultra quality
generate "prompt" --quality ultra        # SDXL, ~180s
generate "prompt" --quality ultra-hd     # SDXL 2048px, ~180s
generate "prompt" --quality 4k-ultra     # SDXL 4096px, ~240s

# Specialized
generate "prompt" --quality photorealistic  # Realistic model + refiner
```

## Recommended Workflow

1. **Test prompt** with `--quality fast` (~10s)
2. **Refine concept** with `--quality quality` (~20s)
3. **Final 4K render** with `--quality 4k` (~21s)
4. **Print quality** with `--quality 4k-ultra` if needed (~240s)

## Examples

### Landscape Photography
```bash
generate "sunset over mountain lake, cinematic" \
  --quality 4k \
  --style realism \
  --seed 42
```

### Character Art
```bash
generate "epic fantasy warrior, detailed armor" \
  --quality 4k \
  --style fantasy \
  --n 4
```

### Abstract Art
```bash
generate "colorful abstract geometric patterns" \
  --quality 4k \
  --seed 12345
```

### Portrait
```bash
generate "professional portrait, studio lighting" \
  --quality 4k \
  --style realism
```

## Summary

✅ **4K support added** - 2048x2048 and 4096x4096 resolutions
✅ **Fast generation** - 4K in ~21 seconds
✅ **High quality** - Includes refiner
✅ **Three 4K options** - 4k, ultra-hd, 4k-ultra
✅ **Easy to use** - Single `--quality` flag

**Start creating 4K images now!**

```bash
generate "your amazing idea" --quality 4k
```
