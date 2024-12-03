# Import necessary modules
import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Payment Section", "fieldname": "payment_section", "fieldtype": "Data", "width": 200},
        {"label": "NTN", "fieldname": "ntn", "fieldtype": "Data", "width": 150},
        {"label": "Taxpayer CNIC", "fieldname": "cnic", "fieldtype": "Data", "width": 150},
        {"label": "Taxpayer Name", "fieldname": "first_name", "fieldtype": "Data", "width": 200},
        {"label": "Taxpayer City", "fieldname": "city", "fieldtype": "Data", "width": 150},
        {"label": "Taxpayer Address", "fieldname": "current_address", "fieldtype": "Data", "width": 150},
        {"label": "Taxpayer Status", "fieldname": "status", "fieldtype": "Data", "width": 150},
        {"label": "Taxpayer Business Name", "fieldname": "status", "fieldtype": "Data", "width": 150},
        {"label": "Taxable Amount (PKR)", "fieldname": "taxable_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Tax Amount (PKR)", "fieldname": "tax_amount", "fieldtype": "Currency", "width": 150}
    ]

def get_data(filters):
    # Fetch raw data
    raw_data = frappe.db.sql("""
        SELECT
            emp.ntn AS ntn,
            emp.cnic AS cnic,
            emp.first_name AS first_name,
            emp.city AS city,
            emp.current_address AS current_address,
            emp.status AS status,
            ss.company AS company,
            ss.name AS salary_slip_name  -- Fetch Salary Slip name for child table joins
        FROM
            `tabSalary Slip` ss
        LEFT JOIN
            `tabEmployee` emp ON ss.employee = emp.name
    """, as_dict=1)
    
    data = []
    for row in raw_data:
        # Determine Payment Section
        if row.get("company") == "Vurke Inc. UAT":
            row["payment_section"] = "Salary of Other Employees u/s 149"
        else:
            row["payment_section"] = "Unknown Section"

        # Fetch Taxable Amount (Basic Amount) from Earnings table
        taxable_amount = frappe.db.get_value(
            "Salary Detail", 
            {"parent": row["salary_slip_name"], "parentfield": "earnings", "salary_component": "Basic"}, 
            "amount"
        )
        row["taxable_amount"] = taxable_amount or 0.0

        # Fetch Tax Amount (Income Tax Deduction) from Deductions table
        tax_amount = frappe.db.get_value(
            "Salary Detail", 
            {"parent": row["salary_slip_name"], "parentfield": "deductions", "salary_component": "Income Tax Deduction"}, 
            "amount"
        )
        row["tax_amount"] = tax_amount or 0.0

        data.append(row)

    return data
