#!/usr/bin/env python3
"""Test SD 3.5 with MPS and memory management"""

import os
import sys
import torch

# Force MPS environment
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = ""

print("="*70)
print("  SD 3.5 MPS Test with Memory Management")
print("="*70)
print()

# Check MPS
print("🔍 System Check:")
print(f"  PyTorch version: {torch.__version__}")
print(f"  MPS available: {torch.backends.mps.is_available()}")
print(f"  MPS built: {torch.backends.mps.is_built()}")
print()

# Check memory
try:
    import psutil
    process = psutil.Process()
    mem = psutil.virtual_memory()
    print(f"💾 Memory Status:")
    print(f"  System total: {mem.total / (1024**3):.1f} GB")
    print(f"  System available: {mem.available / (1024**3):.1f} GB")
    print(f"  System used: {mem.used / (1024**3):.1f} GB ({mem.percent:.1f}%)")
    print()
    
    # Check if we have enough RAM for SD 3.5
    if mem.available < 30:
        print(f"⚠️  WARNING: Only {mem.available / (1024**3):.1f}GB available")
        print(f"   SD 3.5 requires 36GB+ RAM")
        print(f"   Test may fail or be very slow")
        print()
except ImportError:
    print("⚠️  psutil not installed - cannot check memory")
    print()

print("🚀 Starting SD 3.5 test with 8 steps (fast test)...")
print()

# Now run the actual generation
sys.exit(os.system(f'{sys.executable} generate.py "a simple red apple on white background" --model "stabilityai/stable-diffusion-3.5-large" --steps 8 --seed 42 --output test_outputs'))
