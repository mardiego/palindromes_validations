from app.util import is_palindrome  # Import your function


def test_is_palindrome():
    assert is_palindrome("racecar") is True
    assert is_palindrome("Able was I ere I saw Elba") is True
    assert is_palindrome("A man, a plan, a canal, Panama!") is True
    assert is_palindrome("Dabale arroz a la zorra el abad") is True
    assert is_palindrome("12321") is True
    assert is_palindrome("Welcome to palindrome tester") is False