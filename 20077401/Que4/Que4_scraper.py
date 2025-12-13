import csv
from bs4 import BeautifulSoup

SEASON_START = "20 December"
SEASON_END = "30 December"
CSV_FILENAME = "hotel_prices.csv"

# Two "webpages" = two local HTML files
HOTEL_FILES = [
    {"hotel_name": "Hotel Castle House", "file_path": "hotel1.html"},
    {"hotel_name": "Hotel Aungier Street", "file_path": "hotel2.html"},
]


def scrape_hotel_file(hotel_name, file_path):
    """
    Scrape one local HTML file and return a list of room records.
    """
    print(f"\n[INFO] Scraping hotel: {hotel_name}")
    print(f"       File: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
        return []

    soup = BeautifulSoup(html, "html.parser")

    # Each room block is a div.room-card
    room_cards = soup.select("div.room-card")
    records = []

    for card in room_cards:
        name_tag = card.select_one("span.room-name")
        price_tag = card.select_one("span.room-price")
        cap_tag = card.select_one("span.room-capacity")

        room_name = name_tag.get_text(strip=True) if name_tag else "N/A"
        price = price_tag.get_text(strip=True) if price_tag else "N/A"
        capacity = cap_tag.get_text(strip=True) if cap_tag else "N/A"

        record = {
            "hotel_name": hotel_name,
            "room_name": room_name,
            "price_per_night": price,
            "capacity": capacity,
            "season_start": SEASON_START,
            "season_end": SEASON_END,
            "source_file": file_path,
        }

        records.append(record)

    print(f"[INFO] Found {len(records)} rooms for {hotel_name}")
    return records


def write_to_csv(filename, records):
    """
    Store all scraped data in a CSV file.
    """
    if not records:
        print("[WARN] No records to write.")
        return

    fieldnames = list(records[0].keys())

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"\n[INFO] Wrote {len(records)} rows to CSV: {filename}")


def read_and_display_csv(filename):
    """
    Read all data from CSV and print to terminal.
    """
    print(f"\n[INFO] Reading data back from CSV: {filename}\n")

    try:
        with open(filename, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except FileNotFoundError:
        print("[ERROR] CSV file not found.")
        return

    if not rows:
        print("[WARN] CSV file is empty.")
        return

    for i, row in enumerate(rows, start=1):
        print(f"--- Room #{i} ---")
        print(f"Hotel Name      : {row['hotel_name']}")
        print(f"Room Name       : {row['room_name']}")
        print(f"Price per Night : {row['price_per_night']}")
        print(f"Capacity        : {row['capacity']}")
        print(f"Season Start    : {row['season_start']}")
        print(f"Season End      : {row['season_end']}")
        print(f"Source File     : {row['source_file']}")
        print()


def main():
    all_rooms = []

    for hotel in HOTEL_FILES:
        rooms = scrape_hotel_file(hotel["hotel_name"], hotel["file_path"])
        all_rooms.extend(rooms)

    print(f"\n[INFO] Total rooms collected: {len(all_rooms)}")
    if len(all_rooms) < 10:
        print("[WARN] Less than 10 rooms found. Add more rooms if needed.")

    write_to_csv(CSV_FILENAME, all_rooms)
    read_and_display_csv(CSV_FILENAME)


if __name__ == "__main__":
    main()
