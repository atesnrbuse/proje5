# İkinci el telefon ilan analiz sistemi

from html.parser import HTMLParser
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

class PhoneListing:
    def __init__(self, model, fiyat, şehir, durum):
        self.model = model
        self.fiyat = fiyat
        self.şehir = şehir
        self.durum = durum
        
    def __str__(self):
        return f"{self.model} | {self.fiyat} | {self.şehir} | {self.durum}"

class Koleksiyon:
    def __init__(self):
        self.ilanlar = []  
        self.index = 0      

    def ilan_ekle(self, yeni_ilan):
        self.ilanlar.append(yeni_ilan)
        
    def ilan_al(self):
        return self.ilanlar  

    def __iter__(self):
        self.index = 0  
        return self

    def __next__(self):
        if self.index < len(self.ilanlar):
            ilan = self.ilanlar[self.index]
            self.index += 1
            return ilan
        else:
            raise StopIteration  

    def toplam_ilan(self):
        return len(self.ilanlar)
    
class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.in_listing = False      
        self.current_field = None  
        self.current_data = {}
        self.listing = []

    def handle_starttag(self, tag, attrs):   
        attrs_dict = dict(attrs)
        if tag == "div" and attrs_dict.get("class") == "listing":
            self.in_listing = True
        if self.in_listing:
            if tag == "h2":
                self.current_field = "title"
            elif tag == "p":
                self.current_field = attrs_dict.get("class")

    def handle_data(self, data):            
        if self.current_field:
            temiz_veri = data.strip()
            if temiz_veri:
                self.current_data[self.current_field] = temiz_veri

    def handle_endtag(self, tag):            
        if tag in ["h2","p"]:
            self.current_field = None

        elif tag == "div" and self.in_listing:
            listing_nenesi = PhoneListing(
                model = self.current_data.get("title"),
                fiyat = self.current_data.get("price"),
                şehir = self.current_data.get("city"),
                durum = self.current_data.get("condition")
            )

        self.listing.append(listing_nenesi)
        self.in_listing = False
        self.current_data = {}

        def bütce_araligi_üret(başlangic, bitis, artis):
            while başlangic < bitis:
                yield f"{baslangic} - {baslangic + artis}"
                başlangic += artis

            for aralik in bütçe_araligi_üret(0, 30000, 10000):
                print(aralik)

html_içeriği = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Telefon İlanları</title>
</head>
<body>
    <div class = "listing">
        <h2>iPhone13</h2>
        <p class = "fiyat" > 28.500 TL </p>
        <p class = "şehir" > İstanbul </p>
        <p class = "durum"> Temiz </p>
    </div>
    <div class = "listing">
        <h2>Samsung Galaxy S23</h2>
        <p class = "fiyat" > 31.000 TL </p>
        <p class = "şehir"> Ankara </p>
        <p class = "durum" > Çok Temiz </p>
    </div>
    <div class = "listing">
        <h2>Xiaomi 13T</h2>
        <p class = "fiyat" > 19.750 TL </p>
        <p class = "şehir"> İzmir </p>
        <p class = "durum" > İyi </p>
    </div>
    <div class = "listing">
        <h2>İphone 11</h2>
        <p class = "fiyat" > 17.200 TL </p>
        <p class = "şehir"> Bursa </p>
        <p class = "durum" > Normal </p>
    </div>
    <div class = "listing">
        <h2>Samsung Galaxy A55</h2>
        <p class = "fiyat" > 16.800 TL </p>
        <p class = "şehir"> Antalya </p>
        <p class = "durum" > Temiz </p>
    </div>
    <div class = "listing">
        <h2>İphone 15</h2>
        <p class = "fiyat" > 49.000 TL </p>
        <p class = "şehir"> İstanbul </p>
        <p class = "durum" > Sıfıra Yakın </p>
    </div>
    <div class="listing">
        <h2>Honor Magic 6 Pro</h2>
        <p class="fiyat">38.500 TL</p>
        <p class="şehir">Konya</p>
        <p class="durum">Çok Temiz</p>
    </div>
    <div class="listing">
        <h2>Nothing Phone 2</h2>
        <p class="fiyat"> 24.300 TL</p>
        <p class="şehir"> Eskişehir </p>
        <p class="durum"> İyi </p>
    </div>
    <div class="listing">
        <h2>Google Pixel 8</h2>
        <p class="fiyat"> 29.900 TL</p>
        <p class="şehir"> İstanbul </p>
        <p class="durum"> Temiz </p>
    </div>
    <div class="listing">
        <h2>Samsung Galaxy Z Flip 5</h2>
        <p class="fiyat"> 34.600 TL </p>
        <p class="şehir"> Ankara </p>
        <p class="durum"> Çok Temiz </p>
    </div>

</body>
</html>
'''      

soup = BeautifulSoup(html_içeriği, "html.parser")
tüm_ilanlar = []
fiyat_listesi = []  

ilanlar = soup.find_all('div', class_='listing')

for ilan in ilanlar:
    model_etiketi = ilan.find("h2")
    model = model_etiketi.text.strip() if model_etiketi else "Bilinmiyor"

    fiyat_etiketi = ilan.find("p", class_="fiyat")
    if fiyat_etiketi:
        ham_fiyat = fiyat_etiketi.text.strip()
        fiyat = ham_fiyat.replace(".", "").replace("TL", "").strip()
        fiyat_listesi.append(int(fiyat))
    else:
        fiyat = "0"

    sehir_etiketi = ilan.find("p", class_="şehir")
    şehir = sehir_etiketi.text.strip() if sehir_etiketi else "Belirtilmemiş"

    durum_etiketi = ilan.find("p", class_="durum")
    durum = durum_etiketi.text.strip() if durum_etiketi else "Belirtilmemiş"

    ilan_sozlugu = {
        "model": model,
        "price": fiyat,
        "city": şehir,
        "condition": durum
    }

    tüm_ilanlar.append(ilan_sozlugu)

df = pd.DataFrame(tüm_ilanlar)
df.to_csv('telefon_ilanlari.csv', index=False, sep=',', encoding='utf-8-sig')

print(f"Toplam {len(tüm_ilanlar)} ilan başarıyla 'ilanlar.csv' dosyasına kaydedildi!")

print("NUMPY ANALİZ SONUÇLARI")
if len(fiyat_listesi) > 0:
    fiyatlar_nd = np.array(fiyat_listesi)

    ortalama_fiyat = np.mean(fiyatlar_nd)
    en_düşük_fiyat = np.min(fiyatlar_nd)
    en_yüksek_fiyat = np.max(fiyatlar_nd)
    medyan = np.median(fiyatlar_nd)
    std_sapma = np.std(fiyatlar_nd)

    x = np.sum(fiyatlar_nd < 20000)
    y = np.sum(fiyatlar_nd > 30000)

    print(f"- Ortalama Fiyat: {ortalama_fiyat} TL")
    print(f"- En Düşük Fiyat: {en_düşük_fiyat} TL")
    print(f"- En Yüksek Fiyat: {en_yüksek_fiyat} TL")
    print(f"- Medyan: {medyan} TL")
    print(f"- Standart Sapma {std_sapma:.2f}")
    print(f"- 20.000 TL'nin altındaki ilan sayısı: {x}") 
    print(f"- 30.000 TL'nin üstündeki ilan sayısı: {y}") 
else:
    print("Hata: Veri listesi boş!")