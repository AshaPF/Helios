# Helios: Automated XSS Auditing

![image](https://github.com/user-attachments/assets/35347b21-1419-4d75-9edd-ca2efadfcca3)

> **v0.4** — Reworked and modernised for 2026 by [Asha_Official](https://pwnforums.st/User-Asha_Official)  
> Original tool by [@stuub](https://github.com/stuub)

---

## Features

- **Comprehensive Scanning**: Tests URL parameters, POST parameters, headers, and DOM content for XSS vulnerabilities.
- **Multiple Browser Support**: Compatible with Firefox, Chrome, and Chromium for testing.
- **Headless Mode**: Option to run scans in headless browser mode for faster & traditional execution.
- **Parallelised Scanning**: Utilises async multi-threading for efficient scanning of multiple targets.
- **Customisable**: Supports custom headers, cookies, and payload files.
- **Crawling Capability**: Can crawl websites to discover and test additional pages.
- **Detailed Reporting**: Provides comprehensive output with colour-coded console logs and optional file output.
- **DOM XSS Detection**: Advanced detection of DOM-based XSS vulnerabilities including external script analysis.
- **Payload Customisation**: Automatically customises payloads with unique canary strings for accurate detection.
- **Tamper Techniques**: WAF evasion techniques including unicode escape and null-byte injection (new in v0.4).
- **SQLi Detection**: Validates whether SQL injection errors are also present within responses.
- **WAF Detection**: Detect firewalls using both **behavioural** and **static** header checks.
- **Arch Linux / Hyprland Native**: Wayland-first browser flags, system `geckodriver`/`chromedriver` detection, and `uvloop` modern API (new in v0.4).

---

## What's New in v0.4 (2026 Rework)

- Fixed module-level `ClientSession()` crash (no event loop at import time)
- Fixed `uvloop` deprecated `set_event_loop_policy` → `uvloop.install()`
- Fixed `bcolors` defined-after-use crash on startup
- Fixed `bcolors.fail` typo in SQL injection reporting
- Removed duplicate `ChromeDriverManager` import
- Added `--ozone-platform=wayland` and `--headless=new` for Chromium under Hyprland
- System `geckodriver`/`chromedriver` auto-detection (no forced `webdriver-manager` download)
- `aiohttp` session now uses `TCPConnector` with thread limits and a 30s timeout (no more hanging requests)
- Expanded default payload set from 4 → 17 payloads: mutation XSS, template injection, `<details ontoggle>`, CSP-bypass `<object data=data:...>`, and more
- Two new tamper techniques: `unicode` and `nullbyte`
- `X-Forwarded-Host` added to header scan targets
- Bare `except: pass` blocks replaced throughout — failures now log properly

---

## Key Capabilities

- URL parameter analysis & testing
- POST parameter analysis & testing
- DOM content analysis & testing (inline + external scripts)
- Header injection testing (`User-Agent`, `Referer`, `X-Forwarded-For`, `X-Forwarded-Host`)
- Crawling with configurable depth
- WAF detection (static + behavioural)
- Tamper / evasion techniques
- SQLi error detection as a secondary signal

---

## Installation

### Arch Linux (recommended)

```bash
# System packages first
sudo pacman -S python-aiohttp python-beautifulsoup4 python-selenium python-requests geckodriver

# pip for the rest
pip install uvloop webdriver-manager lxml --break-system-packages
```

### Any platform

```bash
pip install -r requirements.txt --break-system-packages
```

---

## Usage

```
python3 helios.py [target_url] [options]
```

### Examples

```bash
# Basic scan
python3 helios.py https://target.com -o output.txt --crawl

# Target list, custom payloads, headless Chromium
python3 helios.py -l targetlist.txt --browser chromium --payload-file xsspayloads.txt \
  -o output.txt --crawl --headless \
  --cookies "session=abcdefg" \
  --headers "X-Forwarded-For:127.0.0.1"

# WAF evasion with unicode tamper
python3 helios.py https://target.com --tamper unicode --headless

# Full header scan with verbose output
python3 helios.py https://target.com --scan-headers --verbose
```

Use `python3 helios.py --help` for the full option list.

---

## Tamper Techniques

| Flag            | Description                                      |
|-----------------|--------------------------------------------------|
| `doubleencode`  | Double URL-encode the payload                    |
| `uppercase`     | Randomly uppercase characters                    |
| `hexencode`     | Hex-encode all characters                        |
| `jsonfuzz`      | JSON-escape the payload                          |
| `spacetab`      | Replace spaces with tabs                         |
| `unicode`       | Unicode-escape alphabetic characters *(new)*     |
| `nullbyte`      | Inject null bytes around `<` and `>` *(new)*     |
| `all`           | Apply all techniques sequentially                |

---

## Screenshots

### POST Method XSS
![image](https://github.com/user-attachments/assets/29b60c24-f832-43b6-b023-18981b462f38)

### DOM-Based XSS
![image](https://github.com/user-attachments/assets/f49efbf6-3a3c-483e-b7b5-dce426a63b41)

### Accurate Payload Detection
![image](https://github.com/user-attachments/assets/96f7d2bf-cdf9-46cd-8b72-c0fa6fcebcc6)

### SQLi Detection
![image](https://github.com/user-attachments/assets/cca33815-5e24-45bc-aea4-9a1cf6eae9d3)

### Scan Summaries
![image](https://github.com/user-attachments/assets/19ff0dde-08a9-4662-a487-9b0cfca7be4f)

---

## Future Development

- Context-aware payload generation based on target response analysis
- Modular / plugin architecture
- Smarter DOM XSS source-to-sink tracing
- JavaScript rendering pipeline improvements
- Getting gud

---

## Note

Helios is under active development. It may contain bugs or limitations. Contributions and feedback are welcome.

---

## Disclaimer

This tool is for **educational and ethical testing purposes only**. Always obtain explicit written authorisation before scanning any web application or network you do not own. The authors accept no liability for misuse.

---

## Authors

- Original tool: [@stuub](https://github.com/stuub)  
- v0.4 rework (2026): [Asha_Official](https://pwnforums.st/User-Asha_Official)
