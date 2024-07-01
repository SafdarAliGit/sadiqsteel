def on_submit(self,method):
    charges = [
        self.cutting_charges,
        self.loading_unloading,
        self.cartage_charges,
        self.total_taxes_and_charges,
        self.total
    ]
    self.grand_total = sum(charge for charge in charges if charge is not None)


def before_save(self,method):
    charges = [
        self.cutting_charges,
        self.loading_unloading,
        self.cartage_charges,
        self.total_taxes_and_charges,
        self.total
    ]
    self.grand_total = sum(charge for charge in charges if charge is not None)
