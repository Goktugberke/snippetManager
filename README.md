# 💻 Kod Bloğu Yöneticisi (Snippet Manager)

Kod Bloğu Yöneticisi, geliştiricilerin sık kullandıkları kod parçacıklarını (snippet’leri) kolayca kaydedip, düzenleyip, yönetebilmeleri için hazırlanmış bir masaüstü uygulamasıdır.  
Uygulama tamamen **Python** ve **CustomTkinter** kullanılarak geliştirilmiştir.

---

## 🚀 Özellikler

- 💾 Kod bloklarını **ekleme**, **düzenleme** ve **silme**  
- 📋 Kodları **panoya kopyalama**  
- 🧩 **JSON tabanlı veri kaydı** (veritabanı kurulumu gerekmez)  
- 🌗 **Karanlık / Aydınlık tema** desteği  
- 💡 **Kullanıcı dostu arayüz**  
- 🪟 PyInstaller ile `.exe` formatına dönüştürülebilir  


---

## ⚙️ Kurulum

### 1️⃣ Python sürümünü kontrol et
> En az **Python 3.10** önerilir.

```bash
python --version
```
### 2️⃣ Gerekli kütüphaneleri yükle
```bash
pip install -r requirements.txt
```
### 3️⃣ Uygulamayı çalıştır
```bash
python snippet_manager.py
```
### 🖥️ Uygulamayı .exe Dosyasına Dönüştürme (İsteğe Bağlı)
PyInstaller kurulu değilse:

```bash
pip install pyinstaller
```
Ardından:

```bash
pyinstaller --onefile --windowed --name="Kod Bloğu Yöneticisi" snippet_manager.py
```
Oluşturulan .exe dosyası dist/ klasörü içinde bulunur.

### 🧠 Neden Bu Uygulama?
Geliştiriciler sık sık kullandıkları kod parçacıklarını genellikle not defterlerinde, dosyalarda ya da online araçlarda saklarlar.
Bu uygulama ile:

Tüm snippet’lerini tek bir yerde tutabilir,

Kolayca kopyalayabilir,

Temaya göre görünümü değiştirebilir,

JSON formatında yedekleyebilirsin.

Kısacası, kişisel kod arşivin artık düzenli, taşınabilir ve kullanışlı bir hale gelir. 🚀
