import dataset


DATABASE = dataset.connect('sqlite:///commit_mo.db')


class User:

    def __init__(self):

        self._database = DATABASE['users']
        self._username = None

    @property
    def username(self):
        return self._username

    def validate(self, username: str, password: str):
        users = self.get(username=username,
                         password=password)
        if not users:
            return False

        (users,) = users
        self._username = users['username']
        return len(users) != 0

    def add(self, username: str, password: str,
            login: str, email: str):

        user = dict(username=username,
                    password=password,
                    login=login, email=email)

        if self.validate(username=username,
                         password=password):
            return False

        self._database.insert(user)
        return True

    def get(self, username, password):
        user = {'username': username, 'password': password}
        return list(self._database.find(**user))

    def remove(self):
        pass
