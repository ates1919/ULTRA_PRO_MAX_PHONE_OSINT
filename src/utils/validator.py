"""
Telefon Numarası Validator Modülü
Profesyonel ve optimize edilmiş
"""

import re
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from typing import Dict, Optional, Tuple

class PhoneValidator:
    """Profesyonel telefon validasyon sınıfı"""
    
    # Türkiye operatör prefix'leri
    TURKISH_OPERATORS = {
        '505': 'Turkcell', '506': 'Turkcell', '507': 'Turkcell',
        '530': 'Turkcell', '531': 'Turkcell', '532': 'Turkcell',
        '533': 'Turkcell', '534': 'Turkcell', '535': 'Turkcell',
        '536': 'Turkcell', '537': 'Turkcell', '538': 'Turkcell',
        '539': 'Turkcell', '561': 'Turkcell',
        
        '541': 'Vodafone', '542': 'Vodafone', '543': 'Vodafone',
        '544': 'Vodafone', '545': 'Vodafone', '546': 'Vodafone',
        '547': 'Vodafone', '548': 'Vodafone', '549': 'Vodafone',
        
        '501': 'Türk Telekom', '502': 'Türk Telekom', 
        '503': 'Türk Telekom', '504': 'Türk Telekom',
        '550': 'Türk Telekom', '551': 'Türk Telekom',
    }
    
    def __init__(self):
        """Constructor"""
        pass
    
    def normalize(self, phone_number: str) -> str:
        """
        Telefon numarasını normalize eder
        
        Args:
            phone_number: Girilen telefon numarası
            
        Returns:
            Normalize edilmiş numara
        """
        # Sadece rakam ve + işareti bırak
        cleaned = re.sub(r'[^\d+]', '', phone_number)
        
        # Format kontrolü
        if cleaned.startswith('0'):
            return '+90' + cleaned[1:]
        elif cleaned.startswith('90'):
            return '+' + cleaned
        elif cleaned.startswith('+'):
            return cleaned
        else:
            # Hiçbir format yoksa Türkiye numarası olarak kabul et
            return '+90' + cleaned
    
    def validate(self, phone_number: str) -> Tuple[bool, Optional[phonenumbers.PhoneNumber]]:
        """
        Telefon numarasını doğrular
        
        Args:
            phone_number: Doğrulanacak telefon numarası
            
        Returns:
            (is_valid, parsed_number)
        """
        try:
            normalized = self.normalize(phone_number)
            parsed = phonenumbers.parse(normalized, None)
            is_valid = phonenumbers.is_valid_number(parsed)
            return is_valid, parsed if is_valid else None
        except Exception as e:
            print(f"Validate hatası: {e}")
            return False, None
    
    def get_basic_info(self, parsed_number: phonenumbers.PhoneNumber) -> Dict:
        """
        Telefon numarasının temel bilgilerini alır
        
        Args:
            parsed_number: Parse edilmiş telefon numarası
            
        Returns:
            Temel bilgiler sözlüğü
        """
        try:
            info = {
                'country': phonenumbers.region_code_for_number(parsed_number) or "Unknown",
                'carrier': carrier.name_for_number(parsed_number, "en") or "Unknown",
                'region': geocoder.description_for_number(parsed_number, "en") or "Unknown",
                'timezones': timezone.time_zones_for_number(parsed_number) or [],
                'is_valid': True,
                'formats': {
                    'e164': phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164),
                    'international': phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                    'national': phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL),
                }
            }
            
            # Türkiye numaraları için operatör tespiti
            if info['country'] == 'TR':
                info['carrier'] = self.detect_turkish_operator(
                    info['formats']['e164']
                )
                info['is_mobile'] = self.is_turkish_mobile(parsed_number)
                info['number_type'] = 'MOBILE' if info['is_mobile'] else 'LANDLINE'
            else:
                info['is_mobile'] = False
                info['number_type'] = 'UNKNOWN'
            
            return info
            
        except Exception as e:
            print(f"get_basic_info hatası: {e}")
            return {
                'country': 'Unknown',
                'carrier': 'Unknown',
                'region': 'Unknown',
                'timezones': [],
                'is_valid': False,
                'is_mobile': False,
                'number_type': 'UNKNOWN',
                'formats': {}
            }
    
    def detect_turkish_operator(self, phone_number: str) -> str:
        """
        Türkiye numaraları için operatör tespiti
        
        Args:
            phone_number: Telefon numarası
            
        Returns:
            Operatör adı
        """
        # Sadece rakamları al
        digits = ''.join(filter(str.isdigit, phone_number))
        
        if len(digits) >= 12 and digits.startswith('90'):
            prefix = digits[2:5]  # 505, 506, vb.
            return self.TURKISH_OPERATORS.get(prefix, "Bilinmeyen Operatör")
        
        return "Bilinmeyen Operatör"
    
    def is_turkish_mobile(self, parsed_number: phonenumbers.PhoneNumber) -> bool:
        """
        Türkiye numarasının mobil olup olmadığını kontrol eder
        
        Args:
            parsed_number: Parse edilmiş telefon numarası
            
        Returns:
            Mobil ise True
        """
        try:
            country = phonenumbers.region_code_for_number(parsed_number)
            if country != 'TR':
                return False
            
            national_number = str(parsed_number.national_number)
            return len(national_number) == 10 and national_number.startswith('5')
            
        except:
            return False
    
    def get_risk_level(self, phone_info: Dict) -> str:
        """
        Telefon numarası için risk seviyesini belirler
        
        Args:
            phone_info: Telefon bilgileri sözlüğü
            
        Returns:
            Risk seviyesi (LOW, MEDIUM, HIGH)
        """
        # Basit risk analizi
        if not phone_info.get('is_valid', False):
            return "HIGH"
        
        country = phone_info.get('country', '')
        
        # Bilinmeyen ülkeler yüksek risk
        if country == 'Unknown':
            return "HIGH"
        
        # Türkiye numaraları düşük risk
        if country == 'TR':
            return "LOW"
        
        # Diğer ülkeler orta risk
        return "MEDIUM"

# Test fonksiyonu
if __name__ == "__main__":
    validator = PhoneValidator()
    
    test_numbers = [
        "+905551234567",
        "05551234567",
        "905551234567",
        "+14155552671",  # USA
        "+442079813000",  # UK
    ]
    
    print("Telefon Validator Testi")
    print("=" * 50)
    
    for number in test_numbers:
        print(f"\nNumara: {number}")
        is_valid, parsed = validator.validate(number)
        
        if is_valid and parsed:
            info = validator.get_basic_info(parsed)
            print(f"  ✓ Geçerli")
            print(f"  Ülke: {info['country']}")
            print(f"  Operatör: {info['carrier']}")
            print(f"  Bölge: {info['region']}")
            print(f"  Tür: {info['number_type']}")
            print(f"  Risk: {validator.get_risk_level(info)}")
        else:
            print(f"  ✗ Geçersiz")
