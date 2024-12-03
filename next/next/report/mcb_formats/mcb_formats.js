// Copyright (c) 2024, vurke and contributors
// For license information, please see license.txt

frappe.query_reports["MCB Formats"] = {
        filters: [
            {
                fieldname: "from_date",
                label: __("From Date"),
                fieldtype: "Date",
            },
            {
                fieldname: "to_date",
                label: __("To Date"),
                fieldtype: "Date",
            },
            {
                fieldname: "status",
                label: __("Status"),
                fieldtype: "Select",
                options: ["Active", "Left"],
                default: "Active"
            },
            {
                fieldname: "branch",
                label: __("Branch"),
                fieldtype: "Link",
                options: "Branch"
            },
            {
                fieldname: "department",
                label: __("Department"),
                fieldtype: "Link",
                options: "Department"
            }
        ]
};
    
