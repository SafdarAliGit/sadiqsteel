# Copyright (c) 2024, Tech Ventures and contributors
# For license information, please see license.txt
import frappe
# import frappe
from frappe.model.document import Document
from sadiqsteel.sadiq_steel.doctype.utils_functions import get_doctype_by_field
from frappe.model.naming import make_autoname

from collections import defaultdict


class DayBookEntry(Document):
    def before_submit(self):
        # Group day_entry_items data by entry_no
        groups = defaultdict(list)
        for item in self.day_book_entry_items:
            groups[item.entry_no].append(item)

        # Create Journal Entry for each group
        for entry_no, items in groups.items():
            self.create_journal_entry(entry_no, items)

    def create_journal_entry(self, entry_no, items):
        # Create a new Journal Entry
        journal_entry = frappe.new_doc("Journal Entry")
        journal_entry.posting_date = self.date
        journal_entry.ref_no = self.name
        journal_entry.ref_doctype = "Day Book Entry"
        journal_entry.remark = f"Journal Entry for Day Entry {entry_no}"

        # Populate Journal Entry with accounts based on the grouped data
        for item in items:
            account_name = None
            party_type = None
            party = None
            credit_in_account_currency = 0
            debit_in_account_currency = 0
            remarks = ''

            if account_info(item.account_name)['account_type'] in ["Receivable", "Payable"]:
                account_name = item.account_name
                party_type = item.party_type
                party = item.party
                credit_in_account_currency = item.received
                debit_in_account_currency = item.payment
                remarks = item.narration
            else:
                account_name = item.account_name
                party_type = None
                party = None
                credit_in_account_currency = item.received
                debit_in_account_currency = item.payment
                remarks = item.narration

            journal_entry.append("accounts", {
                "account": account_name,
                "party_type": party_type,
                "party": party,
                "credit_in_account_currency": credit_in_account_currency,
                "debit_in_account_currency": debit_in_account_currency,
                "remarks": remarks
            })

        # Submit the Journal Entry
        journal_entry.submit()

    def on_cancel(self):
        journal_entries = frappe.get_list("Journal Entry",fields=["name", "docstatus", "amended_from"], filters={"ref_no": self.name})
        for entry in journal_entries:
            if entry.docstatus == 1:
                # Cancel the entry
                doc = frappe.get_doc("Journal Entry", entry.name)
                doc.cancel()
                frappe.db.commit()

                # Generate a new name if it's an amendment
                if entry.amended_from:
                    new_name = int(entry.name.split("-")[-1]) + 1
                else:
                    new_name = f"{entry.name}-{1}"
                make_autoname(new_name, 'Journal Entry')


def account_info(account):
    account_type = frappe.db.get_value("Account", account, "account_type")
    is_group = frappe.db.get_value("Account", account, "is_group")
    return {
        "is_group": is_group,
        "account_type": account_type
    }
