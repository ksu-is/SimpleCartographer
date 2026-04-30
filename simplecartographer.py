import sys

import s2sphere
import gpxpy
import staticmaps
import json
import requests
import tkinter as tk
from tkinter import ttk
import PIL.ImageDraw
from PIL import Image, ImageTk

def textsize(self: PIL.ImageDraw.ImageDraw, *args, **kwargs):
    x, y, w, h = self.textbbox((0, 0), *args, **kwargs)
    return w, h
# Monkeypatch fix for https://github.com/flopp/py-staticmaps/issues/39
PIL.ImageDraw.ImageDraw.textsize = textsize
def display_map(path):
    img = Image.open(path)
    img_tk = ImageTk.PhotoImage(img)
    map_label = ttk.Label(root)
    map_label.pack(pady=10)
    map_label.config(image=img_tk)
    map_label.image = img_tk


tile_providers = {
    "OSM": staticmaps.tile_provider_OSM,
    "World Imagery": staticmaps.tile_provider_ArcGISWorldImagery,
    "Carto_Dark": staticmaps.tile_provider_CartoDarkNoLabels,
    "None": staticmaps.tile_provider_None
}

color_map = {
    "Black": staticmaps.BLACK,
    "Blue": staticmaps.BLUE,
    "Brown": staticmaps.BROWN,
    "Green": staticmaps.GREEN,
    "Orange": staticmaps.ORANGE,
    "Purple": staticmaps.PURPLE,
    "Red": staticmaps.RED,
    "Yellow": staticmaps.YELLOW,
    "White": staticmaps.WHITE,
    "Transparent": staticmaps.TRANSPARENT
}

class Mapper(ttk.Frame):
    """
    An example of a Mapping app developed using the 
    Tkinter and ttk GUI.
    """

    def __init__(self, master):
        """
        Initializes the frame.
        :param master: root.Tk()
        """
        ttk.Frame.__init__(self, master)
        self.show_marker = tk.BooleanVar(value=True)
        self.create_widgets()
        self.bind_buttons(master)
    def generate_map(self):
        self.map_type = self.map_type_combo.get()
        zoom = int(self.zoom_combo.get())
        self.marker_color = self.marker_color_combo.get()
        #line_color = line_color_combo.get()
        try:
            marker_lat = float(self.marker_lat_spin.get())
            marker_long = float(self.marker_long_spin.get())
        except ValueError:
            marker_lat = float(self.marker_lat_spin.get()+"1")
            marker_long = float(self.marker_long_spin.get()+"1")
        context = staticmaps.Context()
        context.set_tile_provider(tile_providers[self.map_type])
        context.set_zoom(zoom)

        # Add marker
        if self.show_marker.get():
            context.add_object(
                staticmaps.Marker(
                    staticmaps.create_latlng(marker_lat, marker_long),
                    color=(color_map[self.marker_color]),
                    size=12
                )
            )

        image = context.render_pillow(600, 400)
        image.save("newmap.png")

        display_map("newmap.png")

    # -----------------------------
    # Display image in Tkinter
    # -----------------------------
    #def display_map(path):
        #img_tk = ImageTk.PhotoImage(img)
        #map_label = ttk.Label(self)
        #map_label.pack(pady=10)
        #map_label.config(image=img_tk)
        #map_label.image = img_tk

    # -----------------------------
    # Combobox event handler
    # -----------------------------
    def on_selection_change():
        generate_map()

    def bind_buttons(self, master):
        """
        Binds keys to their appropriate input
        :param master: root.Tk()
        :return: None
        """
        self.map_type_combo.bind("<<ComboboxSelected>>", self.on_selection_change)
        self.zoom_combo.bind("<<ComboboxSelected>>", self.on_selection_change)
        self.marker_color_combo.bind("<<ComboboxSelected>>", self.on_selection_change)
        self.marker_lat_spin.bind("<<Increment>>", self.on_selection_change)
        self.marker_lat_spin.bind("<<Decrement>>", self.on_selection_change)
        self.marker_lat_spin.bind("<Return>", self.on_selection_change)
        self.marker_long_spin.bind("<<Increment>>", self.on_selection_change)
        self.marker_long_spin.bind("<<Decrement>>", self.on_selection_change)
        self.marker_long_spin.bind("<Return>", self.on_selection_change)
        
    
    def create_widgets(self):
        """
        Creates the widgets to be used in the grid.
        :return: None
        """
        ttk.Label(self, text="Map Style:").grid(row=0, column=0, padx=5)
        self.map_type_combo = ttk.Combobox(
            self,
            values=list(tile_providers.keys()),
            state="readonly"
        )
        self.map_type_combo.current(0)
        self.map_type_combo.grid(row=0, column=1)
        ttk.Label(self, text="Zoom:").grid(row=0, column=2, padx=5)
        
        self.zoom_combo = ttk.Combobox(
            self,
            values=[4, 5, 6, 7, 8, 9, 10],
            state="readonly",
            width=5
        )
        self.zoom_combo.current(3)
        self.zoom_combo.grid(row=0, column=3)

        ttk.Label(self, text="Marker Color:").grid(row=0, column=4, padx=5)
        self.marker_color_combo = ttk.Combobox(
            self,
            values=list(color_map.keys()),
            state="readonly"
        )
        self.marker_color_combo.current(0)
        self.marker_color_combo.grid(row=0, column=5)

        ttk.Label(self, text="Marker Latitude:").grid(row=1, column=1, padx=5)
        self.marker_lat_spin = ttk.Spinbox(
            self,
            from_= -89,
            to= 89,
        )
        self.marker_lat_spin.grid(row=1, column=3)
        ttk.Label(self, text="Marker Longitude:").grid(row=1, column=4, padx=5)
        self.marker_long_spin = ttk.Spinbox(
            self,
            from_= -89,
            to= 89,
        )
        self.marker_long_spin.grid(row=1, column=5)

        self.marker_button = ttk.Checkbutton(
            self, 
            text="Marker", 
            variable= self.show_marker, 
            command= self.generate_map
            )
        self.marker_button.grid(row=1, column=0, padx=5)


root = tk.Tk()
root.geometry()
root.title("Exciting GUI Cartographer")
app = Mapper(root)
app.pack(fill="both", expand=True)
root.mainloop()