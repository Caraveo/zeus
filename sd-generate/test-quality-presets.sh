#!/bin/bash

echo "=================================="
echo "Testing Quality Presets"
echo "=================================="
echo ""
echo "This will test all quality presets with a simple prompt."
echo "Each test uses the same prompt and seed for comparison."
echo ""

PROMPT="a red apple on a wooden table, studio lighting"
SEED=42
OUTPUT="./test-quality-presets"

mkdir -p "$OUTPUT"

echo "Test 1: --quality fast"
./generate "$PROMPT" --quality fast --seed $SEED --output "$OUTPUT/fast"
echo ""

echo "Test 2: --quality quality"
./generate "$PROMPT" --quality quality --seed $SEED --output "$OUTPUT/quality"
echo ""

echo "Test 3: --quality hd"
./generate "$PROMPT" --quality hd --seed $SEED --output "$OUTPUT/hd"
echo ""

echo "Test 4: --quality max"
./generate "$PROMPT" --quality max --seed $SEED --output "$OUTPUT/max"
echo ""

echo "=================================="
echo "Basic tests complete! ✓"
echo ""
echo "Advanced tests (slower, more memory):"
echo ""

read -p "Run SDXL tests? (requires 16GB+ RAM) [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Test 5: --quality ultra"
    ./generate "$PROMPT" --quality ultra --seed $SEED --output "$OUTPUT/ultra"
    echo ""
    
    echo "Test 6: --quality ultra-hd"
    ./generate "$PROMPT" --quality ultra-hd --seed $SEED --output "$OUTPUT/ultra-hd"
    echo ""
fi

read -p "Run photorealistic test? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Test 7: --quality photorealistic"
    ./generate "professional photograph of an apple on a wooden table, studio lighting, 8k" --quality photorealistic --seed $SEED --output "$OUTPUT/photorealistic"
    echo ""
fi

echo "=================================="
echo "All tests complete! ✓"
echo "Check $OUTPUT/ for results"
echo "Compare the quality and file sizes!"
echo "=================================="
