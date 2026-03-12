import requests

def fetch_codeforces_submissions(handle: str):
    
    url = f"https://codeforces.com/api/user.status?handle={handle}"
    
    response = requests.get(url)
    
    data = response.json()
    submissions = data["result"]
    return submissions

if __name__ == "__main__":
    
    submissions = fetch_codeforces_submissions("tourist")
    
    for sub in submissions[:10]:
        
        problem = sub["problem"]["name"]
        verdict = sub["verdict"]
        
        print(problem, verdict)