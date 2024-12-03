import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    """Define the structure and labels for the report columns."""
    return [
        {"label": _("Employee ID"), "fieldname": "employee", "fieldtype": "Data", "width": 120},
        {"label": _("Employee Name"), "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
        {"label": _("Designation"), "fieldname": "designation", "fieldtype": "Data", "width": 150},
        {"label": _("Department"), "fieldname": "department", "fieldtype": "Data", "width": 150},
        {"label": _("Date of Joining"), "fieldname": "date_of_joining", "fieldtype": "Date", "width": 120},
        {"label": _("Branch"), "fieldname": "branch", "fieldtype": "Data", "width": 150},
        {"label": _("Bank Account Number"), "fieldname": "bank_account_no", "fieldtype": "Data", "width": 200},
        {"label": _("Basic Salary"), "fieldname": "basic_salary", "fieldtype": "Currency", "width": 150},
        {"label": _("Gross Salary"), "fieldname": "gross_salary", "fieldtype": "Currency", "width": 150},
        {"label": _("Net Pay"), "fieldname": "net_pay", "fieldtype": "Currency", "width": 150},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
    ]

def get_data(filters):
    """Fetch employee and salary data based on the provided filters."""
    conditions = []
    if filters.get("status"):
        conditions.append("emp.status = %(status)s")
    if filters.get("branch"):
        conditions.append("emp.branch = %(branch)s")
    if filters.get("department"):
        conditions.append("emp.department = %(department)s")
    if filters.get("from_date") and filters.get("to_date"):
        conditions.append("ss.start_date >= %(from_date)s AND ss.end_date <= %(to_date)s")
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"

    data = frappe.db.sql(f"""
        SELECT
            emp.employee AS employee,
            emp.employee_name AS employee_name,
            emp.designation AS designation,
            emp.department AS department,
            emp.date_of_joining AS date_of_joining,
            emp.branch AS branch,
            ss.bank_account_no AS bank_account_no,
            ss.gross_pay AS gross_salary,
            ss.net_pay AS net_pay,
            emp.status AS status
        FROM
            `tabEmployee` emp
        LEFT JOIN
            `tabSalary Slip` ss ON ss.employee = emp.employee
        WHERE
            ss.docstatus = 0 AND {where_clause}
        ORDER BY
            emp.employee_name ASC
    """, filters, as_dict=True)

    return data
