import requests
sesssion = requests.Session()
data = {
    'key':'0121'
}
r = sesssion.post('http://127.0.0.1:5000/check_key',data=data)
print(r.text)
