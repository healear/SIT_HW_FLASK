import requests
class Client:
    """Инициализированный клиент должен быть авторизирован"""
    def __init__(self, url:str, username:str, password:str):
        self.url = url
        self.todo_url = "/todo"
        self.download_url = "/download"
        self.upload_url = "/uploads"
        self.username = username
        self.password = password
        payload = {"username": self.username, "password": self.password}
        response = requests.post(self.url+"/login", json=payload)
        self.token = response.json()['token']
        print("User authenticated, Token: "+self.token)

    def get_todos(self):
        response = requests.get(self.url+self.todo_url, headers={'Authorization': f"Bearer {self.token}"})
        print(response.json())

    def post_todo(self, name):
        payload = {"name": name}
        response = requests.post(self.url+self.todo_url, json=payload, headers={'Authorization': f"Bearer {self.token}"})
        print(response.json())

    def update_todo(self, prev_name, new_name):
        payload = {"name": new_name}
        response = requests.put(self.url+self.todo_url+"/"+prev_name, json=payload, headers={'Authorization': f"Bearer {self.token}"})
        print(response.json())

    def delete_todo(self, name):
        response = requests.delete(self.url + self.todo_url + "/" + name, headers={'Authorization': f"Bearer {self.token}"})
        print(response.json())

    def post_update(self, name):
        files = {'upload': open(f'{name}', 'rb')}
        response = requests.post(self.url+self.upload_url, files=files)
        print(response.json())

    def get_updates(self):
        response = requests.get(self.url+self.upload_url)
        print(response.json())

    def download_update(self, name):
        response = requests.get(self.url+self.download_url+"/"+name)
        with open(name, mode="wb") as download:
            download.write(response.content)
        print(response.status_code)

    def delete_update(self, name):
        response = requests.delete(self.url+self.upload_url+"/"+name)
        print(response.status_code)