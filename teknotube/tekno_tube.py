from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube
from PIL import ImageTk, Image
import os

KlasorAdi = ""
labelBg = "#dcdcdc"
labelFg = "black"

def KlasorSec():
        global KlasorAdi
        KlasorAdi =  filedialog.askdirectory()
        if(len(KlasorAdi) > 1):
            loadingLabel.config(text=KlasorAdi,fg="green")
        else:
            loadingLabel.config(text="Lütfen Klasör Seçiniz!",fg="red")
        
def dosyaDownload():
        
        tur = youtubeChoices.get()
        video = youtubeEntry.get()
        
        if(len(video)>1):
                print(video," - ",KlasorAdi)
                yt = YouTube(video)
                print("Video Adı:",yt.title)
                
                if(tur == downloadChoices[0]):
                    loadingLabel.config(text="Video dosyası indiriliyor...")
                    selectedVideo = yt.streams.get_highest_resolution()
                    selectedVideo.download(KlasorAdi)
                    loadingLabel.config(text=("İndirme Tamamlandı."))
                    
                elif(tur == downloadChoices[1]):
                    loadingLabel.config(text="Müzik dosyası indiriliyor...")
                    selectedVideo = yt.streams.filter(only_audio=True).first()
                    out_file = selectedVideo.download(KlasorAdi)
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    os.rename(out_file, new_file)
                    loadingLabel.config(text=("İndirme Tamamlandı."))
                    
        else:
                loadingLabel.config(text="Lütfen linki giriniz!",fg="red")
           
root = Tk()
root.title("Youtube Video İndirici - Teknostube")    
root.grid_columnconfigure(0, weight=1)  #strech things Horiontally
root.configure(background='#dcdcdc')
root.resizable(False,False)
root.geometry('700x500')

# Load the image
image=Image.open('1.jpg')
img=image.resize((320, 88))
my_img=ImageTk.PhotoImage(img)
label=Label(root, image=my_img)
label.grid(pady=(0,0),column=0,row=0,sticky="N")

youtubeLinkLabel = Label(root,text="Link",fg=labelFg,bg=labelBg,font=("Arial", 10))
youtubeLinkLabel.grid(pady=(15,0),column=0,row=1)
#==========get youtube link in entry box
youtubeEntryVar = StringVar()
youtubeEntry = Entry(root, width=60,textvariable=youtubeEntryVar)
youtubeEntry.grid(pady=(0,0),column=0,row=2) #,sticky="e"

# Asking where to save file label
SaveLabel = Label(root,text="Dosyanın indirileceği yer: ",fg=labelFg,bg=labelBg,font=("Arial", 10))
SaveLabel.grid(pady=(15,0))
# Asking where to save file Button
SaveEntry = Button(root,width=15,bg="green",fg=labelFg,text="Klasör Seç",font=("arial",15),command=KlasorSec)
SaveEntry.grid()

youtubeChooseLabel = Label(root,text="Lütfen indirme türünü seçiniz: ",fg=labelFg,bg=labelBg,font=("Arial", 10))
youtubeChooseLabel.grid(pady=(20,0))

downloadChoices = ["Video","Müzik"]

youtubeChoices = ttk.Combobox(root,values=downloadChoices)
youtubeChoices.grid()
             
downloadButton = Button(root,text="İndir", width=50,fg=labelFg,bg="green",font=("arial",15),command=dosyaDownload)
downloadButton.grid(pady=(40,0))

loadingLabel = Label(root,text="Teknostube",fg=labelFg,bg=labelBg,font=("Arial", 20))
loadingLabel.grid(pady=(20,0))
root.mainloop()