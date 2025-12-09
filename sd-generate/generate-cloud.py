#!/usr/bin/env python3
"""
SD-Generate Cloud: Fast generation using Hugging Face Inference API
Default mode - uses fal-ai provider for fast cloud generation
"""

import os
import sys
import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from huggingface_hub import InferenceClient

def main():
    parser = argparse.ArgumentParser(
        description="SD-Generate Cloud: Fast Text-to-Image via Hugging Face"
    )
    
    parser.add_argument("prompt", type=str, help="Text prompt for generation")
    parser.add_argument("--model", type=str, default="stabilityai/stable-diffusion-3.5-large",
                       help="Model to use (default: SD 3.5 Large)")
    parser.add_argument("--output", type=str, default="./outputs", help="Output directory")
    parser.add_argument("--n", type=int, default=1, help="Number of images")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--negative-prompt", type=str, help="Negative prompt")
    
    args = parser.parse_args()
    
    # Check for API key
    api_key = os.environ.get("HF_TOKEN")
    if not api_key:
        print("Error: HF_TOKEN environment variable not set")
        print("Get your token from: https://huggingface.co/settings/tokens")
        print("Then run: export HF_TOKEN='your-token-here'")
        return 1
    
    # Create client
    client = InferenceClient(
        provider="fal-ai",
        api_key=api_key
    )
    
    print(f"Generating {args.n} image(s) with {args.model}...")
    print(f"Prompt: {args.prompt}")
    if args.negative_prompt:
        print(f"Negative: {args.negative_prompt}")
    print()
    
    # Generate images
    start_time = time.time()
    
    for i in range(args.n):
        try:
            print(f"[{i+1}/{args.n}] Generating...")
            
            # Generate image
            image = client.text_to_image(
                args.prompt,
                model=args.model,
                negative_prompt=args.negative_prompt
            )
            
            # Save image
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"output_{timestamp}_{i+1:03d}.png"
            json_filename = f"output_{timestamp}_{i+1:03d}.json"
            
            image_path = output_dir / filename
            json_path = output_dir / json_filename
            
            image.save(image_path)
            print(f"✓ Saved: {image_path}")
            
            # Save metadata
            metadata = {
                "prompt": args.prompt,
                "negative_prompt": args.negative_prompt,
                "seed": args.seed,
                "model": args.model,
                "provider": "fal-ai",
                "method": "cloud",
                "image_index": i + 1,
                "filename": filename,
                "generation_time": time.time() - start_time
            }
            
            with open(json_path, 'w') as f:
                json.dump(metadata, f, indent=2)
                
        except Exception as e:
            print(f"✗ Error generating image {i+1}: {e}")
            continue
    
    total_time = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"✓ Generation complete!")
    print(f"  Time: {total_time:.2f}s")
    print(f"  Images: {args.n}")
    print(f"{'='*60}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
