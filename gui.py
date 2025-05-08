import tkinter as tk
import random
import json
from models.yolcu import Passenger
from models.queue import Queue
from models.stack import Stack
from models.linkedlist import LinkedList
from utils.olasilik import is_item_dangerous

class BaggageSecuritySimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Bagaj Güvenlik Simülatörü")
        self.root.geometry("900x600")

        self.queue = Queue()
        self.stack = Stack()
        self.blacklist = LinkedList()

        self.total_passengers = 0
        self.alarm_count = 0
        self.blacklist_hit_count = 0
        self.cleared_count = 0
        self.stack_count = 0

        self.passenger_ids = {}

        self.setup_gui()
        self.load_blacklist_from_file()

    def setup_gui(self):
        self.queue_listbox = self.setup_listbox("Passenger Queue", 10, 10)
        self.stack_listbox = self.setup_listbox("Baggage Stack", 220, 10)
        self.linkedlist_text = self.setup_textbox("Blacklist (LinkedList)", 430, 10)
        self.log_text = self.setup_textbox("System Log", 10, 270, h=200, w=620)

        frame5 = tk.LabelFrame(self.root, text="Control Panel")
        frame5.place(x=10, y=480, width=620, height=100)
        tk.Button(frame5, text="Yeni Yolcu Ekle", command=self.add_passenger).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(frame5, text="Simülasyonu Başlat", command=self.start_simulation).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(frame5, text="Raporu Göster", command=self.show_report).pack(side=tk.LEFT, padx=10, pady=10)

        self.blacklist_entry = tk.Entry(self.root)
        self.blacklist_entry.place(x=650, y=30, width=150)
        tk.Button(self.root, text="Kara Listeye Ekle", command=self.gui_add_blacklist).place(x=650, y=60, width=150)
        tk.Button(self.root, text="Load Data", command=self.load_data).place(x=650, y=100, width=150)

    def setup_listbox(self, title, x, y, w=200, h=250):
        frame = tk.LabelFrame(self.root, text=title)
        frame.place(x=x, y=y, width=w, height=h)
        listbox = tk.Listbox(frame)
        listbox.pack(fill=tk.BOTH, expand=True)
        return listbox

    def setup_textbox(self, title, x, y, h=250, w=200):
        frame = tk.LabelFrame(self.root, text=title)
        frame.place(x=x, y=y, width=w, height=h)
        text = tk.Text(frame)
        text.pack(fill=tk.BOTH, expand=True)
        return text

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def update_gui_lists(self):
        self.queue_listbox.delete(0, tk.END)
        for passenger in self.queue:
            self.queue_listbox.insert(tk.END, passenger.id)

        self.stack_listbox.delete(0, tk.END)
        for item in self.stack:
            if is_item_dangerous(item):
                self.stack_listbox.insert(tk.END, item)
                self.stack_listbox.itemconfig(tk.END, {'bg': 'red', 'fg': 'white'})
            else:
                self.stack_listbox.insert(tk.END, item)

        self.linkedlist_text.delete("1.0", tk.END)
        for pid in self.blacklist.to_list():
            self.linkedlist_text.insert(tk.END, f"ID: {pid}\n")

    def add_passenger(self):
        items = random.sample(
            ["laptop", "phone", "liquid", "knife", "camera", "book", "charger", "scissors", "perfume", "battery"],
            random.randint(5, 10)
        )
        numeric_id = random.randint(10000, 99999)
        passenger_name = f"Passenger #{self.total_passengers + 1}"
        full_id = f"{passenger_name} (ID: {numeric_id})"
        self.passenger_ids[passenger_name] = numeric_id

        new_passenger = Passenger(passenger_name, items)
        self.queue.enqueue(new_passenger)
        self.total_passengers += 1
        self.log(f"[EKLE] {full_id} kuyruğa eklendi. Eşyalar: {', '.join(items)}")
        self.update_gui_lists()

    def add_to_blacklist(self, pid):
        self.blacklist.add(pid)
        self.log(f"[BLACKLIST] ID: {pid} kara listeye eklendi.")
        self.save_blacklist_to_file()
        self.update_gui_lists()

    def gui_add_blacklist(self):
        pid = self.blacklist_entry.get()
        if pid and pid.isdigit():
            self.add_to_blacklist(pid)
        else:
            self.log("[UYARI] Kara listeye eklemek için geçerli sayısal bir ID giriniz.")

    def start_simulation(self):
        if self.queue.is_empty():
            self.log("[UYARI] Kuyrukta yolcu yok.")
            return

        passenger = self.queue.dequeue()
        pid_num = self.passenger_ids.get(passenger.id, "????")
        self.log(f"[KONTROL] {passenger.id} (ID: {pid_num}) güvenlik kontrolüne alındı.")

        if self.blacklist.search(str(pid_num)):
            passenger.risk = True
            self.blacklist_hit_count += 1
            self.log(f"[ALARM] {passenger.id} kara listede bulundu! (ID: {pid_num})")

        self.stack.clear()
        for item in passenger.items:
            self.stack.push(item)
            if is_item_dangerous(item):
                passenger.risk = True
                self.log(f"[TEHLİKE] {item} tehlikeli eşya olarak tespit edildi!")

        if passenger.risk:
            self.alarm_count += 1
            self.stack_count += 1
            self.log(f"[SONUÇ] {passenger.id} detaylı incelemeye alındı.")
        else:
            self.cleared_count += 1
            self.log(f"[TEMİZ] {passenger.id} temiz geçti.")

        self.update_gui_lists()

    def load_data(self):
        for _ in range(30):
            self.add_passenger()
        self.log("[YÜKLE] 30 yolcu otomatik yüklendi.")

    def show_report(self):
        report = f"""
[RAPOR]
Toplam Kuyrukta Bekleyen Yolcu: {len(list(self.queue))}
Alarm Verilenler: {self.alarm_count}
Kara Listede Yakalananlar: {self.blacklist_hit_count}
Temiz Geçiş Yapanlar: {self.cleared_count}
İncelenen Bagaj Sayısı (Stack): {self.stack_count}
"""
        self.log(report)

    def load_blacklist_from_file(self):
        try:
            with open("data/kara_liste.json", "r") as f:
                data = json.load(f)
                for pid in data:
                    self.blacklist.add(pid)
            self.log("[YÜKLE] Kara liste dosyadan yüklendi.")
        except FileNotFoundError:
            self.log("[UYARI] Kara liste dosyası bulunamadı.")
        except json.JSONDecodeError:
            self.log("[HATA] kara_liste.json formatı bozuk!")

    def save_blacklist_to_file(self):
        data = self.blacklist.to_list()
        with open("data/kara_liste.json", "w") as f:
            json.dump(data, f, indent=4)
