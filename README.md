# Wealth Journey Projections (RetireForecast)
Monte Carlo–powered retirement planning — delivered as a simple, trustworthy Flask web app **and** a CLI script.

**Live:** https://www.retireforecast.com  
**Stack:** Python · Flask · Jinja · Bootstrap · Matplotlib · Gunicorn · Heroku

---

## What it does
This project estimates the longevity of retirement savings using **Monte Carlo simulation**. You can run it:

- As a **web app** (Flask) with a calculator UI.
- As a **CLI script** (`main.py`) with interactive prompts.

Outputs include:
- Probability of running out of money (bankruptcy probability)
- Average ending balance
- A chart (in the web app) or printed stats (in CLI)

### Investment strategies
- `stocks` → S&P 500
- `bonds` → 10-Year U.S. Treasury
- `sb_blend` → 50/50 stocks/bonds
- `sbc_blend` → 40/50/10 stocks/bonds/cash

> Data are historical percentage returns; **percent values per line** (not decimals).

---

## Project structure (key parts)
```
.
├─ app.py                      # Flask app (routes)
├─ main.py                     # Simulation logic (calculate_results, CLI entry)
├─ config.py                   # Development/Production configs
├─ templates/
│  ├─ base.html
│  ├─ home.html                # Landing + calculator form
│  ├─ results.html             # Shows bankrupt_prob, avg_outcome, chart
│  ├─ about.html               # About page
│  ├─ contact.html             # Contact page
│  └─ sitemap.xml.j2           # XML sitemap template
├─ static/
│  └─ google5ee561638742a290.html  # Google site verification
└─ text_files/
   └─ data_files/
      ├─ 10-yr_TBond_returns_1926-2013_pct.txt
      ├─ SP500_returns_1926-2013_pct.txt
      ├─ S-B-C_blend_1926-2013_pct.txt
      ├─ S-B_blend_1926-2013_pct.txt
      └─ annual_infl_rate_1926-2013_pct.txt
```

---

## Requirements
- Python 3.10+ (3.11 recommended)
- `pip` / `venv`
- Packages in `requirements.txt` (Flask, python-dotenv, matplotlib, Flask-Talisman, etc.)

---

## Local development — Web app

### 1) Clone & install
```bash
git clone <your-repo-url>
cd <repo>
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Environment
Create a `.env` file in the repo root:
```env
APP_ENV=development
SECRET_KEY=change-me
```

### 3) Run
- Plain HTTP (easiest in dev):
```bash
flask run
```
- If you prefer to keep HTTPS redirects on in dev, run with a self-signed cert:
```bash
flask run --cert=adhoc
```
Then open `http://127.0.0.1:5000/` (or `https://127.0.0.1:5000/` for the adhoc cert).

> In production, **Flask-Talisman** enforces HTTPS/HSTS. In development (`APP_ENV=development`), HTTPS forcing is disabled via config flags so you don’t hit redirect/TLS loops.

### 4) Verify data files load
On startup you should see log lines like:
```
INFO:main:Successfully loaded all data files
```
If you see file errors, confirm the names/paths in `text_files/data_files/`.

---

## CLI usage — Interactive script (main.py)

The same simulation engine can run directly from the terminal.

### 1) Ensure data files are in place
Place the following **percent-per-line** text files in `text_files/data_files/`:

- `10-yr_TBond_returns_1926-2013_pct.txt`
- `SP500_returns_1926-2013_pct.txt`
- `S-B-C_blend_1926-2013_pct.txt`
- `S-B_blend_1926-2013_pct.txt`
- `annual_infl_rate_1926-2013_pct.txt`

> Example: a line reading `7.3` means **7.3%**, not `0.073`.

### 2) Run in a terminal (inside your venv)
```bash
python main.py
```

Or from IPython:
```python
%run main.py
```

### 3) Follow the prompts
You’ll be asked for:
- Investment type (`stocks`, `bonds`, `sb_blend`, `sbc_blend`)
- Starting value of investments
- Annual withdrawal (today’s dollars)
- Years in retirement (minimum / most likely / maximum)
- Number of cases (simulations) to run

Press **ENTER** to accept defaults where shown.

### Example interactive session
```text
stocks = SP500
bonds = 10-yr Treasury Bond
sb_blend = 50% SP500 / 50% TBond
sbc_blend = 40% SP500 / 50% TBond / 10% Cash

Press ENTER to take default value shown in [brackets].

Enter investment type: (stocks, bonds, sb_blend, sbc_blend):
[bonds]: sb_blend
Input starting value of investments:
[2000000]:
Input annual pre-tax withdrawal (today's $):
[80000]:
Input minimum years in retirement:
[18]:
Input most-likely years in retirement:
[25]:
Input maximum years in retirement:
[40]:
Input number of cases to run:
[50000]:
```

### Example output
```text
Investment type: sb_blend
Starting value: $2,000,000
Annual Withdrawal: $80,000
Years in retirement (min-most_likely-max): 18-25-40
Number of runs: 50,000

Odds of running out of money: 12.3%
Average outcome: $523,456
Minimum outcome: $0
Maximum outcome: $4,750,897
```
> In CLI mode, results print to the terminal. In web mode, a chart is also rendered.

---

## Routes (web)
- `GET /` → Landing + calculator form (`home.html`)
- `POST /results` → Runs simulation and renders results (`results.html`)
- `GET /about` → About the project/author
- `GET /contact` → Contact info

---

## Configuration (env-driven)
Defined in `config.py`:

**Production defaults** (secure):
- `FORCE_HTTPS=True`
- `SESSION_COOKIE_SECURE=True`
- `STRICT_TRANSPORT_SECURITY=True`
- `PREFERRED_URL_SCHEME="https"`

**Development**:
- `FORCE_HTTPS=False`
- `SESSION_COOKIE_SECURE=False`
- `STRICT_TRANSPORT_SECURITY=False`
- `PREFERRED_URL_SCHEME="http"`

`app.py` selects the config class based on `APP_ENV` (`development` vs `production`) and passes those flags to **Talisman**.

---

## Security & privacy
- HTTPS enforced in production via **Flask-Talisman** (HSTS, secure cookies).
- Inputs are used for on-demand computation; the app does **not** store personal financial data.

---

## Disclaimer
This project is for **educational purposes only** and does **not** constitute financial, legal, or tax advice. Markets are uncertain; results are estimates, not guarantees.

---

