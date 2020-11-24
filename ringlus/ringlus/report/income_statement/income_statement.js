// Copyright (c) 2016, Momscode Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Income Statement"] = {
	"filters": [
        {
            "fieldname":"company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "default": frappe.defaults.get_user_default("company")
        },
    ]
};
