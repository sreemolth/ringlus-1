# -*- coding: utf-8 -*-
# Copyright (c) 2020, Momscode Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class OrdernDispatch(Document):
	pass
@frappe.whitelist()
def get_order_n_dispatch(sales_order):
    item_list = frappe.db.sql("""select sales_order
    from `tabOrder n Dispatch` where sales_order=%s""",(sales_order),as_dict=1)
    return item_list
#def update_order_n_dispatch(doc, Handler=""):
#    order_list=frappe.db.sql("""select production_plan_name from `Production Plan` where production_plan_name = %s""",(doc.name), as_dict=1)
#    for x in order_list:
