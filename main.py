import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import Toplevel
from PIL import Image, ImageTk
import os
from tkinter.ttk import Style

gambar_asli = None
gambar_hasil = None
gambar_abu = None

WARNA_LATAR = "#f5f5f5"
WARNA_TOMBOL = "#FF8C00"  
WARNA_TOMBOL_HOVER = "#FF6B00"  
WARNA_TEKS = "#0E0202"
WARNA_TEKS_TOMBOL = "white"  
WARNA_KANVAS = "#e0e0e0"
WARNA_AKSEN = "#FF6B00"

def tampilkan_gambar(canvas, gambar_cv, sebelum=True):
    if gambar_cv is None:
        return
        
    if len(gambar_cv.shape) == 2:  
        gambar_pil = Image.fromarray(gambar_cv)
    else:
        gambar_rgb = cv2.cvtColor(gambar_cv, cv2.COLOR_BGR2RGB)
        gambar_pil = Image.fromarray(gambar_rgb)
    
    gambar_pil = gambar_pil.resize((350, 300))  
    gambar_tk = ImageTk.PhotoImage(gambar_pil)
    
    if sebelum:
        canvas.gambar_sebelum = gambar_tk  
        canvas.itemconfig(canvas.kontainer_sebelum, image=gambar_tk)
    else:
        canvas.gambar_sesudah = gambar_tk  
        canvas.itemconfig(canvas.kontainer_sesudah, image=gambar_tk)

def muat_gambar():
    global gambar_asli, gambar_hasil, gambar_abu
    path = filedialog.askopenfilename(filetypes=[("File gambar", "*.jpg *.png *.jpeg")])
    if not path:
        return
    
    gambar_asli = cv2.imread(path)
    if gambar_asli is None:
        messagebox.showerror("Error", "Gagal memuat gambar. Pastikan file yang dipilih valid.")
        return

    skala = 50
    lebar = int(gambar_asli.shape[1] * skala / 100)
    tinggi = int(gambar_asli.shape[0] * skala / 100)
    gambar_asli = cv2.resize(gambar_asli, (lebar, tinggi), interpolation=cv2.INTER_AREA)
    
    gambar_hasil = gambar_asli.copy()
    gambar_abu = cv2.cvtColor(gambar_asli, cv2.COLOR_BGR2GRAY)
    
    tampilkan_gambar(kanvas_sebelum, gambar_asli, True)
    tampilkan_gambar(kanvas_sesudah, gambar_asli, False)
    tombol_unduh.config(state=NORMAL)  

def simpan_gambar():
    if gambar_hasil is None:
        messagebox.showwarning("Peringatan", "Tidak ada gambar hasil olahan untuk disimpan!")
        return
    
    path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("Semua file", "*.*")],
        title="Simpan Gambar Hasil"
    )
    
    if not path:
        return
    
    try:
        if len(gambar_hasil.shape) == 2:
            gambar_simpan = cv2.cvtColor(gambar_hasil, cv2.COLOR_GRAY2RGB)
        else:
            gambar_simpan = cv2.cvtColor(gambar_hasil, cv2.COLOR_BGR2RGB)
        
        Image.fromarray(gambar_simpan).save(path)
        messagebox.showinfo("Sukses", f"Gambar berhasil disimpan di:\n{path}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan gambar:\n{str(e)}")

def tampilkan_asli():
    global gambar_hasil
    if gambar_asli is not None:
        gambar_hasil = gambar_asli.copy()
        tampilkan_gambar(kanvas_sesudah, gambar_hasil, False)

def konversi_keabu():
    global gambar_hasil
    if gambar_abu is not None:
        gambar_hasil = gambar_abu.copy()
        tampilkan_gambar(kanvas_sesudah, gambar_hasil, False)

def konversi_biner():
    global gambar_hasil
    if gambar_abu is not None:
        _, gambar_hasil = cv2.threshold(gambar_abu, 127, 255, cv2.THRESH_BINARY)
        tampilkan_gambar(kanvas_sesudah, gambar_hasil, False)

def atur_kecerahan():
    global gambar_hasil
    if gambar_abu is not None:
        gambar_hasil = cv2.add(gambar_abu, 50)
        tampilkan_gambar(kanvas_sesudah, gambar_hasil, False)

def operasi_NOT():
    global gambar_hasil
    if gambar_abu is not None:
        mask = cv2.inRange(gambar_abu, 100, 200)
        gambar_hasil = cv2.bitwise_not(mask)
        tampilkan_gambar(kanvas_sesudah, gambar_hasil, False)


def tampilkan_histogram():
    global gambar_hasil
    if gambar_abu is not None:
        hist = cv2.calcHist([gambar_abu], [0], None, [256], [0, 256])
        gambar_hist = np.zeros((256, 256), dtype=np.uint8)
        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
        for i in range(256):
            cv2.line(gambar_hist, (i, 255), (i, 255 - int(hist[i])), 255)
        gambar_hasil = gambar_hist
        tampilkan_gambar(kanvas_sesudah, gambar_hasil, False)

def penajaman():
    global gambar_hasil
    if gambar_asli is not None:
        kernel = np.array([[-1, -1, -1],
                          [-1, 9, -1],
                          [-1, -1, -1]])
        gambar_hasil = cv2.filter2D(gambar_asli, -1, kernel)
        tampilkan_gambar(kanvas_sesudah, gambar_hasil, False)

def pengaburan():
    global gambar_hasil
    if gambar_asli is not None:
        gambar_hasil = cv2.GaussianBlur(gambar_asli, (5, 5), 0)
        tampilkan_gambar(kanvas_sesudah, gambar_hasil, False)

def deteksi_tepi():
    global gambar_hasil
    if gambar_abu is not None:
        gambar_hasil = cv2.Canny(gambar_abu, 100, 200)
        tampilkan_gambar(kanvas_sesudah, gambar_hasil, False)

def dilasi():
    global gambar_hasil
    if gambar_abu is not None:
        jendela_se = Toplevel(root)
        jendela_se.title("Pilih Elemen Struktur")
        jendela_se.geometry("300x150")
        jendela_se.config(bg=WARNA_LATAR)
        
        Label(jendela_se, text="Pilih Elemen Struktur (SE):", 
              font=("Arial", 10), bg=WARNA_LATAR, fg=WARNA_TEKS).pack(pady=10)
        
        def gunakan_kotak():
            global gambar_hasil
            kernel = np.ones((3, 3), np.uint8)
            gambar_hasil = cv2.dilate(gambar_abu, kernel, iterations=1)
            tampilkan_gambar(kanvas_sesudah, gambar_hasil, False)
            jendela_se.destroy()
        
        def gunakan_silang():
            global gambar_hasil
            kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
            gambar_hasil = cv2.dilate(gambar_abu, kernel, iterations=1)
            tampilkan_gambar(kanvas_sesudah, gambar_hasil, False)
            jendela_se.destroy()
        
        Button(jendela_se, text="Kotak 3x3", width=15, command=gunakan_kotak,
              bg=WARNA_TOMBOL, fg="white", activebackground=WARNA_TOMBOL_HOVER).pack(pady=5)
        Button(jendela_se, text="Silang 3x3", width=15, command=gunakan_silang,
              bg=WARNA_TOMBOL, fg="white", activebackground=WARNA_TOMBOL_HOVER).pack(pady=5)

root = Tk()
root.title("Aplikasi Pengolahan Citra Digital")
root.geometry("1000x700")  
root.resizable(True, True)
root.config(bg=WARNA_LATAR)

style = Style()
style.configure("TButton", padding=6, relief="flat", background=WARNA_TOMBOL, foreground="white")
style.map("TButton", background=[("active", WARNA_TOMBOL_HOVER)])

header = Frame(root, bg=WARNA_LATAR)
header.pack(pady=20)
Label(header, text=" Aplikasi Pengolahan Citra", 
      font=("Arial", 20, "bold"), bg=WARNA_LATAR, fg=WARNA_TEKS).pack()

frame_tombol = Frame(root, bg=WARNA_LATAR)
frame_tombol.pack(pady=10)

baris1 = Frame(frame_tombol, bg=WARNA_LATAR)
baris1.pack()
tombol_baris1 = [
    ("📂 Muat Gambar", muat_gambar),
    ("🖼 Tampilkan Asli", tampilkan_asli),
    ("⚫ greyscale", konversi_keabu),
    ("⚪ Biner", konversi_biner),
    ("💡 Kecerahan", atur_kecerahan)
]
for i, (teks, perintah) in enumerate(tombol_baris1):
    Button(baris1, text=teks, width=15, command=perintah,
          bg=WARNA_TOMBOL, fg="white", activebackground=WARNA_TOMBOL_HOVER,
          font=("Arial", 9), relief="flat").grid(row=0, column=i, padx=5, pady=5)

baris2 = Frame(frame_tombol, bg=WARNA_LATAR)
baris2.pack(pady=5)
tombol_baris2 = [
    ("🔗 operasi NOT", operasi_NOT),
    ("📊 Histogram", tampilkan_histogram),
    ("✨ sharpen", penajaman),
    ("🌫 bluring", pengaburan),
    ("🪒 Deteksi Tepi", deteksi_tepi),
    ("🧱 Dilasi", dilasi),
]
for i, (teks, perintah) in enumerate(tombol_baris2):
    Button(baris2, text=teks, width=15, command=perintah,
          bg=WARNA_TOMBOL, fg="white", activebackground=WARNA_TOMBOL_HOVER,
          font=("Arial", 9), relief="flat").grid(row=0, column=i, padx=5, pady=5)

frame_gambar = Frame(root, bg=WARNA_LATAR)
frame_gambar.pack(pady=20)

frame_sebelum = Frame(frame_gambar, bg=WARNA_LATAR)
frame_sebelum.pack(side=LEFT, padx=20)
Label(frame_sebelum, text="Sebelum", font=("Arial", 12, "bold"), 
     bg=WARNA_LATAR, fg=WARNA_TEKS).pack()
kanvas_sebelum = Canvas(frame_sebelum, width=350, height=300, bg=WARNA_KANVAS, 
                      highlightthickness=2, highlightbackground="#cccccc")
kanvas_sebelum.pack()
kanvas_sebelum.kontainer_sebelum = kanvas_sebelum.create_image(0, 0, anchor=NW)

frame_sesudah = Frame(frame_gambar, bg=WARNA_LATAR)
frame_sesudah.pack(side=LEFT, padx=20)
Label(frame_sesudah, text="Sesudah", font=("Arial", 12, "bold"), 
     bg=WARNA_LATAR, fg=WARNA_TEKS).pack()
kanvas_sesudah = Canvas(frame_sesudah, width=350, height=300, bg=WARNA_KANVAS, 
                     highlightthickness=2, highlightbackground="#cccccc")
kanvas_sesudah.pack()
kanvas_sesudah.kontainer_sesudah = kanvas_sesudah.create_image(0, 0, anchor=NW)

frame_unduh = Frame(root, bg=WARNA_LATAR)
frame_unduh.pack(pady=20)
tombol_unduh = Button(frame_unduh, text="💾 Simpan Gambar Hasil", width=25, 
                    command=simpan_gambar, state=DISABLED,
                    bg=WARNA_TOMBOL,          
                    fg="white",     
                    activebackground=WARNA_TOMBOL_HOVER, 
                    activeforeground="white",  
                    font=("Arial", 11, "bold"), 
                    relief="flat")
tombol_unduh.pack()


footer = Frame(root, bg=WARNA_LATAR)
footer.pack(side="bottom", pady=10)

root.mainloop()
