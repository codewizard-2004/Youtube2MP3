from PIL import Image
Image.CUBIC = Image.BICUBIC
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog , messagebox
import tkinter as tk
import server
import urllib.request
from PIL import Image, ImageTk
import io
import os


root = ttk.Window(themename='yeti')
root.title("YouTube2MP3")
root.geometry('1460x800')
root.iconbitmap("main_logo.ico")
root.resizable(0,0)


main_bg=ttk.PhotoImage(file="bg1.png")
main_bg_label=ttk.Label(root,image=main_bg)
main_bg_label.pack()

def when_formated(e):
    if form.get()=="MP4":
        qual.config(state='readonly')
    if form.get()=="MP3":
        qual.config(state='disabled')


folder=''
def destination():
    global folder
    root.filename=filedialog.askdirectory(initialdir='E:/Users/AMAL',title="Select save location")
    folder=str(root.filename)
    dest.delete(0,END)
    dest.config(state="normal")
    dest.insert(END,folder)

def start_search():
    try:
        if url.get()=='':
            messagebox.showinfo("INFO""Please","Enter a valid URL")
            return
        else:
            global data
            data=server.find_video(url.get())
            if data==0:
                messagebox.showinfo("URL","Use a vaild url")
            else:
                desc.config(text='title: '+data['title']+'\n'+"Channel: "+data['channel'])
                desc.place(x=850,y=350)
                with urllib.request.urlopen(data["thumbnail"]) as u:
                    raw_data=u.read()
                im = Image.open(io.BytesIO(raw_data))
                global img
                img = ImageTk.PhotoImage(im)
                thumb.config(image=img)
                thumb.place(x=850,y=10)
                down.config(state="normal")

        
    except:
        messagebox.showerror("An unexcepted error occured")


def start_download():
    global folder
    if qual.get()=="normal quality":
         reso=0
    else:
        reso=1
    if dest.get()=='':
        messagebox.showinfo("Destination","Enter the path to save")
        return
    else:
        if form.get()=='MP3':
            if server.download_audio(url.get(),folder)==0:
                messagebox.showinfo("Error","an unexpected error occured")
            else:
                messagebox.showinfo("Complete","download complete")
                url.delete(0,END)
                dest.delete(0,END)
                thumb.place_forget()
                os.rename(folder+'/'+data['title']+'.mp4',folder+'/'+data['title']+'.mp3')
                folder=''
                desc.place_forget()
            return
        if form.get()=='MP4':
            
            if server.download_video(url.get(),reso,folder)==0:
                messagebox.showinfo("Error","an unexpected error occured")
            else:
                messagebox.showinfo("Complete","download complete")
                url.delete(0,END)
                dest.delete(0,END)
                thumb.place_forget()
                folder=''
                desc.place_forget()
            return

url_txt="Enter vaid url here"

def onenter(e):
    if url.get()==url_txt:
        url.delete(0,END)
        print(1)
def onleave(e):
    if url.get()=='':
        url.insert(END,url_txt)
    else:
        pass
        


def tandc():
    window=ttk.Toplevel()
    window.geometry('500x300')
    window.resizable(0,0)
    window.title("Terms and Conditions")
    ttk.Label(window,text="This software was created by Amal Varghese\nThis app and all of its text, images are provided\non a basis without any warranty\nYou agree that you must bear all risks associated\nwith the use of this software").pack()


url=ttk.Entry(root,width=47,font=('Helvatica 16'),bootstyle='warning')
url.insert(END,url_txt)
url.bind("<Button-1>",onenter)
url.bind("<Leave>",onleave)
url.place(x=700,y=600)


check=ttk.Button(root,text="SEARCH",bootstyle="warning",width=20,command=start_search)
check.place(x=950,y=650)

saveto=ttk.Button(root,text="SAVE TO",bootstyle="warning",width=20,command=destination)
saveto.place(x=700,y=700)

dest=ttk.Entry(root,width=40,font=('Helvatica 12'),bootstyle='warning')
dest.place(x=900,y=700)

form=ttk.Combobox(root,bootstyle='warning',values=["MP3",'MP4'],state="readonly")
form.current(0)
form.bind("<<ComboboxSelected>>",when_formated)
form.place(x=950,y=400)

qual=ttk.Combobox(root,bootstyle="warning",state='disabled',values=["normal quality",'max quality'])
qual.current(1)
qual.place(x=950,y=450)

thumb=tk.Label(root,height=350,width=500)
desc=ttk.Label(root,bootstyle="warning",font=("helvatica 10"))
down=ttk.Button(root,text="DOWNLOAD",bootstyle="warning",width=20,command=start_download,state='disabled')
down.place(x=950,y=500)


abt=ttk.Button(root,text="Read",bootstyle='warning',width=5,command=tandc)
abt.place(x=170,y=745)


root.mainloop()
