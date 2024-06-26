frappe.ui.form.on('Day Book Entry', {
    refresh(frm) {
        frm.set_query('account_name', 'day_book_entry_items', function (doc, cdt, cdn) {
            var d = locals[cdt][cdn];
            return {
                filters: [
                    ["Account", "is_group", "=", 0]
                ]
            };
        });
    }
});

frappe.ui.form.on('Day Book Entry Items', {
    received: function (frm) {
        day_book_entry_items_totals(frm);
    },
    payment: function (frm) {
        day_book_entry_items_totals(frm);
    },
    account_name: function (frm, cdt, cdn) {
        get_account_balance(frm, cdt, cdn);

        var d = locals[cdt][cdn];
        frappe.call({
            method: 'sadiqsteel.sadiq_steel.doctype.utils.get_party_type',
            args: {
                account: d.account_name,
            },
            callback: function (r) {
                if (!r.exc) {
                    frappe.model.set_value(cdt, cdn, 'party_type', r.message.party_type);
                }
            }
        });


    }
});


function day_book_entry_items_totals(frm) {
    var day_book_entry_items = frm.doc.day_book_entry_items;
    frm.doc.total_received = 0;
    frm.doc.total_payment = 0;

    for (var i in day_book_entry_items) {
        frm.doc.total_received += day_book_entry_items[i].received || 0;
        frm.doc.total_payment += day_book_entry_items[i].payment || 0;
    }
    frm.set_value("diffrence", frm.doc.total_received - frm.doc.total_payment);
    frm.refresh_field('total_received');
    frm.refresh_field('total_payment');
}

function get_account_balance(frm, cdt, cdn) {
    var d = locals[cdt][cdn];

    frappe.call({
        method: 'erpnext.accounts.utils.get_balance_on',
        args: {
            account: d.account_name
        },
        callback: function (r) {
            if (r.message) {
                frappe.model.set_value(d.doctype, d.name, 'balance', r.message);
            }
        }
    });


}

