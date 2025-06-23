from tkinter import *
from modules.loader import load_image
from modules.operations import (
    grayscale, binary, brightness, logic_operation, show_histogram,
    sharpening, blurring, edge_detection, dilation  
)
from modules.utils import show_on_canvas, init_canvas

citra = {
    'original': None,
    'resized': None,
    'gray': None
}

def start_gui():
    global canvas, img_container

    root = Tk()
    root.title("Pengolahan Citra Digital Interaktif")
    root.geometry("520x750")
    root.resizable(False, False)

    Label(root, text="📸 Pengolahan Citra Digital", font=("Arial", 16, "bold")).pack(pady=10)

    canvas, img_container = init_canvas(root)
    canvas.pack()

    Button(root, text="📂 Pilih Gambar", width=35,
           command=lambda: load_image(citra, canvas, img_container)).pack(pady=5)
    Button(root, text="🖼 Gambar Asli", width=35,
           command=lambda: show_on_canvas(citra['resized'], canvas, img_container)).pack(pady=5)

    tombol_aksi = [
        ("🎨 Grayscale", grayscale),
        ("⚫ Binary", binary),
        ("💡 Brightness", brightness),
        ("🔗 Logika", logic_operation),
        ("📊 Histogram", show_histogram),
        ("✨ Sharpening", sharpening),
        ("🌫 Blurring", blurring),
        ("🪒 Edge Detection", edge_detection),
        ("🧱 Dilasi", dilation)
    ]

    for label, fungsi in tombol_aksi:
        Button(root, text=label, width=35,
               command=lambda f=fungsi: f(citra, canvas, img_container)).pack(pady=5)


    root.mainloop()
