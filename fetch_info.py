import requests

def fetch_user_info(handle:str):
    
    url=f"https://codeforces.com/api/user.info?handles={handle}"

    response=requests.get(url)
    data=response.json()
    info=data
    return data["result"]