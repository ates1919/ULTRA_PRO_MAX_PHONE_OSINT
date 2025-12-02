#!/usr/bin/env python3
"""
ULTRA PRO MAX PHONE OSINT - PROFESYONEL ANA UYGULAMA
"""

import sys
import os
import argparse
from pathlib import Path
from colorama import init, Fore, Style

# Colorama'yı başlat
init(autoreset=True)

# Proje yolunu ekle
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

def print_banner():
    """Profesyonel banner göster"""
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════╗
║                ULTRA PRO MAX PHONE OSINT                         ║
║             Profesyonel Telefon Analiz Platformu                 ║
║                  Versiyon 1.0.0                                  ║
╚══════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
{Fore.YELLOW}📱 Bilişim Güvenliği Teknolojisi - Bitirme Projesi{Style.RESET_ALL}
{Fore.GREEN}✅ Tüm sistemler çalışır durumda{Style.RESET_ALL}
{Fore.RED}⚠️  UYARI: Sadece eğitim ve yasal amaçlarla kullanın!{Style.RESET_ALL}
"""
    print(banner)

def analyze_single(number, deep_scan=False, output_format="json"):
    """Tek numara analizi"""
    from src.core.analyzer import PhoneAnalyzer
    
    print(f"\n{Fore.CYAN}[*] Analiz başlatılıyor: {number}{Style.RESET_ALL}")
    
    analyzer = PhoneAnalyzer()
    result = analyzer.analyze(number, deep_scan)
    
    if result['status'] == 'completed':
        print(f"{Fore.GREEN}[+] Analiz başarıyla tamamlandı!{Style.RESET_ALL}")
        
        # Rapor dosyalarını göster
        import glob
        reports = list(Path("reports").glob(f"*{number.replace('+', '').replace(' ', '_')}*"))
        if reports:
            print(f"{Fore.CYAN}[*] Oluşturulan raporlar:{Style.RESET_ALL}")
            for report in reports[-2:]:  # Son 2 raporu göster
                print(f"   📄 {report}")
        
        return True
    else:
        print(f"{Fore.RED}[!] Analiz başarısız: {result.get('error', 'Bilinmeyen hata')}{Style.RESET_ALL}")
        return False

def analyze_batch(file_path, deep_scan=False):
    """Toplu analiz"""
    try:
        with open(file_path, 'r') as f:
            numbers = [line.strip() for line in f if line.strip()]
        
        print(f"{Fore.CYAN}[*] {len(numbers)} numara bulundu, toplu analiz başlatılıyor...{Style.RESET_ALL}")
        
        success_count = 0
        for i, number in enumerate(numbers, 1):
            print(f"\n{Fore.YELLOW}[{i}/{len(numbers)}] {number}{Style.RESET_ALL}")
            
            if analyze_single(number, deep_scan):
                success_count += 1
            
            # 2 saniye bekle (rate limiting)
            if i < len(numbers):
                import time
                time.sleep(2)
        
        print(f"\n{Fore.GREEN}[+] Toplu analiz tamamlandı!{Style.RESET_ALL}")
        print(f"   ✅ Başarılı: {success_count}/{len(numbers)}")
        print(f"   ❌ Başarısız: {len(numbers) - success_count}")
        
    except FileNotFoundError:
        print(f"{Fore.RED}[!] Dosya bulunamadı: {file_path}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Toplu analiz hatası: {e}{Style.RESET_ALL}")

def show_history(limit=10):
    """Analiz geçmişini göster"""
    import glob
    import json
    from datetime import datetime
    
    reports = list(Path("reports").glob("phone_*.json"))
    reports.sort(key=os.path.getmtime, reverse=True)
    
    if not reports:
        print(f"{Fore.YELLOW}[!] Henüz analiz geçmişi yok{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}[*] Son {min(limit, len(reports))} analiz:{Style.RESET_ALL}")
    
    for i, report in enumerate(reports[:limit], 1):
        try:
            with open(report, 'r') as f:
                data = json.load(f)
            
            phone = data.get('phone_number', 'Bilinmiyor')
            date = data.get('analysis_date', '').replace('T', ' ')
            risk = data.get('risk_analysis', {}).get('overall_risk', 'Bilinmiyor')
            
            print(f"\n{i}. {Fore.GREEN}{phone}{Style.RESET_ALL}")
            print(f"   📅 {date}")
            print(f"   ⚖️  Risk: {risk}")
            print(f"   📄 {report.name}")
            
        except:
            print(f"{i}. {report.name}")

def main():
    """Ana fonksiyon"""
    parser = argparse.ArgumentParser(
        description='ULTRA PRO MAX PHONE OSINT - Profesyonel Telefon Analiz Platformu',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Fore.CYAN}ÖRNEK KULLANIMLAR:{Style.RESET_ALL}

{Fore.GREEN}Tek numara analizi:{Style.RESET_ALL}
  python phone_analyzer.py -n "+905551234567"
  python phone_analyzer.py --number "05551234567" --deep

{Fore.GREEN}Toplu analiz:{Style.RESET_ALL}
  python phone_analyzer.py -f numbers.txt
  python phone_analyzer.py --file numbers.txt --deep

{Fore.GREEN}Geçmişi görüntüle:{Style.RESET_ALL}
  python phone_analyzer.py --history
  python phone_analyzer.py --history 20

{Fore.GREEN}Test modu:{Style.RESET_ALL}
  python phone_analyzer.py --test

{Fore.RED}ÖNEMLİ:{Style.RESET_ALL}
- Sadece kendi numaralarınızı veya izin aldığınız numaraları analiz edin
- Kişisel verilerin korunması kanunlarına (KVKK) saygı gösterin
- Bu araç sadece eğitim amaçlıdır
"""
    )
    
    # Ana argümanlar
    parser.add_argument('-n', '--number', help='Analiz edilecek telefon numarası')
    parser.add_argument('-f', '--file', help='Numara listesi içeren dosya')
    parser.add_argument('--deep', action='store_true', help='Derinlemesine analiz yap')
    parser.add_argument('--history', nargs='?', const=10, type=int, 
                       help='Analiz geçmişini göster (opsiyonel: kayıt sayısı)')
    parser.add_argument('--test', action='store_true', help='Sistem testi yap')
    
    args = parser.parse_args()
    
    # Banner göster
    print_banner()
    
    # İşlemi yap
    if args.test:
        print(f"{Fore.CYAN}[*] Sistem testi başlatılıyor...{Style.RESET_ALL}")
        
        # Modül testleri
        test_modules = [
            ("src/utils/validator.py", "Validator Test"),
            ("src/modules/social_analyzer.py", "Sosyal Medya Test"),
            ("src/modules/breach_analyzer.py", "Data Breach Test"),
            ("src/core/analyzer.py", "Ana Analiz Test")
        ]
        
        for module, name in test_modules:
            try:
                print(f"\n{Fore.YELLOW}[*] {name}...{Style.RESET_ALL}")
                os.system(f"python {module}")
                print(f"{Fore.GREEN}[✓] {name} başarılı{Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}[!] {name} başarısız{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}[+] Tüm testler tamamlandı!{Style.RESET_ALL}")
        
    elif args.history:
        show_history(args.history)
        
    elif args.number:
        analyze_single(args.number, args.deep)
        
    elif args.file:
        analyze_batch(args.file, args.deep)
        
    else:
        # Hiçbir argüman yoksa interaktif mod
        print(f"{Fore.CYAN}Lütfen bir işlem seçin:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1.{Style.RESET_ALL} Tek numara analizi")
        print(f"{Fore.GREEN}2.{Style.RESET_ALL} Toplu analiz (dosyadan)")
        print(f"{Fore.GREEN}3.{Style.RESET_ALL} Analiz geçmişini görüntüle")
        print(f"{Fore.GREEN}4.{Style.RESET_ALL} Sistem testi yap")
        print(f"{Fore.GREEN}5.{Style.RESET_ALL} Çıkış")
        
        try:
            choice = input(f"\n{Fore.YELLOW}Seçiminiz (1-5): {Style.RESET_ALL}")
            
            if choice == "1":
                number = input(f"{Fore.CYAN}Telefon numarası: {Style.RESET_ALL}")
                deep = input(f"{Fore.CYAN}Derin analiz? (e/h): {Style.RESET_ALL}").lower() == 'e'
                analyze_single(number, deep)
                
            elif choice == "2":
                filepath = input(f"{Fore.CYAN}Numara listesi dosyası: {Style.RESET_ALL}")
                deep = input(f"{Fore.CYAN}Derin analiz? (e/h): {Style.RESET_ALL}").lower() == 'e'
                analyze_batch(filepath, deep)
                
            elif choice == "3":
                limit = input(f"{Fore.CYAN}Kaç kayıt gösterilsin? (10): {Style.RESET_ALL}")
                limit = int(limit) if limit.strip() else 10
                show_history(limit)
                
            elif choice == "4":
                os.system(f"python {sys.argv[0]} --test")
                
            elif choice == "5":
                print(f"{Fore.GREEN}[*] Çıkış yapılıyor...{Style.RESET_ALL}")
                
            else:
                print(f"{Fore.RED}[!] Geçersiz seçim!{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Kullanıcı tarafından durduruldu.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Hata: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Program kullanıcı tarafından durduruldu.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Kritik hata: {e}{Style.RESET_ALL}")
