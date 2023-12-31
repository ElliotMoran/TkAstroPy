import _tkinter
import tkinter as tk

from tkinter import ttk
from tkinter import filedialog

from astro import calculate_star_flow, calculate_noise_flow, calculate_total_flow

from . import data_page as dp


class InputPage(ttk.Frame):
    def __init__(self, master, controller) -> None:
        super().__init__(master)
        self.controller = controller
 
        self._init_variables()
        self._init_widgets()

    def _read_filepath(self) -> None:
        self.filepath = filedialog.askopenfilename(initialdir='fits/')
        if self.filepath == ():
            self.filepath = ''

        self._on_write()

    def _on_write(self, *_) -> None:
        try:
            star_coord_x_val = self.star_coord_x.get()
            star_coord_y_val = self.star_coord_y.get()
            inner_radius_val = self.inner_radius.get()
            outer_radius_val = self.outer_radius.get()
        except _tkinter.TclError:
            error_text = 'Введите целое число!'
            self.error_label.configure(text=error_text)
            return

        if star_coord_x_val < 0 or star_coord_y_val < 0:
            error_text = 'Координата звезды не может быть отрицательной!'
            self.error_label.configure(text=error_text)
            return
        if inner_radius_val < 0 or outer_radius_val < 0:
            error_text = 'Радиус кольца не может быть отрицательным!'
            self.error_label.configure(text=error_text)
            return
        if inner_radius_val > outer_radius_val:
            error_text = 'Внутренний радиус не может быть больше внешнего!'
            self.error_label.configure(text=error_text)
            return
        if inner_radius_val == outer_radius_val:
            error_text = 'Внутренний радиус не может быть равен внешнему!'
            self.error_label.configure(text=error_text)
            return

        self.error_label.configure(text='')
 
        if self.filepath == '':
            return

        star_coord = (star_coord_x_val, star_coord_y_val)
        try:
            star_flow, _ = calculate_star_flow(
                self.filepath, star_coord, inner_radius_val)
            noise_flow = calculate_noise_flow(
                self.filepath, star_coord, inner_radius_val, outer_radius_val)
            total_flow = calculate_total_flow(
                self.filepath, star_coord, inner_radius_val, outer_radius_val)
        except IndexError:
            error_text = 'Координаты звезды вне диапазона данных файла!'
            self.error_label.configure(text=error_text)

            star_flow = 0.0
            noise_flow = 0.0
            total_flow = 0.0
        except ZeroDivisionError:
            error_text = 'Разница между радиусами мала!'
            self.error_label.configure(text=error_text)

            star_flow = 0.0
            noise_flow = 0.0
            total_flow = 0.0

        self.controller.frames[dp.DataPage].update_labels(
                round(star_flow, 2), 
                round(noise_flow, 2), 
                round(total_flow, 2)
        )
        self.controller.frames[dp.DataPage].update_variables(
                self.filepath,
                star_coord,
                inner_radius_val
        )

    def _init_variables(self) -> None:
        self.filepath = ''

        self.star_coord_x = tk.IntVar()
        self.star_coord_y = tk.IntVar()
        self.inner_radius = tk.IntVar()
        self.outer_radius = tk.IntVar()

        self.star_coord_x.trace_add('write', self._on_write)
        self.star_coord_y.trace_add('write', self._on_write)
        self.inner_radius.trace_add('write', self._on_write)
        self.outer_radius.trace_add('write', self._on_write)

    def _init_widgets(self) -> None:
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=2)

        self.text_input_star_coord_label = ttk.Label(self, text='Введите координаты звезды:')
        self.text_input_inner_radius_label = ttk.Label(self, text='Введите внутренний радиус кольца:')
        self.text_input_outer_radius_label = ttk.Label(self, text='Введите внешний радиус кольца:')
        self.error_label = ttk.Label(self, foreground='red')

        self.entry_star_coord_x = ttk.Entry(self, textvariable=self.star_coord_x)
        self.entry_star_coord_y = ttk.Entry(self, textvariable=self.star_coord_y)
        self.entry_inner_radius = ttk.Entry(self, textvariable=self.inner_radius)
        self.entry_outer_radius = ttk.Entry(self, textvariable=self.outer_radius)

        self.input_file_button = ttk.Button(self, text='Открыть файл', command=self._read_filepath)

        self.text_input_star_coord_label.grid(
                column=0, row=0,
                columnspan=2,
                padx=10, pady=10,
                sticky='nswe'
        )
        self.entry_star_coord_x.grid(
                column=0, row=1,
                padx=50, pady=3,
                sticky='nswe'
        )
        self.entry_star_coord_y.grid(
                column=1, row=1,
                padx=20, pady=3,
                sticky='nswe'
        )
        self.text_input_inner_radius_label.grid(
                column=0, row=2,
                columnspan=2,
                padx=10, pady=20,
                sticky='nswe'
        )
        self.entry_inner_radius.grid(
                column=0, row=3,
                padx=50, pady=3,
                sticky='nswe'
        )
        self.text_input_outer_radius_label.grid(
                column=0, row=4, 
                columnspan=2,
                padx=10, pady=20,
                sticky='nswe'
        )
        self.entry_outer_radius.grid(
                column=0, row=5,
                padx=50, pady=3,
                sticky='nswe'
        )
        self.input_file_button.grid(
                column=0, row=6,
                padx=10, pady=50,
                sticky='nswe'
        )
        self.error_label.grid(
                column=0, row=8,
                columnspan=2,
                padx=10, pady=50,
                sticky='nswe'
        )

