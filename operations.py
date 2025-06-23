import cv2
from modules.utils import show_on_canvas
import numpy as np

def grayscale(citra, canvas, container):
    if citra['original'] is not None:
        gray = cv2.cvtColor(citra['original'], cv2.COLOR_BGR2GRAY)
        citra['gray'] = gray
        show_on_canvas(gray, canvas, container)

def binary(citra, canvas, container):
    if citra.get('gray') is not None:
        _, binary = cv2.threshold(citra['gray'], 127, 255, cv2.THRESH_BINARY)
        show_on_canvas(binary, canvas, container)

def brightness(citra, canvas, container):
    if citra.get('gray') is not None:
        brighter = cv2.add(citra['gray'], 50)
        show_on_canvas(brighter, canvas, container)
