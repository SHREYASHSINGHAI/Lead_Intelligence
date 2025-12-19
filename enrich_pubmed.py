from pubmed_check import get_pubmed_count

def enrich_pubmed_df(df, years=2):
    df["published_recent_paper"] = "no"

    for i, row in df.iterrows():
        name = str(row.get("name", ""))
        title = str(row.get("title", ""))
        search_term = f"{name} {title}"

        try:
            count = get_pubmed_count(search_term, years)
            if count > 0:
                df.at[i, "published_recent_paper"] = "yes"
        except:
            pass

    return df
