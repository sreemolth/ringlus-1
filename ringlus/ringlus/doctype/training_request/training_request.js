// Copyright (c) 2020, Momscode Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Training Request', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on("Training Request", {
	refresh: function(frm) {
		if(frm.doc.docstatus == 1) {
			frm.add_custom_button(__('Expense Claim'), function() {
				frm.events.expense_claim(frm);
			}, __('Create'));
			frm.page.set_inner_btn_group_as_primary(__('Create'));
		}
	},

	expense_claim: function(frm){
		frappe.call({
			method: "ringlus.ringlus.doctype.training_request.training_request.make_expense_claim",
			args:{
				docname: frm.doc.name
			},
			callback: function(r){
				var doc = frappe.model.sync(r.message);
				frappe.set_route('Form', 'Expense Claim', r.message.name);
			}
		});
	}
});
