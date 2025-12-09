# Quality Presets - Easy Mode! 🚀

The `--quality` flag automatically configures the perfect combination of model, refiner, and upscaler for your needs.

**No more worrying about compatibility!** Just pick a quality level.

---

## Quick Start

```bash
# Simple generation
generate "a beautiful cat"

# High quality version
generate "a beautiful cat" --quality max

# Photorealistic version
generate "a beautiful cat" --quality photorealistic
```

---

## Available Presets

### 1. `--quality fast` ⚡
**Speed-optimized, good quality**

```bash
generate "a dragon flying over mountains" --quality fast
```

- **Model:** SD 1.5 (DreamShaper-8)
- **Steps:** 25
- **Refiner:** None
- **Upscale:** None
- **Time:** ~5-10 seconds
- **RAM:** 6-8GB
- **Best for:** Quick iterations, testing prompts

---

### 2. `--quality quality` ✨
**High quality with refiner**

```bash
generate "a mystical forest at sunset" --quality quality
```

- **Model:** SD 1.5 (DreamShaper-8)
- **Steps:** 40
- **Refiner:** SD 1.5 refiner
- **Upscale:** None
- **Time:** ~15-20 seconds
- **RAM:** 8-10GB
- **Best for:** Good quality without upscaling

---

### 3. `--quality hd` 📺
**High resolution with 2x upscaling**

```bash
generate "a detailed steampunk robot" --quality hd
```

- **Model:** SD 1.5 (DreamShaper-8)
- **Steps:** 40
- **Refiner:** None
- **Upscale:** 2x
- **Time:** ~20-25 seconds
- **RAM:** 10-12GB
- **Best for:** Larger images, more detail

---

### 4. `--quality max` 🔥
**Maximum quality - refiner AND upscaler**

```bash
generate "an epic fantasy battle scene" --quality max
```

- **Model:** SD 1.5 (DreamShaper-8)
- **Steps:** 50
- **Refiner:** SD 1.5 refiner
- **Upscale:** 2x
- **Time:** ~30-40 seconds
- **RAM:** 12-14GB
- **Best for:** Final renders, portfolio pieces

---

### 5. `--quality ultra` 🌟
**Ultra quality with SDXL (slower)**

```bash
generate "a hyper-detailed portrait" --quality ultra
```

- **Model:** Stable Diffusion XL
- **Steps:** 50
- **Refiner:** SDXL refiner
- **Upscale:** None
- **Time:** ~60-90 seconds
- **RAM:** 14-16GB
- **Best for:** When you need the absolute best quality

---

### 6. `--quality ultra-hd` 💎
**Ultra HD - SDXL with upscaling (slowest)**

```bash
generate "a cinematic landscape masterpiece" --quality ultra-hd
```

- **Model:** Stable Diffusion XL
- **Steps:** 50
- **Refiner:** SDXL refiner
- **Upscale:** 2x
- **Time:** ~90-120 seconds
- **RAM:** 16GB+
- **Best for:** Print quality, large displays

---

### 7. `--quality photorealistic` 📸
**Photorealistic specialized model**

```bash
generate "professional photograph of a mountain lake" --quality photorealistic
```

- **Model:** Realistic Vision V6
- **Steps:** 45
- **Refiner:** SD 1.5 refiner
- **Upscale:** 2x
- **Time:** ~35-45 seconds
- **RAM:** 12-14GB
- **Best for:** Photo-realistic images, portraits, nature

---

## Comparison Table

| Preset | Speed | Quality | RAM | Resolution | Best Use Case |
|--------|-------|---------|-----|------------|---------------|
| `fast` | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | 6-8GB | Standard | Testing, iterations |
| `quality` | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | 8-10GB | Standard | Good quality, no upscale |
| `hd` | ⚡⚡⚡ | ⭐⭐⭐⭐ | 10-12GB | 2x | Larger images |
| `max` | ⚡⚡ | ⭐⭐⭐⭐⭐ | 12-14GB | 2x | Best SD 1.5 quality |
| `ultra` | ⚡ | ⭐⭐⭐⭐⭐ | 14-16GB | Standard | SDXL quality |
| `ultra-hd` | 💤 | ⭐⭐⭐⭐⭐ | 16GB+ | 2x | Maximum possible |
| `photorealistic` | ⚡⚡ | ⭐⭐⭐⭐⭐ | 12-14GB | 2x | Photos only |

---

## Real World Examples

### Character Design (Anime)
```bash
generate "anime girl with blue hair, magical powers, detailed" \
  --quality max \
  --style anime \
  --n 6
```

### Landscape Art
```bash
generate "epic mountain landscape at golden hour, cinematic" \
  --quality ultra \
  --style fantasy
```

### Portrait Photography
```bash
generate "professional headshot, studio lighting, sharp focus" \
  --quality photorealistic
```

### Concept Art (Fast Iteration)
```bash
generate "sci-fi spaceship design, multiple angles" \
  --quality fast \
  --n 10 \
  --style scifi
```

### Final Render (Maximum Quality)
```bash
generate "a dragon perched on ancient ruins, cinematic lighting, highly detailed" \
  --quality ultra-hd \
  --style fantasy \
  --steps 60
```

---

## Combining with Other Options

Quality presets work with all other options:

### Custom Style
```bash
generate "a warrior" --quality max --style fantasy
```

### Multiple Images
```bash
generate "character concepts" --quality quality --n 8
```

### Custom Seed for Consistency
```bash
generate "character design" --quality max --seed 12345
```

### Custom Steps (Override Preset)
```bash
generate "quick test" --quality max --steps 20
```

### Negative Prompts
```bash
generate "a serene lake" \
  --quality photorealistic \
  --negative-prompt "people, buildings, modern"
```

---

## How Presets Work

When you use `--quality`, the script automatically:

1. ✅ Selects the right base model
2. ✅ Chooses compatible refiner (if any)
3. ✅ Configures upscaling (if any)
4. ✅ Sets optimal inference steps
5. ✅ Ensures everything is compatible

**You can still override any setting:**

```bash
# Use 'max' preset but with custom model
generate "prompt" --quality max --model "path/to/my/model"

# Use 'ultra' preset but with different steps
generate "prompt" --quality ultra --steps 80
```

---

## Decision Guide

**Choose your preset based on:**

### 🎯 I need it FAST
→ `--quality fast`

### 🎨 I want good quality, reasonable speed
→ `--quality quality` or `--quality hd`

### 🏆 I want the BEST SD 1.5 can offer
→ `--quality max`

### 🚀 I want ULTIMATE quality (have time & RAM)
→ `--quality ultra` or `--quality ultra-hd`

### 📸 I specifically need photorealism
→ `--quality photorealistic`

---

## Memory Issues?

If you get "out of memory" errors:

1. **Drop from ultra → max**
2. **Drop from max → quality**
3. **Drop from quality → fast**
4. **Reduce --n** (number of images)

---

## Tips

1. **Start with `--quality fast`** to test your prompt
2. **Use `--quality max`** for most final renders (best balance)
3. **Use `--quality ultra`** only when SD 1.5 isn't enough
4. **Use `--quality photorealistic`** for photos, not art
5. **Combine with `--style`** for even better results

---

## Before and After

**Without preset (manual):**
```bash
generate "a cat" \
  --model "Lykon/DreamShaper-8" \
  --refiner "runwayml/stable-diffusion-v1-5" \
  --upscale 2 \
  --steps 50
```

**With preset (easy):**
```bash
generate "a cat" --quality max
```

**Same result, 80% less typing!** 🎉

---

## No Preset = Fast Mode

If you don't specify `--quality`, you get:
- Model: DreamShaper-8
- Steps: 30
- No refiner
- No upscaling

This is equivalent to `--quality fast` but slightly slower (30 steps vs 25).
