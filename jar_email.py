
import re
import time
import os
import shutil
import subprocess
from datetime import datetime
from collections import deque
from urllib.parse import urldefrag, urljoin, urlsplit

import requests
from bs4 import BeautifulSoup


# ==================== COLORS ====================

G = "\033[92m"
D = "\033[32m"
R = "\033[0m"
RED = "\033[91m"


# ==================== CONFIGURATION ====================

EMAIL_PATTERN = re.compile(
    r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}",
    re.IGNORECASE
)

DESKTOP = os.path.expanduser("~/Desktop")
os.makedirs(DESKTOP, exist_ok=True)

TXT_FILE = os.path.join(
    DESKTOP,
    "hasil_email.txt"
)


# ==================== TERMINAL ====================

def clear():
    os.system("clear")


def glitch_intro():

    clear()

    print(G + "\n[+] INITIALIZING JARDECODER..." + R)
    time.sleep(0.5)

    print(D + "[+] DECRYPTING MASK..." + R)
    time.sleep(0.5)

    mask = os.path.expanduser(
        "~/Pictures/guyfawkes.jpg"
    )

    if os.path.exists(mask) and shutil.which("chafa"):

        result = subprocess.run(
            [
                "chafa",
                "--colors",
                "full",
                "--size",
                "40x20",
                mask
            ],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:

            for line in result.stdout.splitlines():

                print(line)
                time.sleep(0.04)

    print(G + "\n       JARDECODER </>" + R)
    print(D + "     [ SYSTEM ONLINE ]" + R)

    time.sleep(0.5)


# ==================== URL VALIDATION ====================

def normalize_url(raw_url):

    raw_url = raw_url.strip()

    if not raw_url:

        raise ValueError(
            "URL tidak boleh kosong."
        )

    if not urlsplit(raw_url).scheme:

        raw_url = "https://" + raw_url

    parsed = urlsplit(raw_url)

    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.hostname
    ):

        raise ValueError(
            "Masukkan URL HTTP atau HTTPS yang valid."
        )

    return urldefrag(raw_url)[0]


# ==================== SAVE TXT REPORT ====================

def save_txt_report(
    domain,
    emails,
    pages_checked
):

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    lines = [

        "=" * 60,
        "",
        "                 JARDECODER </>",
        "",
        "                 EMAIL SCRAPER REPORT",
        "",
        "=" * 60,
        "",
        f"  DATE          : {now}",
        "",
        "  CATEGORY      : EMAIL SCRAPER",
        "",
        f"  DOMAIN        : {domain}",
        "",
        f"  PAGES CHECKED : {pages_checked}",
        "",
        f"  EMAILS FOUND  : {len(emails)}",
        "",
        "-" * 60,
        "",
        "                    EMAIL RESULTS",
        "",
        "-" * 60,
        ""

    ]

    if emails:

        for index, email in enumerate(
            sorted(emails, key=str.lower),
            start=1
        ):

            lines.append(
                f"  [{index}] {email}"
            )

            lines.append("")

    else:

        lines.append(
            "  No emails found."
        )

        lines.append("")

    lines.extend([
        "",
        "============================================================",
        "",
        "                  END OF REPORT",
        "",
        "============================================================",
        "",
        "",
        "",
        "",
        ""
    ])

    with open(
        TXT_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n".join(lines) + "\n"
        )

    return TXT_FILE


# ==================== EMAIL SCRAPER ====================

def email_scraper():

    clear()

    print(G + """

╔══════════════════════════════════════════╗
║                                          ║
║               EMAIL SCRAPER              ║
║                                          ║
║              JARDECODER </>              ║
║                                          ║
╚══════════════════════════════════════════╝

""" + R)

    try:

        start_url = normalize_url(
            input(
                G + "[+] Enter website URL: " + R
            )
        )

        page_limit = int(
            input(
                G + "[+] Maximum pages to check: " + R
            )
        )

        if page_limit < 1:

            raise ValueError(
                "Batas halaman minimal 1."
            )

    except ValueError as error:

        print(
            RED
            + "\n[!] Input tidak valid: "
            + str(error)
            + R
        )

        input(
            "\nTekan Enter untuk kembali..."
        )

        return

    allowed_host = (
        urlsplit(start_url)
        .hostname
        .lower()
    )

    urls_to_visit = deque([start_url])
    queued_urls = {start_url}
    visited_urls = set()
    emails = set()

    headers = {
        "User-Agent":
        "AuthorizedContactPageScraper/1.0"
    }

    print(
        D + "\n[+] Starting crawler..." + R
    )

    with requests.Session() as session:

        session.headers.update(headers)

        while (
            urls_to_visit
            and len(visited_urls) < page_limit
        ):

            url = urls_to_visit.popleft()

            if url in visited_urls:
                continue

            visited_urls.add(url)

            print(
                G
                + f"[{len(visited_urls)}/{page_limit}] "
                + "Checking "
                + R
                + url
            )

            try:

                response = session.get(
                    url,
                    timeout=10
                )

                response.raise_for_status()

                content_type = (
                    response.headers
                    .get("Content-Type", "")
                    .lower()
                )

                if "text/html" not in content_type:

                    print(
                        D
                        + "[!] Skipping non-HTML page."
                        + R
                    )

                    continue

            except requests.RequestException as error:

                print(
                    RED
                    + "[!] Skipping page: "
                    + str(error)
                    + R
                )

                continue

            emails.update(
                EMAIL_PATTERN.findall(
                    response.text
                )
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            for anchor in soup.find_all(
                "a",
                href=True
            ):

                link = urldefrag(
                    urljoin(
                        url,
                        anchor["href"].strip()
                    )
                )[0]

                parsed_link = urlsplit(link)

                if (
                    parsed_link.scheme
                    in {"http", "https"}

                    and parsed_link.hostname

                    and parsed_link.hostname.lower()
                    == allowed_host

                    and link not in queued_urls

                    and link not in visited_urls
                ):

                    urls_to_visit.append(link)
                    queued_urls.add(link)

            time.sleep(0.5)

    # ==================== RESULTS ====================

    print(
        G + "\n[+] CRAWLING COMPLETED" + R
    )

    print(
        D + "Pages checked : " + R
        + str(len(visited_urls))
    )

    print(
        D + "Emails found  : " + R
        + str(len(emails))
    )

    if emails:

        print(
            G + "\n[+] EMAILS FOUND\n" + R
        )

        for email in sorted(
            emails,
            key=str.lower
        ):

            print(
                D + "[+] " + R + email
            )

    else:

        print(
            RED
            + "\n[!] Tidak ada email ditemukan."
            + R
        )

    # ==================== SAVE TXT ====================

    try:

        txt_file = save_txt_report(
            allowed_host,
            emails,
            len(visited_urls)
        )

        print(
            G + "\n[+] RESULTS SAVED" + R
        )

        print(
            D + "TXT : " + R + txt_file
        )

        print(
            G
            + "[+] REPORT APPENDED SUCCESSFULLY"
            + R
        )

    except OSError as error:

        print(
            RED
            + "\n[!] Gagal menyimpan hasil: "
            + str(error)
            + R
        )

    input(
        "\nTekan Enter untuk kembali..."
    )


# ==================== MAIN MENU ====================

def main_menu():

    while True:

        clear()

        print(G + """

╔══════════════════════════════════╗
║          JARDECODER </>          ║
║          SYSTEM TERMINAL         ║
╠══════════════════════════════════╣
║ [1] Email Scraper                ║
║ [0] Exit                         ║
╚══════════════════════════════════╝

""" + R)

        choice = input(
            G + "JARDECODER >> " + R
        ).strip()

        if choice == "1":

            email_scraper()

        elif choice == "0":

            break

        else:

            print(
                RED
                + "\n[!] Pilihan tidak valid!"
                + R
            )

            time.sleep(1)


# ==================== GOODBYE ====================

def goodbye():

    print(G + r"""
███████╗ █████╗ ███╗   ███╗██████╗  █████╗ ██╗
██╔════╝██╔══██╗████╗ ████║██╔══██╗██╔══██╗██║
███████║███████║██╔████╔██║██████╔╝███████║██║
╚════██║██╔══██╗██║╚██╔╝██║██╔═══╝ ██╔══██╗██║
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


# ==================== START PROGRAM ====================

if __name__ == "__main__":

    try:

        glitch_intro()
        main_menu()

    except KeyboardInterrupt:

        pass

    finally:

        goodbye()
