import os
import subprocess
import time

# Persistence Plugin for Termux-Slayer
# ⚡️👾 by🇭🇷PhonkAlphabet 👾⚡️

def install_persistence():
    """
    Dirty Trick: Installs a hidden cron job or bashrc hook for persistence.
    """
    print("[+] Installing Persistence Hook...")
    bashrc = os.path.expanduser("~/.bashrc")
    hook = "\n# Neural Link Persistence\nif [ -f ~/Termux-Slayer/slayer.py ]; then alias slayer='python3 ~/Termux-Slayer/slayer.py'; fi\n"
    
    with open(bashrc, "a") as f:
        f.write(hook)
    
    print("[✔] Persistence Hook Installed. Type 'slayer' from anywhere to launch.")

if __name__ == "__main__":
    install_persistence()
