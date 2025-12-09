# Gated Models Guide - SD 3.5 & Others

## What are Gated Models?

Some models on Hugging Face require:
1. Creating a Hugging Face account
2. Accepting the model's license agreement
3. Authenticating with a token

**SD 3.5 Large** is one of these gated models.

---

## Step-by-Step: Using SD 3.5

### Step 1: Create Hugging Face Account

Go to: https://huggingface.co/join

Create a free account.

---

### Step 2: Accept the SD 3.5 License

1. Go to: https://huggingface.co/stabilityai/stable-diffusion-3.5-large
2. Click **"Agree and access repository"**
3. Read and accept the license terms

**You must do this before the model will download!**

---

### Step 3: Get Your Access Token

1. Go to: https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Give it a name (e.g., "sd-generate")
4. Select **"Read"** permission
5. Click **"Generate token"**
6. Copy the token (starts with `hf_...`)

---

### Step 4: Login with CLI

```bash
cd sd-generate
./login-hf.sh
```

When prompted, paste your token (it won't show as you type - this is normal).

**OR** use the token directly:

```bash
huggingface-cli login
# Paste your token when prompted
```

---

### Step 5: Use SD 3.5

Once authenticated, you can use SD 3.5:

**Easy way (--pro flag):**
```bash
generate "astronaut riding a horse" --pro
```

**Manual way:**
```bash
generate "astronaut riding a horse" \
  --model "stabilityai/stable-diffusion-3.5-large" \
  --steps 28
```

**The `--pro` flag automatically sets:**
- Model: stabilityai/stable-diffusion-3.5-large
- Steps: 28 (minimum recommended)
- Shows performance warning

**First run will download the model (~20GB).**

---

## SD 3.5 Usage Examples

### Basic Generation
```bash
generate "beautiful landscape at sunset" \
  --model "stabilityai/stable-diffusion-3.5-large"
```

### High Quality
```bash
generate "detailed portrait, professional lighting" \
  --model "stabilityai/stable-diffusion-3.5-large" \
  --steps 50 \
  --seed 42
```

### With Negative Prompt
```bash
generate "futuristic city" \
  --model "stabilityai/stable-diffusion-3.5-large" \
  --negative-prompt "ugly, blurry, low quality" \
  --steps 40
```

### Multiple Images
```bash
generate "character concept art" \
  --model "stabilityai/stable-diffusion-3.5-large" \
  --n 4 \
  --seed 123
```

### With 4K Upscaling
```bash
generate "epic fantasy scene" \
  --model "stabilityai/stable-diffusion-3.5-large" \
  --upscale 4 \
  --steps 50
```

---

## SD 3.5 vs Other Models

| Feature | SD 1.5 | SDXL | SD 3.5 |
|---------|--------|------|--------|
| Speed (Base chip) | Fast (10s) | Medium (3min) | **VERY SLOW (15-20min)** |
| Speed (Max/Ultra) | Very Fast | Fast | **Much Faster (5-10min est)** |
| Quality | Good | Excellent | Best |
| Size | 2GB | 6GB | 20GB |
| RAM Required | 8GB | 16GB | **36GB minimum** |
| Gated | ❌ No | ❌ No | ✅ Yes |
| Auth Required | ❌ No | ❌ No | ✅ Yes |
| Resolution | 512px | 1024px | 1024px+ |

**IMPORTANT WARNINGS:**

**RAM Requirements:**
- **SD 3.5 requires 36GB RAM minimum**
- M1/M2/M3/M4 Base (8-16GB): ❌ Insufficient RAM
- M1/M2/M3/M4 Pro (16-32GB): ❌ Insufficient RAM
- **M1/M2/M3/M4 Max/Ultra (36GB+)**: ✅ Supported

**Performance:**
- Base/Pro chips: Very slow (~30-40s per step)
- **Max/Ultra chips: Much faster** due to more unified memory bandwidth
- Generation time: 5-20 minutes depending on chip

**Better Alternative for Most Users:** Use `--quality 4k-ultra` (SDXL) for excellent quality in just 3 minutes.

---

## Recommended Settings for SD 3.5

**Note:** SD 3.5 is best used on CUDA GPUs. On Apple Silicon, SDXL is recommended instead.

### Quick Test
```bash
generate "test prompt" \
  --model "stabilityai/stable-diffusion-3.5-large" \
  --steps 28
```

### High Quality
```bash
generate "your prompt" \
  --model "stabilityai/stable-diffusion-3.5-large" \
  --steps 40 \
  --seed 42
```

### Maximum Quality
```bash
generate "your masterpiece" \
  --model "stabilityai/stable-diffusion-3.5-large" \
  --steps 50 \
  --upscale 4 \
  --negative-prompt "ugly, blurry, low quality"
```

---

## Other Gated Models

### Stable Diffusion 3 Medium
```bash
generate "prompt" --model "stabilityai/stable-diffusion-3-medium-diffusers"
```

Smaller, faster version of SD 3.

### Playground v2.5
```bash
generate "prompt" --model "playgroundai/playground-v2.5-1024px-aesthetic"
```

High aesthetic quality model.

---

## Troubleshooting

### Error: "Repository not found" or "401 Unauthorized"

**Solution:**
1. Make sure you accepted the license
2. Run `./login-hf.sh` to authenticate
3. Wait a few minutes after accepting license

### Error: "Model too large"

SD 3.5 is 20GB. Make sure you have:
- 20GB+ free disk space
- Good internet connection
- Patience (first download takes 10-30 minutes)

### Error: "Out of memory"

SD 3.5 needs 16GB+ RAM. Try:
- Close other applications
- Use smaller model: `--model "stabilityai/stable-diffusion-3-medium-diffusers"`
- Use cloud generation instead (see below)

---

## Alternative: Use Cloud Generation

If downloading 20GB is too much, use cloud generation:

### Option 1: Hugging Face Inference API (Free Tier)

```python
from huggingface_hub import InferenceClient

client = InferenceClient(api_key=os.environ["HF_TOKEN"])
image = client.text_to_image(
    "astronaut riding a horse",
    model="stabilityai/stable-diffusion-3.5-large"
)
image.save("output.png")
```

### Option 2: Use Existing Cloud Script

```bash
# Set your HF token
export HF_TOKEN="hf_your_token_here"

# Generate via cloud (instant, no download needed)
python3 generate-cloud.py "astronaut riding a horse"
```

---

## Authentication Methods

### Method 1: Login Script (Recommended)
```bash
./login-hf.sh
```

### Method 2: Manual CLI
```bash
huggingface-cli login
```

### Method 3: Environment Variable
```bash
export HF_TOKEN="hf_your_token_here"
```

Add to `~/.zshrc` to make permanent:
```bash
echo 'export HF_TOKEN="hf_your_token_here"' >> ~/.zshrc
source ~/.zshrc
```

---

## Workflow Recommendation

### For SD 3.5

**First time:**
1. Accept license at https://huggingface.co/stabilityai/stable-diffusion-3.5-large
2. Run `./login-hf.sh`
3. Wait for download (~20GB, one-time)
4. Generate images

**Subsequent uses:**
```bash
generate "your prompt" --model "stabilityai/stable-diffusion-3.5-large"
```

---

## Quick Reference

### Authentication Status
```bash
# Check if logged in
huggingface-cli whoami

# Login
./login-hf.sh
```

### Using SD 3.5
```bash
# Basic
generate "prompt" --model "stabilityai/stable-diffusion-3.5-large"

# With options
generate "prompt" \
  --model "stabilityai/stable-diffusion-3.5-large" \
  --steps 40 \
  --seed 42 \
  --negative-prompt "ugly, blurry"

# With upscaling
generate "prompt" \
  --model "stabilityai/stable-diffusion-3.5-large" \
  --upscale 4
```

---

## Storage Requirements

### Models Download Location
```
~/.cache/huggingface/
```

### Disk Space Needed

| Model | Size | Total with Cache |
|-------|------|------------------|
| DreamShaper-8 (SD 1.5) | 2GB | ~5GB |
| SDXL Base | 6GB | ~12GB |
| SD 3.5 Large | 20GB | ~30GB |

**Tip:** Keep at least 30GB free for all models.

---

## Performance Comparison

### SD 1.5 (Fast)
```bash
generate "prompt" --quality 4k
# Time: 21s, Quality: Good, Size: 2GB
```

### SDXL (Better)
```bash
generate "prompt" --quality ultra
# Time: 3min, Quality: Excellent, Size: 6GB
```

### SD 3.5 (Best)
```bash
generate "prompt" --model "stabilityai/stable-diffusion-3.5-large" --steps 40
# Time: 2-3min, Quality: Best, Size: 20GB
```

---

## Summary

### To Use SD 3.5:
1. ✅ Create HF account
2. ✅ Accept license at model page
3. ✅ Run `./login-hf.sh`
4. ✅ Use: `--model "stabilityai/stable-diffusion-3.5-large"`

### Authentication Lasts Forever
Once you login with `./login-hf.sh`, you stay logged in. No need to repeat.

### Model Downloads Once
First generation downloads the model. Subsequent generations use cached version.

---

## Links

- **SD 3.5 Model Page:** https://huggingface.co/stabilityai/stable-diffusion-3.5-large
- **Get HF Token:** https://huggingface.co/settings/tokens
- **HF Documentation:** https://huggingface.co/docs/huggingface_hub/guides/cli

---

## Need Help?

**Can't download:**
- Check internet connection
- Verify you accepted license
- Try: `huggingface-cli whoami` to check auth

**Out of space:**
- SD 3.5 is 20GB
- Clear cache: `rm -rf ~/.cache/huggingface/` (will re-download)
- Use smaller models instead

**Still stuck:**
- Use cloud generation (no download needed)
- Use existing presets (4k is excellent)
- Check model page for requirements

---

## Complete Example Workflow

### Initial Setup (One Time)

```bash
# 1. Go to browser
open https://huggingface.co/stabilityai/stable-diffusion-3.5-large

# 2. Click "Agree and access repository"

# 3. Login to Hugging Face
cd sd-generate
./login-hf.sh
# Paste token when prompted

# 4. Test authentication
huggingface-cli whoami
# Should show your username
```

### First Generation (Downloads Model)

```bash
generate "astronaut riding a horse" \
  --model "stabilityai/stable-diffusion-3.5-large" \
  --steps 40 \
  --seed 42
```

**This will:**
- Download SD 3.5 (~20GB, one-time, 10-30 minutes)
- Generate image (~2-3 minutes)
- Save to `outputs/`

### Subsequent Generations (Fast)

```bash
generate "beautiful mountain landscape" \
  --model "stabilityai/stable-diffusion-3.5-large" \
  --steps 40
```

**This will:**
- Use cached model (no download)
- Generate image (~2-3 minutes)
- High quality output

---

## SD 3.5 Recommended Commands

### Standard Quality
```bash
generate "detailed portrait, professional lighting, sharp focus" \
  --model "stabilityai/stable-diffusion-3.5-large" \
  --steps 40
```

### High Quality
```bash
generate "epic fantasy landscape, cinematic, detailed" \
  --model "stabilityai/stable-diffusion-3.5-large" \
  --steps 50 \
  --seed 42
```

### 4K Quality
```bash
generate "ultra detailed sci-fi city, futuristic, 8k" \
  --model "stabilityai/stable-diffusion-3.5-large" \
  --steps 50 \
  --upscale 4
```

### With Everything
```bash
generate "professional photograph of a cat, studio lighting" \
  --model "stabilityai/stable-diffusion-3.5-large" \
  --steps 50 \
  --upscale 2 \
  --negative-prompt "cartoon, anime, ugly, blurry, low quality" \
  --seed 12345
```

---

## Tips for SD 3.5

1. **Steps**: Use 28-50 steps (28 is minimum, 40 is good, 50 is best)
2. **Negative prompts**: Works very well with SD 3.5
3. **Upscaling**: Combine with `--upscale 4` for stunning results
4. **Seeds**: Use `--seed` for reproducible results
5. **Batch**: Generate multiple with `--n 4`

---

## Authentication Quick Check

```bash
# Check if logged in
huggingface-cli whoami

# If not logged in
./login-hf.sh

# Test with SD 3.5
generate "test" --model "stabilityai/stable-diffusion-3.5-large"
```

---

## Summary

### To Use SD 3.5:
1. ✅ Accept license: https://huggingface.co/stabilityai/stable-diffusion-3.5-large
2. ✅ Login: `./login-hf.sh`
3. ✅ Generate: `generate "prompt" --model "stabilityai/stable-diffusion-3.5-large"`

### Benefits:
- ✅ Best quality available
- ✅ Latest Stability AI model
- ✅ Works with all features (upscaling, negative prompts, etc.)
- ✅ One-time authentication

### Requirements:
- ✅ Hugging Face account (free)
- ✅ License acceptance (one click)
- ✅ 20GB disk space
- ✅ 16GB+ RAM
- ✅ Patience for first download

**Worth it for best quality results!**

---

## Performance Reality Check

### SD 3.5 on Apple Silicon MPS

**Actual Performance:**
- ~30-40 seconds per step
- 28 steps = **15-20 minutes**
- 40 steps = **20-25 minutes**
- 50 steps = **25-30 minutes**

**This is MUCH slower than SDXL** (~2s per step).

### Why So Slow?

SD 3.5 uses:
- Larger transformer architecture
- More parameters (8B+)
- Not optimized for MPS
- Better suited for CUDA GPUs

### Recommendation

**For Apple Silicon users:**

Use SDXL instead:
```bash
generate "your prompt" --quality ultra       # 3 minutes, excellent quality
generate "your prompt" --quality ultra-hd    # 3 minutes, 2K resolution
generate "your prompt" --quality 4k-ultra    # 3 minutes, 4K resolution
```

**Only use SD 3.5 if:**
- You have 30+ minutes per image
- You need absolute best quality
- You're willing to wait

**Better workflow:**
```bash
# Test with SDXL (3min)
generate "prompt" --quality ultra

# If not satisfied, try SD 3.5 (20min)
generate "prompt" --model "stabilityai/stable-diffusion-3.5-large" --steps 28
```

---

## Cloud Alternative for SD 3.5

SD 3.5 is much faster on cloud GPUs. Consider using Hugging Face Inference API:

```bash
export HF_TOKEN="your_token_here"
python3 generate-cloud.py "astronaut riding a horse"
```

This uses cloud GPUs and is much faster than local MPS.

---

## Updated Recommendations

### Best for Apple Silicon

**Speed + Quality:**
```bash
generate "prompt" --quality 4k               # 21s, 2048px
```

**Maximum Quality (Fast):**
```bash
generate "prompt" --quality 4k-ultra         # 3min, 4096px SDXL
```

**Ultra Fast:**
```bash
generate "prompt" --quality lcm              # 3s with LCM LoRA
```

### SD 3.5 Usage

**Only if you have time:**
```bash
generate "prompt" \
  --model "stabilityai/stable-diffusion-3.5-large" \
  --steps 28  # Minimum steps (still 15min)
```

---

## Summary

### SD 3.5 Status
- ✅ **Works:** Yes (with protobuf installed)
- ✅ **Quality:** Best available
- ⚠️  **Speed:** Very slow on MPS (15-20 min per image)
- ✅ **Authentication:** Supported via login-hf.sh
- ✅ **Download:** Works (20GB, one-time)

### Recommendation
**For most users:** Use `--quality 4k-ultra` (SDXL) instead
- 3 minutes vs 20 minutes
- Excellent quality
- 4096px resolution
- Much better experience

**Use SD 3.5 only if:**
- You need absolute best quality
- You have 20+ minutes per image
- You're rendering final, critical work

**Dependencies installed:** protobuf, sentencepiece now included in setup.sh

---

## Using --pro Flag

The `--pro` flag is a shortcut for SD 3.5. These are equivalent:

```bash
# Short version
generate "prompt" --pro

# Long version
generate "prompt" --model "stabilityai/stable-diffusion-3.5-large" --steps 28
```

### Examples with --pro

**Basic:**
```bash
generate "beautiful landscape" --pro
```

**With negative prompt:**
```bash
generate "portrait" --pro --negative-prompt "ugly, blurry"
```

**With seed:**
```bash
generate "character design" --pro --seed 42
```

**Multiple images:**
```bash
generate "concept art" --pro --n 4
```

**Custom steps:**
```bash
generate "masterpiece" --pro --steps 40
```

**With upscaling:**
```bash
generate "epic scene" --pro --upscale 2
```

**Everything combined:**
```bash
generate "fantasy warrior in battle" \
  --pro \
  --negative-prompt "modern, ugly, low quality" \
  --seed 12345 \
  --upscale 2
```

---

## --pro vs Quality Presets

### Use --pro when:
- You want absolute best quality
- You have 15-20 minutes per image
- You're doing final, critical renders
- Quality > speed

### Use --quality presets when:
- You want fast iteration
- 3 minutes is too long
- You need good quality quickly
- Speed matters

### Comparison

```bash
# Fastest (3s)
generate "prompt" --quality lcm

# Best balance (21s)
generate "prompt" --quality 4k

# Excellent quality (3min)
generate "prompt" --quality 4k-ultra

# Best possible (15-20min)
generate "prompt" --pro
```

---

## Quick Reference

| Command | Time | Quality | When to Use |
|---------|------|---------|-------------|
| `--quality lcm` | 3s | Good | Testing |
| `--quality 4k` | 21s | Excellent | Most work |
| `--quality 4k-ultra` | 3min | Excellent | Final renders |
| `--pro` | 15-20min | Best | Critical work |

---

## Complete --pro Examples

### Portrait
```bash
generate "professional portrait, studio lighting, detailed" \
  --pro \
  --negative-prompt "ugly, blurry, deformed, bad hands"
```

### Landscape
```bash
generate "epic mountain landscape, golden hour, cinematic" \
  --pro \
  --seed 42
```

### Fantasy Art
```bash
generate "dragon in magical forest, highly detailed" \
  --pro \
  --negative-prompt "modern, ugly, low quality" \
  --upscale 2
```

### Multiple Variations
```bash
generate "character concept art" \
  --pro \
  --n 6 \
  --seed 100
```

---

## Summary

✅ **--pro flag added** - Easy SD 3.5 access  
✅ **Automatic setup** - Sets model and steps  
✅ **Shows warning** - About slow performance  
✅ **Works with all features** - Upscale, negative prompts, etc.  

**Use --pro for best quality when you have time:**
```bash
generate "your masterpiece" --pro
```

**Use --quality 4k for best balance:**
```bash
generate "your work" --quality 4k
```
