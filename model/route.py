class Route:
    def __init__(self, *args):
        self.names = ['Origen', 'Destino', 'Distancia', 'Tiempo V']
        self.args = ['origin', 'destination', 'distance', 'time_flight']
        self.set(*args)

    def set(self, *args):
        [setattr(self, k, v) for k, v in zip(self.args, args)]

    def __eq__(self, __value: object) -> bool:
        return self.origin == __value.origin and self.destination == __value.destination

    def values(self) -> list:
        return [self.origin.name, self.destination.name, self.distance, self.time_flight]

    def __repr__(self) -> str:
        return f'({self.origin.name}, {self.destination.name}, {self.distance})'

    def __str__(self) -> str:
        return f'{self.origin.name} -> {self.destination.name}'
