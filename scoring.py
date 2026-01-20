def calculate_score(row):
    score = 0

    title = str(row.get("title", "")).lower()
    location = str(row.get("person_location", "")).lower()
    funding = row.get("funding_amount_usd", 0)

    
    # Role Fit (+30)
    
    if any(word in title for word in ["toxicology", "safety", "hepatic", "3d"]):
        score += 30

    
    # Company Intent (Funding Amount)
    
    if funding >= 20_000_000:
        score += 25
    elif funding >= 5_000_000:
        score += 20
    elif funding >= 1_000_000:
        score += 10

    
    # Scientific Intent (+40)
    
    if row.get("published_recent_paper") == "yes":
        score += 40

    
    # Location Hub (+10)
    
    hubs = ["boston", "cambridge", "bay area", "basel", "london"]
    if any(hub in location for hub in hubs):
        score += 10

    return min(score, 100)
