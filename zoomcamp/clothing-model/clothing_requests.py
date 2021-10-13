import requests
data = { 
    "url": "http://bit.ly/mlbookcamp-pants" 
} 
url = "http://localhost:8080/2015-03-31/functions/function/invocations" 
results = requests.post(url, json=data).json()
print(results)