import qrcode
from PIL import Image,ImageTk
import tkinter as tk

root = tk.Tk()
root.geometry("300x300")
entry = tk.Entry(root)
entry.pack()
def click():
    a = entry.get()
    qr = qrcode.QRCode(version=1,box_size=10, border=4)
    qr.add_data(a)
    qr.make(fit= True)
    b = qr.make_image(fill="black", back="white")
    label = tk.Label(root, text= "now qr code generated")
    label.pack()
    b.save("hi.png")

def show():
    win1 = tk.Toplevel(root)
    img = Image.open("hi.png")
    photo = ImageTk.PhotoImage(img)
    label1 = tk.Label(win1, image=photo)
    label1.image = photo
    label1.pack()


button = tk.Button(root, text ="click to generate", command=click)
button.pack()
button2 = tk.Button(root, text ="show", command=show)
button2.pack()
root.mainloop()
