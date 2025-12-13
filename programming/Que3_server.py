import socket
import sqlite3
import json
import datetime


def init_db():
    """Create SQLite database and table if not exists."""
    conn = sqlite3.connect("dbs_admissions.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            qualifications TEXT NOT NULL,
            course TEXT NOT NULL,
            start_year INTEGER NOT NULL,
            start_month INTEGER NOT NULL,
            registration_number TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def generate_reg_number(row_id: int) -> str:
    """Create unique registration no - ex:DBS-2025-000001."""
    year = datetime.datetime.now().year
    return f"DBS-{year}-{row_id:06d}"


def save_application(data: dict) -> str:
    """Connect to DB"""
    conn = sqlite3.connect("dbs_admissions.db")
    cursor = conn.cursor()

    # Insert with temporary registration_number to get row id
    cursor.execute("""
        INSERT INTO applications
        (name, address, qualifications, course, start_year, start_month, registration_number, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["address"],
        data["qualifications"],
        data["course"],
        data["start_year"],
        data["start_month"],
        "TEMP",  # placeholder
        datetime.datetime.now().isoformat()
    ))

    row_id = cursor.lastrowid
    reg_no = generate_reg_number(row_id)

    cursor.execute("""
        UPDATE applications
        SET registration_number = ?
        WHERE id = ?
    """, (reg_no, row_id))

    conn.commit()
    conn.close()
    return reg_no


VALID_COURSES = {
    "MSc in Cyber Security",
    "MSc Information Systems & Computing",
    "MSc Data Analytics"
}


def validate_application(data: dict):
    """Validate data"""
    required = ["name", "address", "qualifications", "course", "start_year", "start_month"]

    for field in required:
        if field not in data:
            return False, f"Missing field: {field}"
        if isinstance(data[field], str) and not data[field].strip():
            return False, f"Field '{field}' cannot be empty."

    if data["course"] not in VALID_COURSES:
        return False, "Invalid course selected."

    # Year Validation
    try:
        year = int(data["start_year"])
        if year < 2020 or year > 2100:
            return False, "Invalid start year."
        data["start_year"] = year
    except ValueError:
        return False, "Start year must be a number."

    # Month Validation
    try:
        month = int(data["start_month"])
        if month < 1 or month > 12:
            return False, "Start month must be between 1 and 12."
        data["start_month"] = month
    except ValueError:
        return False, "Start month must be a number."

    return True, None


def DBS_Server():
    sock = None
    conn = None
    try:
        init_db()
        print("Database initialised (dbs_admissions.db).")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # connection-oriented
        host = '127.0.0.1'
        port = 9999

        print(sock)
        sock.bind((host, port))
        print("\nServer is ready.....")
        sock.listen()
        print("\nServer is listening......")
        sock.settimeout(100)   # max 100 seconds for a connection timeout from client

        conn, addr = sock.accept()
        print("Received connection request from client ", addr)

        # Receive data from client
        raw = conn.recv(4096)
        if not raw:
            print("No data received from client.")
            return

        text = raw.decode()
        print("Raw data from client:", text)

        # Try to parse JSON
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            error_msg = {"status": "error", "message": "Invalid JSON format."}
            conn.sendall(json.dumps(error_msg).encode())
            return

        # Validate data
        is_valid, error_message = validate_application(data)
        if not is_valid:
            error_msg = {"status": "error", "message": error_message}
            conn.sendall(json.dumps(error_msg).encode())
            return

        # Save and generate registration number
        reg_no = save_application(data)
        print("Application saved with registration number:", reg_no)

        # Send success response
        response = {
            "status": "ok",
            "registration_number": reg_no
        }
        conn.sendall(json.dumps(response).encode())

    except TimeoutError:
        print("Server stopped running (timeout, no client connected).")
    except Exception as e:
        print("Server error:")
        print(e)
        try:
            if conn:
                error_msg = {"status": "error", "message": "Server internal error."}
                conn.sendall(json.dumps(error_msg).encode())
        except:
            pass
    finally:
        if conn:
            conn.close()
        if sock:
            sock.close()


if __name__ == "__main__":
    DBS_Server()
