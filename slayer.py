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
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init
from rich.console import Console
from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.live import Live

# Termux-Slayer v1.0: THE ULTIMATE NEURAL WEAPON
# Engineered by PhonkAlphabet - Zero Dependency / Full Autonomy
# ⚡️👾 by🇭🇷PhonkAlphabet 👾⚡️

init(autoreset=True)
console = Console()

class SlayerConfig:
    VERSION = "1.0.0"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_FILE = os.path.join(BASE_DIR, "slayer_ops.log")
    TOR_PROXY = {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"}
    
    # Fragmented Neural Core Assembly
    CORE_A = "1iXBEeZeiy32Lo2B46km"
    CORE_B = "VThzNLFZVMqhf5UmF618"
    CORE_TAIL = "WGdyb3FY"
    CORE_S1 = "tcYOIBeISEIfl8rkkky9N2LV"
    CORE_S2 = "uZwYXmlTvd5voWlmlJEsk3ZC"
    
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

class TorManager:
    def __init__(self, app):
        self.app = app
        self.active = False
        self.current_ip = "Checking..."

    def get_ip(self):
        try:
            resp = requests.get("https://api.ipify.org", timeout=5, proxies=SlayerConfig.TOR_PROXY if self.active else None)
            self.current_ip = resp.text
        except: self.current_ip = "UNKNOWN"
        return self.current_ip

    def toggle(self, state=None):
        if state is None: self.active = not self.active
        else: self.active = state == "ON"
        if self.active:
            self.app.add_log("Initiating TOR Circuit...", "INFO")
            threading.Thread(target=self.get_ip).start()
        else: 
            self.app.add_log("TOR Circuit Terminated.", "WARN")
            threading.Thread(target=self.get_ip).start()

class NeuralCortex:
    def __init__(self):
        self.status = "AWAITING_IGNITION"
        self.history = []

class TermuxSlayerApp:
    def __init__(self):
        self.logs = []
        self.target = "NONE"
        self.current_cmd = ""
        self.first_cmd_issued = False
        self.tor = TorManager(self)
        self.cortex = NeuralCortex()
        self.layout = Layout()
        self.running = True
        
        # Set up signal handler for terminal resize
        if hasattr(signal, 'SIGWINCH'):
            signal.signal(signal.SIGWINCH, self.handle_resize)

    def handle_resize(self, signum, frame):
        # Force a re-render when the terminal is resized
        self.render()

    def add_log(self, msg, level="INFO"):
        colors = {"INFO": "blue", "SUCCESS": "green", "WARN": "yellow", "CRITICAL": "red", "AI": "magenta"}
        t = datetime.now().strftime("%H:%M:%S")
        self.logs.append((t, level, colors.get(level, 'white'), msg))

    def make_layout(self):
        layout = Layout()
        layout.split(
            Layout(name="status", size=1),
            Layout(name="body", ratio=2),
            Layout(name="neural", ratio=3),
            Layout(name="footer", size=3),
        )
        
        # Status Bar
        ctx = f"[bold cyan]CTX:[/] {self.cortex.status}"
        tgt = f"[bold cyan]TGT:[/] {self.target}"
        tor_color = "green" if self.tor.active else "red"
        tor_val = "ON" if self.tor.active else "OFF"
        tor = f"[bold cyan]TOR:[/] [{tor_color}]{tor_val}[/]"
        ip = f"[bold cyan]IP:[/] {self.tor.current_ip}"
        layout["status"].update(Align.center(f"{ctx} | {tgt} | {tor} | {ip}"))

        # Body (Output)
        cols, rows = shutil.get_terminal_size()
        limit = max(3, (rows - 12) // 4)
        body_text = Text()
        for t, lvl, clr, msg in self.logs[-limit:]:
            body_text.append(f"[{t}] ", style="white")
            body_text.append(f"[{lvl}] ", style=f"bold {clr}")
            if " : " in msg:
                parts = msg.split(" : ", 1)
                body_text.append(f"{parts[0]} : ", style="white")
                body_text.append(f"{parts[1]}\n", style="white")
            else:
                body_text.append(f"{msg}\n", style="white")
        layout["body"].update(Panel(body_text, title="Output", border_style="green", title_align="center"))

        # Neural Link
        neural_text = Text()
        if not self.first_cmd_issued:
            cmds = list(SlayerConfig.COMMAND_LIST.items())
            max_cmds = max(5, rows // 5)
            for cmd, desc in cmds[:max_cmds]:
                neural_text.append(f"• {cmd}", style="bold white")
                neural_text.append(f" : {desc}\n", style="white")
        else:
            if self.cortex.history:
                q, a = self.cortex.history[-1]
                neural_text.append(f"TACTICAL ADVICE:\n", style="bold magenta")
                neural_text.append(f"{a}\n", style="magenta")
            else:
                neural_text.append("Awaiting tactical input...", style="italic white")
        layout["neural"].update(Panel(neural_text, title="Neural Link (Live Feedback)", border_style="magenta", title_align="center"))

        # Footer
        layout["footer"].update(Panel(f"[bold green]Slayer-Input > [/][bold white]{self.current_cmd}[/]", border_style="blue"))
        
        return layout

    def render(self):
        cols, rows = shutil.get_terminal_size()
        ui_height = rows - 1
        sys.stdout.write("\033[H\033[2J\033[3J")
        sys.stdout.flush()
        console.print(self.make_layout(), height=ui_height)
        # Move cursor to the very last line for input
        sys.stdout.write(f"\033[{rows};1H")
        sys.stdout.flush()

    def process_command(self, cmd_input):
        if not cmd_input: return
        if not self.first_cmd_issued:
            self.logs = []
            self.first_cmd_issued = True
            
        self.current_cmd = ""
        parts = cmd_input.split()
        cmd = parts[0].upper()
        args = parts[1:]
        
        if cmd == "EXIT": 
            self.running = False
        elif cmd == "API":
            if len(args) == 1 and args[0].upper() == "GSK_":
                self.cortex.status = "LINKED"
                self.add_log("Neural Core Assembled.", "SUCCESS")
            else:
                self.add_log("Manual Key Linked.", "SUCCESS")
        elif cmd == "TOR": 
            self.tor.toggle(args[0].upper() if args else None)
        elif cmd == "AUTO":
            self.target = args[0] if args else "NONE"
            self.add_log(f"AUTO {self.target} : Full-spectrum automation", "CRITICAL")
        elif cmd == "OMEGA":
            self.target = args[0] if args else "NONE"
            self.add_log(f"OMEGA {self.target} : Initiate the brutal OMEGA PROTOCOL override.", "CRITICAL")
        else: 
            self.add_log(f"Processing: {cmd}", "INFO")

    def run(self):
        threading.Thread(target=self.tor.get_ip, daemon=True).start()
        self.add_log("AUTO <target> : Full-spectrum automation", "CRITICAL")
        self.add_log("OMEGA <target> : Initiate the brutal OMEGA PROTOCOL override.", "CRITICAL")
        self.add_log("GEO <ip> : Physical location mapping", "INFO")
        self.add_log("DOS <target> <port> : Service stress test", "WARN")
        self.add_log("WEB <url> : Vulnerability analysis", "INFO")
        self.add_log("HASH <string> : Cryptographic identification", "INFO")
        self.add_log("SHELL <ip> <port> : Reverse shell generation", "SUCCESS")
        self.add_log("EXFIL <target> <file> : Data exfiltration", "INFO")
        
        while self.running:
            self.render()
            try:
                # The input will now happen on the very last line
                cmd = input("")
                self.current_cmd = cmd
                self.process_command(cmd)
            except (KeyboardInterrupt, EOFError):
                break

if __name__ == "__main__":
    app = TermuxSlayerApp()
    app.run()
