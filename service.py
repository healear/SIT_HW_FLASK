
#Сервис для установки значения APP_ENV и возвращения значения этой переменной
class Service:
    def __init__(self, app_env):
        self.APP_ENV = app_env

    def get_env(self):
        return self.APP_ENV