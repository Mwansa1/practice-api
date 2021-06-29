import requests

text = input("Enter a text: ")
url = 'http://text-processing.com/api/sentiment/'
obj = {'text': text}

response = requests.post(url, data=obj)
print(response.json())
