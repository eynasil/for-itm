# Anasel-Ace M. Cañeso, 221473
# 07 March 2024
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

"""
I hereby attest to the truth of the following facts:

I have not discussed the Python code in my program with anyone other than my instructor or the teaching assistants assigned to this course.

I have not used Python code obtained from another student, or any other unauthorized source, whether modified or unmodified.

If any Python code or documentation used in my program was obtained from another source, it has been clearly noted with citations in the comments of my program.
"""
