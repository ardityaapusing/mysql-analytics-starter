from scripts.utils import is_valid_phone, normalize_phone

def test_valid_phone():
    assert is_valid_phone("0812345678")
    assert is_valid_phone("+62812345678")
    assert not is_valid_phone("123")           # too short
    assert not is_valid_phone("08-12-34-56")   # dashes not allowed

def test_normalize_phone():
    assert normalize_phone(" 812345678 ") == "0812345678"
    assert normalize_phone("+62812345678") == "+62812345678"