from tkinter import *
from tkinter import ttk
from Constants import Constant_Images
from PIL import Image, ImageTk
from Computing import compute

preprocess = Toplevel()
preprocess.title("Preprocessing Page")
w = 350
h = 300
ws = preprocess.winfo_screenwidth() # width of the screen
hs = preprocess.winfo_screenheight() # height of the screen
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
preprocess.geometry('%dx%d+%d+%d' % (w, h, x, y))


#radio button değerleri için
var = IntVar()
var.set(2)

print("LOG :: Ön İşleme Sayfası Açıldı. ")

def show_image(img,process=""):
    """
    Verilen fotoğrafı ekranda gösterir.
    """
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
    combo_frame = Frame(preprocess)
    combo_frame.pack()
    labelTop = Label(combo_frame,
                     text="Lütfen Ön İşleme Seçiniz :")
    labelTop.grid(column=0, row=0)

    combobox = ttk.Combobox(combo_frame,
                            values=[
                                "Ön İşlem Seçiniz..",
                                "Renkli Resmi Gri Seviyeye Dönüştürme",
                                "Resmi Büyültme",
                                "Resmi Küçültme",
                                "Resmi Kesme",
                                "Histogram Oluşturma"])

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
        if(choice==1):
            print("LOG :: Resmi Gri Seviyeye  Çevrildi. ")
            result_image = compute.convert2gray(img=Constant_Images.image)
            show_image(result_image, " Gri Seviye Resim")
            Constant_Images.last_image = result_image
            Constant_Images.last_image_is_RGB = False
        elif(choice==2):
            print("LOG :: Resim Büyütülüyor.. ")
            if(Constant_Images.image_is_RGB):
                result_image = compute.zoom_in(img=Constant_Images.image,channel="RGB")
            else:
                result_image = compute.zoom_in(img=Constant_Images.image, channel="I")

            show_image(result_image, " Büyütülmüş Resim")
            Constant_Images.last_image = result_image
            Constant_Images.last_image_is_RGB = Constant_Images.image_is_RGB
        elif (choice == 3):

            print("LOG :: Resim Küçültülüyor.. Boyut :",Constant_Images.image.size)
            if(Constant_Images.image_is_RGB):
                result_image = compute.zoom_out(img=Constant_Images.image, channel="RGB")
            else:
                result_image = compute.zoom_out(img=Constant_Images.image, channel="I")
            print("LOG :: Küçük Resim Boyut :",result_image.size)
            show_image(result_image, " Küçültülmüş Resim")
            Constant_Images.last_image = result_image
            Constant_Images.last_image_is_RGB = Constant_Images.image_is_RGB
        elif (choice == 4):
            print("Resmi Kes")
        elif (choice == 5):
            print("LOG :: Histogram Oluşturuluyor.. ")

            if(not Constant_Images.image_is_RGB):#gri ise
                result_image = compute.draw_hist(result_image,channel="I")
                show_image(result_image, "Gray Histogram")
            else:
                result_imageR, result_imageG, result_imageB = compute.draw_hist(result_image,channel='RGB')
                show_image(result_imageR, "Red Histogram")
                show_image(result_imageG, "Green Histogram")
                show_image(result_imageB, "Blue Histogram")
        else:
            show_image(result_image,"Not Preprocessed Image")


    combobox.bind("<<ComboboxSelected>>", callbackfunc)


def yes():
    """
    Ön işleme yapılsın seneği seçilince çalışır.
    """
    print("LOG :: Ön İşleme Yapmak İstenildi. ")
    var.set(1)
    combo()

def no():
    print("LOG :: Ön İşleme Yapmak İstenilmedi. ")
    """
    ön işleme yapılmasın.
    """
    var.set(2)



Radio1 = Radiobutton(preprocess, text="Ön işleme Yapmak İstiyorum.", variable=var, value=1,command=yes)
Radio1.pack()

Radio2 = Radiobutton(preprocess, text="Ön İşleme Yapmak İstemiyorum.", variable=var, value=2,command=no)
Radio2.pack()

label = Label(preprocess)
label.pack()

def next_window():
    from Interface.Filtering_Page import filtering


#İleri Butonu
next_page = Button(preprocess, text="İleri", fg="white",bg='green', height=3, width=15,command=next_window)
next_page.pack()


preprocess.mainloop()

