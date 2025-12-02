"""
ANA ANALİZ MODÜLÜ
Tüm modülleri birleştirir ve yönetir
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

# Modülleri import et - DOĞRU YOL
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from src.utils.validator import PhoneValidator
    from src.modules.social_analyzer import SocialMediaAnalyzer
    from src.modules.breach_analyzer import BreachAnalyzer
    print("✅ Tüm modüller başarıyla yüklendi")
except ImportError as e:
    print(f"❌ Modül yükleme hatası: {e}")
    # Fallback classes
    class PhoneValidator:
        def __init__(self):
            pass
        def validate(self, phone):
            return False, None
        def get_basic_info(self, parsed):
            return {}
    
    class SocialMediaAnalyzer:
        def __init__(self):
            pass
        def analyze(self, phone, info):
            return {}
        def get_summary(self, results):
            return {}
    
    class BreachAnalyzer:
        def __init__(self):
            pass
        def analyze(self, phone, info):
            return []
        def calculate_breach_score(self, breaches):
            return {}

class PhoneAnalyzer:
    """Ana telefon analiz sınıfı"""
    
    def __init__(self):
        self.validator = PhoneValidator()
        self.social_analyzer = SocialMediaAnalyzer()
        self.breach_analyzer = BreachAnalyzer()
        self.results_dir = Path("reports")
        self.results_dir.mkdir(exist_ok=True)
    
    def analyze(self, phone_number: str, deep_scan: bool = False) -> Dict:
        """
        Telefon numarasını tam analiz eder
        
        Args:
            phone_number: Analiz edilecek telefon numarası
            deep_scan: Derinlemesine tarama yap
            
        Returns:
            Tüm analiz sonuçları
        """
        print(f"\n{'='*60}")
        print(f"📱 TELEFON ANALİZİ BAŞLATILIYOR")
        print(f"{'='*60}")
        print(f"Numara: {phone_number}")
        print(f"Zaman: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Mod: {'DERİN TARAMA' if deep_scan else 'STANDART TARAMA'}")
        print(f"{'='*60}\n")
        
        start_time = time.time()
        analysis_results = {
            'phone_number': phone_number,
            'analysis_date': datetime.now().isoformat(),
            'analysis_mode': 'deep' if deep_scan else 'standard',
            'analysis_duration': 0,
            'status': 'completed'
        }
        
        try:
            # 1. ADIM: TEMEL VALIDATION
            print("[1/4] 🔍 Temel telefon bilgileri alınıyor...")
            is_valid, parsed = self.validator.validate(phone_number)
            
            if not is_valid or not parsed:
                analysis_results['status'] = 'failed'
                analysis_results['error'] = 'Geçersiz telefon numarası'
                return analysis_results
            
            basic_info = self.validator.get_basic_info(parsed)
            analysis_results.update(basic_info)
            
            print(f"   ✅ Ülke: {basic_info.get('country')}")
            print(f"   ✅ Operatör: {basic_info.get('carrier')}")
            print(f"   ✅ Bölge: {basic_info.get('region')}")
            print(f"   ✅ Tür: {basic_info.get('number_type')}")
            
            # 2. ADIM: SOSYAL MEDYA ANALİZİ
            print("\n[2/4] 🌐 Sosyal medya analizi yapılıyor...")
            social_results = self.social_analyzer.analyze(phone_number, basic_info)
            analysis_results['social_media'] = social_results
            
            social_summary = self.social_analyzer.get_summary(social_results)
            analysis_results['social_summary'] = social_summary
            
            print(f"   ✅ Platformlar: {len(social_results)}")
            print(f"   ✅ Bulunan: {len(social_summary['platforms_found'])}")
            print(f"   ✅ Güven: %{social_summary['average_confidence']}")
            
            # 3. ADIM: DATA BREACH ANALİZİ
            print("\n[3/4] 🔓 Data breach analizi yapılıyor...")
            breach_results = self.breach_analyzer.analyze(phone_number, basic_info)
            analysis_results['data_breaches'] = breach_results
            
            if breach_results:
                breach_score = self.breach_analyzer.calculate_breach_score(breach_results)
                analysis_results['breach_score'] = breach_score
                print(f"   ✅ İhlaller: {len(breach_results)}")
                print(f"   ✅ Risk Seviyesi: {breach_score['level']}")
                print(f"   ✅ Skor: {breach_score['score']}/100")
            else:
                print("   ✅ Data breach bulunamadı")
            
            # 4. ADIM: RİSK ANALİZİ
            print("\n[4/4] ⚖️  Risk analizi yapılıyor...")
            risk_analysis = self._calculate_risk_analysis(basic_info, social_summary, breach_results)
            analysis_results['risk_analysis'] = risk_analysis
            
            print(f"   ✅ Genel Risk: {risk_analysis['overall_risk']}")
            print(f"   ✅ Skor: {risk_analysis['score']}/100")
            print(f"   ✅ Seviye: {risk_analysis['level']}")
            
            # Süreyi kaydet
            analysis_duration = time.time() - start_time
            analysis_results['analysis_duration'] = round(analysis_duration, 2)
            
            print(f"\n{'='*60}")
            print(f"✅ ANALİZ TAMAMLANDI!")
            print(f"⏱️  Süre: {analysis_duration:.2f} saniye")
            print(f"{'='*60}")
            
            # Raporu kaydet
            self._save_report(analysis_results)
            
            return analysis_results
            
        except Exception as e:
            print(f"\n❌ ANALİZ HATASI: {e}")
            analysis_results['status'] = 'failed'
            analysis_results['error'] = str(e)
            return analysis_results
    
    def _calculate_risk_analysis(self, basic_info: Dict, social_summary: Dict, 
                                breaches: List[Dict]) -> Dict:
        """Risk analizi yapar"""
        
        score = 0
        factors = []
        
        # 1. Temel bilgiler riski
        country = basic_info.get('country', 'Unknown')
        if country == 'Unknown':
            score += 30
            factors.append(('Bilinmeyen ülke', 30))
        elif country != 'TR':
            score += 15
            factors.append(('Yabancı numara', 15))
        
        # 2. Sosyal medya riski
        social_score = social_summary.get('average_confidence', 0)
        if social_score > 70:
            score += 40
            factors.append(('Yüksek sosyal medya varlığı', 40))
        elif social_score > 40:
            score += 20
            factors.append(('Orta sosyal medya varlığı', 20))
        
        # 3. Data breach riski
        if breaches:
            breach_count = len(breaches)
            score += breach_count * 25
            factors.append((f'{breach_count} data breach', breach_count * 25))
        
        # 4. Numara türü riski
        number_type = basic_info.get('number_type', 'UNKNOWN')
        if number_type == 'MOBILE':
            score += 10
            factors.append(('Mobil numara', 10))
        
        # Skoru sınırla
        score = min(score, 100)
        
        # Risk seviyesi
        if score < 30:
            level = 'ÇOK DÜŞÜK'
            description = 'Minimum risk - normal kullanım'
        elif score < 50:
            level = 'DÜŞÜK'
            description = 'Düşük risk - rutin kontroller yeterli'
        elif score < 70:
            level = 'ORTA'
            description = 'Orta risk - dikkatli olunmalı'
        elif score < 85:
            level = 'YÜKSEK'
            description = 'Yüksek risk - önlem alınmalı'
        else:
            level = 'ÇOK YÜKSEK'
            description = 'Çok yüksek risk - acil önlem gerekli'
        
        # Öneriler
        recommendations = []
        
        if score > 70:
            recommendations.extend([
                "Bu numara ile ilgili şüpheli aktiviteleri izleyin",
                "Gerekirse yetkililere bildirin",
                "Kişisel bilgilerinizi bu numara ile paylaşmayın"
            ])
        elif score > 40:
            recommendations.extend([
                "Sosyal medya gizlilik ayarlarınızı kontrol edin",
                "Şifrelerinizi düzenli değiştirin",
                "İki faktörlü doğrulama kullanın"
            ])
        else:
            recommendations.append("Normal kullanıma devam edebilirsiniz")
        
        return {
            'score': score,
            'level': level,
            'overall_risk': f"%{score} - {level}",
            'description': description,
            'factors': factors,
            'recommendations': recommendations,
            'calculation_method': 'Temel bilgiler + Sosyal medya + Data breach'
        }
    
    def _save_report(self, analysis_results: Dict):
        """Analiz raporunu kaydeder"""
        try:
            # JSON formatında kaydet
            phone_clean = analysis_results['phone_number'].replace('+', '').replace(' ', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"phone_{phone_clean}_{timestamp}.json"
            filepath = self.results_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(analysis_results, f, indent=2, ensure_ascii=False)
            
            print(f"📄 Rapor kaydedildi: {filepath}")
            
            # TXT özeti de oluştur
            self._create_summary_txt(analysis_results, filepath)
            
        except Exception as e:
            print(f"Rapor kaydetme hatası: {e}")
    
    def _create_summary_txt(self, analysis_results: Dict, json_path: Path):
        """Özet TXT raporu oluştur"""
        try:
            txt_path = json_path.with_suffix('.txt')
            
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("ULTRA PRO MAX PHONE OSINT - ANALİZ RAPORU\n")
                f.write("=" * 60 + "\n\n")
                
                f.write(f"📱 TELEFON NUMARASI: {analysis_results['phone_number']}\n")
                f.write(f"📅 ANALİZ TARİHİ: {analysis_results['analysis_date']}\n")
                f.write(f"⏱️  ANALİZ SÜRESİ: {analysis_results.get('analysis_duration', 0)} saniye\n")
                f.write(f"🔧 ANALİZ MODU: {analysis_results['analysis_mode']}\n\n")
                
                # Temel Bilgiler
                f.write("-" * 40 + "\n")
                f.write("TEMEL BİLGİLER\n")
                f.write("-" * 40 + "\n")
                
                basic_keys = ['country', 'carrier', 'region', 'number_type', 'is_mobile']
                for key in basic_keys:
                    if key in analysis_results:
                        value = analysis_results[key]
                        f.write(f"{key.upper():15}: {value}\n")
                
                # Sosyal Medya Özeti
                if 'social_summary' in analysis_results:
                    f.write("\n" + "-" * 40 + "\n")
                    f.write("SOSYAL MEDYA ÖZETİ\n")
                    f.write("-" * 40 + "\n")
                    
                    social = analysis_results['social_summary']
                    f.write(f"Toplam Platform: {social['total_platforms']}\n")
                    f.write(f"Bulunan Platform: {len(social['platforms_found'])}\n")
                    f.write(f"Ortalama Güven: %{social['average_confidence']}\n")
                    f.write(f"Sosyal Medya Riski: {social['risk_level']}\n")
                
                # Data Breach Özeti
                if 'data_breaches' in analysis_results:
                    breaches = analysis_results['data_breaches']
                    f.write("\n" + "-" * 40 + "\n")
                    f.write("DATA BREACH ÖZETİ\n")
                    f.write("-" * 40 + "\n")
                    
                    f.write(f"Toplam İhlal: {len(breaches)}\n")
                    
                    if breaches and 'breach_score' in analysis_results:
                        score = analysis_results['breach_score']
                        f.write(f"Breach Skoru: {score['score']}/100\n")
                        f.write(f"Breach Seviyesi: {score['level']}\n")
                
                # Risk Analizi
                if 'risk_analysis' in analysis_results:
                    f.write("\n" + "-" * 40 + "\n")
                    f.write("RİSK ANALİZİ\n")
                    f.write("-" * 40 + "\n")
                    
                    risk = analysis_results['risk_analysis']
                    f.write(f"GENEL RİSK: {risk['overall_risk']}\n")
                    f.write(f"Açıklama: {risk['description']}\n")
                    f.write(f"Hesaplama: {risk['calculation_method']}\n\n")
                    
                    f.write("Risk Faktörleri:\n")
                    for factor, points in risk.get('factors', []):
                        f.write(f"  • {factor}: +{points} puan\n")
                    
                    f.write("\nÖNERİLER:\n")
                    for rec in risk.get('recommendations', []):
                        f.write(f"  • {rec}\n")
                
                f.write("\n" + "=" * 60 + "\n")
                f.write("RAPOR SONU\n")
                f.write("=" * 60 + "\n")
                f.write(f"Detaylı rapor: {json_path}\n")
                f.write("Not: Bu rapor sadece eğitim amaçlıdır.\n")
            
            print(f"📝 Özet rapor kaydedildi: {txt_path}")
            
        except Exception as e:
            print(f"Özet rapor oluşturma hatası: {e}")

# Test fonksiyonu
if __name__ == "__main__":
    print("ANA ANALİZ MODÜLÜ TESTİ")
    print("=" * 60)
    
    analyzer = PhoneAnalyzer()
    
    test_numbers = [
        "+905551234567",
        # "+14155552671",  # USA test
        # "+442079813000",  # UK test
    ]
    
    for test_number in test_numbers:
        print(f"\n>>> TEST: {test_number}")
        
        try:
            result = analyzer.analyze(test_number, deep_scan=True)
            
            if result['status'] == 'completed':
                print(f"\n✅ Analiz başarılı!")
                print(f"📊 Risk Seviyesi: {result['risk_analysis']['overall_risk']}")
                
                # Önemli bulguları göster
                if 'social_summary' in result:
                    social = result['social_summary']
                    print(f"🌐 Sosyal Medya: {len(social['platforms_found'])} platform")
                
                if 'data_breaches' in result:
                    breaches = result['data_breaches']
                    print(f"🔓 Data Breach: {len(breaches)} ihlal")
                    
            else:
                print(f"❌ Analiz başarısız: {result.get('error', 'Bilinmeyen hata')}")
                
        except Exception as e:
            print(f"❌ Test hatası: {e}")
    
    print("\n" + "=" * 60)
    print("TEST TAMAMLANDI")
    print("=" * 60)
