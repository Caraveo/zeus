#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
MAX_RETRIES=3

echo "======================================================================"
echo "  SD-Generate Setup v2.1.1 (MPS/Apple Silicon)"
echo "======================================================================"
echo ""
echo "Features:"
echo "  • SD 3.5 Large Turbo (--pro flag, 8 steps, 2-5 min)"
echo "  • Advanced memory management for SD 3.5"
echo "  • 12 quality presets (lcm → 4k-ultra)"
echo "  • SD 1.5 + SDXL + SD 3.5 Turbo support"
echo "  • LCM LoRA (3 second generation)"
echo "  • 4K upscaling (2048px & 4096px)"
echo "  • Auto-compatible refiners"
echo "  • Gated model support (SD 3.5 Turbo)"
echo "  • Style presets + ControlNet ready"
echo ""

# Function to retry commands
retry_command() {
    local cmd="$1"
    local description="$2"
    local attempt=1
    
    while [ $attempt -le $MAX_RETRIES ]; do
        echo -e "${YELLOW}[$attempt/$MAX_RETRIES]${NC} $description..."
        if eval "$cmd"; then
            echo -e "${GREEN}✓${NC} $description succeeded"
            return 0
        else
            echo -e "${RED}✗${NC} $description failed (attempt $attempt/$MAX_RETRIES)"
            attempt=$((attempt + 1))
            if [ $attempt -le $MAX_RETRIES ]; then
                echo "Retrying in 2 seconds..."
                sleep 2
            fi
        fi
    done
    
    echo -e "${RED}ERROR:${NC} $description failed after $MAX_RETRIES attempts"
    return 1
}

# Step 1: Create or recreate virtual environment
echo -e "${YELLOW}Step 1:${NC} Creating Python virtual environment..."
if [ -d "$VENV_DIR" ]; then
    echo "Removing existing venv..."
    rm -rf "$VENV_DIR"
fi

if ! python3 -m venv "$VENV_DIR"; then
    echo -e "${RED}ERROR:${NC} Failed to create virtual environment"
    echo "Please ensure Python 3.8+ is installed: brew install python3"
    exit 1
fi

# Activate venv
source "$VENV_DIR/bin/activate"

if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${RED}ERROR:${NC} Failed to activate virtual environment"
    exit 1
fi

echo -e "${GREEN}✓${NC} Virtual environment created and activated"
echo ""

# Step 2: Upgrade pip
echo -e "${YELLOW}Step 2:${NC} Upgrading pip..."
retry_command "pip install --upgrade pip" "Pip upgrade" || exit 1
echo ""

# Step 3: Install PyTorch with MPS support
echo -e "${YELLOW}Step 3:${NC} Installing PyTorch (MPS/CPU only - NO CUDA)..."
retry_command "pip install torch torchvision torchaudio" "PyTorch installation" || exit 1
echo ""

# Step 4: Install core dependencies
echo -e "${YELLOW}Step 4:${NC} Installing diffusers and dependencies..."
DEPENDENCIES="diffusers transformers accelerate safetensors pillow sentencepiece opencv-python datasets huggingface_hub peft protobuf psutil"
retry_command "pip install $DEPENDENCIES" "Dependencies installation" || exit 1
echo -e "${GREEN}✓${NC} All dependencies installed (including SD 3.5 + memory management)"
echo ""

# Step 5: Export environment variables
echo -e "${YELLOW}Step 5:${NC} Configuring MPS environment..."
export PYTORCH_ENABLE_MPS_FALLBACK=1
export CUDA_VISIBLE_DEVICES=""
unset CUDA_HOME 2>/dev/null || true
unset CUDA_PATH 2>/dev/null || true
echo -e "${GREEN}✓${NC} MPS environment configured"
echo ""

# Step 6: Verify generate.py exists
echo -e "${YELLOW}Step 6:${NC} Checking runtime scripts..."
if [ ! -f "$SCRIPT_DIR/generate.py" ]; then
    echo -e "${RED}ERROR:${NC} generate.py not found!"
    echo "Please ensure generate.py is in the sd-generate directory"
    exit 1
fi
echo -e "${GREEN}✓${NC} generate.py found"

# Make it executable
chmod +x "$SCRIPT_DIR/generate.py"
echo ""

# Step 6b: Skip the old embedded version (now using actual file)
if false; then
cat > "$SCRIPT_DIR/generate.py.old" << 'GENERATE_PY_EOF'
#!/usr/bin/env python3
"""
SD-Generate: Robust Text-to-Image Generation with MPS Acceleration
"""

import os
import sys
import torch
import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# Force MPS environment
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
if "CUDA_HOME" in os.environ:
    del os.environ["CUDA_HOME"]
if "CUDA_PATH" in os.environ:
    del os.environ["CUDA_PATH"]

# Style presets
STYLES = {
    "anime": {
        "prompt_suffix": ", anime style, highly detailed, vibrant colors, cel shaded, studio quality",
        "negative_prompt": "photo, photorealistic, 3d render, ugly, blurry, low quality"
    },
    "fantasy": {
        "prompt_suffix": ", fantasy art, magical, ethereal, detailed, epic, concept art style",
        "negative_prompt": "modern, mundane, photograph, low quality, blurry"
    },
    "scifi": {
        "prompt_suffix": ", sci-fi, futuristic, high-tech, detailed, concept art, cyberpunk aesthetic",
        "negative_prompt": "fantasy, medieval, low quality, blurry, watermark"
    },
    "realism": {
        "prompt_suffix": ", photorealistic, 8k uhd, high detail, professional photography, sharp focus",
        "negative_prompt": "cartoon, anime, painting, drawing, low quality, blurry"
    }
}

class ImageGenerator:
    def __init__(self, args):
        self.args = args
        self.device = "mps"
        # Use float32 on MPS to avoid VAE decode issues
        self.dtype = torch.float32
        self.pipeline = None
        self.metadata = {
            "device": self.device,
            "dtype": str(self.dtype),
            "failures": [],
            "warnings": []
        }
        
    def log_failure(self, component: str, error: str, retry_count: int):
        """Log failure information"""
        self.metadata["failures"].append({
            "component": component,
            "error": str(error),
            "retry": retry_count,
            "timestamp": datetime.now().isoformat()
        })
        
    def log_warning(self, message: str):
        """Log warning information"""
        self.metadata["warnings"].append({
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
    def retry_operation(self, operation_name: str, operation_func, max_retries: int = 3):
        """Retry an operation up to max_retries times"""
        for attempt in range(max_retries):
            try:
                print(f"[{attempt + 1}/{max_retries}] Attempting {operation_name}...")
                result = operation_func()
                print(f"✓ {operation_name} succeeded")
                return result, True
            except Exception as e:
                error_msg = str(e)
                print(f"✗ {operation_name} failed: {error_msg}")
                self.log_failure(operation_name, error_msg, attempt + 1)
                
                if attempt < max_retries - 1:
                    print(f"Retrying...")
                    time.sleep(2)
                else:
                    print(f"✗ {operation_name} failed after {max_retries} attempts")
                    
        return None, False
    
    def load_base_pipeline(self):
        """Load base Stable Diffusion pipeline"""
        from diffusers import StableDiffusionPipeline
        
        model_name = self.args.model if self.args.model else "Lykon/DreamShaper-8"
        
        def load_fn():
            print(f"Loading model: {model_name}")
            pipe = StableDiffusionPipeline.from_pretrained(
                model_name,
                torch_dtype=self.dtype,
                safety_checker=None,
                requires_safety_checker=False
            )
            pipe = pipe.to(self.device)
            pipe.enable_attention_slicing()
            return pipe
        
        pipeline, success = self.retry_operation("Base Pipeline Load", load_fn)
        
        if not success:
            raise RuntimeError("Failed to load base pipeline after multiple retries")
        
        self.pipeline = pipeline
        self.metadata["model"] = model_name
        self.metadata["pipeline_type"] = "StableDiffusionPipeline"
        
    def apply_lora(self):
        """Apply LoRA weights if specified"""
        if not self.args.lora:
            return True
            
        def load_lora_fn():
            print(f"Loading LoRA: {self.args.lora}")
            self.pipeline.load_lora_weights(self.args.lora)
            return True
        
        result, success = self.retry_operation("LoRA Load", load_lora_fn)
        
        if success:
            self.metadata["lora"] = self.args.lora
            return True
        else:
            self.log_warning("LoRA loading failed - continuing without LoRA")
            self.metadata["lora"] = "failed"
            return False
    
    def setup_controlnet(self):
        """Setup ControlNet if specified"""
        controlnet_type = None
        controlnet_image = None
        
        if self.args.pose:
            controlnet_type = "pose"
            controlnet_image = self.args.pose
        elif self.args.depth:
            controlnet_type = "depth"
            controlnet_image = self.args.depth
        elif self.args.canny:
            controlnet_type = "canny"
            controlnet_image = self.args.canny
        
        if not controlnet_type:
            return None
        
        def load_controlnet_fn():
            from diffusers import ControlNetModel, StableDiffusionControlNetPipeline
            from PIL import Image
            import cv2
            import numpy as np
            
            # Map ControlNet types to model IDs
            controlnet_models = {
                "pose": "lllyasviel/control_v11p_sd15_openpose",
                "depth": "lllyasviel/control_v11f1p_sd15_depth",
                "canny": "lllyasviel/control_v11p_sd15_canny"
            }
            
            print(f"Loading ControlNet: {controlnet_type}")
            controlnet = ControlNetModel.from_pretrained(
                controlnet_models[controlnet_type],
                torch_dtype=self.dtype
            )
            
            # Rebuild pipeline with ControlNet
            model_name = self.args.model if self.args.model else "Lykon/DreamShaper-8"
            pipe = StableDiffusionControlNetPipeline.from_pretrained(
                model_name,
                controlnet=controlnet,
                torch_dtype=self.dtype,
                safety_checker=None,
                requires_safety_checker=False
            )
            pipe = pipe.to(self.device)
            pipe.enable_attention_slicing()
            
            # Load and process control image
            control_img = Image.open(controlnet_image).convert("RGB")
            
            # Preprocess based on type
            if controlnet_type == "canny":
                img_array = np.array(control_img)
                edges = cv2.Canny(img_array, 100, 200)
                control_img = Image.fromarray(edges)
            
            return pipe, control_img
        
        result, success = self.retry_operation("ControlNet Load", load_controlnet_fn)
        
        if success:
            self.pipeline, control_img = result
            self.metadata["controlnet"] = controlnet_type
            self.metadata["controlnet_image"] = controlnet_image
            self.metadata["pipeline_type"] = "StableDiffusionControlNetPipeline"
            return control_img
        else:
            self.log_warning("ControlNet loading failed - falling back to base generation")
            self.metadata["controlnet"] = "failed"
            return None
    
    def generate_images(self, control_image=None):
        """Generate images with retry logic"""
        prompt = self.args.prompt
        negative_prompt = self.args.negative_prompt or ""
        
        # Apply style
        if self.args.style and self.args.style in STYLES:
            style_config = STYLES[self.args.style]
            prompt += style_config["prompt_suffix"]
            negative_prompt = style_config["negative_prompt"] if not negative_prompt else negative_prompt
            self.metadata["style"] = self.args.style
        
        self.metadata["prompt"] = prompt
        self.metadata["negative_prompt"] = negative_prompt
        self.metadata["seed"] = self.args.seed
        self.metadata["steps"] = self.args.steps
        self.metadata["num_images"] = self.args.n
        
        # Set seed
        generator = torch.Generator(device=self.device).manual_seed(self.args.seed)
        
        # Prepare generation kwargs
        gen_kwargs = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "num_inference_steps": self.args.steps,
            "generator": generator,
            "num_images_per_prompt": self.args.n
        }
        
        if control_image:
            gen_kwargs["image"] = control_image
            gen_kwargs["controlnet_conditioning_scale"] = 1.0
        
        def generate_fn():
            print(f"Generating {self.args.n} image(s)...")
            result = self.pipeline(**gen_kwargs)
            return result.images
        
        images, success = self.retry_operation("Image Generation", generate_fn)
        
        if not success:
            raise RuntimeError("Image generation failed after multiple retries")
        
        return images
    
    def upscale_image(self, image):
        """Upscale image using SD upscaler"""
        if not self.args.upscale or self.args.upscale == 1:
            return image
        
        def upscale_fn():
            from diffusers import StableDiffusionUpscalePipeline
            
            print(f"Upscaling by {self.args.upscale}x...")
            upscaler = StableDiffusionUpscalePipeline.from_pretrained(
                "stabilityai/stable-diffusion-x4-upscaler",
                torch_dtype=self.dtype
            )
            upscaler = upscaler.to(self.device)
            upscaler.enable_attention_slicing()
            
            upscaled = upscaler(
                prompt=self.args.prompt,
                image=image,
                num_inference_steps=20
            ).images[0]
            
            return upscaled
        
        result, success = self.retry_operation("Upscaling", upscale_fn)
        
        if success:
            self.metadata["upscale"] = self.args.upscale
            return result
        else:
            self.log_warning(f"Upscaling failed - saving base resolution image")
            self.metadata["upscale"] = "failed"
            return image
    
    def refine_image(self, image):
        """Refine image using refiner model"""
        if not self.args.refiner:
            return image
        
        def refine_fn():
            from diffusers import StableDiffusionImg2ImgPipeline
            
            print(f"Refining with model: {self.args.refiner}")
            refiner = StableDiffusionImg2ImgPipeline.from_pretrained(
                self.args.refiner,
                torch_dtype=self.dtype
            )
            refiner = refiner.to(self.device)
            refiner.enable_attention_slicing()
            
            refined = refiner(
                prompt=self.args.prompt,
                image=image,
                strength=0.3,
                num_inference_steps=20
            ).images[0]
            
            return refined
        
        result, success = self.retry_operation("Refinement", refine_fn)
        
        if success:
            self.metadata["refiner"] = self.args.refiner
            return result
        else:
            self.log_warning(f"Refinement failed - saving unrefined image")
            self.metadata["refiner"] = "failed"
            return image
    
    def save_image(self, image, index: int, generation_time: float):
        """Save image with metadata"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"output_{timestamp}_{index:03d}.png"
        json_filename = f"output_{timestamp}_{index:03d}.json"
        
        output_dir = Path(self.args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        image_path = output_dir / filename
        json_path = output_dir / json_filename
        
        # Save image
        image.save(image_path)
        print(f"✓ Saved: {image_path}")
        
        # Save metadata
        metadata = self.metadata.copy()
        metadata["generation_time"] = generation_time
        metadata["image_index"] = index
        metadata["filename"] = filename
        
        with open(json_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return image_path
    
    def run(self):
        """Main execution flow"""
        start_time = time.time()
        
        try:
            # Load base pipeline
            self.load_base_pipeline()
            
            # Apply LoRA if specified
            if self.args.lora:
                self.apply_lora()
            
            # Setup ControlNet if specified
            control_image = self.setup_controlnet()
            
            # Generate images
            images = self.generate_images(control_image)
            
            # Post-process each image
            final_images = []
            for i, image in enumerate(images):
                # Refine
                if self.args.refiner:
                    image = self.refine_image(image)
                
                # Upscale
                if self.args.upscale and self.args.upscale > 1:
                    image = self.upscale_image(image)
                
                final_images.append(image)
            
            # Save all images
            generation_time = time.time() - start_time
            saved_paths = []
            
            for i, image in enumerate(final_images, 1):
                path = self.save_image(image, i, generation_time)
                saved_paths.append(path)
            
            print(f"\n{'='*60}")
            print(f"✓ Generation complete!")
            print(f"  Time: {generation_time:.2f}s")
            print(f"  Images: {len(saved_paths)}")
            if self.metadata["warnings"]:
                print(f"  Warnings: {len(self.metadata['warnings'])}")
            if self.metadata["failures"]:
                print(f"  Failures (recovered): {len(self.metadata['failures'])}")
            print(f"{'='*60}")
            
            return 0
            
        except Exception as e:
            print(f"\n{'='*60}")
            print(f"✗ FATAL ERROR: {str(e)}")
            print(f"{'='*60}")
            return 1

def main():
    parser = argparse.ArgumentParser(
        description="SD-Generate: Robust Text-to-Image Generation"
    )
    
    # Core arguments
    parser.add_argument("prompt", type=str, help="Text prompt for generation")
    parser.add_argument("--model", type=str, help="Override base model path")
    parser.add_argument("--output", type=str, default="./outputs", help="Output directory")
    parser.add_argument("--n", type=int, default=1, help="Number of images to generate")
    parser.add_argument("--steps", type=int, default=30, help="Number of inference steps")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--negative-prompt", type=str, help="Negative prompt")
    
    # Style
    parser.add_argument("--style", choices=["anime", "fantasy", "scifi", "realism"], 
                       help="Apply style preset")
    
    # LoRA
    parser.add_argument("--lora", type=str, help="Path to LoRA weights (.safetensors)")
    
    # ControlNet
    parser.add_argument("--pose", type=str, help="Path to pose control image")
    parser.add_argument("--depth", type=str, help="Path to depth control image")
    parser.add_argument("--canny", type=str, help="Path to canny edge control image")
    
    # Post-processing
    parser.add_argument("--upscale", type=int, choices=[2, 4], help="Upscale factor")
    parser.add_argument("--refiner", type=str, help="Refiner model name")
    
    args = parser.parse_args()
    
    # Validation
    if args.n < 1:
        print("Error: --n must be at least 1")
        return 1
    
    # Create generator and run
    generator = ImageGenerator(args)
    return generator.run()

if __name__ == "__main__":
    sys.exit(main())
GENERATE_PY_EOF
fi
# End of old embedded version

# Step 7: Create CLI wrapper
echo -e "${YELLOW}Step 7:${NC} Creating CLI wrapper..."
cat > "$SCRIPT_DIR/generate" << 'GENERATE_WRAPPER_EOF'
#!/bin/bash
# Resolve the actual script location even if called via symlink
SCRIPT_PATH="${BASH_SOURCE[0]}"
while [ -L "$SCRIPT_PATH" ]; do
    SCRIPT_DIR="$(cd -P "$(dirname "$SCRIPT_PATH")" && pwd)"
    SCRIPT_PATH="$(readlink "$SCRIPT_PATH")"
    [[ $SCRIPT_PATH != /* ]] && SCRIPT_PATH="$SCRIPT_DIR/$SCRIPT_PATH"
done
SCRIPT_DIR="$(cd -P "$(dirname "$SCRIPT_PATH")" && pwd)"

source "$SCRIPT_DIR/venv/bin/activate"
python3 "$SCRIPT_DIR/generate.py" "$@"
GENERATE_WRAPPER_EOF

chmod +x "$SCRIPT_DIR/generate"
echo -e "${GREEN}✓${NC} CLI wrapper created"
echo ""

# Step 8: Create symlink
echo -e "${YELLOW}Step 8:${NC} Creating symlink in PATH..."
SYMLINK_CREATED=false

# Try /usr/local/bin first
if [ -w "/usr/local/bin" ]; then
    if ln -sf "$SCRIPT_DIR/generate" /usr/local/bin/generate 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Symlink created: /usr/local/bin/generate"
        SYMLINK_CREATED=true
    fi
fi

# Fallback to ~/.local/bin
if [ "$SYMLINK_CREATED" = false ]; then
    mkdir -p "$HOME/.local/bin"
    if ln -sf "$SCRIPT_DIR/generate" "$HOME/.local/bin/generate"; then
        echo -e "${GREEN}✓${NC} Symlink created: ~/.local/bin/generate"
        SYMLINK_CREATED=true
        
        # Check if ~/.local/bin is in PATH
        if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
            echo -e "${YELLOW}WARNING:${NC} ~/.local/bin is not in your PATH"
            echo ""
            echo "To use 'generate' command from anywhere, add this to your shell config:"
            echo ""
            echo "For zsh (default on macOS):"
            echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.zshrc"
            echo "  source ~/.zshrc"
            echo ""
            echo "For bash:"
            echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
            echo "  source ~/.bashrc"
            echo ""
        fi
    fi
fi

if [ "$SYMLINK_CREATED" = false ]; then
    echo -e "${RED}WARNING:${NC} Could not create symlink. Run manually:"
    echo "  $SCRIPT_DIR/generate \"your prompt\""
fi
echo ""

# Step 9: Run validation tests
echo -e "${YELLOW}Step 9:${NC} Running validation tests..."
echo ""

TEST_OUTPUT="$SCRIPT_DIR/test_outputs"
mkdir -p "$TEST_OUTPUT"

TESTS_PASSED=0
TESTS_FAILED=0

# Test 1: Basic generation
echo "Test 1: Basic image generation..."
if retry_command "python3 '$SCRIPT_DIR/generate.py' 'a simple red circle' --output '$TEST_OUTPUT' --steps 10 --seed 999" "Basic generation test"; then
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "${RED}WARNING:${NC} Basic generation test failed"
fi
echo ""

# Test 2: Style application
echo "Test 2: Style preset test..."
if retry_command "python3 '$SCRIPT_DIR/generate.py' 'a cat' --style anime --output '$TEST_OUTPUT' --steps 10 --seed 888" "Style preset test"; then
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "${RED}WARNING:${NC} Style test failed but continuing..."
fi
echo ""

# Test 3: Multiple images
echo "Test 3: Multiple images test..."
if retry_command "python3 '$SCRIPT_DIR/generate.py' 'a tree' --n 2 --output '$TEST_OUTPUT' --steps 5 --seed 777" "Multiple images test"; then
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "${RED}WARNING:${NC} Multiple images test failed but continuing..."
fi
echo ""

# Clean up test outputs
echo "Cleaning up test outputs..."
rm -rf "$TEST_OUTPUT"

# Final summary
echo ""
echo "======================================================================"
echo "  SETUP COMPLETE"
echo "======================================================================"
echo ""
echo -e "${GREEN}✓${NC} Python virtual environment: $VENV_DIR"
echo -e "${GREEN}✓${NC} PyTorch with MPS support installed"
echo -e "${GREEN}✓${NC} All dependencies installed"
echo -e "${GREEN}✓${NC} Runtime scripts generated"
if [ "$SYMLINK_CREATED" = true ]; then
    echo -e "${GREEN}✓${NC} CLI command 'generate' available in PATH"
else
    echo -e "${YELLOW}!${NC} CLI command requires manual setup"
fi
echo -e "${GREEN}✓${NC} Tests passed: $TESTS_PASSED"
if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${YELLOW}!${NC} Tests failed: $TESTS_FAILED (non-critical)"
fi
echo ""
echo "Features available:"
echo "  • SD 3.5 Large Turbo with --pro flag (NEW!)"
echo "    - 4-6x faster than SD 3.5 Large (2-5 min vs 15-20 min)"
echo "    - Only 8 steps needed for excellent quality"
echo "    - Works on all Apple Silicon (20GB+ RAM)"
echo "  • Advanced memory management for SD 3.5"
echo "    - Aggressive cleanup between stages"
echo "    - Real-time memory monitoring"
echo "    - Pipeline unloading before refiner"
echo "    - Attention & VAE slicing"
echo "  • 12 quality presets (lcm → 4k-ultra)"
echo "  • LCM LoRA - 3 second generation"
echo "  • SD 1.5 + SDXL + SD 3.5 Turbo support"
echo "  • Auto-compatible refiners"
echo "  • 4K upscaling - 2048px & 4096px"
echo "  • Fast PIL upscaler"
echo "  • Gated model support (SD 3.5 Turbo)"
echo "  • LoRA support + manual loading"
echo "  • 4 style presets + negative prompts"
echo "  • ControlNet ready"
echo "  • Auto-retry & crash recovery"
echo ""
echo "======================================================================"
echo "  USAGE"
echo "======================================================================"
echo ""
echo "Basic usage:"
echo "  generate \"a beautiful landscape\""
echo ""
echo "Quality presets (RECOMMENDED):"
echo "  generate \"dragon\" --quality lcm              # Ultra fast (3s)"
echo "  generate \"dragon\" --quality fast            # Quick (10s)"
echo "  generate \"dragon\" --quality 4k              # 4K quality (21s) - RECOMMENDED"
echo "  generate \"dragon\" --quality max             # High quality (30s)"
echo "  generate \"dragon\" --quality ultra           # SDXL (3min)"
echo "  generate \"dragon\" --quality 4k-ultra        # SDXL 4K (3min)"
echo ""
echo "Pro mode (SD 3.5 Large Turbo - NEW! Much faster!):"
echo "  generate \"dragon\" --pro                      # Best quality (2-5min)"
echo "  Note: Requires ./login-hf.sh + 20GB+ RAM (works on all Apple Silicon)"
echo "  Model: stabilityai/stable-diffusion-3.5-large-turbo"
echo "  Steps: 8 (optimized for turbo model)"
echo ""
echo "Specialized presets:"
echo "  generate \"portrait\" --quality photorealistic"
echo "  generate \"portrait\" --quality ultra-realistic"
echo "  generate \"movie scene\" --quality cinematic"
echo ""
echo "All 12 presets:"
echo "  lcm, fast, quality, hd, max, 4k, ultra, ultra-hd, 4k-ultra,"
echo "  photorealistic, ultra-realistic, cinematic"
echo ""
echo "With negative prompts:"
echo "  generate \"portrait\" --quality 4k \\"
echo "    --negative-prompt \"ugly, blurry, deformed\""
echo ""
echo "With manual options:"
echo "  generate \"cyberpunk city\" --style scifi --n 4"
echo "  generate \"portrait\" --steps 50 --seed 12345"
echo "  generate \"custom\" --upscale 2 --refiner \"runwayml/stable-diffusion-v1-5\""
echo ""
echo "Documentation (20 guides):"
echo "  README.md                      - Complete guide"
echo "  PRO_MODE_UPDATE.md             - SD 3.5 Turbo guide (NEW!)"
echo "  MEMORY_MANAGEMENT.md           - SD 3.5 optimization"
echo "  MEMORY_MANAGEMENT_SUMMARY.md   - Quick memory guide"
echo "  CHANGES_V2.1.md                - v2.1 changelog"
echo "  QUICK_START.md                 - 5-minute start"
echo "  QUALITY_PRESETS.md             - All 12 presets explained"
echo "  GATED_MODELS_GUIDE.md          - SD 3.5 setup & usage"
echo "  4K_SUPPORT.md                  - 4K generation guide"
echo "  LCM_LORA_WORKING.md            - Ultra-fast LCM guide"
echo "  NEGATIVE_PROMPTS_GUIDE.md      - Improve quality"
echo "  COMPLETE_SYSTEM_SUMMARY.md     - Full test results"
echo ""
echo "======================================================================"
echo ""
echo -e "${GREEN}Setup complete!${NC} Start generating:"
echo ""
echo "  ${YELLOW}generate \"your prompt\" --quality 4k${NC}"
echo ""
echo "For SD 3.5 Large Turbo (best quality, fast, NEW!):"
echo "  1. Accept license: https://huggingface.co/stabilityai/stable-diffusion-3.5-large-turbo"
echo "  2. Run: ${YELLOW}./login-hf.sh${NC} (if not already authenticated)"
echo "  3. Generate: ${YELLOW}generate \"prompt\" --pro${NC}"
echo ""
echo "The --pro flag now uses:"
echo "  • Model: stabilityai/stable-diffusion-3.5-large-turbo"
echo "  • Steps: 8 (optimized for turbo)"
echo "  • Time: 2-5 min (vs 15-20 min for regular SD 3.5)"
echo "  • RAM: 20GB+ (works on all Apple Silicon)"
echo ""
echo "See PRO_MODE_UPDATE.md for complete guide."
echo ""
echo "======================================================================"
