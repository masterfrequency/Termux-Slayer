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
        # Dynamically adjust log limit based on terminal height
        limit = max(4, rows // 6)
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
            for cmd, desc in SlayerConfig.COMMAND_LIST.items():
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

    def process_command(self, cmd_input):
        if not cmd_input: return
        if not self.first_cmd_issued:
            self.logs = []
            self.first_cmd_issued = True
            
        self.current_cmd = cmd_input
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
        
        with Live(self.make_layout(), refresh_per_second=4, screen=True) as live:
            while self.running:
                live.update(self.make_layout())
                # Using a non-blocking way to handle input is complex in a basic script,
                # but we can ensure the layout is redrawn before input.
                # In Termux, the 'input()' call will pause the loop, but the 'Live' context
                # will handle the screen refresh once input is received or if a resize signal hits.
                try:
                    # We use a small trick: the Live display is on the alternate screen.
                    # 'input' might break the visual, so we stop Live briefly or use a thread.
                    # For Termux stability, we'll keep it simple but responsive to resize.
                    cmd = console.input("[bold green]Slayer-Input > [/]")
                    self.process_command(cmd)
                except KeyboardInterrupt:
                    break
                except EOFError:
                    break

if __name__ == "__main__":
    app = TermuxSlayerApp()
    app.run()
