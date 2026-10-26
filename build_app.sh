#!/usr/bin/env bash
set -e

echo "=== 1. Generating Apple .icns Icon ==="
python make_icon.py

echo "=== 2. Compiling Standalone macOS App with PyInstaller ==="
pyinstaller --noconsole \
            --onedir \
            --windowed \
            --name "Winnie" \
            --icon "Winnie.icns" \
            --add-data "runner.py:." \
            --add-data "Winnie.png:." \
            --add-data "Winnie.icns:." \
            --hidden-import "AppKit" \
            --hidden-import "Foundation" \
            --hidden-import "objc" \
            --osx-bundle-identifier "com.winnie.ide" \
            --clean \
            main.py

echo "============================================="
echo "🎉 Build Complete!"
echo "Your standalone app is located at: dist/Winnie.app"
echo "You can drag it straight into /Applications!"
echo "============================================="
