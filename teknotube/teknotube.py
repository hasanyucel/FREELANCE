from pytube import YouTube
import os,sys
link = input("Lütfen bir link girer misin sevgili kardeşim:  ")
yt = YouTube(link)
print("Başlık: ",yt.title)
print("İzlenme Sayısı: ",yt.views)
print("Uzunluk: ",yt.length, " saniye")

v_or_m = input("Video istiyorsan 1 Müzik istiyorsan 2'ye bas: ")

if v_or_m == '1':
    ys = yt.streams.get_highest_resolution()
    print("İndiriliyor...")
    ys.download()
    print("İndirme Tamamlandı!")
elif v_or_m == '2':
    ys = yt.streams.filter(only_audio=True).first()
    print("İndiriliyor...")
    out_file = ys.download()
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    print("İndirme Tamamlandı!")


def check_quit(inp):
    if inp == 'e':
        sys.exit(0)
    else:
        sys.exit(0)
x = str(input("Lütfen Çıkmak İçin enter tuşuna basın: "))
check_quit(x)