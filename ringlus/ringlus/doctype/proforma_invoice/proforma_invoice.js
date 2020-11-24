// Copyright (c) 2020, Momscode Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Proforma Invoice', {
	// refresh: function(frm) {
		make_sales_invoice: function() {
			frappe.model.open_mapped_doc({
				method: "erpnext.selling.doctype.sales_order.sales_order.make_sales_invoice",
				frm: this.frm
			})
		},
	// }
});
