# Kasa TUI Setup

This guide explains how to make the `ktui` command accessible from anywhere on your system.

## 1. Prerequisites

Ensure you have a virtual environment set up and dependencies installed:

```bash
# Create venv if not exists
python3 -m venv venv
# Activate it
source venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```

## 2. Install as a CLI Tool

Install the package in "editable" mode. This creates the `ktui` command and ensures any changes you make to the code are reflected immediately:

```bash
pip install -e .
```

## 3. Enable Global Access

To run `ktui` from any directory without activating the virtual environment, follow one of these methods:

### Method A: Symlink to `~/bin` (Recommended)

If you have a `bin` directory in your home folder that is already in your `PATH`:

```bash
# Create the symlink (replace /path/to/kasa with your actual project path)
ln -sf /Users/shamik/Documents/kasa/venv/bin/ktui ~/bin/ktui
```

### Method B: Add to PATH in `.zshrc` or `.bashrc`

Add the virtual environment's `bin` directory directly to your shell's configuration:

```bash
# For Zsh (default on macOS)
echo 'export PATH="/Users/shamik/Documents/kasa/venv/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# For Bash
echo 'export PATH="/Users/shamik/Documents/kasa/venv/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## 4. Usage

Once configured, simply type:

```bash
ktui
```

This will launch the interactive TUI for discovering and controlling your Kasa devices.
