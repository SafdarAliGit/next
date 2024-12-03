# Copyright (c) 2024, vurke and contributors
# For license information, please see license.txt

# import frappe


# Import necessary modules
import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "EMP AREA CODE", "fieldname": "emp_area_code", "fieldtype": "Data", "width": 150},
        {"label": "EMP REG SERIAL_NO", "fieldname": "emp_reg_serial_no", "fieldtype": "Data", "width": 150},
        {"label": "EMP SUB-AREA CODE", "fieldname": "emp_sub_area_code", "fieldtype": "Data", "width": 150},
        {"label": "EMP SUB SERIAL NO", "fieldname": "emp_sub_serial_no", "fieldtype": "Data", "width": 150},
        {"label": "NAME", "fieldname": "name", "fieldtype": "Data", "width": 200},
        {"label": "EOBI_NO", "fieldname": "eobi_no", "fieldtype": "Data", "width": 150},
        {"label": "CNIC", "fieldname": "cnic", "fieldtype": "Data", "width": 150},
        {"label": "NIC", "fieldname": "nic", "fieldtype": "Data", "width": 150},
        {"label": "DOB", "fieldname": "dob", "fieldtype": "Date", "width": 150},
        {"label": "DOJ", "fieldname": "doj", "fieldtype": "Date", "width": 150},
        {"label": "DOE", "fieldname": "doe", "fieldtype": "Date", "width": 150},
        {"label": "NO_OF_DAYS_WORKED", "fieldname": "no_of_days_worked", "fieldtype": "Int", "width": 150},
    ]

def get_data(filters):
    # Fetch data from the Employee doctype
    return frappe.db.sql("""
        SELECT
            emp.emp_area_code AS emp_area_code,
            emp.emp_reg_serial_no AS emp_reg_serial_no,
            emp.emp_sub_area_code AS emp_sub_area_code,
            emp.emp_sub_serial_no AS emp_sub_serial_no,
            emp.employee_name AS name,
            emp.eobi_no AS eobi_no,
            emp.cnic AS cnic,
            emp.nic AS nic,
            emp.date_of_birth AS dob,
            emp.date_of_joining AS doj,
            emp.relieving_date AS doe,
            IFNULL(DATEDIFF(emp.relieving_date, emp.date_of_joining), 0) AS no_of_days_worked,  -- Handles NULL values
            NULL AS from_date,  -- Placeholder if these fields don't exist
            NULL AS to_date      -- Replace 'NULL' with valid column names if they exist

        FROM
            `tabEmployee` emp
        WHERE
            emp.status = 'Active'
        ORDER BY
            emp.name ASC
    """, as_dict=1)
