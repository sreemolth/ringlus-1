
from __future__ import unicode_literals

import frappe
import json
import frappe.utils
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form
from frappe import _
from six import string_types
from frappe.model.utils import get_fetch_values
from frappe.model.mapper import get_mapped_doc
from erpnext.stock.stock_balance import update_bin_qty, get_reserved_qty
from frappe.desk.notifications import clear_doctype_notifications
from frappe.contacts.doctype.address.address import get_company_address
from erpnext.controllers.selling_controller import SellingController
from frappe.automation.doctype.auto_repeat.auto_repeat import get_next_schedule_date
from erpnext.selling.doctype.customer.customer import check_credit_limit
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.manufacturing.doctype.production_plan.production_plan import get_items_for_material_requests
from erpnext.accounts.doctype.sales_invoice.sales_invoice import validate_inter_company_party, update_linked_doc,\
	unlink_inter_company_doc
from frappe.model.naming import set_name_by_naming_series
from frappe.model.naming import make_autoname
def on_sales_order_on_submit(doc, handler=""):
    item_list = frappe.db.sql("""select si.name,si.item_code,si.item_name,si.qty,si.delivery_date,si.bom_no
    from `tabSales Order Item` si, `tabSales Order` s
    where s.name = si.parent and si.parenttype = 'Sales Order'
    and s.docstatus = 1 and si.parent = %s""",(doc.name),as_dict=1)
    for s in item_list:
        for x in range(int(s.qty)):
            item2 = frappe.new_doc('Product Serial No')
            item2.flags.ignore_permissions  = True
            item2.serial_no = make_autoname(s.item_code + '-.#####')
            item2.item_code = s.item_code
            item2.sales_order=doc.name
            item2.update({
                'serial_no':item2.serial_no,
                'item_code': item2.item_code,
                'sales_order':item2.sales_order
            }).insert()
    frappe.msgprint(msg = 'Serial No has been Created',
        title = 'Notification',
        indicator = 'green'
    )
    count=0
    serial_no_list = frappe.db.sql("""select serial_no from `tabProduct Serial No` where sales_order=%s""",(doc.name),as_dict=1)
    for d in item_list:
        for x in serial_no_list:
            count=count+1
            item = frappe.new_doc('Production Plan')
            item.flags.ignore_permissions  = True
            item.production_plan_name = doc.name +'_'+d.item_code+'_'+ 'Q'+str(count)
            item.planned_completion_date = d.delivery_date
            item.for_warehouse="Work In Progress - RNG"
            item.product_serial_no=x.serial_no
            item.default_warehouse="Work In Progress - RNG"
            item.sales_order=doc.name
            item.get_items_for_mr=True
            item_list1 = frappe.db.sql("""select name ,transaction_date,customer,grand_total from `tabSales Order` where name=%s """,(doc.name),as_dict=1)
            for j in item_list1:
                item.append('sales_orders', {
                    'sales_order': doc.name,
                    'sales_order_date': j.transaction_date,
                    'customer':j.customer,
                    'grand_total':j.grand_total
               })
            item_list2 = frappe.db.sql("""select si.item_code,si.item_name,si.qty,si.delivery_date,si.bom_no
            from `tabSales Order Item` si, `tabSales Order` s
            where s.name = si.parent and si.parenttype = 'Sales Order'
            and s.docstatus = 1 and si.parent = %s and si.item_code=%s""",(doc.name,d.item_code),as_dict=1)
            for i in item_list2:
                item.append('po_items', {
                    'include_exploded_item':1,
                    'item_code': i.item_code,
                    'bom_no': i.bom_no,
                    'planned_qty': 1,
                })
            item.flags.ignore_permissions  = True
            item.update({
                'production_plan_name':item.production_plan_name,
                'planned_completion_date': item.planned_completion_date,
                'for_warehouse':item.for_warehouse,
                'item_code':item.item_code,
                'product_serial_no':item.product_serial_no,
                'get_items_for_mr':item.get_items_for_mr,
                'default_warehouse':item.default_warehouse,
                'sales_order':item.sales_order,
                'sales_orders': item.sales_orders,
                'po_items':item.po_items
            }).insert()
    frappe.msgprint(msg = 'Production Plan has been Created',
        title = 'Notification',
        indicator = 'green'
    )
    
    order_list1 = frappe.db.sql("""select si.item_code,si.delivery_date
    from `tabSales Order Item` si, `tabSales Order` s
    where s.name = si.parent and si.parenttype = 'Sales Order'
    and s.docstatus = 1 and si.parent = %s""",(doc.name),as_dict=1)
    production_plan_list = frappe.db.sql("""select production_plan_name,status,product_serial_no from `tabProduction Plan` where sales_order=%s""",(doc.name),as_dict=1)
    #if order_list1:
    order_list = frappe.db.sql("""select sales_order from `tabOrder And Dispatch` where sales_order=%s""",(doc.name),as_dict=1)
    if not order_list:
        item1 = frappe.new_doc('Order And Dispatch')
        item1.flags.ignore_permissions  = True
        item1.title = doc.name+"_"+ doc.customer
        item1.sales_order=doc.name
        item1.status = "Open"
        item1.posting_date=doc.transaction_date
        for i in order_list1:
            item1.append('od_items', {
                'item': i.item_code,
                'delivery_date': i.delivery_date,
                'delivery_status': 'Open',
                'sales_order':doc.name,
                'sales_invoice_status':'Draft'
            })
        for j in production_plan_list:
            item1.append('production_plan_no', {
                'production_plan':j.production_plan_name,
                'product_serial_no':j.product_serial_no,
                'production_plan_status':j.status,
                'delivery_date':doc.delivery_date,
                'sales_order':doc.name
            })
        item1.flags.ignore_permissions  = True
        item1.update({
            'title':item1.title,
            'posting_date':item1.posting_date,
            'sales_order':item1.sales_order,
            'status': item1.status,
            'od_items':item1.od_items,
            'production_plan_no':item1.production_plan_no
            }).insert()

    frappe.msgprint(msg = 'Order And Dispatch has been Created',
        title = 'Notification',
        indicator = 'green'
    )
    
        
    return 
@frappe.whitelist()
def get_sales_order_items(sales_order):
    item_list = frappe.db.sql("""select si.item_code,delivery_date
    from `tabSales Order Item` si
    where si.parenttype = 'Sales Order'
    and si.parent = %s""",(sales_order),as_dict=1)
    return item_list
@frappe.whitelist()
def make_proforma_invoice(source_name, target_doc=None, ignore_permissions=False):
    def postprocess(source, target):
        set_missing_values(source, target)
		#Get the advance paid Journal Entries in Sales Invoice Advance
        if target.get("allocate_advances_automatically"):
            target.set_advances()

    def set_missing_values(source, target):
        target.ignore_pricing_rule = 1
        target.flags.ignore_permissions = True
        target.run_method("set_missing_values")
        #target.run_method("set_po_nos")
        target.run_method("calculate_taxes_and_totals")
        if source.company_address:
            target.update({'company_address': source.company_address})
        else:
			# set company address
            target.update(get_company_address(target.company))

        if target.company_address:
            target.update(get_fetch_values("Proforma Invoice", 'company_address', target.company_address))

        # set the redeem loyalty points if provided via shopping cart
        if source.loyalty_points and source.order_type == "Shopping Cart":
            target.redeem_loyalty_points = 1

    def update_item(source, target, source_parent):
        target.amount = flt(source.amount) - flt(source.billed_amt)
        target.base_amount = target.amount * flt(source_parent.conversion_rate)
        target.qty = target.amount / flt(source.rate) if (source.rate and source.billed_amt) else source.qty - source.returned_qty

        if source_parent.project:
            target.cost_center = frappe.db.get_value("Project", source_parent.project, "cost_center")
        if target.item_code:
            item = get_item_defaults(target.item_code, source_parent.company)
            item_group = get_item_group_defaults(target.item_code, source_parent.company)
            cost_center = item.get("selling_cost_center") \
            or item_group.get("selling_cost_center")

    doclist = get_mapped_doc("Sales Order", source_name, {
       "Sales Order": {
            "doctype": "Proforma Invoice",
            "field_map": {
                "party_account_currency": "party_account_currency",
                "payment_terms_template": "payment_terms_template"
            },
            "validation": {
                "docstatus": ["=", 1]
            }
       },
        "Sales Order Item": {
            "doctype": "Proforma Invoice Item",
            "field_map": {
                "name": "so_detail",
                "parent": "sales_order",
            },
            "postprocess": update_item,
            "condition": lambda doc: doc.qty and (doc.base_amount==0 or abs(doc.billed_amt) < abs(doc.amount))
        },
        "Sales Taxes and Charges": {
            "doctype": "Sales Taxes and Charges",
            "add_if_empty": True
        },
        "Sales Team": {
            "doctype": "Sales Team",
            "add_if_empty": True
       }
    }, target_doc, postprocess, ignore_permissions=ignore_permissions)

    return doclist
