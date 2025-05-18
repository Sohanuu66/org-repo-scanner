# simple_repo_scanner.py
import os
import requests
import pandas as pd
from urllib.parse import urljoin

def get_all_repos(org_name, token):
    base_url = f"https://api.github.com/orgs/{org_name}/"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    
    repos = []
    page = 1
    
    while True:
        url = urljoin(base_url, "repos")
        response = requests.get(url, headers=headers, params={"per_page": 100, "page": page})
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break
            
        data = response.json()
        if not data: break
            
        repos.extend([{
            "Name": repo["name"],
            "URL": repo["html_url"],
            "Visibility": "Private" if repo["private"] else "Public",
            "Last Updated": repo["updated_at"]
        } for repo in data])
        
        page += 1
        
    return repos

if __name__ == "__main__":
    token = os.getenv("GITHUB_TOKEN")
    org_name = os.getenv("ORG_NAME")
    
    if not (token and org_name):
        print("Missing environment variables! Need GITHUB_TOKEN and ORG_NAME")
        exit(1)
        
    repos = get_all_repos(org_name, token)
    if repos:
        pd.DataFrame(repos).to_excel("repos_report.xlsx", index=False)
        print("✅ Report generated: repos_report.xlsx")
    else:
        print("❌ No repositories found")
