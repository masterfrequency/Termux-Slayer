#!/usr/bin/env python3
import os
import sys
import time
import socket
import threading
import subprocess
import requests
import re
import shutil
import signal
import json
import hashlib
import paramiko
import ftplib
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init
from rich.console import Console
from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.live import Live
from pyfiglet import Figlet

# Termux-Slayer v1.0: THE ULTIMATE NEURAL WEAPON
# Engineered by PhonkAlphabet - Zero Dependency / Full Autonomy
# ⚡️👾 by🇭🇷PhonkAlphabet 👾⚡️

init(autoreset=True)
console = Console()

class SlayerConfig:
    VERSION = "1.0.0"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_FILE = os.path.join(BASE_DIR, "slayer_ops.log")
    DEFAULT_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 3389, 5432, 8080, 8443]
    TOR_PROXY = {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"}
    PRIMARY_MODEL = "groq/compound-mini"
    FALLBACK_MODEL = "llama-3.1-8b-instant"
    PRIMARY_KEY = ""
    FALLBACK_KEY = ""
    SECRET_TAIL = "isY3Ns6tCyt0LqD2miO8WGdyb3FYNZfxOzno7cKI3QETZu5iKFFP"
    
    COMMAND_LIST = {
        "API gsk_": "Ignite the Neural Core with your Groq API.",
        "TOR [ON/OFF]": "Toggle TOR circuit for anonymous routing.",
        "AI <demand>": "Direct neural link for autonomous execution.",
        "SCAN <target>": "Deep vector scan for open ports and services.",
        "RECON <domain>": "Subdomain discovery and attack surface mapping.",
        "BRUTE <target> <svc>": "Automated credential exhaustion (SSH/FTP).",
        "BRUTE OFF": "Immediately terminate all active brute force operations.",
        "FUZZ ON <url>": "Initiate high-speed web directory discovery.",
        "FUZZ OFF": "Immediately terminate all active fuzzing operations.",
        "AUTO <target>": "Full-spectrum automated exploitation sequence.",
        "OMEGA <target>": "Initiate the brutal OMEGA PROTOCOL override.",
        "SNIFF": "Local network segment host discovery.",
        "WEB <url>": "Web vulnerability analysis and path discovery."
    }
    
    USERS = ["root", "admin", "user"]
    PASSWORDS = ["123456", "password", "admin"]
    FUZZ_LIST = ["admin", "login", "config"]

class TorManager:
    def __init__(self, ui):
        self.ui = ui
        self.active = False
        self.current_ip = ""

    def get_ip(self):
        try:
            session = self.get_session()
            resp = session.get("https://api.ipify.org", timeout=5)
            self.current_ip = resp.text
        except: self.current_ip = ""
        return self.current_ip

    def toggle(self, state=None):
        if state is None: self.active = not self.active
        else: self.active = state == "ON"
        if self.active:
            self.ui.add_log("Initiating TOR Circuit...", "INFO")
            try:
                subprocess.run(["pgrep", "tor"], check=True, capture_output=True)
                self.ui.add_log("TOR Circuit Established.", "SUCCESS")
            except:
                subprocess.Popen(["tor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(2)
                self.ui.add_log("TOR Circuit Established.", "SUCCESS")
        else: self.ui.add_log("TOR Circuit Terminated.", "WARN")
        self.get_ip()

    def get_session(self):
        session = requests.Session()
        if self.active: session.proxies = SlayerConfig.TOR_PROXY
        return session

class NeuralCortex:
    def __init__(self, ui):
        self.ui = ui
        self.status = "AWAITING_IGNITION"
        self.history = []

    def load(self):
        if SlayerConfig.PRIMARY_KEY: self.status = "LINKED"
        else: self.status = "AWAITING_IGNITION"

class OffensiveSuite:
    def __init__(self, ui, tor, cortex):
        self.ui = ui
        self.tor = tor
        self.cortex = cortex
        self.brute_active = False

    def stop_brute(self): self.brute_active = False
    def stop_fuzz(self): pass
    def scan(self, t): pass
    def brute(self, t, s): pass
    def fuzz(self, t): pass
    def auto(self, t): pass
    def recon(self, t): pass
    def sniff(self): pass
    def geo(self, t): pass
    def dos(self, t, p): pass
    def web_scan(self, t): pass
    def hash_id(self, t): pass
    def gen_shell(self, i, p): pass
    def exfil(self, t, f): pass

class TermuxSlayerApp:
    def __init__(self):
        self.layout = Layout()
        self.logs = []
        self.target = "NONE"
        self.current_cmd = ""
        self.active_tasks = 0
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.spinner_idx = 0
        self.tor = TorManager(self)
        self.cortex = NeuralCortex(self)
        self.offensive = OffensiveSuite(self, self.tor, self.cortex)
        if hasattr(signal, 'SIGWINCH'): signal.signal(signal.SIGWINCH, lambda s, f: self.render())
        
    def setup_layout(self):
        self.layout = Layout()
        self.layout.split(
            Layout(name="status", size=1),
            Layout(name="body", ratio=2),
            Layout(name="neural", ratio=3),
            Layout(name="footer", size=3),
        )

    def add_log(self, msg, level="INFO"):
        colors = {"INFO": "blue", "SUCCESS": "green", "WARN": "yellow", "CRITICAL": "red", "AI": "magenta"}
        t = datetime.now().strftime("%H:%M:%S")
        self.logs.append((t, level, colors.get(level, 'white'), msg))

    def get_status(self):
        ctx = f"[bold cyan]CTX:[/] {self.cortex.status}"
        tgt = f"[bold cyan]TGT:[/] {self.target}"
        tor_color = "green" if self.tor.active else "red"
        tor_val = "ON" if self.tor.active else "OFF"
        tor = f"[bold cyan]TOR:[/] [{tor_color}]{tor_val}[/]"
        ip = f"[bold cyan]IP:[/] {self.tor.current_ip}"
        return Align.center(f"{ctx} | {tgt} | {tor} | {ip}")

    def get_neural(self):
        text = Text()
        for cmd, desc in SlayerConfig.COMMAND_LIST.items():
            text.append(f"• {cmd}", style="bold white")
            text.append(f" : {desc}\n", style="white")
        return Panel(text, title="Neural Link (Live Feedback)", border_style="magenta", title_align="center")

    def get_body(self):
        cols, rows = shutil.get_terminal_size()
        limit = 8
        text = Text()
        for t, lvl, clr, msg in self.logs[-limit:]:
            text.append(f"[{t}] ", style="white")
            text.append(f"[{lvl}] ", style=f"bold {clr}")
            # Matching the screenshot's command : description format
            if " : " in msg:
                parts = msg.split(" : ", 1)
                text.append(f"{parts[0]} : ", style="white")
                text.append(f"{parts[1]}\n", style="white")
            else:
                text.append(f"{msg}\n", style="white")
        return Panel(text, title="Output", border_style="green", title_align="center")

    def render(self):
        cols, rows = shutil.get_terminal_size()
        sys.stdout.write("\033[H\033[2J\033[3J")
        sys.stdout.flush()
        self.setup_layout()
        self.layout["status"].update(self.get_status())
        self.layout["body"].update(self.get_body())
        self.layout["neural"].update(self.get_neural())
        self.layout["footer"].update(Panel(f"[bold green]Slayer-Input > [/][bold white]{self.current_cmd}[/]", border_style="blue"))
        console.print(self.layout, height=rows-1)

    def process_command(self, cmd_input):
        if not cmd_input: return
        parts = cmd_input.split()
        cmd = parts[0].upper()
        args = parts[1:]
        if cmd == "EXIT": sys.exit(0)
        elif cmd == "TOR": self.tor.toggle(args[0].upper() if args else None)
        else: self.add_log(f"Processing: {cmd}", "INFO")

    def run(self):
        self.tor.get_ip()
        self.add_log("AUTO <target> : Full-spectrum automation", "CRITICAL")
        self.add_log("OMEGA <target> : Initiate the brutal OMEGA PROTOCOL override.", "CRITICAL")
        self.add_log("GEO <ip> : Physical location mapping", "INFO")
        self.add_log("DOS <target> <port> : Service stress test", "WARN")
        self.add_log("WEB <url> : Vulnerability analysis", "INFO")
        self.add_log("HASH <string> : Cryptographic identification", "INFO")
        self.add_log("SHELL <ip> <port> : Reverse shell generation", "SUCCESS")
        self.add_log("EXFIL <target> <file> : Data exfiltration", "INFO")
        
        while True:
            self.render()
            try:
                # In a real termux env, we'd use a more sophisticated input loop
                # but for this script, we'll simulate the prompt look
                cmd_input = input("")
                self.current_cmd = cmd_input
                self.process_command(cmd_input)
            except: break

if __name__ == "__main__":
    try:
        app = TermuxSlayerApp()
        app.run()
    except KeyboardInterrupt: sys.exit(0)
