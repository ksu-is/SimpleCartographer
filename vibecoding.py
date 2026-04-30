
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
    line_color = line_color_combo.get()
    try:
        marker_lat = float(marker_lat_spin.get())
        marker_long = float(marker_long_spin.get())
    except ValueError:
        marker_lat = 0
        marker_long = 0
    context = staticmaps.Context()
    context.set_tile_provider(tile_providers[map_type])
    context.set_zoom(zoom)

    # Add marker
    if show_marker.get():
        context.add_object(
            staticmaps.Marker(
                staticmaps.create_latlng(marker_lat, marker_long),
                color=(color_map[marker_color]),
                size=12
            )
        )
    try:
        lin_latone = float(line_latone_spin.get())
        lin_longone = float(line_longone_spin.get())
        lin_lattwo = float(line_lattwo_spin.get())
        lin_longtwo = float(line_longtwo_spin.get())
    except ValueError:
        lin_latone = 0
        lin_longone = 0
        lin_lattwo = 0
        lin_longtwo = 0    
    if show_line.get():
        line_start = staticmaps.create_latlng(lin_latone,lin_longone)
        line_end = staticmaps.create_latlng(lin_lattwo, lin_longtwo)
        context.add_object(
            staticmaps.Line(
                [line_start, line_end], color=(color_map[line_color]), width=4
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
    values=[1,2,3,4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,16,17,18,19,20],
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

ttk.Label(control_frame, text="Line Color:").grid(row=0, column=6, padx=5)
line_color_combo = ttk.Combobox(
    control_frame,
    values=list(color_map.keys()),
    state="readonly"
)
line_color_combo.current(0)
line_color_combo.grid(row=0, column=7)
line_color_combo.bind("<<ComboboxSelected>>", on_selection_change)

mark_lat = tk.StringVar(value = 0)
ttk.Label(control_frame, text="Marker Latitude:").grid(row=1, column=1, padx=5)
marker_lat_spin = ttk.Spinbox(
    control_frame,
    from_= -89,
    to= 89,
    textvariable= mark_lat
)
marker_lat_spin.grid(row=1, column=3)
marker_lat_spin.bind("<<Increment>>", on_selection_change)
marker_lat_spin.bind("<<Decrement>>", on_selection_change)
marker_lat_spin.bind("<Return>", on_selection_change)

mark_long = tk.StringVar(value = 0)
ttk.Label(control_frame, text="Marker Longitude:").grid(row=1, column=4, padx=5)
marker_long_spin = ttk.Spinbox(
    control_frame,
    from_= -180,
    to= 179,
    wrap= True,
    textvariable= mark_long 
)
marker_long_spin.grid(row=1, column=5)
marker_long_spin.bind("<<Increment>>", on_selection_change)
marker_long_spin.bind("<<Decrement>>", on_selection_change)
marker_long_spin.bind("<Return>", on_selection_change)
    
show_marker = tk.BooleanVar(value=True)
marker_button = ttk.Checkbutton(control_frame, text="Marker", variable= show_marker).grid(row=1, column=0, padx=5)

line_latone = tk.StringVar(value = 0)
ttk.Label(control_frame, text="Line Lat 1:").grid(row=2, column=1, padx=5)
line_latone_spin = ttk.Spinbox(
    control_frame,
    from_= -89,
    to= 89,
    textvariable= line_latone
)
line_latone_spin.grid(row=2, column=3)
line_latone_spin.bind("<<Increment>>", on_selection_change)
line_latone_spin.bind("<<Decrement>>", on_selection_change)
line_latone_spin.bind("<Return>", on_selection_change)

line_longone = tk.StringVar(value = 0)
ttk.Label(control_frame, text="Line Long 1:").grid(row=2, column=4, padx=5)
line_longone_spin = ttk.Spinbox(
    control_frame,
    from_= -180,
    to= 179,
    wrap= True,
    textvariable= line_longone 
)
line_longone_spin.grid(row=2, column=5)
line_longone_spin.bind("<<Increment>>", on_selection_change)
line_longone_spin.bind("<<Decrement>>", on_selection_change)
line_longone_spin.bind("<Return>", on_selection_change)

line_lattwo = tk.StringVar(value = 0)
ttk.Label(control_frame, text="Line Lat 2:").grid(row=2, column=6, padx=5)
line_lattwo_spin = ttk.Spinbox(
    control_frame,
    from_= -89,
    to= 89,
    textvariable= line_lattwo
)
line_lattwo_spin.grid(row=2, column=7)
line_lattwo_spin.bind("<<Increment>>", on_selection_change)
line_lattwo_spin.bind("<<Decrement>>", on_selection_change)
line_lattwo_spin.bind("<Return>", on_selection_change)

line_longtwo = tk.StringVar(value = 0)
ttk.Label(control_frame, text="Line Long 2:").grid(row=2, column=8, padx=5)
line_longtwo_spin = ttk.Spinbox(
    control_frame,
    from_= -180,
    to= 179,
    wrap= True,
    textvariable= line_longtwo 
)
line_longtwo_spin.grid(row=2, column=9)
line_longtwo_spin.bind("<<Increment>>", on_selection_change)
line_longtwo_spin.bind("<<Decrement>>", on_selection_change)
line_longtwo_spin.bind("<Return>", on_selection_change)

show_line =tk.BooleanVar(value=False)
line_button = ttk.Checkbutton(control_frame, text="Line", variable= show_line).grid(row=2, column=0, padx=5)

map_label = ttk.Label(root)
map_label.pack(pady=10)

# Initial render
generate_map()

root.mainloop()
