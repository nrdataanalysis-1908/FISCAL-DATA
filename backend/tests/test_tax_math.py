from decimal import Decimal, ROUND_HALF_UP


def test_illustrative_tax_math():
    taxable_base = Decimal("1000.00")
    rate_percent = Decimal("5.00")
    result = (taxable_base * rate_percent / Decimal("100")).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    assert result == Decimal("50.00")


def test_dre_example_arithmetic():
    gross_revenue = Decimal("150000.00")
    sales_deductions = Decimal("18000.00")
    cogs = Decimal("55000.00")
    operating_expenses = Decimal("32000.00")
    financial_result = Decimal("5000.00")
    income_tax = Decimal("8000.00")

    net_income = (
        gross_revenue - sales_deductions - cogs
        - operating_expenses - financial_result - income_tax
    )
    assert net_income == Decimal("32000.00")
