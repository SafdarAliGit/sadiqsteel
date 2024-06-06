# my_custom_app.my_custom_app.report.daily_activity_report.daily_activity_report.py
from decimal import Decimal

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    columns = [
        {
            "label": "<b>Date</b>",
            "fieldname": "date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": "<b>VOU#</b>",
            "fieldname": "voucher_no",
            "fieldtype": "Link",
            "options": "Day Book Entry",
            "width": 120
        },
        {
            "label": "<b>Account</b>",
            "fieldname": "account",
            "fieldtype": "Link",
			"options": "Account",
            "width": 120
        },
        {
            "label": "<b>Description</b>",
            "fieldname": "description",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "<b>Debit</b>",
            "fieldname": "received",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": "<b>Credit</b>",
            "fieldname": "payment",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": "<b>Balance</b>",
            "fieldname": "balance",
            "fieldtype": "Currency",
            "width": 120
        }

    ]
    return columns


def get_conditions(filters):
    conditions = []
    if filters.get("from_date"):
        conditions.append(f"dbe.date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append(f"dbe.date <= %(to_date)s")
    return " AND ".join(conditions)


def get_data(filters):
    data = []

    query = """
            SELECT 
                dbe.date,
                dbe.name AS voucher_no,
                dbei.account_name AS account,
                dbei.narration AS description,
                dbei.received,
                dbei.payment,
				0 As balance
            FROM 
                `tabDay Book Entry` AS dbe
            JOIN 
                `tabDay Book Entry Items` AS dbei ON dbe.name = dbei.parent
            WHERE
                dbe.docstatus = 1
                AND {conditions}
            ORDER BY 
                dbe.date
    """.format(conditions=get_conditions(filters))
    query_result = frappe.db.sql(query, filters, as_dict=1)

    # Initialize the balance and totals
    running_balance = 0
    total_received = 0
    total_payment = 0

    # Precompute the balances and totals
    for entry in query_result:
        received = entry['received']
        payment = entry['payment']

        running_balance += received - payment
        entry['balance'] = running_balance  # Add the running balance to the entry

        total_received += received
        total_payment += payment

    # Create the "Grand Total" row
    grand_total = {
        'description': 'Grand Total',
        'received': total_received,
        'payment': total_payment,
        'balance': total_received - total_payment,
        'is_bold': True
    }

    # Append the "Grand Total" row to the data
    data.extend(query_result)
    data.append(grand_total)
    return data
