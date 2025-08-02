#!/bin/bash

# Build script for AI Language Tutor macOS application
# This script creates a .app bundle and optionally a .dmg file

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="AI Language Tutor"
BUNDLE_ID="com.andylaurito92.language-tutor"
VERSION="1.0.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${SCRIPT_DIR}/build"
DIST_DIR="${SCRIPT_DIR}/dist"

echo -e "${BLUE}🎓 Building AI Language Tutor for macOS${NC}"
echo -e "${BLUE}======================================${NC}"

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}❌ This script must be run on macOS${NC}"
    exit 1
fi

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo -e "${YELLOW}📦 PyInstaller not found. Installing...${NC}"
    pip install pyinstaller
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${BLUE}🐍 Python version: ${PYTHON_VERSION}${NC}"

# Clean previous builds
echo -e "${YELLOW}🧹 Cleaning previous builds...${NC}"
rm -rf "${BUILD_DIR}"
rm -rf "${DIST_DIR}"
rm -rf "${SCRIPT_DIR}/*.app"

# Install dependencies if requirements.txt exists
if [[ -f "${SCRIPT_DIR}/requirements_no_audio.txt" ]]; then
    echo -e "${YELLOW}📋 Installing dependencies...${NC}"
    pip install -r "${SCRIPT_DIR}/requirements_no_audio.txt" || {
        echo -e "${YELLOW}⚠️  Some dependencies failed to install, continuing...${NC}"
    }
fi

# Build the application
echo -e "${YELLOW}🔨 Building application with PyInstaller...${NC}"
cd "${SCRIPT_DIR}"

# Run PyInstaller with the spec file
pyinstaller --clean --noconfirm ai-language-tutor.spec

# Check if build was successful
if [[ -d "${DIST_DIR}/${APP_NAME}.app" ]]; then
    echo -e "${GREEN}✅ Application built successfully!${NC}"
    echo -e "${GREEN}📍 Location: ${DIST_DIR}/${APP_NAME}.app${NC}"
    
    # Get app size
    APP_SIZE=$(du -sh "${DIST_DIR}/${APP_NAME}.app" | cut -f1)
    echo -e "${BLUE}📏 App size: ${APP_SIZE}${NC}"
    
    # Test if the app can be launched (without actually opening it)
    echo -e "${YELLOW}🧪 Testing application...${NC}"
    if [[ -f "${DIST_DIR}/${APP_NAME}.app/Contents/MacOS/ai-language-tutor" ]]; then
        echo -e "${GREEN}✅ Executable found and ready${NC}"
    else
        echo -e "${RED}❌ Executable not found${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
fi

# Ask if user wants to create DMG
echo -e "${BLUE}📦 Create DMG for distribution? (y/n)${NC}"
read -r CREATE_DMG

if [[ "$CREATE_DMG" =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}📦 Creating DMG...${NC}"
    
    # Check if create-dmg is installed
    if ! command -v create-dmg &> /dev/null; then
        echo -e "${YELLOW}📦 create-dmg not found. Installing via Homebrew...${NC}"
        if command -v brew &> /dev/null; then
            brew install create-dmg
        else
            echo -e "${RED}❌ Homebrew not found. Please install create-dmg manually or install Homebrew${NC}"
            echo -e "${YELLOW}💡 You can install Homebrew from: https://brew.sh${NC}"
            echo -e "${YELLOW}💡 Then run: brew install create-dmg${NC}"
            exit 1
        fi
    fi
    
    DMG_NAME="${APP_NAME}-${VERSION}.dmg"
    
    # Create DMG
    create-dmg \
        --volname "${APP_NAME}" \
        --volicon "${SCRIPT_DIR}/ai-language-tutor.spec" \
        --window-pos 200 120 \
        --window-size 600 300 \
        --icon-size 100 \
        --icon "${APP_NAME}.app" 175 120 \
        --hide-extension "${APP_NAME}.app" \
        --app-drop-link 425 120 \
        "${DIST_DIR}/${DMG_NAME}" \
        "${DIST_DIR}/${APP_NAME}.app"
    
    if [[ -f "${DIST_DIR}/${DMG_NAME}" ]]; then
        echo -e "${GREEN}✅ DMG created successfully!${NC}"
        echo -e "${GREEN}📍 Location: ${DIST_DIR}/${DMG_NAME}${NC}"
        
        # Get DMG size
        DMG_SIZE=$(du -sh "${DIST_DIR}/${DMG_NAME}" | cut -f1)
        echo -e "${BLUE}📏 DMG size: ${DMG_SIZE}${NC}"
    else
        echo -e "${RED}❌ DMG creation failed${NC}"
    fi
fi

echo -e "${GREEN}🎉 Build process completed!${NC}"
echo -e "${BLUE}📂 Output directory: ${DIST_DIR}${NC}"
echo ""
echo -e "${YELLOW}📋 Next steps:${NC}"
echo -e "${YELLOW}  1. Test the app: open '${DIST_DIR}/${APP_NAME}.app'${NC}"
echo -e "${YELLOW}  2. Distribute the .app or .dmg file to users${NC}"
echo -e "${YELLOW}  3. For App Store distribution, you'll need to sign the app${NC}"
echo ""
echo -e "${BLUE}🔧 Notes:${NC}"
echo -e "${BLUE}  - The app includes all Python dependencies${NC}"
echo -e "${BLUE}  - Users don't need Python installed to run it${NC}"
echo -e "${BLUE}  - First launch may take a few seconds${NC}"