import frappe
from frappe import _
from frappe.model.naming import set_name_by_naming_series

def delivery_note_on_save(doc,Handler=""):
    for i in doc.items:
        item_list = frappe.db.sql("""select do.item_code,do.against_sales_order,do.product_serial_no
        from `tabDelivery Note Item` do where against_sales_order=%s and product_serial_no=%s
        """,(i.against_sales_order,i.product_serial_no),as_dict=1)
        for d in item_list:
            order_and_dispatch_list=frappe.db.sql("""select oi.production_plan,oi.product_serial_no,oi.sales_invoice_status
            from `tabProduction Plan Status` oi where sales_order=%s and  product_serial_no=%s
            """,(d.against_sales_order,d.product_serial_no),as_dict=1)
            for x in order_and_dispatch_list:
                if(x.sales_invoice_status=="Open"):
                    frappe.throw(_("Sales Invoice is required"))
                else:
                    frappe.db.sql("""update `tabProduction Plan Status` set delivery_status = %s where product_serial_no =%s""",((doc.status),d.product_serial_no))

    return item_list
    
def delivery_note_on_approve(doc,Handler=""):
    for x in doc.items:
        delivery_note_list=frappe.db.sql("""select d.customer,d.posting_date,di.warranty,di.against_sales_order,di.item_name,di.qty,di.end_date,di.product_serial_no from `tabDelivery Note` as d INNER JOIN `tabDelivery Note Item` as di where d.name=di.parent and di.parent=%s and di.item_name=%s""",((doc.name), x.item_name), as_dict=1) 
        for s in delivery_note_list:
            for i in range(int(s.qty)):
                frappe.msgprint("helloooooo")
                item = frappe.new_doc('Service Level Agreement')
                item.flags.ignore_permissions  = True
                item.customer = s.customer
                item.start_date = s.posting_date
                item.sales_order = s.against_sales_order
                item.product_serial_number = s.product_serial_no
                item.item_name = s.item_name
                item.end_date = s.end_date
                item.service_level = 'Service Level1'
                item.warranty = s.warranty
                item.update({
                    'customer':item.customer,
                    'start_date':item.start_date,
                    'sales_order':item.sales_order,
                    'product_serial_number':item.product_serial_number,
                    'item_name':item.item_name,
                    'end_date':item.end_date,
                    'warranty':item.warranty
                }).insert()
    frappe.msgprint(msg = 'Service Level Agreement has been Created',
        title = 'Notification',
        indicator = 'green'
    ) 
    return
