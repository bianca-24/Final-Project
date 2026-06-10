# ESG Insight — User Guide

ESG Insight is a Streamlit dashboard that surfaces Environmental, Social, and Governance (ESG) scores derived from SEC filings and annual reports for major US financial-sector companies.

---

## Prerequisites

Before running the dashboard you need:

- Python 3.10+
- A PostgreSQL database populated by the project's data pipeline
- A `.env` file with valid database credentials (copy `.env.example` to get started)

```
DB_HOST=<your-db-host>
DB_PORT=5432
DB_NAME=<your-db-name>
DB_USER=<your-db-user>
DB_PASSWORD=<your-db-password>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Starting the dashboard

```bash
streamlit run Dashboard.py
```

The app opens in your browser at `http://localhost:8501`.

---

## Layout overview

### 1. Company & year selection

At the top of the page are two controls side by side:

| Control | What it does |
|---|---|
| **Search for a company** | Dropdown listing all companies in the database. Type to filter. |
| **Year** | Dropdown showing the filing years available for the selected company. Defaults to the most recent year. |

The company's sector and country appear below the selectors as context.

---

### 2. Score cards

Four coloured cards show the scores for the selected company and year:

| Card | Pillar |
|---|---|
| **Overall ESG** | Average of the three pillar scores |
| **Environment (E)** | Environmental practices and disclosures |
| **Social (S)** | Labour, community, and social impact |
| **Governance (G)** | Board structure, accountability, and transparency |

Each card shows:
- **Numeric score** (0–10 scale)
- **Letter grade** — A+ (≥ 9), A (≥ 8), B+ (≥ 7), B (≥ 6), C+ (≥ 5), C (< 5)

Card colour indicates performance at a glance:

| Colour | Score range |
|---|---|
| Dark green | ≥ 8 |
| Light green | 6–7.9 |
| Orange | 4–5.9 |
| Red | < 4 |

---

### 3. ESG Radar

A filled radar (spider) chart plotting the three pillar scores on a 0–10 scale. Use it to spot whether the company is balanced across pillars or skewed toward one.

---

### 4. Company vs Industry Average

A grouped bar chart comparing the selected company's E, S, and G scores against the average scores of all companies in the database for the same year. The dark-green bars represent the selected company; light-green bars represent the industry average.

---

### 5. Sentiment Summary

A short AI-generated narrative drawn from the company's filing that summarises its overall ESG positioning. It appears in a highlighted box below the charts.

---

### 6. ESG Company Rankings

A scrollable table ranking every company in the database for the selected year by Overall ESG Score (descending). Columns:

`Rank · Company · Sector · Country · ESG Score · Environment · Social · Governance`

Two optional filters sit above the table:

| Filter | How to use |
|---|---|
| **Filter by Sector** | Select a sector from the dropdown to narrow the table to that sector only. Choose *All* to reset. |
| **Search company in rankings** | Type any part of a company name to filter rows in real time. |

---

### 7. Evidence from Report

Three tabs — **Environment**, **Social**, **Governance** — each containing direct quotes extracted from the company's filing. Every quote is paired with a **Justification** that explains why it was selected as evidence for the pillar's score.

This section is useful for auditing or understanding *why* a particular score was assigned.

---

## Covered companies

The dashboard includes 30 US financial-sector companies, including:

Aflac, Allstate, American Express, Bank of America, Berkshire Hathaway, BlackRock, Capital One, Charles Schwab, Citigroup, CME Group, Discover Financial, Fiserv, Goldman Sachs, ICE, JPMorgan Chase, Mastercard, MetLife, Morgan Stanley, Nasdaq, PayPal, PNC Financial, Prudential Financial, State Street, T. Rowe Price, Travelers, US Bancorp, Visa, Wells Fargo.

---

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| *"Could not connect to database"* at startup | Missing or incorrect `.env` values — check `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`. |
| *"No filings found"* in the Year dropdown | The selected company has no entries in the `filings` table for the current database. |
| Score cards show *N/A* | ESG scores have not been generated for that company/year combination. Run the scoring pipeline first. |
| Charts are empty | Same as above — no score data in `esg_scores` for the selected filing. |
