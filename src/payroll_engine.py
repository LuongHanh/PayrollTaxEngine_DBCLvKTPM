from typing import Union

INSURANCE_CEILING = 46800000  # VNĐ
INSURANCE_BHXH_RATE = 0.08    # 8% BHXH
INSURANCE_BHYT_RATE = 0.015   # 1.5% BHYT
INSURANCE_BHTN_RATE = 0.01    # 1% BHTN

SELF_DEDUCTION = 11000000     # VNĐ
DEPENDENT_DEDUCTION = 4400000 # VNĐ per dependent

PERSONAL_TAX_BRACKETS = [
    (0,        5000000,   0.05,     0),
    (5000000,  10000000,  0.10, 250000),
    (10000000, 18000000,  0.15, 750000),
    (18000000, 32000000,  0.20, 1950000),
    (32000000, 52000000,  0.25, 4750000),
    (52000000, 80000000,  0.30, 9750000),
    (80000000, float('inf'), 0.35, 18150000)
]


def calculateInsurance(grossSalary: Union[int, float]) -> int:
    """
    Tính khoản trích đóng bảo hiểm xã hội, y tế, thất nghiệp tổng cộng, chặn trần tại 46.800.000 VNĐ.
    Trích đóng: BHXH 8%, BHYT 1.5%, BHTN 1%.
    """
    try:
        if not isinstance(grossSalary, (int, float)) or grossSalary < 0:
            raise ValueError("grossSalary phải là số không âm.")

        salary_for_insurance = min(grossSalary, INSURANCE_CEILING)
        bhxh = salary_for_insurance * INSURANCE_BHXH_RATE
        bhyt = salary_for_insurance * INSURANCE_BHYT_RATE
        bhtn = salary_for_insurance * INSURANCE_BHTN_RATE
        total = int(round(bhxh + bhyt + bhtn))
        return total
    except Exception as e:
        raise ValueError(f"Lỗi khi tính bảo hiểm: {e}")


def calculateReductions(dependents: int) -> int:
    """
    Tính tổng số tiền giảm trừ: giảm trừ bản thân + giảm trừ người phụ thuộc
    """
    try:
        if not isinstance(dependents, int) or dependents < 0:
            raise ValueError("Số người phụ thuộc phải là số nguyên không âm.")
        total_reduction = SELF_DEDUCTION + dependents * DEPENDENT_DEDUCTION
        return total_reduction
    except Exception as e:
        raise ValueError(f"Lỗi khi tính giảm trừ: {e}")


def calculatePersonalTax(grossSalary: Union[int, float], dependents: int) -> int:
    """
    Tính thuế TNCN theo lũy tiến từng phần.
    """
    try:
        if not isinstance(grossSalary, (int, float)) or grossSalary < 0:
            raise ValueError("grossSalary phải là số không âm.")
        if not isinstance(dependents, int) or dependents < 0:
            raise ValueError("Số người phụ thuộc phải là số nguyên không âm.")

        # Tính các khoản giảm trừ
        insurance = calculateInsurance(grossSalary)
        reductions = calculateReductions(dependents)

        # Thu nhập tính thuế = Lương gross - bảo hiểm - giảm trừ bản thân và người phụ thuộc
        taxable_income = grossSalary - insurance - reductions
        if taxable_income <= 0:
            return 0

        tax = 0
        remaining = taxable_income
        for lower, upper, rate, deduction in PERSONAL_TAX_BRACKETS:
            if taxable_income > lower:
                income_in_bracket = min(remaining, upper - lower)
                if income_in_bracket <= 0:
                    continue
                tax_in_bracket = income_in_bracket * rate
                tax += tax_in_bracket
                remaining -= income_in_bracket
                if remaining <= 0:
                    break
        return int(round(tax))
    except Exception as e:
        raise ValueError(f"Lỗi khi tính thuế thu nhập cá nhân: {e}")