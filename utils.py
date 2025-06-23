import cv2
from PIL import Image, ImageTk
from tkinter import Canvas, NW

def init_canvas(root):
    canvas = Canvas(root, width=300, height=300, bg="gray")
    img_container = canvas.create_image(0, 0, anchor=NW)
    return canvas, img_container

def show_on_canvas(image_cv, canvas, img_container):
    if image_cv is None:
        return
    if len(image_cv.shape) == 2:
        image_pil = Image.fromarray(image_cv)
    else:
        image_rgb = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)

    image_pil = image_pil.resize((300, 300))
    display_image = ImageTk.PhotoImage(image_pil)
    canvas.image = display_image  # untuk mencegah garbage collection
    canvas.itemconfig(img_container, image=display_image)
