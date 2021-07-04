class Local:
    pass


class Building:
    def __init__(self):
        self._locals = set()

    def add_local(self, local: Local):
        self._locals.add(local)
