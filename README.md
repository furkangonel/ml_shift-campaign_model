~Project Schema 🖼️~


### **Kafe & Restoran İşletmeleri için Yapay Zeka Destekli Sipariş ve Vardiya Yönetimi**  

[![GitHub issues](https://img.shields.io/github/issues/furkangonel/ml_shift-campaign_model)](https://github.com/furkangonel/ml_shift-campaign_model/issues)  
[![GitHub stars](https://img.shields.io/github/stars/furkangonel/ml_shift-campaign_model)](https://github.com/furkangonel/ml_shift-campaign_model/stargazers)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  


**ML Shift & Campaign Model API**, kafe ve restoran işletmelerinin **sipariş yönetimini** ve **çalışan vardiya planlamasını** optimize etmek için geliştirilmiş bir **Yapay Zeka tabanlı API**'dir.  


## 📌 Projenin Amacı:
Kafe-Restoran işlemelerinde kullanılan sipariş sistemlerine entregre edebileceğiniz basit bir AI-API. 
API' nin beklediği parametler,
* 1. model için; 
            ```class IncomingData_Model1(BaseModel):
                date: datetime
                name: str
                density_level: float
                work_type: str
                preferred_shift: List[str]
                weekly_sales: float
                day_off_preferred: List[str]
       
        * 2.Model için;
            ```class Product(BaseModel):
                product: str
                price: float
                profit_margin: float
                quantity: int

            ```class IncomingData_Model2(BaseModel):
                order_id: int
                products: List[Product]

    + Shift tahminleyici model(1.model) verilen haftalık bilgilere göre o hafta için oluşturduğu shift planını pdf oalrak indirme imkanı da sunar.
    + Kampanya tahminlyen model(2.model) verilen geçmiş sipariş verilerine göre birliktelik kurallarına uygun kampanya tahminleri oluşturarak pdf içerisinde kampanyaları sunar. (x ürünü alana y %a indirimli veya x ile y ürünlerini birlikte alana topalam %a indirim)

    ÇIKTILAR:

    https://github.com/furkangonel/ml_shift-campaign_model/issues/2#issue-2851830892


    Bu proje içerisinde bulunan iki adet Classifier ML modelleri birbirinden bağımsız olarak eğitilimiştir.

    1. Model: İşletmelerden toplanmış işletme yoğunluğu, çalışan bilgileri-talepleri ve sonuç(target) verileri ile eğitilmiş olup modelden testler sonucu %66 başarım elde edilmiştir.

    2. Model: işletmedeki geçmiş sipariş verileri FP-Growth birliktelik algoritmasından geçirilmiş ve sonrasında bu çıktılar işlenip sınıflandırma modeli eğitiminde kullanılmıştır. Bu eğitim sonucunda da %95 başarım(accuracy) alınmıştır.

| Model  | Açıklama | Başarım Oranı |
|--------|----------|--------------|
| **1. Model** | Çalışan vardiya tahminleme | **%66** |
| **2. Model** | Kampanya önerileri | **%95** |



```sh
git clone https://github.com/furkangonel/ml_shift-campaign_model.git
cd ml_shift-campaign_model
pip install -r requirements.txt
uvicorn main:app --reload
```

```sh
🛠 Kullanılan Teknolojiler
	•	Python 🐍 - Backend geliştirme için
	•	FastAPI 🚀 - API geliştirme
	•	MongoDB 🍃 - NoSQL veritabanı
	•	TensorFlow / Scikit-learn 🤖 - Makine öğrenmesi
```



📜 Lisans

Bu proje MIT Lisansı altında sunulmaktadır. Daha fazla bilgi için 📜 [Lisans](LICENSE) dosyasına göz atabilirsiniz.