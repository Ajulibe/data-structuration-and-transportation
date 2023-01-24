import requests
headers = {"accept": "application/json"}
response = requests.get("https://httpbin.org/get", headers=headers)

print(response.status_code) # 200 OK
print(response.headers["content-type"]) # application/json
print(response.json()) # { "args": {}, "headers": { "Accept": "application/json", "Host": "httpbin.org", "User-Agent": "python-requests/2.22.0" }, "origin": "