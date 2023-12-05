from PIL import Image
from customtkinter import *
from tkinter import Event, Menu

from model.airport import Airport
from model.route import Route

aside_a = None
aside_r = None

lst_airports = []
lst_routes = []


class TableTemplate(CTkFrame):
    def __init__(self, master, title, content, row_element=0):
        super().__init__(master, border_color='#333', border_width=1)
        global lst_airports, lst_routes

        self.home = self.master.master.children['!home']
        self.row_element = row_element
        self.toplevel_window = None
        self.content = content
        self.title = title
        self.menu = None
        self.main = None
        self.origin = ''
        self.view()

    def configure(self, **kwargs):
        self.grid(row=self.row_element, column=0,
                  sticky='nsew', padx=2, pady=2)
        self.bind('<Button-1>', lambda e: self.close_menu())
        return super().configure(**kwargs)

    def body(self):
        self.header()
        self.navbar()
        self.main_template(self.content)

    def header(self):
        folder_image = self.home.get_image('plus')

        header = CTkFrame(self, bg_color='grey17')
        header.pack(side='top', fill='both', expand=True, padx=1, pady=2)

        label = CTkLabel(header, text=self.title)
        label.pack(side='left', fill='both', expand=True)

        add_button = CTkButton(header, text='', fg_color='grey17',
                               width=50, image=folder_image, command=self.add)
        add_button.pack(side='bottom', fill='both', expand=True)

    def navbar(self):
        navbar = CTkFrame(self, bg_color='grey17', height=10, width=10)
        navbar.grid_rowconfigure(0, weight=1)
        navbar.pack(side='top', fill='both', expand=True, padx=1, pady=2)

        if self.title == 'Aeropuertos':
            lst_args = ['Nombre', 'Ubicación', 'Dirección']
            for i, item in enumerate(lst_args):
                navbar.grid_columnconfigure(i, weight=1)
                label = CTkLabel(navbar, text=item)
                label.grid(row=0, column=i, sticky='nsew')

        elif self.title == 'Rutas':
            lst_args = ['Origen', 'Destino', 'Distancia', 'Tiempo V']
            for i, item in enumerate(lst_args):
                navbar.grid_columnconfigure(i, weight=1)
                label = CTkLabel(navbar, text=item)
                label.grid(row=0, column=i, sticky='nsew')

    def main_template(self, content):
        main = CTkScrollableFrame(self, scrollbar_button_color='#29ADB2',
                                  scrollbar_button_hover_color='#0766AD')
        main.bind('<Button-1>', lambda e: self.close_menu())
        main.pack(side='bottom', fill='both', expand=True, padx=1, pady=1)

        if content:
            for i, item in enumerate(content):
                self.add_element(main, item, i)
        else:
            label = CTkLabel(main, text='No hay datos')
            label.pack(side='top', fill='both', expand=True)

        self.main = main

    def add_element(self, root, values: any, row):
        row_element = CTkFrame(root, bg_color='grey14')

        for i, j in enumerate(values.values()):
            row_element.grid_columnconfigure(i, weight=1)
            label = CTkLabel(row_element, text=j)
            label.bind(
                '<Button-3>', lambda e: self.options(e, values, row_element))
            label.bind('<Button-1>', lambda e: self.close_menu())
            label.pack(side='left', fill='both', expand=True)

        row_element.pack(side='top', fill='both', expand=True)

    def options(self, event, element, master):
        self.close_menu()
        self.menu = Menu(self, borderwidth=1, tearoff=0, takefocus=0)
        self.menu.configure(bg='gray17', bd=0, relief='solid', border=1)
        self.menu.configure(font=('Arial', 15), activebackground='gray')
        self.menu.configure(activeforeground='white', foreground='white')

        self.menu.add_command(label='Editar',
                              command=lambda: self.edit(element, master))
        self.menu.add_command(label='Eliminar',
                              command=lambda: self.delete(element, master))
        self.menu.post(event.x_root, event.y_root)

    def close_menu(self):
        if self.menu:
            self.menu.destroy()

    def edit(self, element, master: CTkFrame):
        if self.toplevel_window:
            self.close_toplevel()

        lst_inputs = []
        self.open_toplevel()
        frame = CTkFrame(self.toplevel_window, bg_color='grey14')
        frame.pack(side='top', fill='both', expand=True, padx=20, pady=20)

        if self.title == 'Aeropuertos':
            lst_inputs = self.toplevel_airport(frame, element)

        elif self.title == 'Rutas':
            lst_inputs = self.toplevel_route(frame, element)

        button = CTkButton(frame, text='Actualizar',
                           command=lambda: self.edit_item(element, lst_inputs, master))
        button.pack(side='bottom', fill='both', expand=True, pady=(10, 0))

    def add(self):
        if self.toplevel_window:
            self.close_toplevel()

        lst_inputs = []
        self.open_toplevel()
        frame = CTkFrame(self.toplevel_window, bg_color='grey14')
        frame.pack(side='top', fill='both', expand=True, padx=20, pady=20)

        if self.title == 'Aeropuertos':
            lst_inputs = self.toplevel_airport(frame)

        elif self.title == 'Rutas':
            if len(lst_airports) < 2:
                frame = CTkLabel(frame, text='No hay suficientes aeropuertos')
                frame.pack(side='top', fill='both',
                           expand=True, padx=20, pady=20)
                return

            lst_inputs = self.toplevel_route(frame)

        button = CTkButton(frame, text='Agregar',
                           command=lambda: self.add_item(lst_inputs))
        button.pack(side='bottom', fill='both', expand=True, pady=(10, 0))

    def toplevel_airport(self, frame, element=None):
        lst_args = ['Nombre', 'Ubicación', 'Dirección']
        args = element and element.values() or []
        lst_inputs = []

        for i, arg in enumerate(lst_args):
            frame.grid_columnconfigure(0, weight=1)

            label = CTkLabel(frame, text=arg, bg_color='grey14', anchor='w')
            label.pack(side='top', fill='both', expand=True)

            scanner = CTkEntry(frame, bg_color='grey14')
            scanner.pack(side='top', fill='both', expand=True)
            scanner.insert(0, args.pop(0) if args else '')

            lst_inputs.append(scanner)
        return lst_inputs

    def toplevel_route(self, frame, element=None):
        lst = element and element.values() or []
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

            scanner = CTkComboBox(frame, bg_color='grey14', command=on_select,
                                  values=[i.name for i in lst_airports])
            scanner.set(v)
            if element:
                scanner.configure(state='disabled')

            scanner.pack(side='top', fill='both', expand=True)
            lst_inputs.append(scanner)
            return scanner

        o = lst and lst.pop(0) or lst_airports[0].name
        d = lst and lst.pop(0) or lst_airports[1].name

        select_airport('Origen', o)
        select_airport('Destino', d)

        for arg in ['Distancia', 'Tiempo Velocidad']:
            frame.grid_columnconfigure(0, weight=1)

            label = CTkLabel(
                frame, text=arg, bg_color='grey14', anchor='w')
            label.pack(side='top', fill='both', expand=True)

            scanner = CTkEntry(frame, bg_color='grey14')
            scanner.pack(side='top', fill='both', expand=True)
            scanner.insert(0, lst and lst.pop(0) or '')
            lst_inputs.append(scanner)
        return lst_inputs

    def add_item(self, lst_inputs):
        args = [i.get() for i in lst_inputs]
        if not self.content:
            self.clean_main()

        if self.title == 'Aeropuertos':
            airport = Airport(*args)
            lst_airports.append(airport)

            self.add_element(self.main, airport, len(lst_airports) - 1)
            self.home.add_node(airport)

        elif self.title == 'Rutas':
            origin = next(i for i in lst_airports if i.name == args[0])
            destin = next(i for i in lst_airports if i.name == args[1])
            route = Route(origin, destin, *args[2:])

            origin.lst_ayacents.append(destin)
            destin.lst_ayacents.append(origin)
            lst_routes.append(route)

            self.add_element(self.main, route, len(lst_routes) - 1)
            self.home.add_edge(route)

        self.close_toplevel()

    def edit_item(self, element, lst_inputs, master: CTkFrame):
        args = [i.get() for i in lst_inputs]

        for i, v in enumerate(master.winfo_children()):
            v.configure(text=args[i])

        if self.title == 'Aeropuertos':
            airport = next(i for i in lst_airports if i == element)
            
            for c in aside_r.main.winfo_children():
                for v in c.winfo_children():
                    if v.cget('text') == airport.name:
                        v.configure(text=args[0])

            new_airport = Airport(*args)
            self.home.edit_node(airport, new_airport)

        elif self.title == 'Rutas':
            args[0] = next(i for i in lst_airports if i.name == args[0])
            args[1] = next(i for i in lst_airports if i.name == args[1])
            route = next(i for i in lst_routes if i == element)
            route.set(*args)

            self.home.edit_edge()

        self.close_toplevel()

    def delete(self, element, master: CTkFrame):
        if self.toplevel_window:
            self.close_toplevel()

        self.open_toplevel()
        frame = CTkFrame(self.toplevel_window, bg_color='grey14')
        frame.pack(side='top', fill='both', expand=True, padx=20, pady=20)

        label = CTkLabel(frame, text=f'¿Está seguro de eliminar {element}?')
        label.pack(side='top', fill='both', expand=True, anchor='w')

        button = CTkButton(frame, text='Eliminar', height=40,
                           command=lambda: self.delete_item(element, master))
        button.pack(side='bottom', fill='both', pady=(10, 0))

    def delete_item(self, element, master: CTkFrame):
        if self.title == 'Aeropuertos':
            airport = next(i for i in lst_airports if i == element)

            if lst_routes:
                for c in aside_r.main.winfo_children():
                    for v in c.winfo_children():
                        if v.cget('text') == airport.name:
                            c.destroy()

            lst_airports.remove(airport)
            self.home.delete_node(airport)

        elif self.title == 'Rutas':
            self.home.delete_edge(element)

        master.destroy()
        self.close_toplevel()

    def open_toplevel(self):
        self.toplevel_window = CTkToplevel(self)
        self.toplevel_window.geometry('500x400')
        self.toplevel_window.resizable(False, False)

    def close_toplevel(self):
        self.toplevel_window.destroy()
        self.toplevel_window = None

    def view(self):
        self.configure()
        self.body()

    def clean_main(self):
        for child in self.main.winfo_children():
            child.destroy()

    def update(self) -> None:
        self.home.update()
        return super().update()


class Aside(CTkFrame):
    def __init__(self, master, lst_air, lst_r, **kwargs):
        super().__init__(master, **kwargs)
        global lst_airports, lst_routes
        lst_airports = lst_air
        lst_routes = lst_r
        self.view()

    def configure(self, **kwargs):
        self.pack(side='right', fill='both', expand=True, padx=(4, 2), pady=4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        return super().configure(**kwargs)

    def content(self):
        global aside_a, aside_r
        aside_a = TableTemplate(self, 'Aeropuertos', lst_airports)
        aside_r = TableTemplate(self, 'Rutas', lst_routes, 1)

    def view(self):
        self.configure()
        self.content()
