# -*- coding: utf-8 -*-
# Copyright (c) 2020, Momscode Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, cstr
class TrainingRequest(Document):
	pass
@frappe.whitelist()
def make_expense_claim(docname):
	expense_claim = frappe.db.exists("Expense Claim", {"training_request": docname})
	if expense_claim:
		frappe.throw(_("Expense Claim {0} already exists for the Training Request").format(expense_claim))

	traning_request= frappe.get_doc("Training Request", docname)
	service_expense = sum([flt(d.expense_amount) for d in traning_request.traning_expense])

	claim_amount = service_expense 
	if not claim_amount:
		frappe.throw(_("No additional expenses has been added"))

	exp_claim = frappe.new_doc("Expense Claim")
	exp_claim.employee = traning_request.employee
	exp_claim.training_request = traning_request.name
	exp_claim.remark = _("Expense Claim for Training Request {0}").format(traning_request.event_name)
	exp_claim.append("expenses", {
		"expense_date": traning_request.date,
		"description": _("Traning Expenses"),
		"amount": claim_amount
	})
	return exp_claim.as_dict()