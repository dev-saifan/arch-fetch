# archfetch

A personalized, ultra-fast system fetch utility designed specifically for Arch Linux. Built in Python and compiled ahead-of-time with Nuitka for instant execution.

## Features

- **Blazing Fast:** Zero multi-distro detection bloat—parses system info directly from `/proc` and local pacman state.
- **Custom Hardware Labels:** Cleaned-up metric output, including custom integrated graphics labeling and exact RAM calculations.
- **Aesthetic Terminal Grid:** Perfectly aligned custom Arch Linux ASCII art.

---

## Quick Installation

You can download and install the pre-compiled binary directly to `/usr/local/bin` with this single command:

```bash
sudo wget -O /usr/local/bin/archfetch https://github.com/dev-saifan/arch-fetch/releases/latest/download/archfetch && sudo chmod +x /usr/local/bin/archfetch
```

Once installed, simply run it from anywhere in your terminal:

```bash
archfetch
```

---

## Local Compilation

If you prefer to compile the standalone binary locally from source using Nuitka:

1. Install dependencies:
   ```bash
   pip install nuitka patchelf
   ```

2. Compile:
   ```bash
   python3 -m nuitka --standalone --onefile --output-filename=archfetch code.py
   ```

3. Install:
   ```bash
   sudo install -Dm755 archfetch /usr/local/bin/archfetch
   ```
