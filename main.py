import glob
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import filedialog
import os

#tÜM FONT TİPLERİ İÇİN:
def all_font_types():
    font_dir = "C:\\Windows\\Fonts"
    font_paths = glob.glob(os.path.join(font_dir, "*.ttf"))
    font_names = [os.path.basename(fp).split(".")[0] for fp in font_paths]
    return dict(zip(font_names, font_paths))


all_fonts = all_font_types()


#Fotoğraf yükleme:
def upload_image_button():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        global image1, original_image
        print(f"Opened file: {file_path}")
        original_image = Image.open(file_path)
        new_image(original_image)

def new_image(img):
    max_width, max_height = 800, 600
    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    global image1
    image1 = img.copy()
    photo = ImageTk.PhotoImage(img)
    label_photo.config(image=photo)
    label_photo.image = photo


#Renkleri RGB değerleriyle eşleştiren sözlük:
color_values = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "purple": (128, 0, 128),
    "orange": (255, 165, 0),
    "pink": (255, 192, 203)
}


#Fotoğrafı kaydetmek:
def save_image_button():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
    if file_path:
        if image1:
            image1.save(file_path)
            print(f"Saved file: {file_path}")
        else:
            print("Failed to save!")


#Fotoğrafın üstüne yazıyı eklemek için:
def add_text():
    global image1
    if image1:
        image1 = original_image.copy().convert("RGBA")
        txt_layer = Image.new("RGBA", image1.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)
        text = entry1.get()
        font_type = font_spinbox.get()
        font_size = int(font_size_scale.get())
        color = color_spinbox.get()

        opacity = int((100 - opacity_scale.get()) * 255 / 100)
        rgba_color = color_values[color] + (opacity,)

        font_path = all_fonts.get(font_type, None)
        if font_path:
            try:
                font = ImageFont.truetype(font_path, font_size)
            except IOError:
                font = ImageFont.load_default()
        else:
            font = ImageFont.load_default()

        try:
            x = int(entry_x.get())
            y = int(entry_y.get())
        except ValueError:
            x, y = 10, 10


        #Metni çizmek için:
        draw.text((x, y), text, font=font, fill=rgba_color)

        combined = Image.alpha_composite(image1, txt_layer)

        photo = ImageTk.PhotoImage(combined)
        label_photo.config(image=photo)
        label_photo.image = photo
        image1 = combined


#---------------TKINTER GUI------------------
window = tk.Tk()
window.title("Watermark")
window.minsize(width=900, height=600)

#Font tipi:
bold_font = tkfont.Font(family="Helvetica", size=9, weight="bold")

#Left Frame:
left_frame = tk.Frame(window)
left_frame.grid(row=0, column=0, sticky="nsew")

label_photo = tk.Label(left_frame)
label_photo.grid(row=0, column=0, rowspan=4, columnspan=4, padx=50)

#Right Frame:
right_frame = tk.Frame(window)
right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

button1 = tk.Button(right_frame, text="Upload Image", width=28, height=2, bg="black", fg="white", command=upload_image_button)
button1.grid(row=0, column=0, padx=16, pady=20)

button2 = tk.Button(right_frame, text="Save", width=28, height=2, bg="black", fg="white", command=save_image_button)
button2.grid(row=0, column=1, padx=16, pady=20)

button3 = tk.Button(right_frame, text="Add Watermark", width=28, height=2, bg="black", fg="white", command=add_text)
button3.grid(row=0, column=2, padx=16, pady=20)

#Girilecek metin için başlık:
label1 = Label(right_frame, text="TEXT TO WATERMARK:", font=bold_font)
label1.grid(row=1, column=0, padx=10, pady=25, sticky="w")

#Girilecek metin için entry:
entry1 = Entry(right_frame, width=55)
entry1.grid(row=1, column=1, padx=10, pady=25)
entry1.get()

#Font değişikliği için başlık:
label_font = Label(right_frame, text="Font:", font=bold_font)
label_font.grid(row=2, column=0, padx=40, pady=25, sticky="w")

#Font seçenekleri için spinbox:
font_families = list(all_fonts.keys())
font_spinbox = tk.Spinbox(right_frame, values=font_families, width=50)
font_spinbox.grid(row=2, column=1, padx=10, pady=25)

font_size_label = tk.Label(right_frame, text="Font Size:", font=bold_font)
font_size_label.grid(row=3, column=0, padx=40, pady=25, sticky="w")

#Boyut ölçeklendirme:
font_size_scale = tk.Scale(right_frame, from_=12, to=150, orient="horizontal", length=320)
font_size_scale.grid(row=3, column=1, padx=25, pady=10)

#Renkler ve renk değişikliği için başlık:
color_label = Label(right_frame, text="Color:", font=bold_font)
color_label.grid(row=4, column=0, padx=40, pady=25, sticky="w")

#Renk spinboxı için seçilen rengi arka plan ve metnin rengi yapma:
def spinbox_bg_color(*args):
    selected_color = color_spinbox.get()
    color_spinbox.config(bg=selected_color, fg=selected_color)


#Renk spinbox:
colors = ["red", "green", "blue", "yellow", "black", "white", "purple", "orange", "pink"]
color_spinbox = tk.Spinbox(right_frame, values=colors, command=spinbox_bg_color, width=50)
color_spinbox.grid(row=4, column=1, padx=10, pady=25)

#Spinox olaylarını bağlama:
color_spinbox.bind('<Configure>', lambda event: spinbox_bg_color())
color_spinbox.bind('<ButtonRelease-1>', lambda event: spinbox_bg_color())
color_spinbox.bind('<KeyRelease>', lambda event: spinbox_bg_color())

position_label = Label(right_frame, text="Position (X, Y):", font=bold_font)
position_label.grid(row=6, column=0, padx=40, pady=25, sticky="w")

entry_x = Entry(right_frame, width=10)
entry_x.grid(row=6, column=1, padx=25, pady=25, sticky="w")

entry_y = Entry(right_frame, width=10)
entry_y.grid(row=6, column=1, padx=100, pady=25, sticky="w")

#Grid yapısını genişletme:
window.grid_columnconfigure(0, weight=1)


#Opaklık başlık ve ayarı:
opacity_label = Label(right_frame, text="Opacity:", font=bold_font)
opacity_label.grid(row=5, column=0, padx=40, pady=25, sticky="w")

opacity_scale = tk.Scale(right_frame, from_=0, to=100, orient="horizontal", length=320)
opacity_scale.grid(row=5, column=1, padx=10, pady=25)


window.mainloop()










