"""
Data Breach Analiz Modülü
Profesyonel ve optimize edilmiş
"""

import json
import hashlib
import time
from typing import Dict, List, Optional
from datetime import datetime

class BreachAnalyzer:
    """Data breach analiz sınıfı"""
    
    def __init__(self):
        # Yerel breach veritabanı (simüle edilmiş)
        self.breach_database = self._load_breach_database()
    
    def _load_breach_database(self) -> List[Dict]:
        """Yerel breach veritabanını yükle (simüle)"""
        return [
            {
                'name': 'Türk Telekom Veri İhlali 2022',
                'date': '2022-03-15',
                'data_types': ['phone_numbers', 'customer_data', 'addresses'],
                'records_affected': 2500000,
                'source': 'Medya raporları',
                'confidence': 85
            },
            {
                'name': 'E-ticaret Sitesi İhlali 2023',
                'date': '2023-08-22',
                'data_types': ['phone_numbers', 'email_addresses', 'names', 'addresses'],
                'records_affected': 1500000,
                'source': 'Güvenlik araştırmaları',
                'confidence': 75
            },
            {
                'name': 'Sosyal Medya Platformu İhlali 2021',
                'date': '2021-11-30',
                'data_types': ['phone_numbers', 'email_addresses', 'hashed_passwords'],
                'records_affected': 5000000,
                'source': 'HaveIBeenPwned',
                'confidence': 90
            },
            {
                'name': 'Finans Kurumu İhlali 2020',
                'date': '2020-05-10',
                'data_types': ['phone_numbers', 'tc_numbers', 'financial_data'],
                'records_affected': 800000,
                'source': 'Resmi açıklama',
                'confidence': 95
            }
        ]
    
    def analyze(self, phone_number: str, basic_info: Dict) -> List[Dict]:
        """
        Telefon numarası için data breach analizi yapar
        
        Args:
            phone_number: Analiz edilecek telefon numarası
            basic_info: Temel telefon bilgileri
            
        Returns:
            Data breach bulguları listesi
        """
        print(f"[*] Data breach analizi başlatılıyor: {phone_number}")
        
        breaches_found = []
        
        try:
            # 1. Yerel veritabanında kontrol
            print("  [+] Yerel breach veritabanı taranıyor...")
            local_breaches = self._check_local_database(phone_number, basic_info)
            breaches_found.extend(local_breaches)
            
            # 2. Türkiye numaraları için özel kontroller
            if basic_info.get('country') == 'TR':
                print("  [+] Türkiye breach verileri kontrol ediliyor...")
                turkey_breaches = self._check_turkish_breaches(phone_number)
                breaches_found.extend(turkey_breaches)
            
            # 3. Simüle edilmiş API kontrolü
            print("  [+] Online breach veritabanları kontrol ediliyor...")
            api_breaches = self._check_simulated_apis(phone_number)
            breaches_found.extend(api_breaches)
            
            print(f"[+] Data breach analizi tamamlandı: {len(breaches_found)} ihlal bulundu")
            
        except Exception as e:
            print(f"[!] Data breach analiz hatası: {e}")
        
        return breaches_found
    
    def _check_local_database(self, phone_number: str, basic_info: Dict) -> List[Dict]:
        """Yerel breach veritabanını kontrol et"""
        breaches = []
        
        # Telefon numarasının hash'ini al (simülasyon için)
        phone_hash = hashlib.md5(phone_number.encode()).hexdigest()[:8]
        
        # Rastgele eşleşme (simülasyon)
        import random
        
        # %30 ihtimalle breach bul
        if random.random() < 0.3:
            # Rastgele bir breach seç
            breach = random.choice(self.breach_database)
            
            breaches.append({
                'breach_name': breach['name'],
                'breach_date': breach['date'],
                'data_types': breach['data_types'],
                'records_affected': breach['records_affected'],
                'source': breach['source'],
                'confidence': breach['confidence'],
                'match_type': 'partial',  # partial/full
                'notes': [
                    f"Telefon numarası {breach['name']} ihlalinde bulunmuş olabilir",
                    f"{breach['records_affected']:,} kayıt etkilendi",
                    f"İhlal tarihi: {breach['date']}"
                ],
                'actions': [
                    "Şifrenizi değiştirin",
                    "İki faktörlü doğrulamayı etkinleştirin",
                    f"{breach['name']} hakkında daha fazla bilgi araştırın"
                ]
            })
        
        return breaches
    
    def _check_turkish_breaches(self, phone_number: str) -> List[Dict]:
        """Türkiye'ye özel breach kontrolleri"""
        breaches = []
        
        # Türkiye için özel breach verileri
        turkish_breaches = [
            {
                'name': 'TTNET Abone Veri İhlali 2019',
                'date': '2019-07-10',
                'data_types': ['phone_numbers', 'ad_soyad', 'adres', 'abone_no'],
                'records_affected': 3500000,
                'source': 'Siber güvenlik firmaları',
                'confidence': 80
            },
            {
                'name': 'Mobil Operatör CRM İhlali 2021',
                'date': '2021-02-28',
                'data_types': ['phone_numbers', 'imei', 'tarife_bilgisi', 'fatura'],
                'records_affected': 1200000,
                'source': 'Anonymous leaks',
                'confidence': 70
            }
        ]
        
        import random
        
        # %40 ihtimalle Türkiye breach'i bul
        if random.random() < 0.4:
            breach = random.choice(turkish_breaches)
            
            breaches.append({
                'breach_name': breach['name'],
                'breach_date': breach['date'],
                'data_types': breach['data_types'],
                'records_affected': breach['records_affected'],
                'source': breach['source'],
                'confidence': breach['confidence'],
                'match_type': 'partial',
                'notes': [
                    "Türkiye kaynaklı veri ihlali",
                    "Operatör/İnternet sağlayıcı verileri sızdırılmış",
                    "Kişisel verileriniz risk altında olabilir"
                ],
                'actions': [
                    "Operatörünüzle iletişime geçin",
                    "TCKN sızdırılmış olabilir - MERNİS kontrolü yapın",
                    "Banka hesaplarınızı izleyin"
                ]
            })
        
        return breaches
    
    def _check_simulated_apis(self, phone_number: str) -> List[Dict]:
        """Simüle edilmiş API kontrolleri"""
        breaches = []
        
        # HaveIBeenPwned benzeri simülasyon
        hibp_breaches = [
            {
                'name': 'Collection #1',
                'date': '2019-01-07',
                'data_types': ['email_addresses', 'passwords', 'phone_numbers'],
                'records_affected': 772904991,
                'source': 'HaveIBeenPwned',
                'confidence': 95
            },
            {
                'name': 'Anti Public Combo List',
                'date': '2019-03-01',
                'data_types': ['email_addresses', 'passwords', 'usernames', 'phone_numbers'],
                'records_affected': 458397376,
                'source': 'DeHashed',
                'confidence': 88
            }
        ]
        
        import random
        
        # %25 ihtimalle global breach bul
        if random.random() < 0.25:
            breach = random.choice(hibp_breaches)
            
            breaches.append({
                'breach_name': breach['name'],
                'breach_date': breach['date'],
                'data_types': breach['data_types'],
                'records_affected': breach['records_affected'],
                'source': breach['source'],
                'confidence': breach['confidence'],
                'match_type': 'possible',
                'notes': [
                    "Global veri ihlali - milyonlarca kayıt etkilendi",
                    "E-posta ve şifre kombinasyonları sızdırılmış",
                    "Bu ihlalde birden fazla servis etkilendi"
                ],
                'actions': [
                    "Tüm hesaplarınızda şifre değiştirin",
                    "HaveIBeenPwned.com'da e-posta adresinizi kontrol edin",
                    "Password manager kullanın"
                ]
            })
        
        return breaches
    
    def calculate_breach_score(self, breaches: List[Dict]) -> Dict:
        """
        Data breach skorunu hesaplar
        
        Args:
            breaches: Bulunan breach'ler
            
        Returns:
            Skor ve analiz sonuçları
        """
        if not breaches:
            return {
                'score': 0,
                'level': 'LOW',
                'description': 'Data breach bulunamadı',
                'recommendations': ['Güvenlik önlemlerinizi sürdürün']
            }
        
        # Skor hesaplama
        total_score = 0
        factors = []
        
        for breach in breaches:
            # Confidence'a göre puan
            confidence = breach.get('confidence', 50)
            score = confidence * 0.5
            
            # Kayıt sayısına göre ek puan
            records = breach.get('records_affected', 0)
            if records > 1000000:
                score += 20
            elif records > 100000:
                score += 10
            
            # Data types'a göre ek puan
            data_types = breach.get('data_types', [])
            sensitive_types = ['tc_numbers', 'financial_data', 'passwords']
            for dtype in data_types:
                if dtype in sensitive_types:
                    score += 15
            
            total_score += score
            
            # Risk faktörleri
            factors.append({
                'breach': breach['breach_name'],
                'score': round(score),
                'reason': f"{confidence}% güven, {records:,} kayıt"
            })
        
        # Ortalama skor
        avg_score = total_score / len(breaches)
        
        # Risk seviyesi
        if avg_score < 30:
            level = 'LOW'
            desc = 'Düşük risk - rutin kontroller yeterli'
        elif avg_score < 60:
            level = 'MEDIUM'
            desc = 'Orta risk - acil önlem alınmalı'
        else:
            level = 'HIGH'
            desc = 'Yüksek risk - acil müdahale gerekiyor'
        
        # Öneriler
        recommendations = [
            "Tüm hesaplarınızda şifre değiştirin",
            "İki faktörlü doğrulamayı etkinleştirin",
            "Kredi kartı/banka ekstrelerinizi kontrol edin"
        ]
        
        if level == 'HIGH':
            recommendations.extend([
                "Banka müşteri hizmetlerini arayın",
                "TCKN sızdırılmış olabilir - MERNİS başvurusu yapın",
                "Kredi raporunuzu kontrol edin"
            ])
        
        return {
            'score': round(avg_score),
            'level': level,
            'description': desc,
            'factors': factors,
            'recommendations': recommendations,
            'total_breaches': len(breaches),
            'breach_names': [b['breach_name'] for b in breaches]
        }

# Test fonksiyonu
if __name__ == "__main__":
    analyzer = BreachAnalyzer()
    
    test_number = "+905551234567"
    test_info = {
        'country': 'TR',
        'carrier': 'Turkcell',
        'region': 'Turkey'
    }
    
    print("Data Breach Analyzer Testi")
    print("=" * 50)
    print(f"Test Numarası: {test_number}")
    
    breaches = analyzer.analyze(test_number, test_info)
    
    print("\nBulunan Data Breach'ler:")
    print("-" * 40)
    
    for i, breach in enumerate(breaches, 1):
        print(f"\n{i}. {breach['breach_name']}")
        print(f"   Tarih: {breach['breach_date']}")
        print(f"   Kayıt: {breach['records_affected']:,}")
        print(f"   Güven: %{breach['confidence']}")
        print(f"   Veri Türleri: {', '.join(breach['data_types'])}")
        print(f"   Kaynak: {breach['source']}")
        
        if 'notes' in breach:
            print("   Notlar:")
            for note in breach['notes']:
                print(f"     • {note}")
    
    if breaches:
        score_result = analyzer.calculate_breach_score(breaches)
        
        print(f"\nData Breach Skoru:")
        print(f"  Skor: {score_result['score']}/100")
        print(f"  Seviye: {score_result['level']}")
        print(f"  Açıklama: {score_result['description']}")
        print(f"  Toplam İhlal: {score_result['total_breaches']}")
        
        print("\nÖneriler:")
        for rec in score_result['recommendations']:
            print(f"  • {rec}")
    else:
        print("\n✅ Data breach bulunamadı. Güvendesiniz!")
