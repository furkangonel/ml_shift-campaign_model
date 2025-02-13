~Project Schema 🖼️~


https://github.com/furkangonel/ml_shift-campaign_model/issues/1#issue-2851744995

    Projenin Amacı: Kafe-Restoran işlemelerinde kullanılan sipariş sistemlerine entregre edebileceğiniz basit bir AI-API. 
        API' nin beklediği parametler,
        * 1. model için; 
            class IncomingData_Model1(BaseModel):
                date: datetime
                name: str
                density_level: float
                work_type: str
                preferred_shift: List[str]
                weekly_sales: float
                day_off_preferred: List[str]
       
        * 2.Model için;
            class Product(BaseModel):
                product: str
                price: float
                profit_margin: float
                quantity: int

            class IncomingData_Model2(BaseModel):
                order_id: int
                products: List[Product]

    + Shift tahminleyici model(1.model) verilen haftalık bilgilere göre o hafta için oluşturduğu shift planını pdf oalrak indirme imkanı da sunar.
    + Kampanya tahminlyen model(2.model) verilen geçmiş sipariş verilerine göre birliktelik kurallarına uygun kampanya tahminleri oluşturarak pdf içerisinde kampanyaları sunar. (x ürünü alana y %a indirimli veya x ile y ürünlerini birlikte alana topalam %a indirim)

    ÇIKTILAR:

    https://github.com/furkangonel/ml_shift-campaign_model/issues/2#issue-2851830892


    Bu proje içerisinde bulunan iki adet Classifier ML modelleri birbirinden bağımsız olarak eğitilimiştir.

    1. Model: İşletmelerden toplanmış işletme yoğunluğu, çalışan bilgileri-talepleri ve sonuç(target) verileri ile eğitilmiş olup modelden testler sonucu %66 başarım elde edilmiştir.

    2. Model: işletmedeki geçmiş sipariş verileri FP-Growth birliktelik algoritmasından geçirilmiş ve sonrasında bu çıktılar işlenip sınıflandırma modeli eğitiminde kullanılmıştır. Bu eğitim sonucunda da %95 başarım(accuracy) alınmıştır.




1️⃣ Projeyi Klonla

git clone https://github.com/furkangonel/ml_shift-campaign_model.git
cd ml_shift-campaign_model


2️⃣ Gerekli Bağımlılıkları Yükleyin
pip install -r requirements.txt


3️⃣ Projeyi Çalıştır
uvicorn main:app --reload



🛠 Kullanılan Teknolojiler
	•	Python 🐍 - Backend geliştirme için
	•	FastAPI 🚀 - API geliştirme
	•	MongoDB 🍃 - NoSQL veritabanı
	•	TensorFlow / Scikit-learn 🤖 - Makine öğrenmesi




📜 Lisans

Bu proje MIT Lisansı altında sunulmaktadır. Daha fazla bilgi için LICENSE dosyasına göz atabilirsiniz.