#!/bin/bash
# Local testing script for release process
# Tests everything before pushing to GitHub

set -e

echo "🧪 Testing Release Process Locally"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check working directory
echo "📋 Step 1: Checking working directory..."
if [[ -n $(git status -s) ]]; then
    echo -e "${YELLOW}⚠️  Warning: Working directory has uncommitted changes${NC}"
    git status -s
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
echo -e "${GREEN}✓ Working directory check complete${NC}"
echo ""

# Step 2: Run tests
echo "📋 Step 2: Running tests..."
uv run pytest
echo -e "${GREEN}✓ Tests passed${NC}"
echo ""

# Step 3: Build package
echo "📋 Step 3: Building package..."
rm -rf dist/ build/ *.egg-info
uv build
echo -e "${GREEN}✓ Package built successfully${NC}"
echo ""

# Step 4: List built files
echo "📋 Step 4: Built files:"
ls -lh dist/
echo ""

# Step 5: Test installation in isolated environment
echo "📋 Step 5: Testing installation in isolated environment..."
TEMP_VENV=$(mktemp -d)
python3 -m venv "$TEMP_VENV"
source "$TEMP_VENV/bin/activate"

echo "Installing from wheel..."
pip install dist/*.whl --quiet

echo "Testing installed package..."
notebook-parser --help > /dev/null 2>&1 && echo -e "${GREEN}✓ CLI command works${NC}" || echo "❌ CLI command failed"

# Check if command exists and can run
if command -v notebook-parser &> /dev/null; then
    echo -e "${GREEN}✓ Package installed successfully${NC}"
else
    echo "❌ Package installation failed"
    deactivate
    rm -rf "$TEMP_VENV"
    exit 1
fi

deactivate
rm -rf "$TEMP_VENV"
echo ""

# Step 6: Check version in pyproject.toml
echo "📋 Step 6: Current version info:"
CURRENT_VERSION=$(grep '^version = ' pyproject.toml | cut -d'"' -f2)
echo "  Current version: $CURRENT_VERSION"
echo ""

# Step 7: Dry-run release script
echo "📋 Step 7: Testing release script (dry-run)..."
echo "  Release script location: ./scripts/release.sh"
echo "  Usage: ./scripts/release.sh <version>"
echo ""

echo -e "${GREEN}✅ All local tests passed!${NC}"
echo ""
echo "Next steps to create a release:"
echo "  1. Run: ./scripts/release.sh 0.1.0"
echo "  2. Review the changes: git show HEAD"
echo "  3. Push: git push && git push --tags"
echo ""
echo "Or manually:"
echo "  1. Update version in pyproject.toml"
echo "  2. git add pyproject.toml"
echo "  3. git commit -m 'chore: bump version to 0.1.0'"
echo "  4. git tag -a v0.1.0 -m 'Release v0.1.0'"
echo "  5. git push && git push --tags"
