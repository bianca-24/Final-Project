import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cur = conn.cursor()

for table in ['companies', 'esg_scores', 'filings']:
    cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name='{table}'")
    print(f"\n{table}:", cur.fetchall())
    
cur.execute("SELECT DISTINCT pillar FROM esg_scores")
print("Pillars:", cur.fetchall())

cur.execute("SELECT DISTINCT EXTRACT(YEAR FROM filing_date) FROM filings")
print("Years:", cur.fetchall())

cur.execute("SELECT DISTINCT filing_date FROM filings LIMIT 5")
print("Filing dates:", cur.fetchall())

cur.execute("SELECT DISTINCT subcategory FROM esg_scores LIMIT 20")
print("Subcategories:", cur.fetchall())

cur.execute("SELECT evidence_quote FROM esg_scores WHERE evidence_quote IS NOT NULL LIMIT 3")
print("Evidence:", cur.fetchall())