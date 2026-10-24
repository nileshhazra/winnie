# 🐻 Winnie — Python for Everyone

A modern, lightweight, beginner-friendly Python IDE for macOS inspired by [Thonny](https://github.com/thonny/thonny). Built from scratch with **PySide6 (Qt for Python)**.

![macOS](https://img.shields.io/badge/platform-macOS-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-purple.svg)

---

## ✨ Features

- **🐾 Step-by-Step Visual Debugger**: Step through code line-by-line (`F7` / `⌘⌥S`). Watch an amber execution highlight and line pointer advance as you trace logic.
- **✦ Live Variables Inspector**: Real-time table tracking variable names, types, and values as code executes.
- **⚡ Safe Execution Engine**: Runs user code in an isolated subprocess (`QProcess`). Infinite loops or crashes never freeze the IDE.
- **💬 Interactive Terminal**: Supports user `input()` with real-time streaming standard I/O.
- **🎨 Dark & Light Modes**: Beautiful themes with modern monochromatic vector icons.
- **⌨️ Python Auto-Indentation**: Automatic 4-space indentation after colons (`:`), PEP 8 tab key, and smart backspacing.
- **🍎 Native macOS Integration**:
  - Unsaved dot (`●`) in the red close button and title bar.
  - Native macOS Menu Bar (`File` menu).
  - High-DPI Liquid Glass icon.

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| `⌘ ⏎` | **Run Script** |
| `F7` / `⌘ ⌥ S` | **Step Line-by-Line** (Debugger) |
| `⌘ .` or `⎋` | **Stop Execution** |
| `⌘ K` | **Clear Terminal & Variables** |
| `⌘ T` | **Toggle Dark / Light Theme** |
| `⌘ J` | **Toggle Bottom Terminal** |
| `⌘ L` | **Toggle Variables Panel** |
| `⌘ +` / `⌘ -` | **Zoom In / Out** (Fonts) |
| `⌘ 0` | **Reset Font Zoom** |
| `⌘ S` / `⌘ ⇧ S` | **Save / Save As** |
| `⌘ O` / `⌘ N` | **Open / New File** |

---

## 🛠️ Running from Source

### Prerequisites
- macOS (Apple Silicon or Intel)
- Python 3.10+

### Setup
```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/winnie.git
cd winnie

# 2. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch Winnie
python main.py
```

---

## 📦 Building Standalone `Winnie.app`

```bash
# Build standalone macOS .app bundle
bash build_app.sh

# Open the compiled app in Finder
open dist
```

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
