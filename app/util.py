
# Method to check if a string is a palindrome
def is_palindrome(string):
    print(f"Check if {string} is a Palindrome")
    string_cleaned = ''.join(char.lower() for char in string if char.isalnum())
    return string_cleaned == string_cleaned[::-1]