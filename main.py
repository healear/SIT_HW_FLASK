from client import Client
if __name__ == '__main__':
    url = "http://127.0.0.1:5000"

    username = "vasya"
    password = "50555"
    c = Client(url=url, username=username, password=password)
    """c.get_todos()
    c.post_todo("sit")
    c.get_todos()
    c.update_todo("sit", "tis")
    c.get_todos()
    c.delete_todo("tis")
    c.get_todos()
    c.post_update("template.jpg")
    c.delete_update("template.jpg")"""