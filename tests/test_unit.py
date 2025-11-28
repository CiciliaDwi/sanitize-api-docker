from app.main import sanitize

def test_multiple_words():
    assert sanitize("Kotor itu jorok", ["kotor", "jorok"]) == "K***r itu j***k"

def test_substring_replaced_too():
    assert sanitize("main kotor-kotoran", ["kotor"]) == "main k***r-k***ran"
