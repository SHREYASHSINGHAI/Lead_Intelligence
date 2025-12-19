import pandas as pd
from enrich_pubmed import enrich_pubmed_df
from scoring import calculate_score

print("Loading Clay enriched leads...")
df = pd.read_csv("data/leads_clay_enriched.csv")

if df.empty:
    raise ValueError("CSV is empty")

# --------------------------
# Normalize Column Names
# --------------------------
df = df.rename(columns={
    "Name": "name",
    "Email": "email",
    "Person Location": "person_location",
    "Title": "title",
    "Company": "company",
    "Latest Funding": "funding_amount",
    "Company HQ": "company_hq"
})

# --------------------------
# PubMed Enrichment
# --------------------------
print("Checking PubMed publications...")
df = enrich_pubmed_df(df)

# --------------------------
# Funding Amount Normalization
# --------------------------
print("Normalizing funding amount...")

def normalize_funding_amount(value):
    if pd.isna(value):
        return 0

    text = str(value).lower().replace(",", "").replace("$", "").strip()

    try:
        if "million" in text:
            return float(text.replace("million", "").strip()) * 1_000_000
        if "m" in text:
            return float(text.replace("m", "").strip()) * 1_000_000
        if "k" in text:
            return float(text.replace("k", "").strip()) * 1_000
        return float(text)
    except:
        return 0

df["funding_amount_usd"] = df["funding_amount"].apply(normalize_funding_amount)

# --------------------------
# Scoring
# --------------------------
print("Scoring leads...")
df["score"] = df.apply(calculate_score, axis=1)
df = df.sort_values("score", ascending=False)

# --------------------------
# Save Output
# --------------------------
df.to_csv("data/leads_ranked.csv", index=False)
print("✅ Pipeline complete. leads_ranked.csv saved.")
