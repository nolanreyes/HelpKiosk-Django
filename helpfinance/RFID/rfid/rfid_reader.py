from mfrc522 import SimpleMFRC522


class RFIDReader:
    def __init__(self):
        self.reader = SimpleMFRC522()

    def read_card(self):
        try:
            print("Place the card near the reader")
            id, text = self.reader.read()
            print("ID: ", id)
            print("Text: ", text)
            return id, text
        except Exception as e:
            print("An error occurred: ", e)
            return None, None

    def write_card(self, text):
        try:
            print("Place the card near the reader")
            self.reader.write(text)
            print("Data written to the card")
        except Exception as e:
            print("An error occurred: ", e)

    def clear_card(self):
        try:
            print("Place the card near the reader")
            self.reader.write("")  # Write an empty string to the card
            print("Card cleared")
        except Exception as e:
            print("An error occurred: ", e)
