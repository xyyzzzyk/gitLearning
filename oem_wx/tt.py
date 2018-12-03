import requests
import json
 
response = requests.get("http://httpbin.org/get")
print(type(response))
print(response.json())