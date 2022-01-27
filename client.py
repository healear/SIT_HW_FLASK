import requests
class Client:
    """Инициализированный клиент должен быть авторизирован"""
    def __init__(self, username:str, password:str):
        self.url = "http://127.0.0.1:5000/"
        self.username = username
        self.password = password
        payload = {"username": username, "password": password}
        response = requests.post(self.url+"login", json=payload)
        self.token = response.json()['token']
        print("User authenticated, Token: "+self.token)

    def get_todos(self):
        response = requests.get(self.url+"todo", headers={'Authorization': f"Bearer {self.token}"})
        print(response.json())

    def post_todo(self, name):
        payload = {"name": name}
        response = requests.post(self.url+"todo", json=payload, headers={'Authorization': f"Bearer {self.token}"})
        print(response.json())

    def update_todo(self, prev_name, new_name):
        payload = {"name": new_name}
        response = requests.put(self.url+"todo"+"/"+prev_name, json=payload, headers={'Authorization': f"Bearer {self.token}"})
        print(response.json())

    def delete_todo(self, name):
        response = requests.delete(self.url + "todo" + "/" + name, headers={'Authorization': f"Bearer {self.token}"})
        print(response.json())