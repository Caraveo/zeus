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
import gc
import psutil
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

# Quality presets - automatic model combinations
QUALITY_PRESETS = {
    "fast": {
        "description": "Fast generation, good quality (SD 1.5)",
        "model": "Lykon/DreamShaper-8",
        "steps": 25,
        "refiner": None,
        "upscale": None
    },
    "quality": {
        "description": "High quality with refiner (SD 1.5 + refiner)",
        "model": "Lykon/DreamShaper-8",
        "steps": 40,
        "refiner": "runwayml/stable-diffusion-v1-5",
        "upscale": None
    },
    "hd": {
        "description": "High quality with 2x upscaling (SD 1.5 + upscale)",
        "model": "Lykon/DreamShaper-8",
        "steps": 40,
        "refiner": None,
        "upscale": 2
    },
    "max": {
        "description": "Maximum quality (SD 1.5 + refiner + 2x upscale)",
        "model": "Lykon/DreamShaper-8",
        "steps": 50,
        "refiner": "runwayml/stable-diffusion-v1-5",
        "upscale": 2
    },
    "ultra": {
        "description": "Ultra quality (SDXL + refiner, slower, needs 16GB RAM)",
        "model": "stabilityai/stable-diffusion-xl-base-1.0",
        "steps": 50,
        "refiner": "stabilityai/stable-diffusion-xl-refiner-1.0",
        "upscale": None
    },
    "ultra-hd": {
        "description": "Ultra HD (SDXL + refiner + 2x upscale, needs 16GB+ RAM)",
        "model": "stabilityai/stable-diffusion-xl-base-1.0",
        "steps": 50,
        "refiner": "stabilityai/stable-diffusion-xl-refiner-1.0",
        "upscale": 2
    },
    "4k": {
        "description": "4K quality (SD 1.5 + refiner + 4x upscale to ~2048px)",
        "model": "Lykon/DreamShaper-8",
        "steps": 50,
        "refiner": "runwayml/stable-diffusion-v1-5",
        "upscale": 4
    },
    "4k-ultra": {
        "description": "4K Ultra (SDXL + refiner + 4x upscale, needs 16GB+ RAM)",
        "model": "stabilityai/stable-diffusion-xl-base-1.0",
        "steps": 50,
        "refiner": "stabilityai/stable-diffusion-xl-refiner-1.0",
        "upscale": 4
    },
    "photorealistic": {
        "description": "Photorealistic quality (Realistic Vision + refiner + 2x)",
        "model": "SG161222/Realistic_Vision_V6.0_B1_noVAE",
        "steps": 45,
        "refiner": "runwayml/stable-diffusion-v1-5",
        "upscale": 2
    },
    "ultra-realistic": {
        "description": "Ultra realistic high detail (SD 1.5 + refiner + 2x, 60 steps)",
        "model": "Lykon/DreamShaper-8",
        "steps": 60,
        "refiner": "runwayml/stable-diffusion-v1-5",
        "upscale": 2
    },
    "cinematic": {
        "description": "Cinematic quality (SD 1.5 + refiner + 2x, extra steps)",
        "model": "Lykon/DreamShaper-8",
        "steps": 60,
        "refiner": "runwayml/stable-diffusion-v1-5",
        "upscale": 2
    },
    "lcm": {
        "description": "Fast LCM LoRA generation (SD 1.5 + LCM LoRA, 4-8 steps)",
        "model": "Lykon/DreamShaper-8",
        "steps": 8,
        "refiner": None,
        "upscale": None,
        "lora": "latent-consistency/lcm-lora-sdv1-5"
    },
    "sd3.5": {
        "description": "SD 3.5 Large Turbo (newest, fast, requires HF auth)",
        "model": "stabilityai/stable-diffusion-3.5-large-turbo",
        "steps": 8,
        "refiner": None,
        "upscale": None,
        "use_sd3": True
    },
    "sd3.5-4k": {
        "description": "SD 3.5 Large Turbo with 4K upscaling (requires HF auth)",
        "model": "stabilityai/stable-diffusion-3.5-large-turbo",
        "steps": 8,
        "refiner": None,
        "upscale": 4,
        "use_sd3": True
    }
}

# Memory Management Utilities
def cleanup_memory(aggressive=False):
    """Clean up memory on MPS device"""
    try:
        # Collect Python garbage
        gc.collect()
        
        # Clear MPS cache
        if torch.backends.mps.is_available():
            torch.mps.empty_cache()
            
        # Aggressive mode for SD 3.5
        if aggressive:
            gc.collect()
            time.sleep(0.5)  # Give system time to release memory
            if torch.backends.mps.is_available():
                torch.mps.empty_cache()
                
    except Exception as e:
        print(f"⚠️  Memory cleanup warning: {e}")

def get_memory_info():
    """Get current memory usage information"""
    try:
        process = psutil.Process()
        mem_info = process.memory_info()
        virtual_mem = psutil.virtual_memory()
        
        return {
            "process_rss_gb": mem_info.rss / (1024**3),
            "process_vms_gb": mem_info.vms / (1024**3),
            "system_used_gb": virtual_mem.used / (1024**3),
            "system_available_gb": virtual_mem.available / (1024**3),
            "system_percent": virtual_mem.percent
        }
    except Exception as e:
        return {"error": str(e)}

def log_memory_status(label=""):
    """Log current memory status"""
    mem_info = get_memory_info()
    if "error" not in mem_info:
        print(f"💾 Memory [{label}]: Process={mem_info['process_rss_gb']:.1f}GB, "
              f"System={mem_info['system_used_gb']:.1f}GB/{mem_info['system_used_gb'] + mem_info['system_available_gb']:.1f}GB "
              f"({mem_info['system_percent']:.1f}%)")
    else:
        print(f"⚠️  Could not read memory info: {mem_info['error']}")

class ImageGenerator:
    def __init__(self, args):
        self.args = args
        self.device = "mps"
        # Use float32 on MPS to avoid VAE decode issues
        self.dtype = torch.float32
        self.pipeline = None
        self.refiner_pipeline = None  # Keep track of refiner separately
        self.is_sd3 = False  # Track if using SD 3.5
        self.metadata = {
            "device": self.device,
            "dtype": str(self.dtype),
            "failures": [],
            "warnings": []
        }
        
        # Log initial memory state
        log_memory_status("Startup")
        
        self.apply_quality_preset()  # Apply preset if specified (after metadata init)
    
    def apply_quality_preset(self):
        """Apply quality preset if specified"""
        if not hasattr(self.args, 'quality') or not self.args.quality:
            return
        
        preset_name = self.args.quality
        if preset_name not in QUALITY_PRESETS:
            print(f"Warning: Unknown quality preset '{preset_name}', ignoring")
            return
        
        preset = QUALITY_PRESETS[preset_name]
        print(f"Applying quality preset: {preset_name}")
        print(f"  → {preset['description']}")
        
        # Apply preset settings (don't override if user explicitly set them)
        if not self.args.model:
            self.args.model = preset['model']
            print(f"  → Model: {preset['model']}")
        
        if not hasattr(self.args, 'steps_override') or not self.args.steps_override:
            self.args.steps = preset['steps']
            print(f"  → Steps: {preset['steps']}")
        
        if not self.args.refiner and preset['refiner']:
            self.args.refiner = preset['refiner']
            print(f"  → Refiner: {preset['refiner']}")
        
        if not self.args.upscale and preset.get('upscale'):
            self.args.upscale = preset['upscale']
            print(f"  → Upscale: {preset['upscale']}x")
        
        # Apply LoRA if preset specifies one
        if not self.args.lora and preset.get('lora'):
            self.args.lora = preset['lora']
            print(f"  → LoRA: {preset['lora']}")
        
        # Mark if this is SD 3.5 model
        if preset.get('use_sd3'):
            self.args.use_sd3 = True
        
        print()
        self.metadata["quality_preset"] = preset_name
        
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
        """Load base Stable Diffusion pipeline with memory management"""
        from diffusers import StableDiffusionPipeline, StableDiffusionXLPipeline, DiffusionPipeline
        
        model_name = self.args.model if self.args.model else "Lykon/DreamShaper-8"
        
        # Detect model type
        is_sdxl = "xl" in model_name.lower()
        is_sd3 = "3.5" in model_name or "3-5" in model_name or hasattr(self.args, 'use_sd3')
        self.is_sd3 = is_sd3
        
        # Aggressive memory cleanup before loading large models
        if is_sd3 or is_sdxl:
            print("🧹 Preparing memory for large model...")
            cleanup_memory(aggressive=True)
            log_memory_status("Before model load")
        
        def load_fn():
            print(f"Loading model: {model_name}")
            
            if is_sd3:
                print("  → Detected SD 3.5 model (gated - requires HF authentication)")
                print("  → Run ./login-hf.sh if not authenticated")
                print("  → Enabling aggressive memory optimization for SD 3.5")
                
                # Clean memory before loading
                cleanup_memory(aggressive=True)
                
                # Load with memory-efficient settings
                pipe = DiffusionPipeline.from_pretrained(
                    model_name,
                    torch_dtype=torch.bfloat16,
                    device_map=self.device,
                    low_cpu_mem_usage=True,
                    use_safetensors=True
                )
                
                # Enable memory optimizations
                try:
                    pipe.enable_attention_slicing(slice_size="auto")
                    print("  → Enabled attention slicing")
                except:
                    pass
                
                try:
                    pipe.enable_vae_slicing()
                    print("  → Enabled VAE slicing")
                except:
                    pass
                    
                # Clean memory after loading
                cleanup_memory(aggressive=True)
                
            elif is_sdxl:
                print("  → Detected SDXL model, using StableDiffusionXLPipeline")
                
                # Clean before loading
                cleanup_memory(aggressive=False)
                
                pipe = StableDiffusionXLPipeline.from_pretrained(
                    model_name,
                    torch_dtype=self.dtype,
                    variant="fp16" if self.dtype == torch.float16 else None,
                    use_safetensors=True,
                    low_cpu_mem_usage=True
                )
                pipe = pipe.to(self.device)
                pipe.enable_attention_slicing()
                
                try:
                    pipe.enable_vae_slicing()
                    print("  → Enabled VAE slicing")
                except:
                    pass
                    
            else:
                print("  → Using StableDiffusionPipeline")
                pipe = StableDiffusionPipeline.from_pretrained(
                    model_name,
                    torch_dtype=self.dtype,
                    safety_checker=None,
                    requires_safety_checker=False,
                    low_cpu_mem_usage=True
                )
                pipe = pipe.to(self.device)
                pipe.enable_attention_slicing()
            
            return pipe
        
        pipeline, success = self.retry_operation("Base Pipeline Load", load_fn)
        
        if not success:
            raise RuntimeError("Failed to load base pipeline after multiple retries")
        
        self.pipeline = pipeline
        self.metadata["model"] = model_name
        
        if is_sd3:
            self.metadata["pipeline_type"] = "DiffusionPipeline (SD 3.5)"
            self.metadata["memory_optimizations"] = "attention_slicing,vae_slicing,aggressive_cleanup"
        elif is_sdxl:
            self.metadata["pipeline_type"] = "StableDiffusionXLPipeline"
            self.metadata["memory_optimizations"] = "attention_slicing,vae_slicing"
        else:
            self.metadata["pipeline_type"] = "StableDiffusionPipeline"
            self.metadata["memory_optimizations"] = "attention_slicing"
        
        # Log memory after loading
        log_memory_status("After model load")
        
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
        """Generate images with retry logic and memory management"""
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
        
        # Memory cleanup before generation (especially important for SD 3.5)
        if self.is_sd3:
            print("🧹 Cleaning memory before generation...")
            cleanup_memory(aggressive=True)
            log_memory_status("Before generation")
        
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
        
        # Memory cleanup after generation
        if self.is_sd3:
            print("🧹 Cleaning memory after generation...")
            cleanup_memory(aggressive=True)
            log_memory_status("After generation")
        else:
            cleanup_memory(aggressive=False)
        
        return images
    
    def upscale_image(self, image):
        """Upscale image using simple PIL resize (SD upscaler has MPS issues)"""
        if not self.args.upscale or self.args.upscale == 1:
            return image
        
        print(f"⚠️  Note: Using PIL upscaling instead of SD upscaler (MPS memory issues)")
        print(f"   Upscaling {self.args.upscale}x with LANCZOS algorithm...")
        
        def upscale_fn():
            from PIL import Image
            
            # Get current size
            width, height = image.size
            
            # Calculate new size
            new_width = width * self.args.upscale
            new_height = height * self.args.upscale
            
            print(f"   {width}x{height} → {new_width}x{new_height}")
            
            # Use high-quality LANCZOS resampling
            upscaled = image.resize((new_width, new_height), Image.LANCZOS)
            
            return upscaled
        
        result, success = self.retry_operation("Upscaling", upscale_fn, max_retries=1)
        
        if success:
            self.metadata["upscale"] = self.args.upscale
            self.metadata["upscale_method"] = "PIL_LANCZOS"
            return result
        else:
            self.log_warning(f"Upscaling failed - saving base resolution image")
            self.metadata["upscale"] = "failed"
            return image
    
    def refine_image(self, image):
        """Refine image using refiner model with memory management"""
        if not self.args.refiner:
            return image
        
        # Unload main pipeline to free memory for refiner (especially for SD 3.5)
        if self.is_sd3:
            print("🧹 Unloading main pipeline to free memory for refiner...")
            if self.pipeline is not None:
                del self.pipeline
                self.pipeline = None
            cleanup_memory(aggressive=True)
            log_memory_status("Before refiner load")
        
        def refine_fn():
            from diffusers import StableDiffusionImg2ImgPipeline, StableDiffusionXLImg2ImgPipeline
            
            print(f"Refining with model: {self.args.refiner}")
            
            # Check if this is an SDXL refiner
            is_sdxl = "xl" in self.args.refiner.lower()
            
            if is_sdxl:
                # Use SDXL pipeline for SDXL models
                refiner = StableDiffusionXLImg2ImgPipeline.from_pretrained(
                    self.args.refiner,
                    torch_dtype=self.dtype,
                    variant="fp16" if self.dtype == torch.float16 else None,
                    low_cpu_mem_usage=True
                )
            else:
                # Use standard pipeline for SD 1.5/2.x models
                refiner = StableDiffusionImg2ImgPipeline.from_pretrained(
                    self.args.refiner,
                    torch_dtype=self.dtype,
                    safety_checker=None,
                    requires_safety_checker=False,
                    low_cpu_mem_usage=True
                )
            
            refiner = refiner.to(self.device)
            refiner.enable_attention_slicing()
            
            try:
                refiner.enable_vae_slicing()
            except:
                pass
            
            # Store refiner for later cleanup
            self.refiner_pipeline = refiner
            
            refined = refiner(
                prompt=self.args.prompt,
                image=image,
                strength=0.3,
                num_inference_steps=20
            ).images[0]
            
            # Cleanup refiner after use
            if self.is_sd3:
                del refiner
                self.refiner_pipeline = None
                cleanup_memory(aggressive=True)
            
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
        """Main execution flow with comprehensive memory management"""
        start_time = time.time()
        
        try:
            # Check available memory before starting (for SD 3.5)
            if self.is_sd3 or (hasattr(self.args, 'use_sd3') and self.args.use_sd3):
                mem_info = get_memory_info()
                if "error" not in mem_info:
                    available_gb = mem_info["system_available_gb"]
                    if available_gb < 30:
                        print(f"⚠️  WARNING: Low memory detected ({available_gb:.1f}GB available)")
                        print(f"   SD 3.5 requires 36GB+ RAM. Generation may fail or be very slow.")
                        print(f"   Consider using --quality 4k-ultra (SDXL) instead for better performance.")
                        self.log_warning(f"Low memory: {available_gb:.1f}GB available (36GB+ recommended for SD 3.5)")
            
            # Load base pipeline
            self.load_base_pipeline()
            
            # Apply LoRA if specified
            if self.args.lora:
                self.apply_lora()
                cleanup_memory(aggressive=self.is_sd3)
            
            # Setup ControlNet if specified
            control_image = self.setup_controlnet()
            if control_image is not None:
                cleanup_memory(aggressive=self.is_sd3)
            
            # Generate images
            images = self.generate_images(control_image)
            
            # Post-process each image
            final_images = []
            for i, image in enumerate(images):
                print(f"\n📸 Processing image {i+1}/{len(images)}")
                
                # Refine
                if self.args.refiner:
                    image = self.refine_image(image)
                    cleanup_memory(aggressive=self.is_sd3)
                
                # Upscale
                if self.args.upscale and self.args.upscale > 1:
                    image = self.upscale_image(image)
                    cleanup_memory(aggressive=self.is_sd3)
                
                final_images.append(image)
            
            # Final cleanup before saving
            if self.pipeline is not None:
                del self.pipeline
                self.pipeline = None
            if self.refiner_pipeline is not None:
                del self.refiner_pipeline
                self.refiner_pipeline = None
            cleanup_memory(aggressive=True)
            
            # Save all images
            generation_time = time.time() - start_time
            saved_paths = []
            
            for i, image in enumerate(final_images, 1):
                path = self.save_image(image, i, generation_time)
                saved_paths.append(path)
            
            # Log final memory state
            log_memory_status("Complete")
            
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
            
            # Emergency cleanup
            try:
                if self.pipeline is not None:
                    del self.pipeline
                if self.refiner_pipeline is not None:
                    del self.refiner_pipeline
                cleanup_memory(aggressive=True)
            except:
                pass
            
            return 1

def main():
    parser = argparse.ArgumentParser(
        description="SD-Generate: Robust Text-to-Image Generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Quality Presets (--quality):
  fast          Fast generation, good quality (SD 1.5)
  quality       High quality with refiner (SD 1.5 + refiner)
  hd            High quality with 2x upscaling (SD 1.5 + upscale → 1024px)
  max           Maximum quality (SD 1.5 + refiner + 2x upscale → 1024px)
  ultra         Ultra quality (SDXL + refiner, slower, needs 16GB RAM)
  ultra-hd      Ultra HD (SDXL + refiner + 2x upscale → 2048px)
  4k            4K quality (SD 1.5 + refiner + 4x upscale → 2048px)
  4k-ultra      4K Ultra (SDXL + refiner + 4x upscale → 4096px)
  photorealistic Photorealistic (Realistic Vision + refiner + 2x)
  ultra-realistic Ultra realistic with detail LoRA (NEW!)
  cinematic     Cinematic film look with LoRA (NEW!)

Examples:
  generate "a cat" --quality fast
  generate "a dragon" --quality max --n 4
  generate "portrait" --quality ultra-realistic
  generate "movie scene" --quality cinematic
  generate "landscape" --quality 4k-ultra
        """
    )
    
    # Core arguments
    parser.add_argument("prompt", type=str, help="Text prompt for generation")
    
    # Pro mode - SD 3.5 Large Turbo (shortcut)
    parser.add_argument("--pro", action="store_true", 
                       help="Use SD 3.5 Large Turbo (best quality, fast, 8 steps, requires HF auth)")
    
    # Quality preset (easy mode!)
    parser.add_argument("--quality", type=str, 
                       choices=["fast", "quality", "hd", "max", "ultra", "ultra-hd", "4k", "4k-ultra", "photorealistic", "ultra-realistic", "cinematic", "lcm"],
                       help="Quality preset (auto-configures model, refiner, upscaler, LoRA)")
    
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
    parser.add_argument("--upscale", type=int, choices=[2, 4], help="Upscale factor (uses stabilityai/stable-diffusion-x4-upscaler)")
    parser.add_argument("--refiner", type=str, help="Refiner model name (e.g., 'runwayml/stable-diffusion-v1-5' for SD1.5 compatible)")
    
    args = parser.parse_args()
    
    # Handle --pro flag (shortcut for SD 3.5 Large Turbo)
    if args.pro:
        if not args.model:
            args.model = "stabilityai/stable-diffusion-3.5-large-turbo"
        if not hasattr(args, 'steps_override') or not args.steps_override:
            args.steps = 8  # Optimized for Turbo model (4-8 steps recommended)
        args.use_sd3 = True
        print("Pro mode enabled: Using SD 3.5 Large Turbo")
        print("⚠️  REQUIREMENTS:")
        print("   • 20GB+ RAM recommended (works on all Apple Silicon)")
        print("   • HF authentication (run ./login-hf.sh)")
        print("   • Must accept license at: https://huggingface.co/stabilityai/stable-diffusion-3.5-large-turbo")
        print("   • ~2-5 min per image (much faster than regular SD 3.5)")
        print("\n🧠 MEMORY OPTIMIZATIONS ENABLED:")
        print("   • Aggressive memory cleanup between stages")
        print("   • Attention slicing and VAE slicing")
        print("   • Pipeline unloading before refiner/upscale")
        print("   • Continuous memory monitoring")
        print()
    
    # Track if user explicitly set steps (to avoid overriding with preset)
    # Check if steps was explicitly passed by user
    import sys
    args.steps_override = '--steps' in sys.argv
    
    # Validation
    if args.n < 1:
        print("Error: --n must be at least 1")
        return 1
    
    # Create generator and run
    generator = ImageGenerator(args)
    return generator.run()

if __name__ == "__main__":
    sys.exit(main())
