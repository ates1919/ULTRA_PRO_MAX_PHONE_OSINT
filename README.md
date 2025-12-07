# 🚀 ULTRA PRO MAX PHONE OSINT

**Profesyonel Telefon Numarası Analiz ve OSINT Platformu**  
*Bilişim Güvenliği Teknolojisi 

---

## 📋 İÇİNDEKİLER
1. [Proje Hakkında](#-proje-hakkında)
2. [Özellikler](#-özellikler)
3. [Kurulum](#-kurulum)
4. [Kullanım](#-kullanım)
5. [Modüller](#-modüller)
6. [Raporlama](#-raporlama)
7. [Yasal Uyarılar](#⚠️-yasal-uyarılar)
8. [Ekran Görüntüleri](#-ekran-görüntüleri)
9. [Teknolojiler](#-teknolojiler)
10. [Katkı](#-katkı)

---

## 🎯 PROJE HAKKINDA

Bu proje, **Bilişim Güvenliği Teknolojisi** bölümü bitirme projesi olarak geliştirilmiştir. Telefon numaraları üzerinde **OSINT (Open Source Intelligence)** analizleri yaparak, bir telefon numarası hakkında mümkün olan tüm açık kaynak bilgileri toplar ve analiz eder.

**Amaç:** Eğitim amaçlı profesyonel bir OSINT aracı geliştirmek ve güvenlik farkındalığı oluşturmak.

---

## ✨ ÖZELLİKLER

### 🔍 Temel Analiz
- Telefon numarası validasyonu ve doğrulama
- Ülke, operatör, bölge bilgileri
- Numara türü tespiti (Mobil/Sabit)

### 🌐 Sosyal Medya Analizi
- **WhatsApp** - Hesap varlığı ve bağlantılar
- **Telegram** - Profil kontrolü
- **Google** - İnternet üzerinde arama
- **Facebook** - Profil taraması
- **Instagram** - Telefon ile kayıt kontrolü

### 🔓 Data Breach Analizi
- Yerel breach veritabanı taraması
- Türkiye'ye özel ihlal kontrolleri
- Global breach veritabanı simülasyonu
- Risk skorlama ve öneriler

### ⚡ Diğer Özellikler
- Otomatik risk analizi ve skorlama
- JSON ve TXT formatında raporlama
- Toplu analiz (dosyadan çoklu numara)
- Analiz geçmişi takibi
- Profesyonel CLI arayüzü
- Sistem test modülü

---

## 🛠️ KURULUM

### Gereksinimler
- Python 3.8+
- pip (Python paket yöneticisi)
- 2GB+ RAM (Optimize edilmiş)

### Kurulum Adımları

\`\`\`bash
# 1. Repoyu klonlayın
git clone <repo-url>
cd ULTRA_PRO_MAX_PHONE_OSINT

# 2. Virtual environment oluşturun
python3 -m venv venv

# 3. Virtual environment'ı aktif edin
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows

# 4. Gerekli paketleri yükleyin
pip install -r requirements.txt
\`\`\`

### Hızlı Başlangıç
\`\`\`bash
# Ortamı hazırlayın
cp .env.example .env
# .env dosyasını düzenleyin (opsiyonel)

# Sistemi test edin
python phone_analyzer.py --test
\`\`\`

---

## 🚀 KULLANIM

### Temel Kullanım
\`\`\`bash
# Yardım menüsü
python phone_analyzer.py --help

# Tek numara analizi
python phone_analyzer.py -n "+905551234567"
python phone_analyzer.py --number "05551234567" --deep

# Toplu analiz
python phone_analyzer.py -f numbers.txt
python phone_analyzer.py --file numbers.txt --deep

# Analiz geçmişi
python phone_analyzer.py --history
python phone_analyzer.py --history 20

# Sistem testi
python phone_analyzer.py --test
\`\`\`

### Interaktif Mod
Hiçbir argüman vermeden çalıştırırsanız interaktif menü açılır:
\`\`\`bash
python phone_analyzer.py
\`\`\`

---

## 🧩 MODÜLLER

### 1. Validator Modülü (\`src/utils/validator.py\`)
- Telefon numarası normalizasyonu
- Ülke ve operatör tespiti
- Numara türü belirleme
- Risk seviyesi analizi

### 2. Sosyal Medya Analiz Modülü (\`src/modules/social_analyzer.py\`)
- Çoklu platform taraması
- Güven skorlama
- Platform özel bağlantılar
- Özet raporlama

### 3. Data Breach Modülü (\`src/modules/breach_analyzer.py\`)
- Yerel breach veritabanı
- Türkiye özel ihlaller
- Global breach simülasyonu
- Risk skorlama ve öneriler

### 4. Ana Analiz Modülü (\`src/core/analyzer.py\`)
- Tüm modülleri koordine eder
- Risk analizi yapar
- Rapor oluşturur
- Süreç yönetimi

---

## 📊 RAPORLAMA

Sistem iki tür rapor oluşturur:

### 1. JSON Raporu (\`reports/phone_*.json\`)
\`\`\`json
{
  "phone_number": "+905551234567",
  "country": "TR",
  "carrier": "Turkcell",
  "risk_analysis": {
    "score": 75,
    "level": "YÜKSEK",
    "recommendations": [...]
  },
  "social_media": {...},
  "data_breaches": [...]
}
\`\`\`

### 2. TXT Özet Raporu (\`reports/phone_*.txt\`)
\`\`\`
============================================================
ULTRA PRO MAX PHONE OSINT - ANALİZ RAPORU
============================================================

📱 TELEFON NUMARASI: +905551234567
📅 ANALİZ TARİHİ: 2025-12-03 00:07:40
⏱️  ANALİZ SÜRESİ: 5.18 saniye

TEMEL BİLGİLER
----------------------------------------
COUNTRY       : TR
CARRIER       : Turkcell
REGION        : Turkey
NUMBER_TYPE   : MOBILE

RİSK ANALİZİ
----------------------------------------
GENEL RİSK: %75 - YÜKSEK
Açıklama: Yüksek risk - önlem alınmalı

ÖNERİLER:
• Bu numara ile ilgili şüpheli aktiviteleri izleyin
• Gerekirse yetkililere bildirin
• Kişisel bilgilerinizi bu numara ile paylaşmayın
\`\`\`

---

## ⚠️ YASAL UYARILAR

### ❌ **YAPILMAYACAKLAR:**
- İzinsiz kişisel veri toplama
- Başkalarının telefon numaralarını izinsiz analiz etme
- Ticari amaçla kullanma
- Yasal sınırları aşma

### ✅ **YAPILABİLİRLER:**
- Kendi telefon numaranızı analiz etme
- Yazılı izin aldığınız numaraları analiz etme
- Eğitim ve araştırma amaçlı kullanma
- Güvenlik farkındalığı oluşturma

### ⚖️ **YASAL SONUÇLAR:**
- Kişisel verilerin korunması kanunu (KVKK) ihlali
- Haberleşmenin gizliliğini ihlal
- Özel hayatın gizliliğini ihlal
- Ağır cezai yaptırımlar

**BU ARAÇ SADECE EĞİTİM AMAÇLIDIR!**

---

## 📸 EKRAN GÖRÜNTÜLERİ

\`\`\`
╔══════════════════════════════════════════════════════════════════╗
║                ULTRA PRO MAX PHONE OSINT                         ║
║             Profesyonel Telefon Analiz Platformu                 ║
║                  Versiyon 1.0.0                                  ║
╚══════════════════════════════════════════════════════════════════╝
\`\`\`

**Analiz Süreci:**
\`\`\`
[1/4] 🔍 Temel telefon bilgileri alınıyor...
[2/4] 🌐 Sosyal medya analizi yapılıyor...
[3/4] 🔓 Data breach analizi yapılıyor...
[4/4] ⚖️  Risk analizi yapılıyor...
✅ ANALİZ TAMAMLANDI!
\`\`\`

---

## 💻 TEKNOLOJİLER

- **Python 3.13** - Ana programlama dili
- **phonenumbers** - Telefon numarası parsing
- **requests/BeautifulSoup** - Web scraping
- **SQLite** - Yerel veritabanı
- **colorama** - Renkli CLI arayüzü
- **Jinja2** - Rapor şablonları

### Mimari
\`\`\`
ULTRA_PRO_MAX_PHONE_OSINT/
├── src/                    # Kaynak kodlar
│   ├── core/              # Ana analiz modülü
│   ├── utils/             # Yardımcı fonksiyonlar
│   └── modules/           # Analiz modülleri
├── data/                  # Veriler ve cache
├── reports/               # Analiz raporları
├── logs/                  # Sistem logları
└── config/                # Konfigürasyon dosyaları
\`\`\`

---

## 👥 KATKı

### Öğrenci Bilgileri
- **Adı Soyadı:** [Öğrenci Adı Soyadı]
- **Öğrenci No:** [Öğrenci Numarası]
- **Bölüm:** Bilişim Güvenliği Teknolojisi
- **Danışman:** [Danışman Hoca Adı]
- **Dönem:** 2024-2025 Güz Dönemi

### Proje Sunumu
1. **PowerPoint Sunumu** - Proje tanıtımı ve demo
2. **Teknik Rapor** - 30-50 sayfa detaylı rapor
3. **Live Demo** - Canlı sistem gösterimi
4. **Kaynak Kod** - Tam açık kaynak kod

### Lisans
Bu proje eğitim amaçlıdır. Ticari kullanıma kapalıdır.

---

## 📞 İLETİŞİM

- **Email:** [25370301036@subu.edu.tr]
- **Okul:** [Sakarya Uygulamalı Bilimler Üniversitesi]
- **Bölüm:** Bilişim Güvenliği Teknolojisi

---

## 🙏 TEŞEKKÜRLER


*Son Güncelleme: Aralık 2025*  
*Versiyon: 1.0.0*  
*Durum: Aktif Geliştirme*
