from tkinter import *
from tkinter import ttk
from Constants import Constant_Images
from PIL import Image, ImageTk
from Computing import compute

morphologic = Toplevel()
morphologic.title("Morphologic Page")
w = 350
h = 300
ws = morphologic.winfo_screenwidth() # width of the screen
hs = morphologic.winfo_screenheight() # height of the screen
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
morphologic.geometry('%dx%d+%d+%d' % (w, h, x, y))

# radio button değerleri için
var = IntVar()
var.set(2)


def show_image(img, process=""):
    """
    Verilen fotoğrafı ekranda gösterir.
    """
    im_window = Toplevel()
    im_window.title(process)

    image_frame = Frame(im_window)
    image_frame.pack()
    photo = ImageTk.PhotoImage(img)

    text = Label(image_frame, text="İşlem :"+process)
    text.pack()

    myimage = Label(image_frame, image=photo)
    myimage.image = photo
    myimage.pack()


def combo():
    """
    Combobox u ekranda gösterir. Ayrıca tıklandığında gerçekleşecek olaylar burada yer alır.
    """
    combo_frame = Frame(morphologic)
    combo_frame.pack()
    labelTop = Label(combo_frame,
                     text="Lütfen İşlem Seçiniz :")
    labelTop.grid(column=0, row=0)

    combobox = ttk.Combobox(combo_frame,
                            values=[
                                "İşlem Seçiniz..",
                                "Siyah beyaz resimde genişletme",
                                "Siyah beyaz resimde erozyon",
                                "Siyah beyaz resimde açma",
                                "Siyah beyaz resimde kapama"])

    combobox.grid(column=0, row=1)
    combobox.current(0)

    def callbackfunc(cmb):
        """
        Combobox tan gelen durumlara göre grekli işlemleri yapan fonksiyonları çağrır. Ve dönen resmi
        show_image fonksiyonuna göndererek fotoğrafı ekranda gösterir.
        """
        print(combobox.current(), combobox.get())
        choice = combobox.current()
        result_image = Constant_Images.image
        if (choice == 1):
            print("genişletme..")
            result_image = compute.dilation(Constant_Images.image)
            show_image(result_image,"Genişleme İşlemi Uygulanmış Resim")
            Constant_Images.last_image = result_image
            Constant_Images.last_image_is_RGB = Constant_Images.image_is_RGB
        elif (choice == 2):
            print("erozyon")
            result_image = compute.erosion(Constant_Images.image)
            show_image(result_image, "Erezyon İşlemi Uygulanmış Resim")
            Constant_Images.last_image = result_image
            Constant_Images.last_image_is_RGB = Constant_Images.image_is_RGB
        elif (choice == 3):
            print("açma")
            result_image = compute.opening(Constant_Images.image)
            show_image(result_image, "Açma İşlemi Uygulanmış Resim")
            Constant_Images.last_image = result_image
            Constant_Images.last_image_is_RGB = Constant_Images.image_is_RGB
        elif (choice == 4):
            print("kapama")
            result_image = compute.closing(Constant_Images.image)
            show_image(result_image, "Kapama İşlemi Uygulanmış Resim")
            Constant_Images.last_image = result_image
            Constant_Images.last_image_is_RGB = Constant_Images.image_is_RGB
        else:
            show_image(result_image, "Morfolojik İşlem Uygulanmamış Resim")

    combobox.bind("<<ComboboxSelected>>", callbackfunc)


def yes():
    """
    Filtreleme yapılsın seneği seçilince çalışır.
    """

    var.set(1)
    print("Yes")
    combo()


def no():
    """
    filtreleme yapılmasın.
    """
    var.set(2)
    print("No")


Radio1 = Radiobutton(morphologic, text="Morfolojik İşlem Uygulamak İstiyorum.", variable=var, value=1, command=yes)
Radio1.pack()

Radio2 = Radiobutton(morphologic, text="Morfolojik İşlem Uygulamak İstemiyorum.", variable=var, value=2, command=no)
Radio2.pack()

label = Label(morphologic)
label.pack()

def next_window():
    from Interface.Segmentation_Page import segmentation


#İleri Butonu
next_page = Button(morphologic, text="İleri", fg="white",bg='green', height=3, width=15,command=next_window)
next_page.pack()


morphologic.mainloop()

