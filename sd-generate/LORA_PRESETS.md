# LoRA Support 🎨

## Manual LoRA Usage

The system supports **manual LoRA loading** with the `--lora` flag:

```bash
# With a local LoRA file
generate "prompt" --lora ./path/to/lora.safetensors

# With Hugging Face LoRA
generate "prompt" --lora "username/lora-repo"
```

---

## Quality Presets (No Auto-LoRA)

The `ultra-realistic` and `cinematic` presets do **NOT** automatically load LoRAs. They simply use higher steps for better quality:

### `ultra-realistic` Preset
```bash
generate "detailed portrait" --quality ultra-realistic
```

**What it does:**
- Model: SD 1.5 (DreamShaper-8)
- Steps: 60 (extra high)
- Refiner: Yes
- Upscale: 2x
- Time: ~25s

**Note:** Name is for clarity - it uses extra steps, not auto-LoRA

### `cinematic` Preset
```bash
generate "movie scene" --quality cinematic
```

**What it does:**
- Model: SD 1.5 (DreamShaper-8)
- Steps: 60 (extra high)
- Refiner: Yes
- Upscale: 2x
- Time: ~24s

**Note:** Use with `--style` for cinematic effects

---

## Manual LoRA Examples

### With Local File
```bash
generate "your prompt" \
  --lora "./loras/detail-enhancer.safetensors" \
  --quality max
```

### With Hugging Face Repo
```bash
generate "your prompt" \
  --lora "ostris/detail-lora" \
  --quality max
```

### Combined with Styles
```bash
generate "anime character" \
  --lora "./anime-style.safetensors" \
  --style anime \
  --quality max
```

---

## Finding LoRAs

### CivitAI
1. Go to https://civitai.com
2. Search for LoRAs
3. Download `.safetensors` files
4. Use with `--lora` flag

### Hugging Face
1. Search for "lora" models
2. Use repo name with `--lora`
3. Example: `--lora "username/lora-name"`

---

## LoRA Tips

1. **SD 1.5 LoRAs** work with SD 1.5 models
2. **SDXL LoRAs** work with SDXL models
3. **Check compatibility** before downloading
4. **Start subtle** - LoRAs work best with refiners
5. **Combine carefully** - Not all LoRAs work together

---

## Presets Summary

| Preset | Auto-LoRA | Extra Steps | Best For |
|--------|-----------|-------------|----------|
| ultra-realistic | ❌ No | ✅ Yes (60) | High detail |
| cinematic | ❌ No | ✅ Yes (60) | Movie scenes |

Both presets use **extra inference steps** instead of LoRAs for higher quality.

---

## Why No Auto-LoRA?

- LoRAs require specific files to be downloaded
- Different users want different LoRAs
- Manual control gives more flexibility
- Presets focus on proven settings (steps, refiner, upscale)

---

## Recommended Workflow

**1. Start without LoRA:**
```bash
generate "your prompt" --quality max
```

**2. If you want more detail, try ultra-realistic:**
```bash
generate "your prompt" --quality ultra-realistic
```

**3. If you have a LoRA, add it manually:**
```bash
generate "your prompt" --quality max --lora "./your-lora.safetensors"
```

---

## All Quality Presets

### Standard (No LoRA)
- `fast` - Quick (10s)
- `quality` - + Refiner (18s)
- `hd` - + 2x upscale (20s)
- `max` - + Refiner + 2x (30s)
- `4k` - + Refiner + 4x (21s)

### High Steps (No LoRA)
- `ultra-realistic` - 60 steps + refiner + 2x
- `cinematic` - 60 steps + refiner + 2x

### SDXL (No LoRA)
- `ultra` - SDXL + refiner (170s)
- `ultra-hd` - SDXL + refiner + 2x (180s)
- `4k-ultra` - SDXL + refiner + 4x (240s)

### Specialized
- `photorealistic` - Realistic model + refiner + 2x

---

## Summary

✅ **Manual LoRA support** - Use `--lora` flag  
✅ **Presets work without LoRAs** - Based on proven settings  
✅ **Flexible** - Add LoRAs to any preset  
✅ **Simple** - No automatic downloads needed  

**Use LoRAs manually for full control!**
