# 🔎 Gravatar Interactive OSINT Tool

**TR 🇹🇷 | EN 🇬🇧**

An interactive Python-based OSINT tool for retrieving publicly available Gravatar profile information from email addresses.

E-posta adresleri üzerinden herkese açık Gravatar profil bilgilerini sorgulamak için geliştirilmiş interaktif Python tabanlı OSINT aracıdır.

> ⚠️ **Important / Önemli:** This tool should only be used with email addresses you are authorized to investigate.
> Bu araç yalnızca inceleme yetkinizin bulunduğu e-posta adresleri üzerinde kullanılmalıdır.

---

# 🇹🇷 Türkçe

## 📌 Hakkında

**Gravatar Interactive OSINT Tool**, bir e-posta adresini Gravatar üzerinde sorgulayarak mevcut herkese açık profil bilgilerini toplamaya ve düzenlemeye yardımcı olan terminal tabanlı bir Python aracıdır.

Araç, e-posta adresinden MD5 hash oluşturur ve Gravatar'ın mevcut API uç noktalarını kullanarak profil bilgilerini almaya çalışır.

Öncelikle Gravatar V3 API denenir. Başarısız olması durumunda Legacy API üzerinden tekrar sorgulama yapılır.

## ✨ Özellikler

* 📧 Tek e-posta adresi sorgulama
* 📂 `.txt` dosyasından e-posta listesi yükleme
* 🔐 E-posta adresinden Gravatar MD5 hash oluşturma
* 👤 Profil adı bilgisi
* 🆔 Kullanıcı adı bilgisi
* 📍 Konum bilgisi
* 🔗 Gravatar profil bağlantısı
* 🔗 Bağlı/verified hesap bilgileri
* 💰 Profilde bulunan kripto cüzdan bilgileri
* 🔄 Gravatar V3 API desteği
* 🔙 Legacy API fallback desteği
* 🧹 Geçersiz e-posta adreslerini filtreleme
* ♻️ Aynı e-posta adreslerini tekrar sorgulamama
* 💾 JSON çıktı desteği
* 📊 CSV çıktı desteği
* ⏱️ Sorgular arasında otomatik bekleme

## 📋 Gereksinimler

* Python 3.8+
* İnternet bağlantısı
* `requests`

## 🚀 Kurulum

Repoyu klonlayın:

```bash
git clone https://github.com/USERNAME/REPOSITORY.git
cd REPOSITORY
```

Gerekli Python paketini yükleyin:

```bash
pip install -r requirements.txt
```

## ▶️ Kullanım

Programı çalıştırın:

```bash
python gravatar.py
```

Ana menü:

```text
==================================================
       GRAVATAR INTERACTIVE OSINT TOOL
==================================================
  1) Tek E-posta Sorgula
  2) E-posta Listesi (.txt) Yükle
  3) Sonuçları Kaydet (JSON/CSV)
  0) Çıkış
==================================================
```

### 1️⃣ Tek E-posta Sorgulama

Menüden `1` seçeneğini seçin ve e-posta adresini girin:

```text
E-posta adresini girin: example@example.com
```

Program e-posta adresini doğrular, hash oluşturur ve Gravatar profilini sorgular.

### 2️⃣ E-posta Listesi

Bir `.txt` dosyası içerisindeki birden fazla e-posta adresini sorgulayabilirsiniz.

Örnek:

```text
example1@example.com
example2@example.com
example3@example.com
```

Program geçerli e-posta adreslerini filtreler ve aynı adreslerin tekrar sorgulanmasını engeller.

### 3️⃣ Sonuçları Kaydetme

Toplanan sonuçları iki farklı formatta kaydedebilirsiniz:

```text
JSON
CSV
```

Oluşturulan dosyalar:

```text
gravatar_sonuclar.json
gravatar_sonuclar.csv
```

JSON çıktısı tüm profil verilerini saklarken CSV çıktısı temel profil bilgilerini içerir.

## 📊 Toplanan Bilgiler

Gravatar profilinde mevcut olması halinde aşağıdaki bilgiler alınabilir:

```text
Email
MD5 Hash
Name
Username
Location
Description
Profile URL
Avatar URL
Connected Accounts
Crypto Wallets
API Version
```

Profil ayrıştırma işlemi hem V3 hem de Legacy API formatlarına göre yapılmaktadır.

## ⏱️ Request Delay

Varsayılan sorgu bekleme süresi:

```text
2 seconds
```

Bu değer `REQUEST_DELAY` değişkeninden değiştirilebilir.

Program ayrıca HTTP istekleri için `15 saniyelik` timeout kullanır.

## 🔒 Gizlilik ve Güvenlik

Bu araç e-posta adresleri ve profil bilgileriyle çalıştığı için elde edilen verileri dikkatli şekilde saklayın.

* API yanıtlarını veya kişisel verileri herkese açık şekilde paylaşmayın.
* Sonuç dosyalarını GitHub'a yüklemeden önce kontrol edin.
* Başkalarına ait e-posta adreslerini izinsiz araştırmayın.
* Hassas bilgileri public repository içerisinde tutmayın.

## ⚠️ Yasal Uyarı

Bu proje eğitim, araştırma ve yetkili OSINT çalışmaları amacıyla hazırlanmıştır.

Yetkiniz olmayan kişilere ait e-posta adreslerini araştırmak, kişisel bilgileri toplamak veya elde edilen verileri kötüye kullanmak yerel yasalara ve hizmet şartlarına aykırı olabilir.

Yazılımın kötüye kullanımından geliştirici sorumlu değildir.

---

# 🇬🇧 English

## 📌 About

**Gravatar Interactive OSINT Tool** is a terminal-based Python tool designed to retrieve and organize publicly available Gravatar profile information using email addresses.

The tool generates an MD5 hash from an email address and attempts to retrieve available profile information from Gravatar.

It first attempts to use the Gravatar V3 API and falls back to the Legacy API if the first request is unsuccessful.

## ✨ Features

* 📧 Single email lookup
* 📂 Load email lists from `.txt` files
* 🔐 Generate Gravatar MD5 hashes
* 👤 Profile name information
* 🆔 Username information
* 📍 Location information
* 🔗 Gravatar profile URL
* 🔗 Connected/verified accounts
* 💰 Cryptocurrency wallet information
* 🔄 Gravatar V3 API support
* 🔙 Legacy API fallback
* 🧹 Email format validation
* ♻️ Duplicate email filtering
* 💾 JSON export
* 📊 CSV export
* ⏱️ Automatic request delay

## 📋 Requirements

* Python 3.8+
* Internet connection
* `requests`

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/USERNAME/REPOSITORY.git
cd REPOSITORY
```

Install the required dependency:

```bash
pip install -r requirements.txt
```

## ▶️ Usage

Run the tool:

```bash
python gravatar.py
```

Main menu:

```text
==================================================
       GRAVATAR INTERACTIVE OSINT TOOL
==================================================
  1) Single Email Lookup
  2) Load Email List (.txt)
  3) Save Results (JSON/CSV)
  0) Exit
==================================================
```

### 1️⃣ Single Email Lookup

Select option `1` and enter an email address:

```text
Enter email address: example@example.com
```

The tool validates the email, generates its hash, and attempts to retrieve the associated Gravatar profile.

### 2️⃣ Email List

You can process multiple email addresses from a `.txt` file.

Example:

```text
example1@example.com
example2@example.com
example3@example.com
```

The tool validates the addresses and removes duplicates before processing them.

### 3️⃣ Save Results

Results can be exported in two formats:

```text
JSON
CSV
```

Generated files:

```text
gravatar_sonuclar.json
gravatar_sonuclar.csv
```

JSON stores the collected profile data, while CSV exports the main profile fields.

## 📊 Collected Information

When available, the tool can retrieve:

```text
Email
MD5 Hash
Name
Username
Location
Description
Profile URL
Avatar URL
Connected Accounts
Crypto Wallets
API Version
```

The parser supports both V3 and Legacy Gravatar response formats.

## ⏱️ Request Delay

The default delay between requests is:

```text
2 seconds
```

This value can be changed using the `REQUEST_DELAY` variable.

The HTTP request timeout is configured to `15 seconds`.

## 🔒 Privacy & Security

Because this tool processes email addresses and profile information, collected data should be handled responsibly.

* Do not publicly share API responses or personal information.
* Review exported files before uploading them to GitHub.
* Do not investigate email addresses without proper authorization.
* Do not store sensitive personal information in a public repository.

## ⚠️ Legal Disclaimer

This project is intended for educational purposes, research, and authorized OSINT activities.

Investigating email addresses without authorization, collecting personal information, or misusing collected data may violate applicable laws or service terms.

The developer is not responsible for any misuse of this software.

---

# 📁 Project Structure / Proje Yapısı

```text
.
├── gravatar.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

# 📄 License / Lisans

This project is licensed under the **MIT License**.

Bu proje **MIT License** altında lisanslanmıştır.

See the `LICENSE` file for the complete license text.

Tam lisans metni için `LICENSE` dosyasına bakınız.

# ⭐ Support / Destek

If you find this project useful, consider giving it a ⭐ on GitHub.

Projeyi faydalı bulduysanız GitHub üzerinde ⭐ bırakabilirsiniz.

For bug reports and feature requests, please use GitHub Issues.

Hata bildirimleri ve özellik önerileri için GitHub Issues bölümünü kullanabilirsiniz.
