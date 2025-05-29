import requests
import json
import pandas as pd

# SonarQube API Details
BASE_URL = "https://your-sonarqube-server/api"
AUTH_TOKEN = "<YOUR_TOKEN>"  # Replace with your SonarQube token

# Headers for authentication
headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}

# Step 1: Fetch All Projects
projects_url = f"{BASE_URL}/projects/search"
projects_response = requests.get(projects_url, headers=headers)
projects = projects_response.json().get("components", [])

all_issues = []

# Step 2: Fetch Issues for Each Project
SEVERITIES = "CRITICAL,BLOCKER,MAJOR,MINOR"

for project in projects:
    project_key = project["key"]
    issues_url = f"{BASE_URL}/issues/search"
    params = {
        "componentKeys": project_key,
        "severities": SEVERITIES,
        "ps": 500  # Adjust this if pagination is needed
    }
    
    response = requests.get(issues_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        for issue in data.get("issues", []):
            # Extracting CVE details from tags
            cve_tags = [tag for tag in issue.get("tags", []) if "CVE-" in tag]
            all_issues.append({
                "Project": project["name"],
                "Issue Key": issue["key"],
                "Severity": issue["severity"],
                "CVE": ", ".join(cve_tags) if cve_tags else "N/A"  # Format CVE list
            })
    else:
        print(f"Failed to fetch data for project: {project['name']} | Status Code: {response.status_code}")

# Step 3: Save to CSV
df = pd.DataFrame(all_issues)
df.to_csv("sonar_all_projects_cve_issues.csv", index=False)

print("SonarQube issues report with CVE details saved successfully.")
