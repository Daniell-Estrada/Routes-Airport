from customtkinter import *

from components.aside import Aside
from components.home import Home


class AirTransport(CTk):
    def __init__(self, lst_airports, lst_routes) -> None:
        super().__init__()
        self.lst_airports = lst_airports
        self.lst_routes = lst_routes
        self.show()

    def configure(self, **kwargs):
        set_appearance_mode('System')
        set_default_color_theme("blue")
        self.title('Air Transport')
        self.minsize(1200, 500)
        return super().configure(**kwargs)

    def content(self):
        Home(self, self.lst_airports, self.lst_routes)
        Aside(self, self.lst_airports, self.lst_routes)

    def update(self):
        return super().update()

    def show(self):
        self.configure()
        self.content()
        self.mainloop()
