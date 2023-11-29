import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

from .input_page import InputPage
from .data_page import DataPage


class TkApp(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.wm_title('Tkinter Astro App')
        self.wm_geometry(self._get_init_geometry())

        self._configure_font()
        self._configure_frames()

    def _configure_font(self) -> None:
        default_font = tkFont.nametofont('TkDefaultFont')
        default_font.configure(size=14)
        self.option_add('*Font', default_font)

    def _configure_frames(self) -> None:
        container = ttk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for FrameClass in (InputPage, DataPage):
            frame = FrameClass(container, self)

            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self._show_frame(InputPage)

    def _show_frame(self, FrameClass):
        frame = self.frames[FrameClass]
        frame.tkraise()

    def _get_init_geometry(self) -> str:
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
 
        app_width = str(screen_width // 2)
        app_height = str(screen_height // 2)

        app_xcenter = str(screen_width // 4)
        app_ycenter = str(screen_height // 4)

        return f'{app_width}x{app_height}+{app_xcenter}+{app_ycenter}'

