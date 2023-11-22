import requests

url = 'http://localhost:8000/chat/'
data = {'message': '안녕하세요!'}
headers = {'Content-Type': 'application/json'}

response = requests.post(url, json=data, headers=headers)
print(response.json())