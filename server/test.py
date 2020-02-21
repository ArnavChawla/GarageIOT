import requests
sesssion = requests.Session()
data = {
    'key':'1'
}
r = sesssion.post('http://192.168.86.45:5000/check_key',data=data)
print(r.text)
