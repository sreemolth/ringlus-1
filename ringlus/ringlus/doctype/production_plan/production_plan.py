import frappe
from datetime import date
from frappe.utils import nowdate
from frappe.model.naming import set_name_by_naming_series
from frappe.model.naming import make_autoname

def production_plan_on_save(doc,Handler=""):
    frappe.msgprint("hai")
    order_and_dispatch_list=frappe.db.sql("""select oi.production_plan
    from `tabProduction Plan Status` oi where sales_order=%s and production_plan=%s
    """,(doc.sales_order,doc.production_plan_name),as_dict=1)
    if order_and_dispatch_list:
        frappe.msgprint(doc.production_plan_name)
        frappe.db.sql("""update `tabProduction Plan Status` set production_plan_status = %s where production_plan =%s""",((doc.status),doc.production_plan_name))
    item_list = frappe.db.sql("""select p.production_plan_name,pi.item_code from `tabProduction Plan` p inner join `tabProduction Plan Item` pi where p.name=pi.parent and p.name =%s""", (doc.name), as_dict=1)
    item_list2 = frappe.db.sql("""select ps.sales_order from `tabProduction Plan` p inner join `tabProduction Plan Sales Order` ps where p.name=ps.parent and p.name=%s""", (doc.name), as_dict=1)
    if doc.status == 'In Process':
        today = nowdate()
        x = frappe.utils.get_datetime(today).strftime('%d')
        y=frappe.utils.get_datetime(today).strftime('%m')
        z=frappe.utils.get_datetime(today).strftime('%Y')
        for s in item_list:
            for r in item_list2:
                item2 = frappe.new_doc('Product Serial No')
                item2.flags.ignore_permissions  = True
                #frappe.msgprint("Submitted")
                #frappe.msgprint(today)
                #serialday=frappe.utils.get_datetime(nowdate()).strftime('%d')
                #serialmnth=frappe.utils.get_datetime(nowdate()).strftime('%m')
                #serialyear=frappe.utils.get_datetime(nowdate()).strftime('%Y')
                item2.serial_no = make_autoname('RNG'+x+y+z+'-.###')
                item2.production_plan_name = s.production_plan_name
                item2.item_code = s.item_code
                item2.sales_order = r.sales_order
                item2.update({
                    'serial_no':item2.serial_no,
                    'production_plan_name':item2.production_plan_name,
                    'item_code':item2.item_code,
                    'sales_order':item2.sales_order
                    }).insert()

        frappe.msgprint(doc.production_plan_name)
        serial_no_list = frappe.db.sql("""select serial_no from `tabProduct Serial No` where production_plan_name=%s""",(doc.production_plan_name),as_dict=1)
        #plan_list = frappe.db.sql("""select production_plan_name from `tabProduction Plan` where production_plan_name=%s""",(doc.name), as_dict=1)
        for x in serial_no_list:
            frappe.msgprint("hello")
            frappe.msgprint(x.serial_no)
            frappe.db.sql("""update `tabProduction Plan` set product_serial_no = %s where production_plan_name =%s""",((x.serial_no), doc.production_plan_name))
            #frappe.db.sql("""update `tabProduction Plan Status` set product_serial_no = %s where production_plan =%s""",((x.serial_no), doc.production_plan)) 
                #frappe.db.sql("""update `Production Plan Status` set product_serial_no = %s where production_plan = %s""",((y.production_plan_name), doc.production_plan))
        plan_list = frappe.db.sql("""select p.product_serial_no from `tabProduction Plan` p  where p.production_plan_name =%s""", (doc.production_plan_name), as_dict=1)
        for y in plan_list:
            frappe.msgprint(y.product_serial_no)
            frappe.db.sql("""update `tabProduction Plan Status` set product_serial_no = %s where production_plan = %s""",((y.product_serial_no), doc.production_plan_name))
        #for m in item_list:
        #    for n in serial_no_list:
        #        doc.product_serial_no=n.serial_no
                #count=count+1
                #item = frappe.new_doc('Production Plan')
                #item.product_serial_no=n.serial_no
                #item.flags.ignore_permissions  = True
                #item.update({
                #    'product_serial_no':item.product_serial_no
                #}).insert()
    return order_and_dispatch_list



