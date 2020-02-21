from flask import Flask
from flask import request
from flask import render_template
import json
import new
from twilio.rest import Client
client = Client('api-key', 'api-secret')
from twilio.rest import TwilioRestClient
app = Flask(__name__)
data = []
class pin():
    def __init__(self,name, pin,position):
        self.name = name
        self.pin = pin
        self.position = position

@app.route('/')
def method():
    return render_template('main.html')
@app.route('/creator',methods=["POST"])
def create():
        print(request.form)
        a_dict = { request.form["pin"]: {
            "name": request.form["name"]
        }}
        with open('keys.json') as f:
            data = json.load(f)

        data.update(a_dict)
        print(data)
        with open('keys.json', 'w') as f:
            json.dump(data, f)


        return render_template('main.html')
@app.route('/check_key',methods=["POST"])
def check():
    jso = json.loads(open('keys.json').read())
    print(request.form["key"])
    key =request.form["key"]
    try:
        name = jso[key]
        print(name)
        client.messages.create(from_='',#add phone numbers
                           to='',#add phone numbers
                           body=name["name"]+ " opened your garage")
        return "true"
    except:
        return "false"
@app.route('/open',methods=["POST"])
def doting():
	new.correct_passcode_entered()
@app.route('/manager')
def timg():
    data = []
    jso = json.loads(open("keys.json").read())
    i = 0
    for item in jso:
        data.append(pin(jso[item]["name"],item,i))
        i+=1
    return(render_template('manager.html',data=data))
@app.route("/delete",methods=["POST"])
def delete():
    with open('keys.json', 'r') as data_file:
        data1 = json.load(data_file)
    data1.pop(str(request.form["position"]), None)
    with open('keys.json', 'w') as data_file:
        print(data1)
        json.dump(data1, data_file)
        data_file.close()
    data = []
    jso = json.loads(open("keys.json").read())
    i = 0
    for item in jso:
        data.append(pin(jso[item]["name"], item, i))
        i += 1
    return(render_template('manager.html', data=data))
if __name__ == '__main__':
    app.run('0.0.0.0')
