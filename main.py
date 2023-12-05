from air_transport import AirTransport

from model.airport import Airport
from model.route import Route


lst_airports = [
    Airport('A', 1, 5, []),
    Airport('B', 2, 4, []),
    Airport('C', 3, 3, []),
    Airport('D', 4, 2, []),
    Airport('E', 5, 1, []),
]
lst_routes = [
    Route(lst_airports[0], lst_airports[1], 100, 30),
    Route(lst_airports[1], lst_airports[2], 400, 10),
    Route(lst_airports[2], lst_airports[0], 400, 10),
    Route(lst_airports[2], lst_airports[3], 120, 12),
    Route(lst_airports[4], lst_airports[0], 250, 10),
]


def main():
    AirTransport(lst_airports, lst_routes)


if __name__ == '__main__':
    main()
