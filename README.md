# ESG Insight

**ESG Insight** is an end-to-end platform that extracts, scores, and visualises Environmental, Social, and Governance (ESG) performance for 28 major US financial-sector companies using their SEC 10-K filings and Google's Gemini AI.

---

## How it works

```
SEC EDGAR  →  main.ipynb  →  data/*.json  →  database_setup.ipynb  →  PostgreSQL
                                                                           ↓
                                                                    scoring.ipynb
                                                                    (Gemini 2.5 Flash)
                                                                           ↓
                                                                    Dashboard.py
                                                                    (Streamlit)
```

1. **Scrape** — `main.ipynb` fetches the latest 10-K filing for each company from EDGAR, strips HTML/XBRL noise, and saves ESG-relevant text chunks to `data/`.
2. **Load** — `database_setup.ipynb` creates the PostgreSQL schema and loads companies, filings, and chunks.
3. **Score** — `scoring.ipynb` calls Gemini 2.5 Flash to evaluate each company on the E, S, and G pillars (0–10) using GRI 300/400 and TCFD frameworks.
4. **Visualise** — `Dashboard.py` is a Streamlit app that displays scores, charts, rankings, and evidence quotes.

---

## Covered companies

28 US financial-sector companies across 6 sectors:

| Sector | Companies |
|---|---|
| **Bank** | JPMorgan, Goldman Sachs, Bank of America, Wells Fargo, Citigroup, Morgan Stanley, US Bancorp, PNC Financial |
| **Capital Management** | BlackRock, State Street, Charles Schwab, Berkshire Hathaway, T. Rowe Price |
| **Insurance** | MetLife, Prudential Financial, Aflac, Allstate, Travelers |
| **Fintech** | Visa, Mastercard, PayPal, Fiserv |
| **Credit** | American Express, Capital One, Discover Financial |
| **Exchange** | ICE, Nasdaq, CME Group |

---

## Prerequisites

- Python 3.10+
- PostgreSQL 14+ (local or remote)
- A Google AI API key (for Gemini 2.5 Flash)

---

## Installation

```bash
git clone https://github.com/bianca-24/Final-Project.git
cd Final-Project
pip install -r requirements.txt
```

Copy the environment template and fill in your credentials:

```bash
cp .env.example .env
```

`.env` variables:

```
DB_HOST=<your-db-host>
DB_PORT=5432
DB_NAME=<your-db-name>
DB_USER=<your-db-user>
DB_PASSWORD=<your-db-password>
GOOGLE_API_KEY=<your-gemini-api-key>
```

---

## Usage

Run the steps in order. Each notebook is self-contained and skips work that has already been done.

### Step 1 — Scrape filings

Open and run all cells in `main.ipynb`.

- Fetches the most recent 10-K from EDGAR for each of the 28 companies.
- Filters chunks to those containing ESG-relevant keywords.
- Saves output as `data/<Company>_<date>_chunks.json`.
- Already-scraped companies are skipped automatically.

### Step 2 — Set up the database

Open and run all cells in `database_setup.ipynb`.

Creates four tables in your PostgreSQL database and loads the chunk files:

| Table | Description |
|---|---|
| `companies` | Company name, sector, country |
| `filings` | Filing metadata (type, date, file path) |
| `chunks` | 500-word ESG-relevant text windows |
| `esg_scores` | AI-generated pillar scores, justifications, summaries, and evidence quotes |

### Step 3 — Score companies

Open and run all cells in `scoring.ipynb`.

- Calls Gemini 2.5 Flash for each company × pillar combination.
- Scores are 0–10, grounded in GRI 300/400 series, TCFD, and SASB Financial Sector standards.
- Already-scored pillars are skipped; failed calls are retried up to 5 times.
- Saves `score`, `justification`, `summary`, and `evidence_quote` to `esg_scores`.

### Step 4 — Run the dashboard

```bash
streamlit run Dashboard.py
```

Open `http://localhost:8501` in your browser. See [`docs/user-guide.md`](docs/user-guide.md) for a full walkthrough of all dashboard features.

---

## Dashboard features

- **Score cards** — Overall, E, S, and G scores with letter grades (A+–C) and colour coding
- **ESG Radar** — Spider chart showing balance across the three pillars
- **Company vs Industry Average** — Grouped bar chart benchmarking a company against all peers
- **Sentiment Summary** — AI-generated narrative from the filing
- **Rankings table** — All 28 companies ranked by ESG score, filterable by sector
- **Evidence quotes** — Direct quotes from the 10-K that support each pillar score

---

## Deployment

### Running locally

```bash
streamlit run Dashboard.py
```

### Deploying to Streamlit Community Cloud

1. Push the repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo.
3. Set the main file to `Dashboard.py`.
4. Add all `.env` variables as **Secrets** in the app settings.
5. Deploy — the app will be available at a public URL.

### Running against a remote database

The dashboard connects to any PostgreSQL instance reachable from the host. Set `DB_HOST` to your server's IP or hostname. The project was developed and tested against a VPS-hosted PostgreSQL instance.

To run the scraping and scoring notebooks against a remote database, update the connection parameters in `database_setup.ipynb` and `scoring.ipynb` to match your remote host, then run them as usual.

---

## Project structure

```
Final-Project/
├── Dashboard.py           # Streamlit dashboard
├── main.ipynb             # EDGAR scraper and chunker
├── database_setup.ipynb   # PostgreSQL schema creation and data loading
├── scoring.ipynb          # Gemini AI scoring pipeline
├── data/                  # Scraped ESG chunk files (one JSON per company)
├── scraper/               # Experimental scraper notebooks
├── docs/
│   └── user-guide.md      # End-user guide for the dashboard
├── .env.example           # Environment variable template
├── requirements.txt       # Python dependencies
└── test_db.py             # Database connection test
```
