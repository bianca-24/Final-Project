# AGENTS.md

This project analyses ESG factors in corporate annual reports 
for 30 major banks using NLP and LLMs.

## How to run
1. Install dependencies: `pip install -r requirements.txt`
2. Add your Google API key to a `.env` file as GOOGLE_API_KEY
3. Run the scraper: `python scraper.py`
4. Run the dashboard: `streamlit run dashboard/app.py`

## Tasks an AI agent can help with
- Writing new ESG scoring categories in `src/scoring.py`
- Writing tests in `tests/`
- Improving code documentation