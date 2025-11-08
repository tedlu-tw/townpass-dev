#!/bin/bash
# Fix SSL Certificate Issues on macOS

echo "🔧 Fixing SSL Certificate Issues on macOS..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "Found Python version: $PYTHON_VERSION"

# Try to find and run the Install Certificates command
CERT_SCRIPT="/Applications/Python ${PYTHON_VERSION}/Install Certificates.command"

if [ -f "$CERT_SCRIPT" ]; then
    echo "✓ Found certificate installer"
    echo "Running: $CERT_SCRIPT"
    "$CERT_SCRIPT"
    echo ""
    echo "✅ SSL certificates have been installed"
else
    echo "⚠️  Certificate installer not found at: $CERT_SCRIPT"
    echo ""
    echo "Alternative solutions:"
    echo "1. Install certifi package:"
    echo "   pip install --upgrade certifi"
    echo ""
    echo "2. Or run the scripts with verify_ssl=False (not recommended for production)"
fi
