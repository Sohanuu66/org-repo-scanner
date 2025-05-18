import requests
import pandas as pd
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ORG_NAME = os.getenv("GITHUB_ORG")

API_URL = f"https://api.github.com/orgs/{ORG_NAME}/repos"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_repos():
    repos = []
    page = 1
    while True:
        response = requests.get(API_URL, headers=HEADERS, params={"per_page": 100, "page": page})
        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            break
        data = response.json()
        if not data:
            break
        for repo in data:
            repos.append({
                "Name": repo["name"],
                "Visibility": "Private" if repo["private"] else "Public",
                "Fork": repo["fork"],
                "URL": repo["html_url"],
                "Last Updated": repo["updated_at"]
            })
        page += 1
    return repos

def save_to_excel(data):
    df = pd.DataFrame(data)
    df.to_excel("repos_report.xlsx", index=False)

if __name__ == "__main__":
    repos = get_repos()
    if repos:
        save_to_excel(repos)
    else:
        print("No repositories found or error occurred.")
