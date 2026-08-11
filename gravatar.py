#!/usr/bin/env python3
"""
Gravatar Interactive OSINT Tool - 2026 Edition
E-posta adreslerinden Gravatar profilleri üzerinden istihbarat toplar.
Tamamen interaktif menü yapısına sahiptir.
"""

import hashlib
import json
import re
import sys
import time
import csv
from pathlib import Path

try:
    import requests
except ImportError:
    print("❌ 'requests' kütüphanesi eksik. Kurulum: pip install requests")
    sys.exit(1)

# --- SABİTLER ---
REQUEST_DELAY = 2.0  # Ban yememek için bekleme süresi
USER_AGENT = 'Mozilla/5.0 (compatible; GravatarOSINT/2026.1)'
TIMEOUT = 15

# API Endpoint'leri
API_V3 = 'https://api.gravatar.com/v3/profiles/{hash}'
API_LEGACY = 'https://en.gravatar.com/{hash}.json'

# E-posta Regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

# Global sonuç listesi
ALL_PROFILES = []


def validate_email(email):
    """E-posta formatını doğrular ve temizler."""
    email = email.strip().lower()
    if not email:
        return None
    if EMAIL_REGEX.match(email):
        return email
    return None


def get_gravatar_hash(email):
    """MD5 hash üretir."""
    return hashlib.md5(email.encode('utf-8')).hexdigest()


def fetch_profile(email_hash):
    """Gravatar'dan veri çeker (V3 -> Legacy fallback)."""
    headers = {'User-Agent': USER_AGENT}

    # 1. Yeni V3 API Dene
    try:
        resp = requests.get(API_V3.format(hash=email_hash), headers=headers, timeout=TIMEOUT)
        if resp.status_code == 200:
            return resp.json(), 'v3'
    except requests.exceptions.RequestException:
        pass

    # 2. Eski Legacy API Dene
    try:
        resp = requests.get(API_LEGACY.format(hash=email_hash), headers=headers, timeout=TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            if 'entry' in data and data['entry']:
                return data['entry'][0], 'legacy'
    except (requests.exceptions.RequestException, ValueError):
        pass

    return None, None


def parse_profile(data, api_version, email):
    """Veriyi standartlaştırır."""
    profile = {
        'email': email,
        'hash': get_gravatar_hash(email),
        'name': '',
        'username': '',
        'location': '',
        'description': '',
        'profile_url': '',
        'avatar_url': '',
        'phone_numbers': [],
        'accounts': [],
        'crypto_wallets': [],
        'api_version': api_version
    }

    if api_version == 'v3':
        profile['name'] = data.get('display_name', '') or data.get('name', {}).get('formatted', '')
        profile['username'] = data.get('profile_url', '').split('/')[-1] if data.get('profile_url') else ''
        profile['location'] = data.get('current_location', '')
        profile['description'] = data.get('description', '')
        profile['profile_url'] = data.get('profile_url', '')
        profile['avatar_url'] = data.get('avatar_url', '')
        
        for acc in data.get('verified_accounts', []) or []:
            profile['accounts'].append({
                'service': acc.get('service_type', ''),
                'username': acc.get('username', ''),
                'url': acc.get('url', '')
            })
            
        for cur in data.get('crypto_addresses', []) or []:
            profile['crypto_wallets'].append({
                'type': cur.get('type', ''),
                'address': cur.get('value', '')
            })
            
    else:  # legacy
        profile['name'] = data.get('name', {}).get('formatted', '') if isinstance(data.get('name'), dict) else str(data.get('name', ''))
        profile['username'] = data.get('preferredUsername', '')
        profile['location'] = data.get('currentLocation', '')
        profile['description'] = data.get('aboutMe', '')
        profile['profile_url'] = data.get('profileUrl', '')
        profile['avatar_url'] = data.get('thumbnailUrl', '')

        for acc in data.get('accounts', []) or []:
            profile['accounts'].append({
                'service': acc.get('shortname', ''),
                'username': acc.get('username', ''),
                'url': acc.get('url', '')
            })
            
        for cur in data.get('currency', []) or []:
            profile['crypto_wallets'].append({
                'type': cur.get('type', ''),
                'address': cur.get('value', '')
            })

    return profile


def print_profile(profile):
    """Sonucu ekrana basar."""
    print(f"\n{'=' * 60}")
    print(f"📧 E-posta: {profile['email']}")
    print(f"🔑 Hash:    {profile['hash']}")
    print('=' * 60)

    if profile['name']: print(f"👤 İsim:      {profile['name']}")
    if profile['username']: print(f"🆔 Kullanıcı: {profile['username']}")
    if profile['location']: print(f"📍 Konum:     {profile['location']}")
    if profile['profile_url']: print(f"🔗 Profil:    {profile['profile_url']}")
    
    if profile['accounts']:
        print("\n🔗 Bağlı Hesaplar:")
        for a in profile['accounts']:
            print(f"   • {a['service']}: {a['username']}")
            
    if profile['crypto_wallets']:
        print("\n💰 Kripto Cüzdanları:")
        for c in profile['crypto_wallets']:
            print(f"   • [{c['type']}] {c['address']}")

    if not any([profile['name'], profile['username'], profile['accounts']]):
        print("\nℹ️  Profil bulundu ama detay bilgisi boş.")


def save_results(format_type='json'):
    """Sonuçları dosyaya kaydeder."""
    if not ALL_PROFILES:
        print("⚠️  Kaydedilecek veri yok.")
        return

    filename = f"gravatar_sonuclar.{format_type}"
    path = Path(filename)

    if format_type == 'json':
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(ALL_PROFILES, f, ensure_ascii=False, indent=2)
    elif format_type == 'csv':
        fieldnames = ['email', 'name', 'username', 'location', 'profile_url']
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            for p in ALL_PROFILES:
                writer.writerow(p)

    print(f"\n💾 Sonuçlar '{filename}' dosyasına kaydedildi!")


def process_emails(email_list):
    """Email listesini işler."""
    unique_emails = []
    seen = set()
    
    # Filtreleme
    for e in email_list:
        valid = validate_email(e)
        if valid and valid not in seen:
            unique_emails.append(valid)
            seen.add(valid)

    if not unique_emails:
        print("❌ Geçerli e-posta bulunamadı.")
        return

    print(f"\n📋 Toplam {len(unique_emails)} benzersiz e-posta işlenecek.")
    print(f"⏱️  Tahmini süre: ~{len(unique_emails) * REQUEST_DELAY:.0f} saniye")
    print("=" * 60)

    found_count = 0
    for i, email in enumerate(unique_emails, 1):
        print(f"\n[{i}/{len(unique_emails)}] Sorgulanıyor: {email}")
        
        email_hash = get_gravatar_hash(email)
        data, api_ver = fetch_profile(email_hash)

        if data:
            profile = parse_profile(data, api_ver, email)
            ALL_PROFILES.append(profile)
            print_profile(profile)
            found_count += 1
        else:
            print("   ❌ Profil bulunamadı.")

        if i < len(unique_emails):
            time.sleep(REQUEST_DELAY)

    print(f"\n{'=' * 60}")
    print(f"✅ Tarama bitti! Bulunan: {found_count}/{len(unique_emails)}")


def main():
    while True:
        print("\n" + "=" * 50)
        print("       GRAVATAR INTERACTIVE OSINT TOOL")
        print("=" * 50)
        print("  1) Tek E-posta Sorgula")
        print("  2) E-posta Listesi (.txt) Yükle")
        print("  3) Sonuçları Kaydet (JSON/CSV)")
        print("  0) Çıkış")
        print("=" * 50)

        choice = input("\nSeçiminiz (0-3): ").strip()

        if choice == "1":
            email = input("E-posta adresini girin: ").strip()
            process_emails([email])
            
        elif choice == "2":
            filepath = input("Dosya yolunu girin (örn: emailler.txt): ").strip()
            path = Path(filepath)
            if not path.exists():
                print("❌ Dosya bulunamadı!")
                continue
            
            with open(path, 'r', encoding='utf-8') as f:
                emails = [line.strip() for line in f if line.strip()]
            process_emails(emails)

        elif choice == "3":
            fmt = input("Format seçin (json/csv): ").strip().lower()
            if fmt in ['json', 'csv']:
                save_results(fmt)
            else:
                print("❌ Geçersiz format.")

        elif choice == "0":
            print("👋 Görüşmek üzere!")
            break
        
        else:
            print("❌ Geçersiz seçim.")

if __name__ == '__main__':
    main()