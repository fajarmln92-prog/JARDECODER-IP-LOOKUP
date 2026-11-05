
import os
import time
import socket
import shutil
import subprocess
import requests
from datetime import datetime

# ===== WARNA TERMINAL =====
G = "\033[92m"
D = "\033[32m"
R = "\033[0m"
RED = "\033[91m"

# ===== FILE HASIL =====
SAVE_FILE = os.path.expanduser("~/Desktop/hasil_ip.txt")


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def save_history(category, domain, ip, geo):
    """Simpan hasil lookup dalam format laporan vertikal."""

    os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)

    if domain:
        platform = domain.split(".")[0].upper()
    else:
        platform = "OWN PUBLIC IP"

    location_title = f"{platform} LOCATION INFORMATION"

    with open(SAVE_FILE, "a", encoding="utf-8") as file:

        file.write("\n\n")
        file.write("============================================================\n\n")
        file.write("                 JARDECODER </>\n\n")
        file.write("                   LOOKUP REPORT\n\n")
        file.write("============================================================\n\n\n")

        file.write(f"  DATE          : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        file.write(f"  CATEGORY      : {category}\n\n")
        file.write(f"  DOMAIN        : {domain if domain else 'Own Public IP'}\n\n")
        file.write(f"  IP ADDRESS    : {ip}\n\n\n")

        file.write("------------------------------------------------------------\n\n")
        file.write(f"             {location_title}\n\n")
        file.write("------------------------------------------------------------\n\n\n")

        file.write(f"  COUNTRY       : {geo.get('country', '')}\n\n")
        file.write(f"  REGION        : {geo.get('region', '')}\n\n")
        file.write(f"  CITY          : {geo.get('city', '')}\n\n")
        file.write(f"  ISP           : {geo.get('isp', '')}\n\n\n")

        file.write("------------------------------------------------------------\n\n")
        file.write("                    COORDINATES\n\n")
        file.write("------------------------------------------------------------\n\n\n")

        file.write(f"  LATITUDE      : {geo.get('latitude', '')}\n\n")
        file.write(f"  LONGITUDE     : {geo.get('longitude', '')}\n\n\n")

        file.write("------------------------------------------------------------\n\n")
        file.write("                    GOOGLE MAPS\n\n")
        file.write("------------------------------------------------------------\n\n\n")

        file.write(f"  LINK          : {geo.get('google_maps', '')}\n\n\n")

        file.write("============================================================\n\n")
        file.write("                  END OF REPORT\n\n")
        file.write("============================================================\n\n\n")


def get_geolocation(ip):
    """Ambil informasi lokasi perkiraan dari alamat IP."""
    try:
        response = requests.get(
            f"https://ipwho.is/{ip}",
            timeout=15
        )
        response.raise_for_status()
        data = response.json()

        if not data.get("success"):
            print(f"{RED}[!] Geolocation gagal: {data.get('message', 'Unknown error')}{R}")
            return None

        connection = data.get("connection") or {}
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        maps_url = ""
        if latitude is not None and longitude is not None:
            maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"

        return {
            "country": data.get("country", ""),
            "region": data.get("region", ""),
            "city": data.get("city", ""),
            "isp": connection.get("isp", ""),
            "latitude": latitude if latitude is not None else "",
            "longitude": longitude if longitude is not None else "",
            "google_maps": maps_url
        }

    except requests.RequestException as error:
        print(f"{RED}[!] Gagal menghubungi layanan geolocation: {error}{R}")
        return None


def show_result(category, domain, ip):
    print(f"\n{G}[+] IP Address : {ip}{R}")
    print(f"{D}[*] Mengambil informasi lokasi...{R}")

    geo = get_geolocation(ip)

    if geo is None:
        print(f"{RED}[!] Data geolocation gagal. Hasil tidak disimpan.{R}")
        return

    print(f"\n{G}===== HASIL LOOKUP ====={R}")
    print(f"IP Address : {ip}")
    print(f"Country    : {geo['country']}")
    print(f"Region     : {geo['region']}")
    print(f"City       : {geo['city']}")
    print(f"ISP        : {geo['isp']}")
    print(f"Latitude   : {geo['latitude']}")
    print(f"Longitude  : {geo['longitude']}")
    print(f"Google Maps: {geo['google_maps']}")

    try:
        save_history(category, domain, ip, geo)
        print(f"\n{G}[+] Hasil tersimpan: {SAVE_FILE}{R}")
    except OSError as error:
        print(f"{RED}[!] Gagal menyimpan hasil: {error}{R}")


def domain_lookup():
    domain = input(f"\n{G}[?] Masukkan domain: {R}").strip()

    if not domain:
        print(f"{RED}[!] Domain tidak boleh kosong.{R}")
        return

    domain = domain.replace("https://", "").replace("http://", "")
    domain = domain.split("/")[0].strip()

    try:
        ip = socket.gethostbyname(domain)
        show_result("DOMAIN IP LOOKUP", domain, ip)
    except socket.gaierror:
        print(f"{RED}[!] Domain tidak ditemukan atau tidak dapat di-resolve.{R}")


def public_ip_lookup():
    print(f"\n{D}[*] Mengambil public IP...{R}")

    try:
        response = requests.get("https://api.ipify.org", timeout=15)
        response.raise_for_status()
        ip = response.text.strip()

        if not ip:
            print(f"{RED}[!] Public IP tidak berhasil didapatkan.{R}")
            return

        show_result("OWN PUBLIC IP LOOKUP", "", ip)

    except requests.RequestException as error:
        print(f"{RED}[!] Gagal mengambil public IP: {error}{R}")


def glitch_intro():
    clear()
    print(f"{G}[+] INITIALIZING JARDECODER...{R}")
    time.sleep(0.5)
    print(f"{D}[+] DECRYPTING MASK...{R}")
    time.sleep(0.5)

    mask_path = os.path.expanduser("~/Pictures/guyfawkes.jpg")

    if shutil.which("chafa") and os.path.exists(mask_path):
        subprocess.run(
            ["chafa", "--colors", "full", "--size", "40x20", mask_path],
            check=False
        )
    else:
        print(f"{RED}[!] Mask image atau chafa tidak ditemukan.{R}")

    print(f"\n{G}      JARDECODER </>{R}")
    print(f"{D}      [ SYSTEM ONLINE ]{R}")
    time.sleep(1)


def show_menu():
    clear()
    print(f"{G}╔════════════════════════════════════╗{R}")
    print(f"{G}║          JARDECODER </>            ║{R}")
    print(f"{G}║          SYSTEM TERMINAL           ║{R}")
    print(f"{G}╠════════════════════════════════════╣{R}")
    print(f"{G}║  [1] Domain IP Lookup               ║{R}")
    print(f"{G}║  [2] Own Public IP Lookup           ║{R}")
    print(f"{G}║  [0] Exit                           ║{R}")
    print(f"{G}╚════════════════════════════════════╝{R}")



def goodbye():
    clear()
    print(G + r"""
███████╗ █████╗ ███╗   ███╗██████╗  █████╗ ██╗
██╔════╝██╔══██╗████╗ ████║██╔══██╗██╔══██╗██║
███████║███████║██╔████╔██║██████╔╝███████║██║
╚════██║██╔══██║██║╚██╔╝██║██╔═══╝ ██╔══██╗██║
███████║██║  ██║██║ ╚═╝ ██║██║     ██║  ██║██║
╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝

     ██╗██╗   ██╗███╗   ███╗██████╗  █████╗
     ██║██║   ██║████╗ ████║██╔══██╗██╔══██╗
     ██║██║   ██║██╔████╔██║██████╔╝███████║
██   ██║██║   ██║██║╚██╔╝██║██╔═══╝ ██╔══██╗
╚█████╔╝╚█████╔╝██║ ╚═╝ ██║██║     ██║  ██║
 ╚════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝  ╚═╝

         SCRIPT BY : JARDECODER</>
""" + R)


def main():
    glitch_intro()

    while True:
        show_menu()
        choice = input(f"\n{G}[JARDECODER] pilih menu: {R}").strip()

        if choice == "1":
            domain_lookup()
            input(f"\n{D}Tekan Enter untuk kembali ke menu...{R}")

        elif choice == "2":
            public_ip_lookup()
            input(f"\n{D}Tekan Enter untuk kembali ke menu...{R}")

        elif choice == "0":
            goodbye()
            break

        else:
            print(f"{RED}[!] Pilihan tidak valid.{R}")
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        goodbye()
