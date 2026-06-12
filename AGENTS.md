# AGENTS.md

This file documents how AI agents — specifically Claude Code — were used during development of the ESG Insight project.

---

## Project overview

ESG Insight analyses Environmental, Social, and Governance (ESG) factors in 10-K SEC filings for 28 major US financial-sector companies using NLP and LLMs (Google Gemini 2.5 Flash). The pipeline scrapes EDGAR, stores data in PostgreSQL, scores each company on E/S/G pillars, and presents results in a Streamlit dashboard.

---

## How Claude Code was used

### README and AGENTS.md

Claude Code updated `README.md` from a single-line placeholder to a full project overview including:
- End-to-end pipeline diagram
- Company coverage table by sector
- Installation and step-by-step usage instructions for all four pipeline stages
- Dashboard feature list
- Local and Streamlit Community Cloud deployment guide
- Project directory structure

`AGENTS.md` (this file) was also rewritten to accurately reflect the current codebase and Claude Code usage.

---

## Tasks well-suited for AI agents in this project

- **Adding new ESG scoring sub-categories** — extend the `pillar_definitions` dict in `scoring.ipynb` with new GRI/SASB criteria and add the corresponding keywords to the chunk filter
- **Writing database migration scripts** — adding columns or indexes to the `esg_scores` or `companies` tables
- **Extending company coverage** — adding new CIK entries to `COMPANY_CIKS` in `main.ipynb` and the `companies` list in `database_setup.ipynb`
- **Dashboard enhancements** — new chart types or filter controls in `Dashboard.py`
- **Writing tests** — unit tests for the chunker (`is_xbrl_noise`, `chunk_text`) and the scoring prompt logic

---

## Running the project

```bash
# Install dependencies
pip install -r requirements.txt

# Set credentials
cp .env.example .env   # then fill in DB_* and GOOGLE_API_KEY

# Run pipeline
# 1. main.ipynb          — scrape EDGAR and save chunks
# 2. database_setup.ipynb — create schema and load chunks
# 3. scoring.ipynb        — score all companies with Gemini

# Launch dashboard
streamlit run Dashboard.py
```
