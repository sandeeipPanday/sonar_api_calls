import requests
import pandas as pd

# Black Duck API Details
BLACKDUCK_URL = "https://your-blackduck-server"
API_TOKEN = "<YOUR_TOKEN>"  # Replace with your actual API token
PROJECT_NAME = "<PROJECT_NAME>"  # Replace with your project name

# Headers for authentication
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/json"
}

def fetch_project():
    """Retrieve project details by name."""
    projects_url = f"{BLACKDUCK_URL}/api/projects"
    response = requests.get(projects_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch projects! Status Code: {response.status_code}")
        return None
    
    projects = response.json().get("items", [])
    for project in projects:
        if project["name"] == PROJECT_NAME:
            return project
    print(f"Project '{PROJECT_NAME}' not found!")
    return None

def fetch_latest_version(project):
    """Retrieve the latest scanned version for the project."""
    version_url = project["_meta"]["href"] + "/versions"
    response = requests.get(version_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch versions for project: {project['name']}")
        return None
    
    versions = response.json().get("items", [])
    return versions[0] if versions else None  # Assuming first entry is latest

def fetch_vulnerabilities(version):
    """Retrieve vulnerabilities and CVE details."""
    vuln_url = f"{BLACKDUCK_URL}/api/versions/{version['_meta']['href'].split('/')[-1]}/vulnerabilities"
    response = requests.get(vuln_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch vulnerabilities for version: {version['versionName']}")
        return []
    
    return response.json().get("items", [])

# Step 1: Get project details
project = fetch_project()
if not project:
    exit()

# Step 2: Get latest version
latest_version = fetch_latest_version(project)
if not latest_version:
    exit()

# Step 3: Get vulnerabilities
vulnerabilities = fetch_vulnerabilities(latest_version)

# Step 4: Save to Excel
df = pd.DataFrame([
    {"Project": PROJECT_NAME, "Version": latest_version["versionName"], "Severity": vuln["severity"], "CVE": vuln.get("cveId", "N/A")}
    for vuln in vulnerabilities
])

df.to_excel(f"{PROJECT_NAME}_blackduck_report.xlsx", index=False)
print(f"Scan report for '{PROJECT_NAME}' saved successfully!")
