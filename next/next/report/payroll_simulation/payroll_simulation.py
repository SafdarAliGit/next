import frappe

def execute(filters=None):
    # Define columns
    columns = [
        {"label": "Date of Joining", "fieldname": "date_of_joining", "fieldtype": "Date", "width": 120},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 150},
        {"label": "Designation", "fieldname": "designation", "fieldtype": "Data", "width": 150},
        {"label": "City", "fieldname": "city", "fieldtype": "Data", "width": 120},
        {"label": "Base Salary", "fieldname": "base_salary", "fieldtype": "Currency", "width": 120},
        {"label": "Allowances", "fieldname": "allowances", "fieldtype": "Currency", "width": 120},
        {"label": "Gross Pay", "fieldname": "gross_pay", "fieldtype": "Currency", "width": 120},
        {"label": "Income Tax", "fieldname": "income_tax", "fieldtype": "Currency", "width": 120},
        {"label": "Employee Deductions", "fieldname": "employee_deductions", "fieldtype": "Currency", "width": 150},
        {"label": "Net Salary", "fieldname": "net_salary", "fieldtype": "Currency", "width": 120},
        {"label": "Bank Account No", "fieldname": "bank_account_no", "fieldtype": "Data", "width": 150},
        {"label": "Bank Name", "fieldname": "bank_name", "fieldtype": "Data", "width": 150},
        {"label": "CTC", "fieldname": "ctc", "fieldtype": "Currency", "width": 120},
        {"label": "Custom Leave Balance", "fieldname": "custom_leave_balance", "fieldtype": "Int", "width": 150},
    ]

    # Fetch data
    data = fetch_salary_data(filters)

    return columns, data


def fetch_salary_data(filters):
    query = """
        SELECT
            e.date_of_joining,
            ss.employee_name,
            e.designation,
            e.city,
            SUM(CASE WHEN sd.parentfield = 'earnings' AND sd.salary_component = 'Basic' THEN sd.amount ELSE 0 END) AS base_salary,
            SUM(CASE WHEN sd.parentfield = 'earnings' AND sd.salary_component != 'Basic' THEN sd.amount ELSE 0 END) AS allowances,
            ss.gross_pay,
            SUM(CASE WHEN sd.parentfield = 'deductions' THEN sd.amount ELSE 0 END) AS employee_deductions,
            ss.net_pay AS net_salary,
            ss.current_month_income_tax AS income_tax,
            ss.bank_account_no,
            ss.bank_name,
            ss.ctc,
            e.custom_leave_balance
        FROM
            `tabSalary Slip` ss
        LEFT JOIN
            `tabEmployee` e ON ss.employee = e.name
        LEFT JOIN
            `tabSalary Detail` sd ON sd.parent = ss.name
    """

    if filters.get("from_date") and filters.get("to_date"):
        query += " AND ss.start_date >= %(from_date)s AND ss.end_date <= %(to_date)s"

    query += " GROUP BY ss.name"

    return frappe.db.sql(query, filters, as_dict=True)
