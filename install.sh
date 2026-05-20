#!/data/data/com.termux/files/usr/bin/bash

# TERMUX-SLAYER UNIVERSAL INSTALLER
# Engineered by PhonkAlphabet
# ⚡️👾 by🇭🇷PhonkAlphabet 👾⚡️

set -e

PURPLE='\033[0;35m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo -e "${PURPLE}"
cat << "EOF"
  _____  _    _  ____  _   _ _  __
 |  __ \| |  | |/ __ \| \ | | |/ /
 | |__) | |__| | |  | |  \| | ' / 
 |  ___/|  __  | |  | | . ` |  <  
 | |    | |  | | |__| | |\  | . \ 
 |_|    |_|  |_|\____/|_| \_|_|\_\

           _      _____  _    _          ____  ______ _______ 
     /\   | |    |  __ \| |  | |   /\   |  _ \|  ____|__   __|
    /  \  | |    | |__) | |__| |  /  \  | |_) | |__     | |   
   / /\ \ | |    |  ___/|  __  | / /\ \ |  _ <|  __|    | |   
  / ____ \| |____| |    | |  | |/ ____ \| |_) | |____   | |   
 /_/    \_\______|_|    |_|  |_/_/    \_\____/|______|  |_|   
EOF
echo -e "         -- NEURAL RED TEAM v1.0 --${NC}"
echo -e "         -- Engineered by PhonkAlphabet --\n"

# 1. Storage Setup
echo -e "${BLUE}[1/4] Initializing Storage...${NC}"
if [ -d "/sdcard" ]; then
    echo -e "${GREEN}[✔] Storage already linked.${NC}"
else
    termux-setup-storage
    sleep 2
fi

# 2. Dependency Injection
echo -e "${BLUE}[2/4] Injecting Core Dependencies...${NC}"
pkg update -y && pkg upgrade -y
pkg install -y git python clang make cmake ninja libffi openssl tur-repo rust lsd neofetch tor torsocks coreutils curl binutils libsodium -y

# 3. Python Neural Stack
echo -e "${BLUE}[3/4] Synchronizing Python Neural Stack...${NC}"
# Pre-install pynacl with system libsodium to bypass compilation bottlenecks
echo -e "${BLUE}[*] Hardening pynacl build environment...${NC}"
export SODIUM_INSTALL=system
pip install pynacl --break-system-packages
pip install colorama requests tqdm rich pyfiglet paramiko --break-system-packages

# 4. Finalizing & Auto-Run
echo -e "${BLUE}[4/4] Finalizing Installation...${NC}"
cd $HOME/Termux-Slayer
chmod +x slayer.py

# Explicit Python Verification
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[!] Python3 not found. Attempting emergency reinstall...${NC}"
    pkg install python -y
fi

echo -e "${GREEN}[✔] TERMUX-SLAYER ACTIVATED.${NC}"

# Reminder: Set your GROQ_API_KEY for the Neural Core
if [ -z "$GROQ_API_KEY" ]; then
    echo -e "${YELLOW}[!] WARNING: Neural Core requires ignition.${NC}"
    echo -e "${CYAN}[*] Use 'API <key>' inside Slayer to power up the brain.${NC}"
fi

echo -e "${PURPLE}Starting Termux-Slayer...${NC}"
sleep 2
python3 slayer.py
