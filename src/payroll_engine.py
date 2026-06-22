def calculateInsurance(grossSalary):
    # 1. Kiểm tra ngoại lệ lương âm
    if grossSalary < 0:
        raise ValueError("Mức lương Gross không được âm.")
    
    # 2. Quy tắc chặn trần đóng bảo hiểm ở mức 46.800.000 VNĐ
    SALARY_CEILING = 46800000
    insurance_base = min(grossSalary, SALARY_CEILING)
    
    # 3. Tính các tỷ lệ trích đóng (Tổng cộng 10.5%)
    bhxh = insurance_base * 0.08
    bhyt = insurance_base * 0.015
    bhtn = insurance_base * 0.01
    
    return bhxh + bhyt + bhtn


def calculateReductions(dependents):
    # 1. Kiểm tra ngoại lệ số lượng người phụ thuộc
    if not isinstance(dependents, int) or dependents < 0:
        raise TypeError("Số lượng người phụ thuộc phải là số nguyên không âm.")
        
    # 2. Tính giảm trừ bản thân (11tr) và người phụ thuộc (4.4tr/người)
    PERSONAL_REDUCTION = 11000000
    # DEPENDENT_REDUCTION = 4400000 # Hằng số này sẽ được AI đổi thành 5.5tr ở phần sau
    DEPENDENT_REDUCTION = 5500000 # Đã cập nhật từ 4.4tr lên 5.5tr theo luật mới
    
    return PERSONAL_REDUCTION + (dependents * DEPENDENT_REDUCTION)


def calculatePersonalTax(grossSalary, dependents):
    # 1. Tính toán các khoản thành phần
    insurance = calculateInsurance(grossSalary)
    reductions = calculateReductions(dependents)
    
    # 2. Tính thu nhập tính thuế (TNTT)
    taxable_income = grossSalary - insurance - reductions
    
    # Nếu thu nhập tính thuế nhỏ hơn hoặc bằng 0 thì không phải nộp thuế
    if taxable_income <= 0:
        return 0.0
        
    # 3. Áp dụng biểu thuế lũy tiến từng phần 7 bậc của Việt Nam
    tax = 0.0
    # Các mốc biên tính thuế (triệu VNĐ) chuyển đổi sang VNĐ thực tế
    if taxable_income <= 5000000:
        tax = taxable_income * 0.05
    elif taxable_income <= 10000000:
        tax = 5000000 * 0.05 + (taxable_income - 5000000) * 0.10
    elif taxable_income <= 18000000:
        tax = 5000000 * 0.05 + 5000000 * 0.10 + (taxable_income - 10000000) * 0.15
    elif taxable_income <= 32000000:
        tax = 250000 + 500000 + 1200000 + (taxable_income - 18000000) * 0.20
    elif taxable_income <= 52000000:
        tax = 250000 + 500000 + 1200000 + 2800000 + (taxable_income - 32000000) * 0.25
    elif taxable_income <= 80000000:
        tax = 250000 + 500000 + 1200000 + 2800000 + 5000000 + (taxable_income - 52000000) * 0.30
    else:
        tax = 250000 + 500000 + 1200000 + 2800000 + 5000000 + 8400000 + (taxable_income - 80000000) * 0.35
        
    return round(tax, 2)