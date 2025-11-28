from app.main import app

def test_api_uses_app_banned_words_txt():
    client = app.test_client()
    res = client.post("/sanitize", json={"text": "Kotor itu jorok"})
    assert res.status_code == 200
    assert res.get_json()["cleaned"] == "K***r itu j***k"
