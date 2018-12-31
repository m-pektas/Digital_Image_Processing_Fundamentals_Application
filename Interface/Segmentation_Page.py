from tkinter import *
from tkinter import ttk
from Constants import Constant_Images
from PIL import Image, ImageTk
from Computing import compute

segmentation = Toplevel()
segmentation.title("Segmentation Page")
w = 350
h = 300
ws = segmentation.winfo_screenwidth() # width of the screen
hs = segmentation.winfo_screenheight() # height of the screen
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
segmentation.geometry('%dx%d+%d+%d' % (w, h, x, y))

# radio button değerleri için
var = IntVar()
var.set(2)


def show_image(img, process=""):
    """
    Verilen fotoğrafı ekranda gösterir.
    """

    if (img.size[0] > 1500 or img.size[1] > 1500):
        basewidth = 800
        baseheight = 800
        wpercent = (basewidth / float(img.size[0]))
        hpercent = (baseheight / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(wpercent)))
        hsize = int((float(img.size[1]) * float(hpercent)))
        img = img.resize((wsize, hsize), Image.ANTIALIAS)

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
    combo_frame = Frame(segmentation)
    combo_frame.pack()
    labelTop = Label(combo_frame,
                     text="Lütfen İşlem Seçiniz :")
    labelTop.grid(column=0, row=0)

    combobox = ttk.Combobox(combo_frame,
                            values=[
                                "İşlem Seçiniz..",
                                "Gri seviye resimde eşik değeri bulma",
                                "Siyah beyaz resimde 4’lü komşuluk ile nesne bulma ve gösterme",
                                "Gri seviye resimde istenilen bir yöntemle nesne bulma ve gösterme",
                                "Renkli resimde istenilen bir yöntemle nesne bulma ve gösterme",
                                "Gri Resmi Siyah Beyaz'a çevirme"])

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
            print("Gri seviye resimde eşik değeri bulma")
            threshold = compute.Thresholding(result_image)
            print("Thresold : ",threshold)
        elif (choice == 2):
            print("Siyah beyaz resimde 4’lü komşuluk ile nesne bulma ve gösterme")
            result_image = compute.find_object(result_image)
            show_image(result_image,"segmente edilmeye çalışıldı.")
            Constant_Images.last_image = result_image
            Constant_Images.last_image_is_RGB = Constant_Images.image_is_RGB
        elif (choice == 3):
            print("Gri seviye resimde istenilen bir yöntemle nesne bulma ve gösterme")
        elif (choice == 4):
            print("Renkli resimde istenilen bir yöntemle nesne bulma ve gösterme")
        elif (choice == 5):
            print("Gri resmi Siyah beyaza çevir.")
            threshold = compute.Thresholding(result_image)
            result_image = compute.gray2white_and_black(img=result_image,threshold=threshold)
            show_image(img=result_image,process=" Siyah Beyaz Resme Çevirildi.")
            Constant_Images.last_image = result_image
            Constant_Images.last_image_is_RGB = Constant_Images.image_is_RGB
        else:
            show_image(result_image, "Morfolojik İşlem Uygulanmamış Resim")

    combobox.bind("<<ComboboxSelected>>", callbackfunc)


def yes():
    """
    segmentasyon yapılsın seneği seçilince çalışır.
    """

    var.set(1)
    print("Yes")
    combo()


def no():
    """
    segmentasyon yapılmasın.
    """
    var.set(2)
    print("No")


Radio1 = Radiobutton(segmentation, text="Segmentasyon Uygulamak İstiyorum.", variable=var, value=1, command=yes)
Radio1.pack()

Radio2 = Radiobutton(segmentation, text="Segmentasyon Uygulamak İstemiyorum.", variable=var, value=2, command=no)
Radio2.pack()

label = Label(segmentation)
label.pack()

def next_window():
    from Interface.Save_Page import save


#İleri Butonu
next_page = Button(segmentation, text="İleri", fg="white",bg='green', height=3, width=15,command=next_window)
next_page.pack()

segmentation.mainloop()

