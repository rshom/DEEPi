import requests
import json



def send_command():
    
    url = 'http://localhost:5000/cmd/'
    
    data = '[{"$key": 8},{"$key": 7}]'

    headers = {"Content-Type": "application/json"}
    
    response = requests.put(url, data=data, headers=headers)
    
    res = response.json()
    
    print(res)
