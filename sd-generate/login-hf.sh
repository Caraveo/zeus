#!/bin/bash

echo "======================================================================"
echo "  Hugging Face Login - Required for Gated Models"
echo "======================================================================"
echo ""
echo "Some models (like SD 3.5) require authentication and license acceptance."
echo ""
echo "Steps:"
echo "1. Create account at https://huggingface.co"
echo "2. Accept model license at https://huggingface.co/stabilityai/stable-diffusion-3.5-large"
echo "3. Get token from https://huggingface.co/settings/tokens"
echo ""
echo "Logging in with huggingface-cli..."
echo ""

source "$(dirname "$0")/venv/bin/activate"

huggingface-cli login

echo ""
echo "======================================================================"
echo "  Login Complete!"
echo "======================================================================"
echo ""
echo "You can now use gated models like SD 3.5:"
echo "  generate \"prompt\" --model \"stabilityai/stable-diffusion-3.5-large\""
echo ""
echo "Or add SD 3.5 preset (coming soon):"
echo "  generate \"prompt\" --quality sd3.5"
echo ""
echo "======================================================================"
