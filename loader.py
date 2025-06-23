import cv2
from tkinter import filedialog
from modules.utils import show_on_canvas

def load_image(citra_dict, canvas, img_container):
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if not path:
        return
    img = cv2.imread(path)
    if img is None:
        print("Gagal membuka gambar.")
        return

    scale_percent = 50
    dim = (int(img.shape[1] * scale_percent / 100), int(img.shape[0] * scale_percent / 100))
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    citra_dict['original'] = img
    citra_dict['resized'] = resized
    citra_dict['gray'] = gray

    show_on_canvas(resized, canvas, img_container)
