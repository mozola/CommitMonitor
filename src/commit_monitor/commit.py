class Commit:

    def __init__(self):
        self._name = None
        self._date = None
        self._auth = None

    @property
    def name(self):
        return self._name

    @property
    def date(self):
        return self._date

    @property
    def auth(self):
        return self._auth

    def get_auth(self):
        pass

    def get_date(self):
        pass

    def get_name(self):
        pass
