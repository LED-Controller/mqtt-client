import requests

REST_URL = "http://host.docker.internal:8080"
Password = {"password": "test"}


def authenticate():
    token = requests.post(REST_URL+"/login", json=Password)
    header = {'Authorization': 'Bearer ' + token.json()['token']}
    print("Verbindung mit Backend erfolgreich")
    return header

def getlamps(header):
    response = requests.get(REST_URL+"/lamps", headers=header)
    return response.json()


def updatelamps(header, lamp):
    requests.post(REST_URL + "/update", json=lamp, headers=header)
