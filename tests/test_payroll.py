import pytest
from src.payroll_engine import (
    calculateInsurance,
    calculateReductions,
    calculatePersonalTax,
)

# ------ Insurance Function Tests ------

def test_TC_INS_01_basic_rate():
    # Lương nhỏ hơn giới hạn trần, tính đúng bảo hiểm (10.5%)
    salary = 20000000  # < 46,800,000
    expected = int(round(20000000 * 0.105))
    assert calculateInsurance(salary) == expected

def test_TC_INS_02_exact_cap():
    # Lương đúng bằng trần
    salary = 46800000
    expected = int(round(46800000 * 0.105))
    assert calculateInsurance(salary) == expected

def test_TC_INS_03_above_cap():
    # Lương vượt trần, bị chặn ở mức 46.8 triệu
    salary = 60000000
    cap = 46800000
    expected = int(round(cap * 0.105))
    assert calculateInsurance(salary) == expected

def test_TC_INS_04_zero_salary():
    # Lương = 0, bảo hiểm cũng phải = 0
    salary = 0
    expected = 0
    assert calculateInsurance(salary) == expected

# ------ Reductions Function Tests ------

def test_TC_RED_01_self_deduction_only():
    # Không có người phụ thuộc, chỉ áp dụng giảm trừ bản thân
    dependents = 0
    expected = 11000000
    assert calculateReductions(dependents) == expected

def test_TC_RED_02_with_dependents():
    # Có người phụ thuộc
    dependents = 2
    expected = 11000000 + 2 * 4400000
    assert calculateReductions(dependents) == expected

# ------ Personal Income Tax - 7 brackets, value boundary analysis ------

# Helper: gross = salary, deps = num of dependents
# Suppose no dependents for boundary test, only self deduction

def boundary_tax_input(gross):
    """Common input for boundary value, no dependents."""
    return calculatePersonalTax(gross, dependents=0)

def tax_for_gross(gross):
    return boundary_tax_input(gross)

def insurance_for_gross(gross):
    # Insurance subject to cap
    cap = 46800000
    base = gross
    return int(round(base * 0.105))

def taxable_income_for(gross):
    return gross - insurance_for_gross(gross) - 11000000

def test_TC_TAX_01_below_first_threshold():
    # Thu nhập tính thuế âm, thuế = 0
    gross = 11000000  # giảm trừ bản thân, BH xấp xỉ 1.155tr, thu nhập chịu thuế < 0
    assert tax_for_gross(gross) == 0

def test_TC_TAX_02_exact_first_threshold():
    # Thu nhập tính thuế đúng bằng 0
    gross = 11000000 + insurance_for_gross(11000000)
    # Tiền lương gross bằng đúng bảo hiểm + giảm trừ, thì thu nhập chịu thuế = 0
    assert tax_for_gross(gross) == 0

def test_TC_TAX_03_enter_second_bracket():
    # Đầu bậc 2: 5tr đầu 5%, +1đ ở phần vượt
    # Lấy lương gross sao cho taxable = 5,000,001
    tax_income = 5_000_001
    gross = tax_income + insurance_for_gross(11000000 + tax_income) + 11000000
    assert tax_for_gross(gross) == int(round(5_000_001 * 0.05))

def test_TC_TAX_04_exact_second_bracket_upper():
    # Bậc 2 vượt 5tr -> 10tr đầu bậc 2, phần 5tr đầu 5%, phần còn lại lên 10%
    # Test ở taxable_income = 10,000,000
    tax_income = 10_000_000
    gross = tax_income + insurance_for_gross(11000000 + tax_income) + 11000000
    # 5tr đầu 5%, 5tr tiếp 10%
    expected_tax = 5_000_000 * 0.05 + 5_000_000 * 0.1
    assert tax_for_gross(gross) == int(round(expected_tax))

def test_TC_TAX_05_lower_third_bracket():
    # Giá trị sát ngay dưới đầu bậc 3
    tax_income = 18_000_000 - 1
    gross = tax_income + insurance_for_gross(11000000 + tax_income) + 11000000
    # 5tr x 5%, 5tr x 10%, 7.999.999 x 15%
    expected_tax = 5_000_000 * 0.05 + 5_000_000 * 0.1 + (tax_income - 10_000_000) * 0.15
    assert tax_for_gross(gross) == int(round(expected_tax))

def test_TC_TAX_06_exact_third_bracket():
    # Đúng sát đầu bậc 4
    tax_income = 18_000_000
    gross = tax_income + insurance_for_gross(11000000 + tax_income) + 11000000
    expected_tax = 5_000_000 * 0.05 + 5_000_000 * 0.1 + 8_000_000 * 0.15
    assert tax_for_gross(gross) == int(round(expected_tax))

def test_TC_TAX_07_lower_fourth_bracket():
    # Bậc 4: 32tr
    tax_income = 32_000_000
    gross = tax_income + insurance_for_gross(11000000 + tax_income) + 11000000
    expected_tax = (
        5_000_000 * 0.05 +
        5_000_000 * 0.1 +
        8_000_000 * 0.15 +
        14_000_000 * 0.2
    )
    assert tax_for_gross(gross) == int(round(expected_tax))

def test_TC_TAX_08_lower_fifth_bracket():
    # Bậc 5: 52tr
    tax_income = 52_000_000
    gross = tax_income + insurance_for_gross(11000000 + tax_income) + 11000000
    expected_tax = (
        5_000_000 * 0.05 +
        5_000_000 * 0.1 +
        8_000_000 * 0.15 +
        14_000_000 * 0.2 +
        20_000_000 * 0.25
    )
    assert tax_for_gross(gross) == int(round(expected_tax))

def test_TC_TAX_09_lower_sixth_bracket():
    # Bậc 6: 80tr
    tax_income = 80_000_000
    gross = tax_income + insurance_for_gross(11000000 + tax_income) + 11000000
    expected_tax = (
        5_000_000 * 0.05 +
        5_000_000 * 0.1 +
        8_000_000 * 0.15 +
        14_000_000 * 0.2 +
        28_000_000 * 0.25 +
        28_000_000 * 0.3
    )
    assert tax_for_gross(gross) == int(round(expected_tax))

def test_TC_TAX_10_lower_seventh_bracket():
    # Bậc 7: 80tr+
    tax_income = 100_000_000
    gross = tax_income + insurance_for_gross(11000000 + tax_income) + 11000000
    expected_tax = (
        5_000_000*0.05 +
        5_000_000*0.1 +
        8_000_000*0.15 +
        14_000_000*0.2 +
        28_000_000*0.25 +
        32_000_000*0.3 +
        (tax_income-80_000_000)*0.35
    )
    assert tax_for_gross(gross) == int(round(expected_tax))

def test_TC_TAX_11_exact_seventh_bracket():
    # Giá trị biên ngay đầu bậc 7
    tax_income = 80_000_000
    gross = tax_income + insurance_for_gross(11000000 + tax_income) + 11000000
    expected_tax = (
        5_000_000*0.05 +
        5_000_000*0.1 +
        8_000_000*0.15 +
        14_000_000*0.2 +
        28_000_000*0.25 +
        20_000_000*0.3
    )
    assert tax_for_gross(gross) == int(round(expected_tax))

def test_TC_TAX_12_any_dependents():
    # Có người phụ thuộc làm taxable về 0 -> tax = 0
    gross = 15_000_000
    dependents = 2  # ~ 19 triệu giảm trừ
    assert calculatePersonalTax(gross, dependents) == 0

def test_TC_TAX_13_large_salary_many_dependents():
    # Lương rất lớn nhưng nhiều người phụ thuộc làm thu nhập chịu thuế giảm mạnh
    gross = 100_000_000
    dependents = 8  # 44tr giảm trừ
    # Calculate expected tax manually if needed
    tax = calculatePersonalTax(gross, dependents)
    assert isinstance(tax, int)
    assert tax > 0

def test_TC_TAX_14_int_rounding():
    # Kiểm tra làm tròn đúng kiểu int
    gross = 30_000_000
    res = calculatePersonalTax(gross, 0)
    assert isinstance(res, int)

# ------ Exception Handling Tests ------

def test_TC_EXC_01_negative_input():
    with pytest.raises(ValueError):
        calculateInsurance(-5000000)
    with pytest.raises(ValueError):
        calculateReductions(-1)
    with pytest.raises(ValueError):
        calculatePersonalTax(-10000000, 0)
    with pytest.raises(ValueError):
        calculatePersonalTax(10000000, -2)

def test_TC_EXC_02_wrong_type_input():
    with pytest.raises(ValueError):
        calculateInsurance("abc")
    with pytest.raises(ValueError):
        calculateReductions("1")
    with pytest.raises(ValueError):
        calculatePersonalTax("salary", 0)
    with pytest.raises(ValueError):
        calculatePersonalTax(10000000, [1, 2])