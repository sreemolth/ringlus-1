from __future__ import unicode_literals
import frappe
from frappe.model.mapper import get_mapped_doc  
from frappe.model.document import Document
from frappe.model.document import get_doc
from frappe.model.document import Document

@frappe.whitelist()
def make_expense_claim(source_name, target_doc=None):
    target_doc = get_mapped_doc("Issue", source_name, {
        "Issue": {
            "doctype": "Expense Claim",
            "field_map": {
                "name": "issue"
            }
        },
    }, target_doc) 

    return target_doc

@frappe.whitelist()     
def make_material_request(source_name, target_doc=None):
    target_doc = get_mapped_doc("Issue", source_name, {
        "Issue": {
            "doctype": "Material Request",
            "field_map": {
                "name": "issue"
                }
                 },
                }, target_doc)
    target_doc.material_request_type = "Material Issue" 

    return target_doc 

@frappe.whitelist()
def get_sales_order_details(customer):
    
    project_list1 = frappe.db.sql(""" select distinct sales_order from `tabService Level Agreement` where customer= %s""",(customer),as_dict=1)

    return project_list1