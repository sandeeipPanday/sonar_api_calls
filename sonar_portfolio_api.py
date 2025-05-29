import requests
import json
import pandas as pd

# SonarQube API URL and Token
BASE_URL = "https://your-sonarqube-server/api/issues/search"
AUTH_TOKEN = "<YOUR_TOKEN>"  # Replace with your SonarQube token

# List of portfolio keys
PORTFOLIOS = ["portfolio1", "portfolio2", "portfolio3"]  # Add all your portfolio keys here

# Define severity filters
SEVERITIES = "CRITICAL,BLOCKER,MAJOR,MINOR"

# Headers for authentication
headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}

# Collect issues from all portfolios
all_issues = []

for portfolio in PORTFOLIOS:
    params = {
        "componentKeys": portfolio,
        "severities": SEVERITIES,
        "ps": 500  # Adjust page size as needed
    }
    
    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        for issue in data.get("issues", []):
            all_issues.append({
                "portfolio": portfolio,
                "key": issue["key"],
                "severity": issue["severity"],
                "cve": ", ".join(issue.get("tags", []))  # Extract CVE tags if available
            })
    else:
        print(f"Failed to fetch data for portfolio: {portfolio} | Status Code: {response.status_code}")

# Save to CSV
df = pd.DataFrame(all_issues)
df.to_csv("sonar_issues_report.csv", index=False)

print("Report saved successfully.")