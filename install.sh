#!/data/data/com.termux/files/usr/bin/bash
clear
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║    TIKTOK FOLLOWER TERMUX BRUTAL v2.0   ║"
echo "║         By X - Quantum Hacker           ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Update termux
echo "[⚡] Updating Termux packages..."
pkg update -y && pkg upgrade -y

# Install dependencies
echo "[📦] Installing dependencies..."
pkg install -y python git nodejs curl wget nano proot

# Install Python packages
echo "[🐍] Installing Python packages..."
pip install --upgrade pip
pip install requests colorama prettytable tqdm

# Create directory
echo "[📁] Setting up directories..."
mkdir -p ~/tiktok-brutal
cd ~/tiktok-brutal

# Download main script
echo "[⬇️] Downloading main script..."
curl -L -o tiktok_follower.py https://raw.githubusercontent.com/example/tiktok-brutal/main/tiktok_follower.py
curl -L -o config.json https://raw.githubusercontent.com/example/tiktok-brutal/main/config.json

# Make executable
chmod +x tiktok_follower.py

# Create session file
echo "[🔑] Creating session file..."
cat > session.txt << EOF
# Paste your TikTok sessionid here
# How to get sessionid:
# 1. Open TikTok in Chrome/Firefox
# 2. Press F12 → Application → Cookies
# 3. Copy 'sessionid' value
# 
# Example: 
# sessionid=abc123def456ghi789
EOF

echo ""
echo "[✅] INSTALLATION COMPLETE!"
echo "[🚀] Run: cd ~/tiktok-brutal && python tiktok_follower.py"
echo ""
