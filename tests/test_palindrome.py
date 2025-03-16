from app.palindrome import Palindrome


def test_palindrome_creation():
    p = Palindrome("A man, a plan, a canal, Panama!", "English")
    assert p.text == "A man, a plan, a canal, Panama!"
    assert p.language == "English"


def test_palindrome_get():
    p = Palindrome("racecar", "English")
    result = p.get()
    assert result == "Palindrome racecar has been successfully added"