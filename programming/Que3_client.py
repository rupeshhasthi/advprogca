import socket
import json

# Collect Applicant Information
def collect_applicant_info():
    print("=== DBS Admission Application ===")
    name = input("Full Name: ").strip()
    address = input("Address: ").strip()
    qualifications = input("Educational Qualifications: ").strip()

    print("\nAvailable Courses:")
    print("  1. MSc in Cyber Security")
    print("  2. MSc Information Systems & Computing")
    print("  3. MSc Data Analytics")

    course_map = {
        "1": "MSc in Cyber Security",
        "2": "MSc Information Systems & Computing",
        "3": "MSc Data Analytics"
    }

    course = ""
    while True:
        choice = input("Enter course number (1-3): ").strip()
        if choice in course_map:
            course = course_map[choice]
            break
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")

    while True:
        start_year = input("Intended start year (e.g. 2025): ").strip()
        if start_year.isdigit():
            break
        else:
            print("Start year must contain only digits.")

    while True:
        start_month = input("Intended start month (1-12): ").strip()
        if start_month.isdigit():
            m = int(start_month)
            if 1 <= m <= 12:
                break
            else:
                print("Month must be between 1 and 12.")
        else:
            print("Start month must contain only digits.")

    return {
        "name": name,
        "address": address,
        "qualifications": qualifications,
        "course": course,
        "start_year": start_year,
        "start_month": start_month
    }


def DBS_Client():
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '127.0.0.1'
        port = 9999

        print("Client requesting connection to the server....")
        sock.connect((host, port))
        print("Connected to server.")

        # Collect data from user
        app_data = collect_applicant_info()
        json_data = json.dumps(app_data)

        # Send data to server
        sock.sendall(json_data.encode())
        print("\nApplication sent to server. Waiting for response...")

        # Receive response from server
        response = sock.recv(4096)
        if not response:
            print("No response received from server.")
            return

        response_text = response.decode()
        print("Raw response from server:", response_text)

        # Parse server response
        try:
            resp = json.loads(response_text)
        except json.JSONDecodeError:
            print("Server returned invalid data.")
            return

        if resp.get("status") == "ok":
            reg_no = resp.get("registration_number")
            print("\n=== Application Successful ===")
            print("Your unique DBS registration number is:", reg_no)
            print("Please keep this number for all future correspondence.")
        else:
            print("\n=== Application Failed ===")
            print("Reason:", resp.get("message", "Unknown error."))

    except ConnectionAbortedError:
        print("Connection is aborted...")
    except ConnectionRefusedError:
        print("Server refused to connect...")
    except ConnectionError:
        print("Connection error....")
    except Exception as e:
        print("Error.....")
        print(e)
    finally:
        if sock:
            sock.close()


if __name__ == "__main__":
    DBS_Client()
