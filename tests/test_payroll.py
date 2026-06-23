import pytest
from src.payroll_engine import calculateInsurance, calculateReductions, calculatePersonalTax

# ====== INSURANCE TESTS (REQ_01 & REQ_02) ======

def test_TC_INS_01():
    # Lương gross dưới trần, kiểm tra tỷ lệ 10.5%
    gross = 10_000_000
    expected = round(gross * 0.105)
    assert calculateInsurance(gross) == pytest.approx(expected)

def test_TC_INS_02():
    # Lương gross nhỏ hơn trần, kiểm tra tỷ lệ 10.5%
    gross = 5_500_000
    expected = round(gross * 0.105)
    assert calculateInsurance(gross) == pytest.approx(expected)

def test_TC_INS_03():
    # Lương gross đúng bằng trần, kiểm tra chặn trần 46,800,000
    gross = 46_800_000
    expected = round(46_800_000 * 0.105)
    assert calculateInsurance(gross) == pytest.approx(expected)

def test_TC_INS_04():
    # Lương gross vượt trần, kiểm tra vẫn chặn tại 46,800,000
    gross = 70_000_000
    expected = round(46_800_000 * 0.105)
    assert calculateInsurance(gross) == pytest.approx(expected)


# ====== REDUCTIONS TESTS (REQ_03) ======

def test_TC_RED_01():
    # 0 người phụ thuộc, chỉ giảm trừ bản thân
    dependents = 0
    expected = 11_000_000
    assert calculateReductions(dependents) == expected

def test_TC_RED_02():
    # 3 người phụ thuộc (Luật cũ/Yêu cầu: 4.4tr/người)
    dependents = 3
    expected = 11_000_000 + 3 * 4_400_000
    assert calculateReductions(dependents) == expected


# ====== TAX BRACKETS TESTS (REQ_04) ======

def test_TC_TAX_01():
    # Thu nhập tính thuế <= 0: không phát sinh thuế
    gross = 15_000_000
    dependents = 1_000  # Giảm trừ vượt gross
    assert calculatePersonalTax(gross, dependents) == 0

def test_TC_TAX_02():
    # Vừa hết bậc 1: Thu nhập tính thuế tròn đúng 5,000,000
    gross = 17_877_095
    # BH = 1,877,095; Giảm trừ = 11,000,000 -> TNTT = 5,000,000
    # Thuế = 5,000,000 * 5% = 250,000
    assert calculatePersonalTax(gross, 0) == pytest.approx(250000)

def test_TC_TAX_03():
    # Đại diện bậc 1: Thu nhập tính thuế tròn đúng 2,000,000
    gross = 14_525_140
    # BH = 1,525,140; Giảm trừ = 11,000,000 -> TNTT = 2,000,000
    # Thuế = 2,000,000 * 5% = 100,000
    assert calculatePersonalTax(gross, 0) == pytest.approx(100000)

def test_TC_TAX_04():
    # Chạm ranh bậc 2: Thu nhập tính thuế tròn đúng 10,000,000
    gross = 23_463_687
    # BH = 2,463,687; Giảm trừ = 11,000,000 -> TNTT = 10,000,000
    # Thuế = (5tr * 5%) + (5tr * 10%) = 750,000
    assert calculatePersonalTax(gross, 0) == pytest.approx(750000)

def test_TC_TAX_05():
    # Đại diện bậc 2: Thu nhập tính thuế tròn đúng 8,000,000
    gross = 21_229_050
    # BH = 2,229,050; Giảm trừ = 11,000,000 -> TNTT = 8,000,000
    # Thuế = (5tr * 5%) + (3tr * 10%) = 550,000
    assert calculatePersonalTax(gross, 0) == pytest.approx(550000)

def test_TC_TAX_06():
    # Chạm ranh bậc 3: Thu nhập tính thuế tròn đúng 18,000,000
    gross = 32_402_235
    # BH = 3,402,235; Giảm trừ = 11,000,000 -> TNTT = 18,000,000
    # Thuế = 250k + 500k + (8tr * 15%) = 1,950,000
    assert calculatePersonalTax(gross, 0) == pytest.approx(1950000)

def test_TC_TAX_07():
    # Đại diện bậc 3: Thu nhập tính thuế tròn đúng 15,000,000
    gross = 29_050_279
    # BH = 3,050,279; Giảm trừ = 11,000,000 -> TNTT = 15,000,000
    # Thuế = 250k + 500k + (5tr * 15%) = 1,500,000
    assert calculatePersonalTax(gross, 0) == pytest.approx(1500000)

def test_TC_TAX_08():
    # Chạm ranh bậc 4: Thu nhập tính thuế tròn đúng 32,000,000 (Gross vượt trần đóng BH)
    gross = 47_914_000
    # BH chặn trần = 4,914,000; Giảm trừ = 11,000,000 -> TNTT = 32,000,000
    # Thuế = 250k + 500k + 1.2tr + (14tr * 20%) = 4,750,000
    assert calculatePersonalTax(gross, 0) == pytest.approx(4750000)

def test_TC_TAX_09():
    # Đại diện bậc 4: Thu nhập tính thuế tròn đúng 40,000,000
    gross = 55_914_000
    # BH = 4,914,000; Giảm trừ = 11,000,000 -> TNTT = 40,000,000
    # Thuế = 250k + 500k + 1.2tr + 2.8tr + (8tr * 25%) = 6,750,000
    assert calculatePersonalTax(gross, 0) == pytest.approx(6750000)

def test_TC_TAX_10():
    # Chạm ranh bậc 5: Thu nhập tính thuế tròn đúng 52,000,000
    gross = 67_914_000
    # BH = 4,914,000; Giảm trừ = 11,000,000 -> TNTT = 52,000,000
    assert calculatePersonalTax(gross, 0) == pytest.approx(9750000)

def test_TC_TAX_11():
    # Đại diện bậc 5: Thu nhập tính thuế tròn đúng 60,000,000
    gross = 75_914_000
    # BH = 4,914,000; Giảm trừ = 11,000,000 -> TNTT = 60,000,000
    assert calculatePersonalTax(gross, 0) == pytest.approx(12150000)

def test_TC_TAX_12():
    # Chạm ranh bậc 6: Thu nhập tính thuế tròn đúng 80,000,000
    gross = 95_914_000
    # BH = 4,914,000; Giảm trừ = 11,000,000 -> TNTT = 80,000,000
    assert calculatePersonalTax(gross, 0) == pytest.approx(18150000)

def test_TC_TAX_13():
    # Đại diện bậc 6: Thu nhập tính thuế tròn đúng 90,000,000
    gross = 105_914_000
    # BH = 4,914,000; Giảm trừ = 11,000,000 -> TNTT = 90,000,000
    assert calculatePersonalTax(gross, 0) == pytest.approx(21650000)

def test_TC_TAX_14():
    # Đại diện bậc 7: Thu nhập tính thuế tròn đúng 140,000,000
    gross = 155_914_000
    # BH = 4,914,000; Giảm trừ = 11,000,000 -> TNTT = 140,000,000
    assert calculatePersonalTax(gross, 0) == pytest.approx(39150000)


# ====== EXCEPTION TESTS (REQ_05) ======

def test_TC_EXC_01():
    # Lương âm gây lỗi
    with pytest.raises(ValueError):
        calculatePersonalTax(-10000000, 0)

def test_TC_EXC_02():
    # Người phụ thuộc âm gây lỗi
    with pytest.raises(ValueError):
        calculateReductions(-1)