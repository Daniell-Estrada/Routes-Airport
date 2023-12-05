class Airport:
    def __init__(self, *args):
        self.names = ['Nombre', 'Ubicación', 'Dirección']
        self.args = ['name', 'location', 'adress']
        self.lst_ayacents = []
        self.set(*args)

    def set(self, *args):
        [setattr(self, k, v) for k, v in zip(self.args, args)]

    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name

    def values(self) -> list:
        return [self.name, self.location, self.adress]

    def __repr__(self) -> str:
        return f'{self.name}'

    def __str__(self) -> str:
        return self.name
