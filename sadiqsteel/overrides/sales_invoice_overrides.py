# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice

form_grid_templates = {"items": "templates/form_grid/item_grid.html"}

class SalesInvoiceOverrides(SalesInvoice):
    def before_save(self):
        self.grand_total = sum(
            getattr(self, attr, 0) for attr in [
                'cutting_charges',
                'loading_unloading',
                'cartage_charges',
                'total_taxes_and_charges',
                'total'
            ]
        )


