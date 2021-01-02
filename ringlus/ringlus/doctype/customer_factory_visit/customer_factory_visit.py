# -*- coding: utf-8 -*-
# Copyright (c) 2020, Momscode Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CustomerFactoryVisit(Document):
	pass
@frappe.whitelist()
def holidays_visit_date(visit_date):
    holiday_list = frappe.db.sql("""select holiday_date from `tabHoliday`
        where  holiday_date = %s """,(visit_date),as_dict=1)
    return holiday_list