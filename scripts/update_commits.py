# scripts/update_commits.py
import csv, os, requests
from datetime import datetime, timezone

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
SINCE = "2025-10-01T00:00:00Z"   # 해커톤 시작 시각 ISO8601
UNTIL = "2026-03-31T23:59:59Z"  # 해커톤 종료 시각

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}

def get_commit_count(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {"since": SINCE, "until": UNTIL, "per_page": 100}
    count = 0
    page = 1
    while True:
        params["page"] = page
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
        data = r.json()
        if not data:
            break
        count += len(data)
        if len(data) < 100:
            break
        page += 1
    return count

with open("teams.csv", newline="", encoding="utf-8") as f:
    reader = list(csv.DictReader(f))

for row in reader:
    owner = row["id"]
    repo = row["repo"]
    commits = get_commit_count(owner, repo)
    row["commits"] = str(commits)

fieldnames = reader[0].keys()
with open("teams.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(reader)
