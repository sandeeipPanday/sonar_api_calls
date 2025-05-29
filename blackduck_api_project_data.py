import requests
import json
import pandas as pd

# Black Duck API Details
BLACKDUCK_URL = "https://your-blackduck-server"
API_TOKEN = "<YOUR_TOKEN>"  # Replace with your actual API token

# Headers for authentication
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/json"
}

def fetch_projects():
    """Retrieve all projects from Black Duck."""
    projects_url = f"{BLACKDUCK_URL}/api/projects"
    response = requests.get(projects_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch projects! Status Code: {response.status_code}")
        print("Response:", response.text)
        return []
    
    projects_data = response.json()
    return projects_data.get("items", [])

def fetch_latest_version(project):
    """Retrieve the latest scanned version of a project."""
    version_url = project["_meta"]["href"] + "/versions"
    response = requests.get(version_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch versions for project: {project['name']}")
        return None
    
    versions = response.json().get("items", [])
    return versions[0] if versions else None  # Assuming first entry is latest version

def fetch_vulnerabilities(version):
    """Retrieve vulnerabilities and CVE details for a specific version."""
    vuln_url = f"{BLACKDUCK_URL}/api/versions/{version['_meta']['href'].split('/')[-1]}/vulnerabilities"
    response = requests.get(vuln_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch vulnerabilities for version: {version['versionName']}")
        return []
    
    return response.json().get("items", [])

# Step 1: Fetch projects
projects = fetch_projects()

if not projects:
    print("No projects found! Exiting...")
    exit()

all_vulnerabilities = []

# Step 2: Loop through projects and retrieve vulnerabilities
for project in projects:
    latest_version = fetch_latest_version(project)
    if not latest_version:
        continue  # Skip if no versions available

    vulnerabilities = fetch_vulnerabilities(latest_version)
    
    for vuln in vulnerabilities:
        all_vulnerabilities.append({
            "Project": project["name"],
            "Version": latest_version["versionName"],
            "Severity": vuln["severity"],
            "CVE": vuln.get("cveId", "N/A")
        })

# Step 3: Save data to Excel
df = pd.DataFrame(all_vulnerabilities)
df.to_excel("blackduck_scan_report.xlsx", index=False)

print("Black Duck scan report saved successfully!")
