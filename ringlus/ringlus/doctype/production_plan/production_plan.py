import frappe

from frappe.model.naming import set_name_by_naming_series


def production_plan_on_save(doc,Handler=""):
    
    order_and_dispatch_list=frappe.db.sql("""select oi.production_plan
    from `tabProduction Plan Status` oi where sales_order=%s and production_plan=%s
    """,(doc.sales_order,doc.production_plan_name),as_dict=1)
    if order_and_dispatch_list:
        frappe.msgprint(doc.production_plan_name)
        frappe.db.sql("""update `tabProduction Plan Status` set production_plan_status = %s where production_plan =%s""",((doc.status),doc.production_plan_name))
    return order_and_dispatch_list