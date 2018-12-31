import numpy
from tkinter import *
from tkinter import ttk
from Constants import Constant_Images
from PIL import Image, ImageTk

save = Toplevel()
save.title("Save Page")
save.geometry("300x300")

# radio button değerleri için
var = IntVar()
var.set(2)


def combo():
    """
    Combobox u ekranda gösterir. Ayrıca tıklandığında gerçekleşecek olaylar burada yer alır.
    """
    combo_frame = Frame(save)
    combo_frame.pack()
    labelTop = Label(combo_frame,
                     text="Lütfen İşlem Seçiniz :")
    labelTop.grid(column=0, row=0)

    combobox = ttk.Combobox(combo_frame,
                            values=[
                                "Format Seçiniz..",
                                "JPG",
                                "PNG",
                                "BITMAP"])

    combobox.grid(column=0, row=1)
    combobox.current(0)

    def callbackfunc(cmb):
        """
        Combobox tan gelen durumlara göre grekli işlemleri yapan fonksiyonları çağrır. Ve dönen resmi
        show_image fonksiyonuna göndererek fotoğrafı ekranda gösterir.
        """
        result_image = Constant_Images.image
        print(combobox.current(), combobox.get())
        choice = combobox.current()
        if (choice == 1):
            print("JPG")
            Constant_Images.image_type = "JPEG"
        elif (choice == 2):
            print("PNG")
            Constant_Images.image_type = "PNG"


    combobox.bind("<<ComboboxSelected>>", callbackfunc)

combo()

def save_image():
    print()
    if Constant_Images.image_type == "JPEG":
        Constant_Images.image.convert('RGB').save(Constant_Images.save_directory + '/my_saved_photo.jpeg',Constant_Images.image_type)
    elif Constant_Images.image_type == "PNG":
        Constant_Images.image.convert('RGB').save(Constant_Images.save_directory + '/my_saved_photo.png',Constant_Images.image_type)

#İleri Butonu
next_page = Button(save, text="Save", fg="white",bg='blue', height=3, width=15,command=save_image)
next_page.pack()
save.mainloop()

