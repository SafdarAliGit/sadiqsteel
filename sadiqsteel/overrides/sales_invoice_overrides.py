# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice

form_grid_templates = {"items": "templates/form_grid/item_grid.html"}


class SalesInvoiceOverrides(SalesInvoice):
    def on_submit(self):
        charges = [
            self.cutting_charges,
            self.loading_unloading,
            self.cartage_charges,
            self.total_taxes_and_charges,
            self.total
        ]
        self.grand_total = sum(charge for charge in charges if charge is not None)

    def before_save(self):
        charges = [
            self.cutting_charges,
            self.loading_unloading,
            self.cartage_charges,
            self.total_taxes_and_charges,
            self.total
        ]
        self.grand_total = sum(charge for charge in charges if charge is not None)
