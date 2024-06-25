import requests
import os

BRAPI_BASE_URL = os.environ.get("BRAPI_BASE_URL")
BRAPI_TOKEN = os.environ.get("BRAPI_TOKEN")

class BrapiApi:
    
    def do_request(self, path:str, method:str="GET", params:dict=dict(), payload:dict=dict()) -> dict:
        
        url = f"{BRAPI_BASE_URL}{path}"

        headers = {"Authorization": "Bearer %s" % BRAPI_TOKEN}

        response = requests.request(method=method, url=url, headers=headers, params=params, json=payload)

        if response.status_code >= 200 and response.status_code <= 299:
            return response.json()
        else:
            err_msg = f"Erro ao acessar a api do brapi no endpoint: {url}, finalizou com status: {response.status_code}"
            raise ConnectionError(err_msg)
        
    def list_tickers(self, params:dict=dict()) -> dict:
        path = "/available"
        return self.do_request(path, "GET", params)
    
    def ticker_quote(self, ticker_code:str, params:dict=dict()) -> dict:
        path = f"/quote/{ticker_code}"
        return self.do_request(path, "GET", params)