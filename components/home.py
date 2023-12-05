from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from customtkinter import *
from PIL import Image
import networkx as nx


from model.route import Route

lst_airports = []
lst_routes = []


class Home(CTkFrame):
    def __init__(self, master, lst_air, lst_r):
        super().__init__(master, bg_color='grey17', width=500)
        global lst_airports, lst_routes
        lst_airports = lst_air
        lst_routes = lst_r

        self.toplevel_window = None
        self.G = nx.Graph()
        self.esmall = []
        self.pos = None
        self.view()

    def configure(self, **kwargs):
        self.pack(side='left', fill='both', expand=True, padx=(4, 2), pady=4)
        return super().configure(**kwargs)

    def body(self):
        self.config_plt()
        self.search()

    def config_plt(self):
        fig, ax = plt.subplots(facecolor='#2B2B2B')
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

        ax.margins(0.3)
        plt.axis("off")
        plt.tight_layout()

        self.config_nx(fig, ax)

    def config_nx(self, fig, ax):
        icon_image = Image.open('./assets/img/airport.png')

        self.G.add_nodes_from([airport.name for airport in lst_airports])
        self.update_edges()

        self.pos = pos = nx.spring_layout(self.G, seed=7)

        nx.draw_networkx_nodes(
            self.G, pos, node_size=500, node_color='#2b2b2b')
        nx.draw_networkx_edges(self.G, pos, edgelist=self.esmall,
                               width=3, alpha=0.5, edge_color="#00E7FF",
                               style="dashed")

        elarge = [(u, v) for (u, v) in self.G.edges if (u, v)
                  not in self.esmall and (v, u) not in self.esmall]

        nx.draw_networkx_edges(
            self.G,
            pos=pos,
            ax=ax,
            width=3,
            arrows=True,
            arrowstyle="-",
            edgelist=elarge,
            min_source_margin=15,
            min_target_margin=15,
        )

        nx.draw_networkx_labels(self.G, pos, font_size=20,
                                font_family="sans-serif", font_color="white")
        edge_labels = nx.get_edge_attributes(self.G, "weight")
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels)

        tr_figure = ax.transData.transform
        tr_axes = fig.transFigure.inverted().transform

        icon_size = .12 if len(self.G.nodes) <= 1 \
            else (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.04
        icon_center = icon_size * .5

        for n in self.G.nodes:
            xf, yf = tr_figure(pos[n])
            xa, ya = tr_axes((xf, yf))
            # get overlapped axes and plot icon
            a = plt.axes(
                [xa - icon_center, ya - icon_center - .07, icon_size, icon_size])
            a.imshow(icon_image)
            a.axis("off")

    def add_node(self, airport):
        self.G.add_node(airport.name)
        self.update()

    def add_edge(self, route):
        origin = route.origin.name
        destination = route.destination.name
        time = int(route.time_flight)
        distance = int(route.distance) / time

        self.G.add_edge(origin, destination, weight=distance)
        self.update()

    def edit_node(self, old_airport, new_airport):
        global lst_routes

        for i in lst_routes:
            if i.origin == old_airport:
                i.origin = new_airport

            elif i.destination == old_airport:
                i.destination = new_airport

        i = lst_airports.index(old_airport)
        lst_airports[i] = new_airport
        self.update_edges()
        self.delete_node(old_airport)

    def edit_edge(self, new):
        self.update_lst_routes(new)
        self.update()

    def delete_node(self, airport):
        self.G.remove_node(airport.name)
        self.update_lst_routes()
        self.update()

    def delete_edge(self, route):
        self.G.remove_edge(route.origin.name, route.destination.name)
        self.update_lst_routes()
        self.update()

    def update_lst_routes(self, new=None):
        global lst_routes
        lst_routes = []

        for (u, v, d) in self.G.edges(data=True):
            o = next((i for i in lst_airports if i.name == u), None)
            ds = next((i for i in lst_airports if i.name == v), None)
            lst_routes.append(Route(o, ds, d['distance'], d['time']))

        if new:
            lst_routes.append(new)

    def update_edges(self):
        self.G.add_edges_from([(route.origin.name, route.destination.name, {
            "weight":  round(int(route.distance) / int(route.time_flight), 2),
            'distance': round(int(route.distance), 2),
            'time': round(int(route.time_flight), 2)
        }) for route in lst_routes])

    def update(self):
        for item in self.winfo_children():
            item.destroy()

        self.body()
        return super().update()

    def search(self):
        icon = self.get_image('search')
        search = CTkButton(master=self,
                           text='',
                           bg_color='grey17',
                           fg_color='grey17',
                           border_width=0,
                           corner_radius=8,
                           image=icon,
                           hover=True,
                           width=25,
                           height=25,
                           )
        search.pack(side='left', fill='x', padx=(5, 0), pady=(0, 5))
        search.bind('<Button-1>', lambda e: self.search_button())

    def search_button(self):
        if self.toplevel_window:
            self.toplevel_window.destroy()
            self.toplevel_window = None

        self.open_toplevel()
        frame = CTkFrame(master=self.toplevel_window, bg_color='grey17')
        frame.pack(side='top', fill='both', expand=True)

        lst_inputs = self.toplevel_select(frame)

        button = CTkButton(frame, text='Buscar',
                           command=lambda: self.dijkstra(lst_inputs))
        button.pack(side='bottom', fill='both', expand=True, pady=(10, 0))

    def dijkstra(self, lst_inputs):
        origin = lst_inputs[0].get()
        destin = lst_inputs[1].get()

        try:
            path = nx.dijkstra_path(self.G, origin, destin)
            self.esmall = [(path[i], path[i+1]) for i in range(len(path)-1)]

            self.close_toplevel()
            self.update()

        except nx.NetworkXNoPath:
            label = CTkLabel(self.toplevel_window,
                             text=f'No existe la ruta entre {origin} y {destin}',
                             font=('Arial', 12, 'bold'),
                             text_color='red'
                             )
            label.pack(side='top', fill='both', expand=True, anchor='w')
            label.after(2000, lambda: label.destroy())

    def toplevel_select(self, frame):
        lst_inputs = []

        def select_airport(t, v):
            def on_select(cbox):
                cbox1 = frame.children['!ctkcombobox']
                cbox2 = frame.children['!ctkcombobox2']

                if cbox1.get() == cbox2.get():
                    lst = self.update_available_airports(cbox1.get())
                    cbox2.set(lst[0].name)

            label = CTkLabel(frame, text=f'Lista de Aeropuertos {t}')
            label.pack(side='top', fill='both',
                       expand=True, anchor='w')

            scanner = CTkComboBox(frame, bg_color='grey14', command=on_select, width=20,
                                  values=[i.name for i in lst_airports])
            scanner.set(v)
            scanner.pack(side='top', fill='both', expand=True)
            lst_inputs.append(scanner)
            return scanner

        o = lst_airports[0].name
        d = lst_airports[1].name
        select_airport('Origen', o)
        select_airport('Destino', d)

        return lst_inputs

    def update_available_airports(self, name):
        return [i for i in lst_airports if i.name != name]

    def open_toplevel(self):
        self.toplevel_window = CTkToplevel(self)
        self.toplevel_window.geometry('300x200')
        self.toplevel_window.resizable(False, False)

    def close_toplevel(self):
        self.toplevel_window.destroy()
        self.toplevel_window = None

    def get_image(self, name):
        icon = Image.open(f'./assets/img/{name}.png')
        icon = icon.resize((25, 25))
        return CTkImage(icon, size=(25, 25))

    def view(self):
        self.configure()
        self.body()
