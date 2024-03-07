# Python: Basic

def savings(gross_pay, tax_rate, expenses):
    import math
    after_tax_pay = math.floor(gross_pay - (gross_pay * tax_rate))
    return after_tax_pay - expenses

def material_waste(total_material, material_units, num_jobs, job_consumption):
    total_consumed = num_jobs * job_consumption
    return str(total_material - total_consumed) + material_units

def interest(principal, rate, periods):
    import math
    simple_interest = principal * rate * periods
    return math.floor(principal + simple_interest)
