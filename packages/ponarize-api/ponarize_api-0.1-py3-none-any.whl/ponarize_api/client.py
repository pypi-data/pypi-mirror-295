import requests

class PonarizeApiClient:
    
    def __init__(self, api_key:str):
        self.api_key = api_key
        
    def categorize_domain(self, domain:str):
        URL = "https://www.ponarize.com/api/check/domain"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"{self.api_key}"
        }
        payload = {
            "domain": domain
        }
        
        response = requests.post(URL, json=payload, headers=headers)
        data = response.json()
        return data
    
    def check_ip(self, ip:str):
        URL = "https://www.ponarize.com/api/check/ip"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"{self.api_key}"
        }
        payload = {
            "ip": ip
        }
        
        response = requests.post(URL, json=payload, headers=headers)
        data = response.json()
        return data
