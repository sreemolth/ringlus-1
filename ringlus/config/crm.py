from __future__ import unicode_literals
import frappe
from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words
from frappe import _

def get_data():
    	return [
		{
			"label": _("Sales Pipeline"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "Customer Factory Visit",
					"description": _("Customer Factory Visit"),
					"onboard": 1,
				},
				

            ]
		}
	] 