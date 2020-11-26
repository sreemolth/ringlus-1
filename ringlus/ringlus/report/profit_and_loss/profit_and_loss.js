// Copyright (c) 2016, Momscode Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Profit and Loss"] = {
	"filters": [

	]
};
frappe.require("assets/erpnext/js/financial_statements.js", function() {
	frappe.query_reports["Profit and Loss"] = $.extend({},
		erpnext.financial_statements);

	frappe.query_reports["Profit and Loss"]["filters"].push(
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Project', txt);
			}
		},
		{
			"fieldname": "accumulated_values",
			"label": __("Accumulated Values"),
			"fieldtype": "Check"
		},
		{
			"fieldname": "include_default_book_entries",
			"label": __("Include Default Book Entries"),
			"fieldtype": "Check",
			"default": 1
		}
	);
});
