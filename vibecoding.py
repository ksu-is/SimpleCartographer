
import tkinter as tk
from tkinter import ttk
import staticmaps
import PIL.ImageDraw
from PIL import Image, ImageTk

def textsize(self: PIL.ImageDraw.ImageDraw, *args, **kwargs):
    x, y, w, h = self.textbbox((0, 0), *args, **kwargs)
    return w, h

# Monkeypatch fix for https://github.com/flopp/py-staticmaps/issues/39
PIL.ImageDraw.ImageDraw.textsize = textsize
# -----------------------------
# Map generation function
# -----------------------------
def generate_map():
    map_type = map_type_combo.get()
    zoom = int(zoom_combo.get())
    marker_color = marker_color_combo.get()
    #line_color = line_color_combo.get()
    try:
        marker_lat = float(marker_lat_spin.get())
        marker_long = float(marker_long_spin.get())
    except ValueError:
        marker_lat = float(marker_lat_spin.get()+"1")
        marker_long = float(marker_long_spin.get()+"1")
    context = staticmaps.Context()
    context.set_tile_provider(tile_providers[map_type])
    context.set_zoom(zoom)

    # Add marker
    if marker_var.get() == "1":
        context.add_object(
            staticmaps.Marker(
                staticmaps.create_latlng(marker_lat, marker_long),
                color=(color_map[marker_color]),
                size=12
            )
        )

    image = context.render_pillow(600, 400)
    image.save("map.png")

    display_map("map.png")

# -----------------------------
# Display image in Tkinter
# -----------------------------
def display_map(path):
    img = Image.open(path)
    img_tk = ImageTk.PhotoImage(img)
    map_label.config(image=img_tk)
    map_label.image = img_tk

# -----------------------------
# Combobox event handler
# -----------------------------
def on_selection_change(event):
    generate_map()

# -----------------------------
# Tkinter UI
# -----------------------------
root = tk.Tk()
root.title("Simple Cartographer")

control_frame = ttk.Frame(root)
control_frame.pack(pady=5)

# Tile providers
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


ttk.Label(control_frame, text="Map Style:").grid(row=0, column=0, padx=5)
map_type_combo = ttk.Combobox(
    control_frame,
    values=list(tile_providers.keys()),
    state="readonly"
)
map_type_combo.current(0)
map_type_combo.grid(row=0, column=1)
map_type_combo.bind("<<ComboboxSelected>>", on_selection_change)

ttk.Label(control_frame, text="Zoom:").grid(row=0, column=2, padx=5)
zoom_combo = ttk.Combobox(
    control_frame,
    values=[4, 5, 6, 7, 8, 9, 10],
    state="readonly",
    width=5
)
zoom_combo.current(3)
zoom_combo.grid(row=0, column=3)
zoom_combo.bind("<<ComboboxSelected>>", on_selection_change)

ttk.Label(control_frame, text="Marker Color:").grid(row=0, column=4, padx=5)
marker_color_combo = ttk.Combobox(
    control_frame,
    values=list(color_map.keys()),
    state="readonly"
)
marker_color_combo.current(0)
marker_color_combo.grid(row=0, column=5)
marker_color_combo.bind("<<ComboboxSelected>>", on_selection_change)

ttk.Label(control_frame, text="Marker Latitude:").grid(row=1, column=1, padx=5)
marker_lat_spin = ttk.Spinbox(
    control_frame,
    from_= -89,
    to= 89,
)
marker_lat_spin.grid(row=1, column=3)
marker_lat_spin.bind("<<Increment>>", on_selection_change)
marker_lat_spin.bind("<<Decrement>>", on_selection_change)
marker_lat_spin.bind("<Return>", on_selection_change)

ttk.Label(control_frame, text="Marker Longitude:").grid(row=1, column=4, padx=5)
marker_long_spin = ttk.Spinbox(
    control_frame,
    from_= -89,
    to= 89,
)
marker_long_spin.grid(row=1, column=5)
marker_long_spin.bind("<<Increment>>", on_selection_change)
marker_long_spin.bind("<<Decrement>>", on_selection_change)
marker_long_spin.bind("<Return>", on_selection_change)

marker_var = tk.IntVar
marker_button = ttk.Checkbutton(control_frame, text="Marker", variable= marker_var).grid(row=1, column=0, padx=5)

map_label = ttk.Label(root)
map_label.pack(pady=10)

# Initial render
generate_map()

root.mainloop()
