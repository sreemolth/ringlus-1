import frappe
import frappe, json
from frappe import msgprint, _
from six import string_types, iteritems

from frappe.model.document import Document
from frappe.utils import cstr, flt, cint, nowdate, add_days, comma_and, now_datetime, ceil
from frappe.utils.csvutils import build_csv_response
from erpnext.manufacturing.doctype.bom.bom import validate_bom_no, get_children
from erpnext.manufacturing.doctype.work_order.work_order import get_item_details
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from frappe.model.document import Document
from frappe.utils import cstr, flt, cint, nowdate, add_days, comma_and, now_datetime, ceil
from frappe.model.naming import set_name_by_naming_series
from erpnext.manufacturing.doctype.bom.bom import validate_bom_no, get_children
from erpnext.manufacturing.doctype.work_order.work_order import get_item_details
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults

def production_plan_on_save(doc,Handler=""):
    
    order_and_dispatch_list=frappe.db.sql("""select oi.production_plan
    from `tabProduction Plan Status` oi where sales_order=%s and production_plan=%s
    """,(doc.sales_order,doc.production_plan_name),as_dict=1)
    if order_and_dispatch_list:
        
        frappe.db.sql("""update `tabProduction Plan Status` set production_plan_status = %s where production_plan =%s""",((doc.status),doc.production_plan_name))
    return order_and_dispatch_list
  
def make(doc,Handler=""):
        '''Create Material Requests grouped by Sales Order and Material Request Type'''
        material_request_list = []
        material_request_map = {}
        msgprint(_(doc.name))
        for item in doc.mr_items:
            item_doc = frappe.get_cached_doc('Item', item.item_code)
            material_request_type = item.material_request_type or item_doc.default_material_request_type

            # key for Sales Order:Material Request Type:Customer
            key = '{}:{}:{}'.format(item.sales_order, material_request_type, item_doc.customer or '')
            schedule_date = add_days(nowdate(), cint(item_doc.lead_time_days))

            if not key in material_request_map:
                # make a new MR for the combination
                material_request_map[key] = frappe.new_doc("Material Request")
                material_request = material_request_map[key]
                material_request.update({
                    "transaction_date": nowdate(),
                    "title":doc.production_plan_name+'_'+material_request_type,
                    #"production_plan_no":doc.name,
                    "production_plan_name":doc.production_plan_name,
                    "status": "Draft",
                    "company": doc.company,
                    "requested_by": frappe.session.user,
                    'material_request_type': material_request_type,
                    'customer': item_doc.customer or ''
                })
                material_request_list.append(material_request)
            else:
                material_request = material_request_map[key]

            # add item
            material_request.append("items", {
                "item_code": item.item_code,
                "qty": item.quantity,
                "schedule_date": schedule_date,
                "warehouse": item.warehouse,
                "sales_order": item.sales_order,
                'production_plan': item.name,
                #'production_plan_name':item.production_plan_name,
                'material_request_plan_item': item.name,
                "project": frappe.db.get_value("Sales Order", item.sales_order, "project") \
                    if item.sales_order else None
            })

        for material_request in material_request_list:
            # submit
            material_request.flags.ignore_permissions = 1
            material_request.run_method("set_missing_values")

            if doc.get('submit_material_request'):
                material_request.submit()
            else:
                material_request.save()

        frappe.flags.mute_messages = False

        if material_request_list:
            material_request_list = ["""<a href="#Form/Material Request/{0}">{1}</a>""".format(m.name, m.name) \
                for m in material_request_list]
            msgprint(_("{0} created").format(comma_and(material_request_list)))
        else :
            msgprint(_("No material request created"))
