from tkinter import *
from tkinter import ttk
from Constants import Constant_Images,Filters
from PIL import Image, ImageTk
from Computing import compute

filtering = Toplevel()
filtering.title("Filtering Page")
w = 350
h = 300
ws = filtering.winfo_screenwidth() # width of the screen
hs = filtering.winfo_screenheight() # height of the screen
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
filtering.geometry('%dx%d+%d+%d' % (w, h, x, y))

# radio button değerleri için
var = IntVar()
var.set(2)

def show_image(img,process=""):
    """
    Verilen fotoğrafı ekranda gösterir.
    """
    if(img.size[0]>1500 or img.size[1]>1500):
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

    text = Label(image_frame, text="Resim :"+process)
    text.pack()

    myimage = Label(image_frame, image=photo)
    myimage.image = photo
    myimage.pack()

    print("LOG :: Yeni Pencerede Fotoğran Gösterildi. ")


def combo():
    """
    Combobox u ekranda gösterir. Ayrıca tıklandığında gerçekleşecek olaylar burada yer alır.
    """
    combo_frame = Frame(filtering)
    combo_frame.pack()
    labelTop = Label(combo_frame,
                     text="Lütfen Filtre Seçiniz :")
    labelTop.grid(column=0, row=0)

    combobox = ttk.Combobox(combo_frame,
                            values=[
                                "Filtre Seçiniz..",
                                "Bulanıklaştırma Filtresi",
                                "Keskinleştirme Filtresi",
                                "Ortanca Filtresi",
                                "Laplace Filtresi",
                                "Kenar Bulma Filtresi"])

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

            print("LOG :: Bulanıklaştırma Filtresi Uygulanıyor.. ")
            if (Constant_Images.image_is_RGB):
                result_image = compute.conv2d(img=Constant_Images.image,filter=Filters.blur_filter, channel="RGB")
            else:
                result_image = compute.conv2d(img=Constant_Images.image, filter=Filters.blur_filter, channel="I")
            show_image(result_image, "Bulanıklaştırma Filtresi Uygulanmış Resim")
            Constant_Images.last_image = result_image
        elif (choice == 2):

            print("LOG :: Keskinleştirme  Filtresi Uygulanıyor.. ")
            if (Constant_Images.image_is_RGB):
                result_image = compute.conv2d(img=Constant_Images.image,filter=Filters.sharpen_filter, channel="RGB")
            else:
                result_image = compute.conv2d(img=Constant_Images.image, filter=Filters.sharpen_filter, channel="I")
            show_image(result_image, "Keskinleştirme Filtresi Uygulanmış Resim")
            Constant_Images.last_image = result_image
            Constant_Images.last_image_is_RGB = Constant_Images.image_is_RGB
        elif (choice == 3):

            print("LOG :: Median  Filtresi Uygulanıyor.. ")
            if(Constant_Images.image_is_RGB):
                result_image = compute.median(img=Constant_Images.image, channel="RGB")
            else:
                result_image = compute.median(img=Constant_Images.image, channel="I")

            show_image(result_image, "Median Filtresi Uygulanmış Resim")
            Constant_Images.last_image = result_image
            Constant_Images.last_image_is_RGB = Constant_Images.image_is_RGB
        elif (choice == 4):

            print("LOG :: Laplace  Filtresi Uygulanıyor.. ")
            if (Constant_Images.image_is_RGB):
                result_image = compute.conv2d(img=Constant_Images.image,filter=Filters.laplace_filter, channel="RGB")
            else:
                result_image = compute.conv2d(img=Constant_Images.image,filter=Filters.laplace_filter,  channel="I")

            show_image(result_image, "Laplace Filtresi Uygulanmış Resim")
            Constant_Images.last_image = result_image
            Constant_Images.last_image_is_RGB = Constant_Images.image_is_RGB
        elif (choice == 5):

            print("LOG :: Kenar Bulma  Filtresi Uygulanıyor.. ")
            if(Constant_Images.image_is_RGB):
                result_image = compute.edge_detect(img=Constant_Images.image, channel="RGB")
            else:
                result_image = compute.edge_detect(img=Constant_Images.image, channel="I")
            show_image(result_image, "Kenar Bulma Filtresi Uygulandı.")
            Constant_Images.last_image = result_image
            Constant_Images.last_image_is_RGB = Constant_Images.image_is_RGB
        else:
            show_image(result_image, "Not Filtered Image")

    combobox.bind("<<ComboboxSelected>>", callbackfunc)


def yes():
    """
    Filtreleme yapılsın seneği seçilince çalışır.
    """
    print("LOG :: Filtre Uygulanmak İstenildi. ")
    var.set(1)
    print("Yes")
    combo()


def no():
    """
    filtreleme yapılmasın.
    """

    print("LOG :: Filtre Uygulanmak İstenilmedi. ")
    var.set(2)


Radio1 = Radiobutton(filtering, text="Filtre Uygulamak İstiyorum.", variable=var, value=1, command=yes)
Radio1.pack()

Radio2 = Radiobutton(filtering, text="Filtre Uygulamak İstemiyorum.", variable=var, value=2, command=no)
Radio2.pack()

label = Label(filtering)
label.pack()

def next_window():
    from Interface.Morphologic_Page import morphologic


#İleri Butonu
next_page = Button(filtering, text="İleri", fg="white",bg='green', height=3, width=15,command=next_window)
next_page.pack()

filtering.mainloop()

