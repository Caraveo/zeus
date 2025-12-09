#!/bin/bash

echo "=================================="
echo "Testing Refiner & Upscaler"
echo "=================================="
echo ""

# Test 1: Basic generation (no refiner/upscaler)
echo "Test 1: Basic generation..."
./generate "a red apple on a table" --steps 20 --seed 42 --output ./test-outputs

echo ""
echo "Test 1 complete! ✓"
echo ""

# Test 2: With SD 1.5 refiner (compatible)
echo "Test 2: With SD 1.5 refiner (compatible with DreamShaper-8)..."
./generate "a blue sphere" --steps 20 --refiner "runwayml/stable-diffusion-v1-5" --seed 43 --output ./test-outputs

echo ""
echo "Test 2 complete! ✓"
echo ""

# Test 3: With upscaler 2x
echo "Test 3: With 2x upscaler..."
./generate "a green cube" --steps 20 --upscale 2 --seed 44 --output ./test-outputs

echo ""
echo "Test 3 complete! ✓"
echo ""

# Test 4: With both refiner and upscaler
echo "Test 4: With refiner AND upscaler (maximum quality)..."
./generate "a yellow pyramid" --steps 20 --refiner "runwayml/stable-diffusion-v1-5" --upscale 2 --seed 45 --output ./test-outputs

echo ""
echo "=================================="
echo "All tests complete! ✓"
echo "Check ./test-outputs/ for results"
echo "=================================="
