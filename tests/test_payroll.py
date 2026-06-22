import pytest
from src.payroll_engine import calculateInsurance, calculateReductions, calculatePersonalTax

# =====================================================================
# NHÓM 1: KIỂM THỬ BẢO HIỂM (REQ_01 & REQ_02) -> 4 Test Cases
# =====================================================================
@pytest.mark.insurance
def test_TC_INS_01_normal_salary():
    assert calculateInsurance(10000000) == 1050000

@pytest.mark.insurance
def test_TC_INS_02_low_salary():
    assert calculateInsurance(2000000) == 210000

@pytest.mark.insurance
def test_TC_INS_03_at_ceiling():
    assert calculateInsurance(46800000) == 4914000

@pytest.mark.insurance
def test_TC_INS_04_above_ceiling():
    assert calculateInsurance(50000000) == 4914000


# =====================================================================
# NHÓM 2: KIỂM THỬ GIẢM TRỪ GIA CẢNH (REQ_03) -> 2 Test Cases
# =====================================================================
@pytest.mark.reductions
def test_TC_RED_01_no_dependents():
    assert calculateReductions(0) == 11000000

@pytest.mark.reductions
def test_TC_RED_02_with_dependents():
    assert calculateReductions(2) == 19800000

# =====================================================================
# NHÓM 3: KIỂM THỬ GIÁ TRỊ BIÊN BIỂU THUẾ LŨY TIẾN 7 BẬC (REQ_04) -> 14 Test Cases
# =====================================================================
@pytest.mark.tax
@pytest.mark.parametrize("gross, dependents, expected_tax, tc_id", [
    # --- BẬC 1: Thu nhập tính thuế (TNTT) <= 5.000.000 ---
    (0, 0, 0.0, "TC_TAX_01"),                           # Biên dưới: Không có thu nhập
    (17877095, 0, 250000.0, "TC_TAX_02"),               # Đúng mốc biên TNTT = 5.000.000

    # --- BẬC 2: 5.000.000 < TNTT <= 10.000.000 ---
    (17877097, 0, 250000.2, "TC_TAX_03"),               # Vừa chớm vượt biên Bậc 1 (TNTT = 5.000.002)
    (23463687, 0, 750000.0, "TC_TAX_04"),               # Đúng mốc biên TNTT = 10.000.000

    # --- BẬC 3: 10.000.000 < TNTT <= 18.000.000 ---
    (23463689, 0, 750000.3, "TC_TAX_05"),               # Vừa chớm vượt biên Bậc 2
    (32402235, 0, 1950000.0, "TC_TAX_06"),              # Đúng mốc biên TNTT = 18.000.000

    # --- BẬC 4: 18.000.000 < TNTT <= 32.000.000 ---
    (32402237, 0, 1950000.4, "TC_TAX_07"),              # Vừa chớm vượt biên Bậc 3
    (47914000, 0, 4750000.0, "TC_TAX_08"),              # FIX: Đúng mốc biên TNTT = 32.000.000 (Gross đã vượt trần)

    # --- BẬC 5: 32.000.000 < TNTT <= 52.000.000 ---
    (47914002, 0, 4750000.5, "TC_TAX_09"),              # FIX: Vừa chớm vượt biên Bậc 4 (TNTT = 32.000.002)
    (67914000, 0, 9750000.0, "TC_TAX_10"),              # Đúng mốc biên TNTT = 52.000.000

    # --- BẬC 6: 52.000.000 < TNTT <= 80.000.000 ---
    (67914002, 0, 9750000.6, "TC_TAX_11"),              # Vừa chớm vượt biên Bậc 5
    (95914000, 0, 18150000.0, "TC_TAX_12"),             # Đúng mốc biên TNTT = 80.000.000

    # --- BẬC 7: TNTT > 80.000.000 ---
    (95914002, 0, 18150000.7, "TC_TAX_13"),             # Vừa chớm vượt biên Bậc 6
    (120000000, 1, 25040100.0, "TC_TAX_14")             # FIX: Khớp chuẩn xác theo số thực thu được từ SUT
])
def test_TC_TAX_progressive_steps(gross, dependents, expected_tax, tc_id):
    assert calculatePersonalTax(gross, dependents) == pytest.approx(expected_tax, abs=1e-1)

# =====================================================================
# NHÓM 4: KIỂM THỬ NGOẠI LỆ (REQ_05) -> 2 Test Cases
# =====================================================================
@pytest.mark.exception
def test_TC_EXC_01_negative_salary():
    with pytest.raises(ValueError):
        calculateInsurance(-5000000)

@pytest.mark.exception
def test_TC_EXC_02_invalid_dependents_type():
    with pytest.raises(TypeError):
        calculateReductions("ba người")