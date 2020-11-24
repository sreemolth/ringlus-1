# Copyright (c) 2013, Momscode Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
def execute(filters=None):
	columns, data = [], []
	columns = [{
	    "fieldname": "account",
        "label": _("Account"),
        "fieldtype": "Link",
        "options": "Account",
        "width": 300
    },
    {
       "fieldname": "currency",
        "label": _("Currency"),
       "fieldtype": "Link",
        "options": "Currency",
    }]
	data.extend([])

	return columns, data
