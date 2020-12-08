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