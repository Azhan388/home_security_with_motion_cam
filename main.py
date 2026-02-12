import serial
import cv2
import os
import time
import requests
import winsound
from datetime import datetime

# --- KONFIGURASI ---
TOKEN = "8166786260:AAGereS8weHOFneN82oM0kog8_ZKXUot55k"
CHAT_ID = 7078535974
PORT = 'COM3'

def send_telegram(image_path):
    # Pastikan tidak ada spasi di token
    t = TOKEN.strip()
    url = f"https://api.telegram.org/bot{t}/sendPhoto"
    
    try:
        with open(image_path, 'rb') as photo:
            payload = {'chat_id': CHAT_ID, 'caption': '⚠️ PERINGATAN: Gerakan terdeteksi!'}
            files = {'photo': photo}
            response = requests.post(url, data=payload, files=files)
            
            # Mari kita bongkar jawabannya jika masih gagal
            res_json = response.json()
            if res_json.get("ok"):
                print("✅ FOTO BERHASIL TERKIRIM KE TELEGRAM!")
            else:
                print(f"❌ TELEGRAM ERROR: {res_json.get('description')}")
    except Exception as e:
        print(f"❌ KESALAHAN SISTEM: {e}")

# --- INISIALISASI ---
if not os.path.exists('captures'):
    os.makedirs('captures')

try:
    ser = serial.Serial(PORT, 9600, timeout=1)
    cap = cv2.VideoCapture(0) # 0 adalah kamera default
    time.sleep(2)
    print("Sistem Aktif... Siap mengirim foto ke @AzkaHomeSecurity_Bot")
except Exception as e:
    print(f"❌ Gagal Inisialisasi: {e}")
    exit()

try:
    while True:
        if ser.in_waiting > 0:
            raw_line = ser.readline().decode('utf-8', errors='ignore').strip()
            
            if "ADA_ORANG" in raw_line:
                print("🚨 Ada orang! Memotret...")
                winsound.Beep(1000, 500)
                
                ret, frame = cap.read()
                if ret:
                    waktu = datetime.now().strftime("%Y%m%d_%H%M%S")
                    nama_file = f"captures/security_{waktu}.jpg"
                    cv2.imwrite(nama_file, frame)
                    
                    # Kirim foto
                    send_telegram(nama_file)
                
                time.sleep(3) # Tunggu 3 detik sebelum deteksi lagi
except KeyboardInterrupt:
    print("Sistem Berhenti.")
finally:
    ser.close()
    cap.release()