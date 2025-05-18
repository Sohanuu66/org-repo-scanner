# simple_repo_scanner.py
import os
import requests
import pandas as pd
from urllib.parse import urljoin

def get_all_repos(org_name, token):
    """Fetch all repositories with basic info"""
    base_url = f"https://api.github.com/orgs/{org_name}/"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    
    repos = []
    page = 1
    
    while True:
        url = urljoin(base_url, "repos")
        params = {
            "per_page": 100,
            "page": page,
            "type": "all"  # includes both public and private
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching repos: {response.status_code} - {response.text}")
            break
            
        data = response.json()
        if not data:
            break
            
        for repo in data:
            repos.append({
                "Repository Name": repo["name"],
                "URL": repo["html_url"],
                "Visibility": "Private" if repo["private"] else "Public",
                "Last Updated": repo["updated_at"]
            })
            
        page += 1
        
    return repos

def save_to_excel(data, filename="repos_report.xlsx"):
    """Save repository data to Excel file"""
    if not data:
        print("⚠No repositories found to generate report")
        return False
        
    df = pd.DataFrame(data)
    df["Last Updated"] = pd.to_datetime(df["Last Updated"])
    df.sort_values("Last Updated", ascending=False, inplace=True)
    df.to_excel(filename, index=False)
    print(f"Report saved as {filename}")
    return True

if __name__ == "__main__":
    # Get credentials from environment variables
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    ORG_NAME = os.getenv("ORG_NAME")
    
    if not GITHUB_TOKEN or not ORG_NAME:
        print("Error: Missing environment variables")
        print("Please set GITHUB_TOKEN and ORG_NAME")
        exit(1)
    
    repositories = get_all_repos(ORG_NAME, GITHUB_TOKEN)
    if repositories:
        save_to_excel(repositories)
