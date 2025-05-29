import requests
import json
import pandas as pd

# Black Duck API Details
BLACKDUCK_URL = "https://your-blackduck-server"
API_TOKEN = "<YOUR_TOKEN>"  # Replace with your Black Duck API token

# Headers for authentication
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/json"
}

# Step 1: Get list of projects
projects_url = f"{BLACKDUCK_URL}/api/projects"
projects_response = requests.get(projects_url, headers=headers)
projects = projects_response.json()["items"]

all_vulnerabilities = []

for project in projects:
    project_name = project["name"]
    version_url = project["_meta"]["href"] + "/versions"
    
    # Step 2: Get latest version (scan)
    version_response = requests.get(version_url, headers=headers)
    versions = version_response.json()["items"]
    
    if versions:
        latest_version = versions[0]  # Assume first one is latest
        version_id = latest_version["_meta"]["href"].split("/")[-1]
        
        # Step 3: Get vulnerabilities for this version
        vuln_url = f"{BLACKDUCK_URL}/api/versions/{version_id}/vulnerabilities"
        vuln_response = requests.get(vuln_url, headers=headers)
        vulnerabilities = vuln_response.json()["items"]

        for vuln in vulnerabilities:
            all_vulnerabilities.append({
                "Project": project_name,
                "Severity": vuln["severity"],
                "CVE": vuln.get("cveId", "N/A")
            })

# Step 4: Save to Excel
df = pd.DataFrame(all_vulnerabilities)
df.to_excel("blackduck_scan_report.xlsx", index=False)

print("Black Duck scan data saved successfully.")
