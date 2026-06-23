def calculateInsurance(grossSalary):
    """
    Tính số tiền bảo hiểm phải đóng từ lương gross.
    8% BHXH + 1.5% BHYT + 1% BHTN, tổng 10.5%. Chặn trần tại 46,800,000 VNĐ.
    """
    CAP = 46800000
    RATE = 0.105

    if not isinstance(grossSalary, (int, float)) or isinstance(grossSalary, bool):
        raise ValueError("grossSalary phải là số (int hoặc float).")
    if grossSalary < 0:
        raise ValueError("grossSalary không được là số âm.")
    if grossSalary == 0:
        return 0
    base_salary = min(grossSalary, CAP)
    insurance = base_salary * RATE
    return int(round(insurance))


def calculateReductions(dependents):
    """
    Tính giảm trừ gia cảnh: bản thân 11tr, mỗi người phụ thuộc 4.4tr.
    """
    BASE_SELF = 11_000_000
    BASE_DEP = 4_400_000

    if not isinstance(dependents, int):
        raise ValueError("Số người phụ thuộc phải là số nguyên (int).")
    if dependents < 0:
        raise ValueError("Số người phụ thuộc không được là số âm.")

    return BASE_SELF + dependents * BASE_DEP


def calculatePersonalTax(grossSalary, dependents):
    """
    Tính thuế TNCN dựa trên bảng thuế lũy tiến từng phần gồm 7 bậc, kiểu Việt Nam.
    Trả về số tiền thuế thu nhập cá nhân phải đóng (làm tròn int).
    """
    # Biểu thuế (từng phần): [(giới hạn, suất thuế), ...] các mức là giới hạn trên của từng bậc
    BRACKETS = [
        (5_000_000, 0.05),
        (10_000_000, 0.10),
        (18_000_000, 0.15),
        (32_000_000, 0.20),
        (52_000_000, 0.25),
        (80_000_000, 0.30),
        (float('inf'), 0.35)
    ]

    # Kiểm tra đầu vào
    if not isinstance(grossSalary, (int, float)) or isinstance(grossSalary, bool):
        raise ValueError("grossSalary phải là số (int hoặc float).")
    if not isinstance(dependents, int):
        raise ValueError("dependents phải là số nguyên (int).")
    if grossSalary < 0:
        raise ValueError("grossSalary không được là số âm.")
    if dependents < 0:
        raise ValueError("dependents không được là số âm.")

    # Bước 1: Tính các khoản giảm trừ & bảo hiểm
    insurance = calculateInsurance(grossSalary)
    reductions = calculateReductions(dependents)

    # Bước 2: Thu nhập tính thuế
    taxable_income = grossSalary - insurance - reductions

    if taxable_income <= 0:
        return 0

    # Bước 3: Tính thuế theo lũy tiến từng phần
    tax = 0.0
    remaining = taxable_income
    lower = 0

    for upper, rate in BRACKETS:
        amount = min(remaining, upper - lower)
        if amount > 0:
            tax += amount * rate
            remaining -= amount
        lower = upper
        if remaining <= 0:
            break

    return int(round(tax))