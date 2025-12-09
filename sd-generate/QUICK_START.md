# Quick Start Guide 🚀

## Installation

```bash
cd sd-generate
./setup.sh
```

**That's it!** Setup takes ~5 minutes.

---

## First Test

```bash
generate "a beautiful sunset" --quality lcm
```

Should complete in ~3 seconds! ⚡

---

## All 12 Quality Presets

### Ultra Fast
```bash
generate "prompt" --quality lcm              # 3s ⚡⚡⚡⚡⚡
```

### Fast  
```bash
generate "prompt" --quality fast             # 10s ⚡⚡⚡⚡
generate "prompt" --quality quality          # 18s ⚡⚡⚡
```

### HD
```bash
generate "prompt" --quality hd               # 20s, 1024px
generate "prompt" --quality max              # 30s, 1024px + refiner
```

### 4K ⭐ RECOMMENDED
```bash
generate "prompt" --quality 4k               # 21s, 2048px
```

### Ultra (SDXL)
```bash
generate "prompt" --quality ultra            # 3min, SDXL
generate "prompt" --quality ultra-hd         # 3min, SDXL 2048px
generate "prompt" --quality 4k-ultra         # 3min, SDXL 4096px
```

### Specialized
```bash
generate "prompt" --quality photorealistic   # Photo model
generate "prompt" --quality ultra-realistic  # High detail (60 steps)
generate "prompt" --quality cinematic        # Movie style (60 steps)
```

---

## Common Options

### Multiple Images
```bash
generate "character concepts" --quality lcm --n 20
```

### With Style
```bash
generate "anime warrior" --quality 4k --style anime
```

### With Negative Prompt
```bash
generate "portrait" --quality 4k \
  --negative-prompt "ugly, blurry, deformed"
```

### Custom Seed (reproducible)
```bash
generate "landscape" --quality 4k --seed 42
```

### Everything Combined
```bash
generate "epic fantasy battle scene" \
  --quality 4k-ultra \
  --style fantasy \
  --negative-prompt "modern, ugly, low quality" \
  --seed 12345 \
  --n 4
```

---

## Tested & Working

| Feature | Status | Example |
|---------|--------|---------|
| LCM LoRA | ✅ | `--quality lcm` |
| SD 1.5 | ✅ | `--quality fast` |
| SDXL | ✅ | `--quality ultra` |
| Refiners | ✅ | `--quality quality` |
| 4K (2048px) | ✅ | `--quality 4k` |
| 4K (4096px) | ✅ | `--quality 4k-ultra` |
| Upscaling | ✅ | `--upscale 2` or `4` |
| Styles | ✅ | `--style anime` |
| Negative | ✅ | `--negative-prompt "text"` |
| LoRA | ✅ | `--lora path.safetensors` |

---

## Quick Reference

### Speed Priority
```bash
generate "prompt" --quality lcm       # 3s
```

### Balance (Best Overall)
```bash
generate "prompt" --quality 4k        # 21s
```

### Maximum Quality
```bash
generate "prompt" --quality 4k-ultra  # 3min
```

---

## Tips

1. **Start with `lcm`** for testing prompts
2. **Use `4k`** for final renders (best balance)
3. **Use `ultra`** when you need absolute best quality
4. **Add `--n 10`** for multiple variations
5. **Use `--seed`** for reproducible results
6. **Use negative prompts** to fix common issues

---

## Documentation

- `README.md` - Full guide
- `QUALITY_PRESETS.md` - All presets explained
- `NEGATIVE_PROMPTS_GUIDE.md` - Improve quality
- `4K_SUPPORT.md` - 4K details
- `LCM_LORA_WORKING.md` - Ultra-fast generation

---

## Get Started Now!

```bash
# Test (3 seconds)
generate "test prompt" --quality lcm

# High quality (21 seconds)
generate "your amazing idea" --quality 4k

# Maximum (3 minutes)
generate "your masterpiece" --quality 4k-ultra
```

**Start creating! 🎨✨**
