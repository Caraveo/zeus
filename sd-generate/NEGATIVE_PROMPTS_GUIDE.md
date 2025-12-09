# Negative Prompts Guide 🚫

## What are Negative Prompts?

**Negative prompts** tell the AI what to **avoid** in the generated image.

- ✅ Improve image quality
- ✅ Remove unwanted elements
- ✅ Fix common issues (hands, faces, artifacts)
- ✅ Control style better

---

## Basic Usage

```bash
generate "your prompt" --negative-prompt "things to avoid"
```

### Example
```bash
generate "beautiful portrait of a woman" \
  --negative-prompt "ugly, deformed, blurry, low quality"
```

---

## Common Negative Prompts

### For Portraits
```bash
--negative-prompt "ugly, deformed, blurry, bad anatomy, bad hands, missing fingers, extra fingers, poorly drawn hands, poorly drawn face, mutation, mutated, extra limbs, bad proportions"
```

### For Photorealism
```bash
--negative-prompt "cartoon, anime, painting, drawing, illustration, low quality, blurry, watermark, text, signature"
```

### For Anime/Art
```bash
--negative-prompt "photo, photorealistic, 3d render, ugly, blurry, low quality, watermark, signature, text"
```

### For Landscapes
```bash
--negative-prompt "people, person, human, face, portrait, text, watermark, low quality, blurry"
```

### For Fantasy Art
```bash
--negative-prompt "modern, mundane, photograph, low quality, blurry, watermark, ugly"
```

---

## Examples with Quality Presets

### High Quality Portrait
```bash
generate "professional portrait, studio lighting" \
  --quality 4k \
  --negative-prompt "ugly, deformed, blurry, bad hands, bad face"
```

### Landscape Photography
```bash
generate "mountain lake at sunset, dramatic sky" \
  --quality 4k \
  --style realism \
  --negative-prompt "people, buildings, text, watermark"
```

### Anime Character
```bash
generate "anime girl with blue hair" \
  --quality max \
  --style anime \
  --negative-prompt "photo, 3d, ugly, low quality, text"
```

### Fantasy Scene
```bash
generate "dragon in magical forest" \
  --quality 4k \
  --style fantasy \
  --negative-prompt "modern, mundane, ugly, blurry"
```

---

## Tested Example

**Command:**
```bash
generate "beautiful portrait of a woman" \
  --negative-prompt "ugly, deformed, blurry, low quality, bad hands, bad anatomy" \
  --quality quality \
  --seed 123
```

**Results:**
- ✅ Time: 21.1 seconds
- ✅ Quality: Improved (no deformities)
- ✅ Negative prompt applied successfully
- ✅ Better overall composition

**Metadata shows:**
```json
{
  "prompt": "beautiful portrait of a woman",
  "negative_prompt": "ugly, deformed, blurry, low quality, bad hands, bad anatomy",
  "quality_preset": "quality"
}
```

---

## Tips for Good Negative Prompts

### 1. Be Specific
```bash
# Good
--negative-prompt "bad hands, missing fingers, extra fingers"

# Too vague
--negative-prompt "bad"
```

### 2. Address Common Issues
Common problems to negate:
- `bad hands, bad anatomy`
- `blurry, low quality`
- `deformed, mutation`
- `watermark, text, signature`
- `extra limbs, extra fingers`

### 3. Match Your Goal
For photorealism, avoid:
- `cartoon, anime, painting, drawing`

For anime, avoid:
- `photo, photorealistic, 3d`

### 4. Don't Overdo It
```bash
# Good (focused)
--negative-prompt "blurry, low quality, deformed"

# Bad (too long, conflicting)
--negative-prompt "blurry, sharp, ugly, beautiful, dark, bright, ..."
```

---

## Negative Prompt Templates

### Universal Quality Improver
```bash
--negative-prompt "low quality, blurry, ugly, deformed, bad anatomy"
```

### No Text/Watermarks
```bash
--negative-prompt "text, watermark, signature, logo, letters, words"
```

### No People (for landscapes)
```bash
--negative-prompt "people, person, human, face, portrait"
```

### No Modern Elements (for fantasy)
```bash
--negative-prompt "modern, contemporary, urban, cars, technology"
```

### Fix Common AI Issues
```bash
--negative-prompt "bad hands, bad anatomy, mutation, extra limbs, missing limbs, floating limbs, poorly drawn hands, poorly drawn face"
```

---

## Combining with Styles

Style presets already include negative prompts! But you can override:

### Anime Style (Built-in Negative)
```bash
generate "anime girl" --style anime
# Auto-adds: "photo, photorealistic, 3d render, ugly, blurry, low quality"
```

### Override Style Negative
```bash
generate "anime girl" \
  --style anime \
  --negative-prompt "your custom negative prompt"
# Your custom negative replaces the style default
```

### Add to Style Negative
Use both by not using `--negative-prompt` flag

---

## Real World Examples

### Portrait Photography
```bash
generate "professional headshot, studio lighting, sharp focus" \
  --quality photorealistic \
  --negative-prompt "blurry, low quality, bad face, bad eyes, deformed, ugly, bad hands"
```

### Fantasy Landscape
```bash
generate "epic fantasy castle on mountain, dramatic clouds" \
  --quality 4k \
  --style fantasy \
  --negative-prompt "modern, people, cars, text, low quality"
```

### Cinematic Scene
```bash
generate "detective in rain, film noir, dramatic lighting" \
  --quality cinematic \
  --negative-prompt "bright, colorful, cheerful, low quality, blurry"
```

### Product Photo
```bash
generate "luxury watch on marble surface, studio lighting" \
  --quality 4k \
  --negative-prompt "people, hands, low quality, blurry, distorted, text"
```

---

## Quick Reference

| Goal | Negative Prompt |
|------|-----------------|
| Better quality | `low quality, blurry, ugly` |
| Fix anatomy | `bad hands, bad anatomy, deformed` |
| No watermarks | `text, watermark, signature, logo` |
| No people | `people, person, human, face` |
| Photorealistic | `cartoon, anime, painting, drawing` |
| Anime/Art | `photo, photorealistic, 3d` |
| Clean | `artifacts, noise, grain` |

---

## Testing Negative Prompts

### Without Negative Prompt
```bash
generate "portrait" --quality quality --seed 123
```

### With Negative Prompt
```bash
generate "portrait" \
  --quality quality \
  --seed 123 \
  --negative-prompt "ugly, blurry, deformed"
```

Use the **same seed** to see the difference!

---

## Advanced Tips

### 1. Stack Negatives
```bash
--negative-prompt "low quality, blurry, ugly, deformed, bad anatomy, bad hands, text, watermark"
```

### 2. Genre-Specific
For anime:
```bash
--negative-prompt "photo, photorealistic, 3d render, western cartoon"
```

For photos:
```bash
--negative-prompt "anime, cartoon, painting, drawing, illustration"
```

### 3. Problem-Solving
If you get bad hands:
```bash
--negative-prompt "bad hands, missing fingers, extra fingers, fused fingers, malformed hands"
```

If faces look weird:
```bash
--negative-prompt "bad face, ugly face, asymmetric face, poorly drawn face, mutation"
```

---

## All Commands with Negative Prompts

### Fast Test
```bash
generate "test" --quality lcm --negative-prompt "ugly, blurry"
```

### High Quality
```bash
generate "portrait" --quality 4k --negative-prompt "deformed, ugly"
```

### SDXL
```bash
generate "landscape" --quality ultra --negative-prompt "people, text"
```

### With Everything
```bash
generate "epic dragon battle" \
  --quality 4k-ultra \
  --style fantasy \
  --negative-prompt "modern, ugly, low quality" \
  --seed 42 \
  --n 4
```

---

## Summary

✅ **Easy to use** - Just add `--negative-prompt "text"`  
✅ **Improves quality** - Removes unwanted elements  
✅ **Works with all presets** - Combine freely  
✅ **Tested and working** - Portrait test passed  

**Use negative prompts to take control of your generations!**

```bash
generate "your prompt" \
  --quality 4k \
  --negative-prompt "ugly, blurry, low quality"
```
