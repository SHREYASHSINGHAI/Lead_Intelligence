import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Lead Intelligence Dashboard",
    layout="wide"
)

st.title("🔬 Lead Intelligence Dashboard")

df = pd.read_csv("data/leads_ranked.csv")

# Rank column
df = df.sort_values("score", ascending=False).reset_index(drop=True)
df.insert(0, "rank", df.index + 1)

# Search
search = st.text_input("🔍 Search by name, company, title or location")

if search:
    df = df[
        df["name"].str.contains(search, case=False, na=False) |
        df["company"].str.contains(search, case=False, na=False) |
        df["title"].str.contains(search, case=False, na=False) |
        df["person_location"].str.contains(search, case=False, na=False)
    ]

# Display table
st.dataframe(
    df[
        [
            "rank",
            "score",
            "name",
            "title",
            "company",
            "funding_amount",
            "person_location",
            "company_hq",
            "email"
        ]
    ],
    use_container_width=True
)

# Download
st.download_button(
    "⬇️ Download CSV",
    data=df.to_csv(index=False),
    file_name="ranked_leads.csv",
    mime="text/csv"
)
