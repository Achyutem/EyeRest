#!/bin/bash

set -e

REPO_URL="https://github.com/achyutem/eyeRest.git"
INSTALL_DIR="$HOME/.local/share/eyeRest"
DESKTOP_FILE="$HOME/.local/share/applications/Eyerest.desktop"

echo "🧠 Detecting OS and package manager..."

OS="$(uname)"
PM=""

# Detect OS and package manager
if [[ "$OS" == "Darwin" ]]; then
    OS_TYPE="macOS"
    PM="brew"
elif [[ -f /etc/arch-release ]]; then
    OS_TYPE="Arch Linux"
    PM="pacman"
elif command -v apt &>/dev/null; then
    OS_TYPE="Debian-based"
    PM="apt"
elif command -v dnf &>/dev/null; then
    OS_TYPE="Fedora"
    PM="dnf"
else
    echo "❌ Unsupported OS or package manager."
    exit 1
fi

echo "✅ OS detected: $OS_TYPE"
echo "📦 Package manager: $PM"

install_dependency() {
    local pkg="$1"
    echo "🔧 Installing $pkg..."
    case "$PM" in
        pacman) sudo pacman -S --noconfirm "$pkg" ;;
        apt) sudo apt update && sudo apt install -y "$pkg" ;;
        dnf) sudo dnf install -y "$pkg" ;;
        brew) brew install "$pkg" ;;
    esac
}

echo "🔍 Checking for Python 3..."
if ! command -v python3 &>/dev/null; then
    install_dependency "python3"
fi

echo "🔍 Checking for Tkinter..."
if ! python3 -c "import tkinter" &>/dev/null; then
    case "$PM" in
        pacman) install_dependency "tk" ;;
        apt) install_dependency "python3-tk" ;;
        dnf) install_dependency "python3-tkinter" ;;
        brew)
            install_dependency "tcl-tk"
            echo "⚠️ On macOS, you may need to configure PATH to use Homebrew's Python with Tk."
            ;;
    esac
fi

# Install EyeRest
if [[ -d "$INSTALL_DIR" ]]; then
    echo "ℹ️ $INSTALL_DIR already exists. Skipping clone."
else
    echo "📦 Cloning EyeRest into $INSTALL_DIR..."
    git clone "$REPO_URL" "$INSTALL_DIR" || {
        echo "❌ Failed to clone repository."
        exit 1
    }
fi

# Create desktop shortcut
echo "⚙️ Creating desktop launcher..."
mkdir -p "$(dirname "$DESKTOP_FILE")"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=EyeRest
Exec=python3 $INSTALL_DIR/eyeRest.py
Icon=preferences-desktop-display
Comment=Take eye breaks regularly
Terminal=false
Categories=Utility;
EOF

chmod +x "$DESKTOP_FILE"

echo "✅ EyeRest installed. Launch it from your app menu!"
