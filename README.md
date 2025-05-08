# simulations
Airplane baggage check simulation


# 🧳 Baggage Security Simulator

Python ile geliştirilmiş bir GUI uygulamasıdır. Amaç, havaalanı benzeri bir ortamda yolcu bagajlarını kontrol ederek, şüpheli eşyaları ve kara listedeki kişileri tespit etmektir.

---

## 🚀 Özellikler

- **Tkinter GUI** ile kullanıcı dostu arayüz
- **Queue (Kuyruk):** Yolcular FIFO mantığıyla sıraya girer
- **Stack (Yığın):** Eşyalar LIFO mantığıyla kontrol edilir
- **LinkedList (Bağlantılı Liste):** Kara listedeki kişiler burada tutulur
- **JSON Entegrasyonu:** Kara liste dosyaya kaydedilir ve tekrar yüklenebilir
- **Gerçekçi Eşya Kontrolü:** Tehlikeli eşyalar listesine göre %50 şansla alarm tetiklenir

---

## 🗂️ Klasör Yapısı

```bash
baggage_security_simulator/
├── main.py                 # Programın başlangıç noktası
├── gui.py                  # Tüm arayüz ve simülasyon işlemleri
├── models/                 # Veri yapıları
│   ├── queue.py
│   ├── stack.py
│   ├── linkedlist.py
│   ├── yolcu.py
│   └── __init__.py
├── utils/
│   ├── olasilik.py         # Tehlikeli eşya kontrol fonksiyonu
│   └── __init__.py
├── data/
│   └── kara_liste.json     # Kara liste kayıtları (ID listesi)
