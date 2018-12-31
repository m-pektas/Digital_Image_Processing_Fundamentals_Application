from tkinter import *
import tkinter as tk
from tkinter.font import Font

from PIL import Image, ImageTk
from tkinter import filedialog
from Constants import Constant_Images

Global_Image = None

window_background = 'LightBlue4'


root = Tk()
root.title("Digital Image Processing")

#pencereyi ekranın merkezinde açar.
w = 540
h = 710
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.configure(background=window_background,padx=20,pady=20)

frame = Frame(root)
frame.grid(row=0, column=0)
frame.config(background=window_background)

#buttonlar
main_frame = Frame(frame)
main_frame.grid(row=0, column=0)

#resim frame
image_frame = Frame(frame)
image_frame.grid(row=1, column=0)

#menu frame
menu_frame = Frame(frame)
menu_frame.grid(row=1, column=1)
menu_frame.config(bd=5)

#resim
text = Label(image_frame, text="Açılan Resim :")
text.grid(row=0, column=0)

#resim için çerçeve
myimage = Label(image_frame, height=38, width=71)
myimage.grid(row=1, column=0)


print("LOG :: Program Çalıştı. ")
def image_choose_btn():
    path = filedialog.askopenfilename(filetypes=[("Image File",'.jpg'),("Image File",'.png')])
    print(path)
    im = Image.open(path).convert("RGB")

    #image convert gray or RGB
    image_px = im.load()
    if (image_px[0, 0][0] == image_px[0, 0][1] and
            image_px[0, 0][0] == image_px[0, 0][2] and
            image_px[0, 0][1] == image_px[0, 0][2]):

        im = im.convert("I")
        Constant_Images.image_is_RGB = FALSE

    print(im.mode)

    #resim geçmişine ekle
    Constant_Images.image_migration.append(im)
    Constant_Images.image_migration_index += 1
    Constant_Images.image_migration_RGB.append(Constant_Images.image_is_RGB)


    basewidth = 500
    baseheight = 550
    wpercent = (basewidth / float(im.size[0]))
    hpercent = (baseheight / float(im.size[1]))
    wsize = int((float(im.size[0]) * float(wpercent)))
    hsize = int((float(im.size[1]) * float(hpercent)))
    img = im.resize((wsize, hsize), Image.ANTIALIAS)

    Constant_Images.image = im
    photo = ImageTk.PhotoImage(img)

    myimage = Label(image_frame, image=photo)
    myimage.image = photo
    myimage.grid(row=1, column=0)
    #myimage.bind("<Button>", mouseClick)

    #ileri butonu aktif edildi.
    next_page.config(state='normal')

    print("LOG :: Resim Yüklendi. ")

def next_window():
    from Interface.Preprocess_Page import preprocess

def save():
    print("LOG :: Çıktı Orjinal Resme Uygulanıyor.. ")
    Constant_Images.image = Constant_Images.last_image
    Constant_Images.image_is_RGB = Constant_Images.last_image_is_RGB

    #resim geçimişine ekle
    Constant_Images.image_migration.append(Constant_Images.image)
    Constant_Images.image_migration_index +=1
    Constant_Images.image_migration_RGB.append(Constant_Images.image_is_RGB)
    print("migration_index :",Constant_Images.image_migration_index)

    basewidth = 500
    baseheight = 550
    wpercent = (basewidth / float(Constant_Images.image.size[0]))
    hpercent = (baseheight / float(Constant_Images.image.size[1]))
    wsize = int((float(Constant_Images.image.size[0]) * float(wpercent)))
    hsize = int((float(Constant_Images.image.size[1]) * float(hpercent)))
    img = Constant_Images.image.resize((wsize, hsize), Image.ANTIALIAS)

    photo = ImageTk.PhotoImage(img)
    myimage = Label(image_frame, image=photo)
    myimage.image = photo
    myimage.grid(row=1, column=0)

def back():


    index = Constant_Images.image_migration_index
    if index == 0:
        return
    print("LOG :: Orjinal Resmin Üzerindeki Değişiklik Geri Alınıyor... ")
    Constant_Images.image = Constant_Images.image_migration[index-1]
    Constant_Images.image_is_RGB = Constant_Images.image_migration_RGB[index-1]
    Constant_Images.image_migration.remove(Constant_Images.image_migration[index])
    Constant_Images.image_migration_RGB.remove(Constant_Images.image_migration_RGB[index])
    Constant_Images.image_migration_index -= 1

    basewidth = 500
    baseheight = 550
    wpercent = (basewidth / float(Constant_Images.image.size[0]))
    hpercent = (baseheight / float(Constant_Images.image.size[1]))
    wsize = int((float(Constant_Images.image.size[0]) * float(wpercent)))
    hsize = int((float(Constant_Images.image.size[1]) * float(hpercent)))
    img = Constant_Images.image.resize((wsize, hsize), Image.ANTIALIAS)

    photo = ImageTk.PhotoImage(img)
    myimage = Label(image_frame, image=photo)
    myimage.image = photo
    myimage.grid(row=1, column=0)

helv36 = Font(family='Helvetica', size=12, weight='bold')
#BUTTONLARRRR

#Dosya seç butonuna tıklanma olayı
resim_sec = Button(main_frame, text="Resim Seç", fg="white",bg='black', height=3, width=12, command=image_choose_btn,bd=5,
                   font=helv36)
resim_sec.grid(row=0,column=0)

next_page = Button(main_frame, text="Uygula", fg="white",bg='maroon4', height=3, width=11,command=save,bd=5,font=helv36)
next_page.grid(row=0, column=1)

next_page = Button(main_frame, text="İşlemi Geri Al", fg="white",bg='firebrick4', height=3, width=11,command=back,bd=5,font=helv36)
next_page.grid(row=0, column=2)

#İleri Butonu
next_page = Button(main_frame, text="İleri", fg="white",bg='PaleGreen2', height=3, width=11,command=next_window,bd=5,font=helv36)
next_page.grid(row=0, column=3)
next_page.config(state='disabled')


root.mainloop()