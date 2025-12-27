# Hades II Save Manager (哈迪斯 II 存档管理器)

![UI Mockup](C:/Users/Administrator/.gemini/antigravity/brain/59e790bf-f980-405b-be41-10e3abd0eace/ui_mockup_hades_save_manager_png_1766834126351.png)

A lightweight, visually immersive desktop application for managing your **Hades II** save files. Built with Python and PySide6, this tool provides a safe and easy way to backup and restore your progress.

---

## 🌟 Features (功能特性)

- **📁 Smart Discovery**: Automatically detects your Hades II save directory on Windows.
- **🛡️ One-Click Backup**: Instantly archives your `Profile1` save files to a localized `bak` folder.
- **🔄 Easy Restoration**: Restore previously backed-up saves with a single click, protecting you from accidental progress loss.
- **🎨 Hades Aesthetic**: A custom UI theme inspired by the game's iconic dark and gold visual style.
- **⚡ Fast & Lightweight**: Minimal overhead, built with PySide6 for a smooth native experience.

---

## 🚀 Quick Start (快速开始)

### Prerequisites (前提条件)
- **Python 3.12+**
- **[uv](https://github.com/astral-sh/uv)** (Recommended package manager)

### Running from Source (直接运行)
1. Clone the repository or download the source code.
2. Open a terminal in the project directory.
3. Run the following command:
   ```bash
   uv run main.py
   ```

---

## 🛠️ Build Instructions (打包指南)

If you want to compile the application into a standalone executable (`.exe`):

1. Install development dependencies:
   ```bash
   uv sync --group dev
   ```
2. Run the PyInstaller build:
   ```bash
   uv run pyinstaller HadesSaveManager.spec
   ```
3. Your executable will be available in the `dist` directory.

---

## 📂 Project Structure (项目结构)

```text
.
├── main.py                # Main application logic & GUI
├── HadesSaveManager.spec  # PyInstaller configuration
├── pyproject.toml         # Project metadata & dependencies
└── README.md              # This file
```

---

## 📝 Usage Notes (使用说明)

- **Default Save Path**: The tool looks for saves in `~/Saved Games/Hades II`. You can manually select a different folder if your saves are stored elsewhere.
- **Backup Location**: Backups are stored in a folder named `bak` inside your selected save directory.

---

## 📜 License (许可)

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Developed with ❤️ for the Hades community.
