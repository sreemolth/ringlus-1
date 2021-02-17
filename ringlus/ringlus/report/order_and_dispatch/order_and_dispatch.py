# Copyright (c) 2013, Momscode Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import getdate

def execute(filters=None):
	columns, data = [], []
	todo_list = frappe.get_list('ToDo', fields=["title", "posting_date", "status"],filters={'status': 'Open'})
	columns = [_("ID")+":Link/Order And Dispatch:90", _("Posting Date")+"::60", _("Status")+ ":Date"]
	return columns, data
