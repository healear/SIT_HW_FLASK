from client import Client
if __name__ == '__main__':
    username = "vasya"
    password = "505555"
    c = Client(username, password)
    c.get_todos()
    c.post_todo("sit")
    c.get_todos()
    c.update_todo("sit", "tis")
    c.get_todos()
    c.delete_todo("tis")
    c.get_todos()
