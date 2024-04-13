from rfid.rfid_reader import RFIDReader
from api.api_caller import send_data_to_server


def main():
    reader = RFIDReader()
    url = 'http://192.168.0.156:8000/helpfinance/api/'
    while True:
        print("\n1. Read from card")
        print("2. Write to card")
        print("3. Clear card")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            id, text = reader.read_card()
            if id and text:
                print(f"Read from card: ID={id}, Text={text}")
                try:
                    response = send_data_to_server(url, {'id': id, 'text': text})
                    print("Response from server:", response)
                except Exception as e:
                    print("An error occured:", e)
        elif choice == '2':
            text = input("Enter the text to write to the card: ")
            reader.write_card(text)
        elif choice == '3':
            reader.clear_card()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
