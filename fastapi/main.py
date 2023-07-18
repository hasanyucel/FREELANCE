from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def bismillahirrahmanirrahim():
    result = {
                "KuranAPI" : "Bismillahirrahmanirrahim!",
                "Api Dokümanı" : "/docs",
                "Diller": "/languages"
             }
    return result

@app.get("/languages")
def languages():
    result = {
                "Almanca (Abu Rida)":"de_aburida",
                "İngilizce (Yusuf Ali)":"en_yusufali",
                "Fransızca (Hamidullah)":"fr_hamidullah",
                "İtalyanca (Piccardo)":"it_piccardo",
                "Japonca":"ja_japanese",
                "KU (Asan)":"ku_asan",
                "Orjinal Arapça":"quran_text",
                "Rusça (Muntahab)":"ru_muntahab",
                "Türkçe (Diyanet)":"tr_diyanet",
                "Özbekçe (Sodik)":"uz_sodik"
             }
    return result 
