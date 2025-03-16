
# Class to create a new Palindrome object
class Palindrome:
    # Constructor
    def __init__(self, text, language):
        self.text = text
        self.language = language

    def get(self):
        print(f"Palindrome {self.text} has been successfully added")
        return f"Palindrome {self.text} has been successfully added"

    def covert_to_dict(self):
        return {
            "text": self.text,
            "language": self.language
        }
