# Building AI Language Tutor for macOS

This guide explains how to build the AI Language Tutor as a native macOS application that users can run without installing Python or dependencies.

## Overview

The build process creates:
- **`.app` bundle**: A native macOS application that can be run by double-clicking
- **`.dmg` file**: A disk image for easy distribution and installation

## Quick Start

### Automated Building (Recommended)

The easiest way to build the application is using the provided build script:

```bash
# Make the script executable (if needed)
chmod +x build_macos.sh

# Run the build script
./build_macos.sh
```

The script will:
1. Install required dependencies
2. Build the `.app` bundle using PyInstaller
3. Optionally create a `.dmg` file for distribution

### Manual Building

If you prefer to build manually:

```bash
# 1. Install PyInstaller
pip install pyinstaller

# 2. Install app dependencies (optional AI packages may fail)
pip install -r requirements_build.txt

# 3. Build the app
pyinstaller --clean --noconfirm ai-language-tutor.spec

# 4. Create DMG (optional)
brew install create-dmg
create-dmg \
  --volname "AI Language Tutor" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "AI Language Tutor.app" 175 120 \
  --hide-extension "AI Language Tutor.app" \
  --app-drop-link 425 120 \
  "dist/AI-Language-Tutor-1.0.0.dmg" \
  "dist/AI Language Tutor.app"
```

## Requirements

### System Requirements
- **macOS 10.13** or later
- **Python 3.8+** (for building only)
- **Homebrew** (for installing `create-dmg`)

### Build Dependencies
- `pyinstaller` - For creating the app bundle
- `create-dmg` - For creating DMG files (install via `brew install create-dmg`)

## File Structure

The build process uses these key files:

```
.
├── launcher.py              # Main launcher script
├── ai-language-tutor.spec   # PyInstaller configuration
├── build_macos.sh          # Automated build script
├── requirements_build.txt   # Essential dependencies for building
└── .github/workflows/build-macos.yml  # CI/CD workflow
```

### Key Files Explained

- **`launcher.py`**: The entry point that starts the Streamlit server and opens the browser
- **`ai-language-tutor.spec`**: PyInstaller specification defining what to include in the bundle
- **`build_macos.sh`**: Automated build script with interactive prompts
- **`requirements_build.txt`**: Minimal dependencies needed for the app to function

## Build Output

After building, you'll find:

```
dist/
├── AI Language Tutor.app    # The macOS application bundle
└── AI-Language-Tutor-1.0.0.dmg  # Distribution disk image (if created)
```

## GitHub Actions CI/CD

The repository includes a GitHub Actions workflow (`.github/workflows/build-macos.yml`) that automatically builds the application on:

- Push to `main` or `develop` branches
- New tags (creates releases)
- Manual workflow dispatch

### Artifacts

The CI creates these artifacts:
- **`AI-Language-Tutor-macOS-app`**: The `.app` bundle
- **`AI-Language-Tutor-macOS-dmg`**: The `.dmg` file

### Releases

When you create a new tag (e.g., `v1.0.0`), the workflow automatically creates a GitHub release with the DMG file attached.

## Distribution

### For End Users

1. **From .app bundle**: Users can copy the app to their Applications folder and run it
2. **From .dmg file**: Users mount the DMG and drag the app to Applications

### First Launch

- The app may take a few seconds to start on first launch
- macOS may show a security warning for unsigned apps
- Users may need to right-click → "Open" to bypass Gatekeeper

## Signing and Notarization (Optional)

For production distribution, consider:

1. **Code Signing**: Sign the app with an Apple Developer certificate
2. **Notarization**: Submit to Apple for notarization to avoid security warnings

```bash
# Example signing (requires Apple Developer account)
codesign --force --sign "Developer ID Application: Your Name" "dist/AI Language Tutor.app"

# Example notarization
xcrun notarytool submit "dist/AI-Language-Tutor-1.0.0.dmg" \
  --apple-id "your-apple-id@example.com" \
  --password "app-specific-password" \
  --team-id "YOUR_TEAM_ID" \
  --wait
```

## Troubleshooting

### Common Issues

1. **"App is damaged" error**: This happens with unsigned apps. Users should right-click → Open
2. **Missing dependencies**: Some AI packages may not install. The app will still work with basic functionality
3. **Large app size**: The bundled app includes Python and all dependencies (~200MB+)

### Build Failures

1. **PyInstaller not found**: Run `pip install pyinstaller`
2. **create-dmg not found**: Run `brew install create-dmg`
3. **Module import errors**: Some optional dependencies may fail - this is usually OK

### Testing the Build

```bash
# Test the built app
open "dist/AI Language Tutor.app"

# Check app contents
ls -la "dist/AI Language Tutor.app/Contents/"
```

## Customization

### App Icon

To add a custom icon:
1. Create an `.icns` file (macOS icon format)
2. Update the `icon` parameter in `ai-language-tutor.spec`
3. Rebuild the app

### App Information

Modify the `info_plist` section in `ai-language-tutor.spec` to customize:
- Bundle identifier
- Version numbers
- Copyright information
- System requirements

## Support

For issues with building or distributing the macOS app, please:
1. Check the troubleshooting section above
2. Review the GitHub Actions logs for CI builds
3. Open an issue in the repository with build logs