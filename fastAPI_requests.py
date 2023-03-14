import simplejson
import django
import requests
import json
def request_1():
    url = "http://127.0.0.1:5000/api"
    data ={"input":"My name is Alex and I live in America"}
    data = json.dumps(data)
    response = requests.post(url, json=data)
    # print(response.status_code) # if 200ish it is working with no error else there is a problem

def request_2():
    url = "http://127.0.0.1:5000/api"
    response = requests.get(url)
    print(response.text)
    print(response.status_code)


if __name__ == '__main__':
    request_1()
    request_2()