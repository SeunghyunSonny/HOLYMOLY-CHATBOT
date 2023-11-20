import requests

url = "http://127.0.0.1:8000/chat/"  # Correct URL
data = {'message': 'do you know about Tim hortons?'}  # Replace with your actual data


response = requests.post(url, json=data)
print(response)
data = response.json()
print(data)