import frappe

from frappe.model.naming import set_name_by_naming_series


def delivery_note_on_save(doc,Handler=""):
    item_list = frappe.db.sql("""select do.item_code,do.against_sales_order,do.product_serial_no
    from `tabDelivery Note Item` do
    """,as_dict=1)
    for d in item_list:
        order_and_dispatch_list=frappe.db.sql("""select oi.production_plan,oi.product_serial_no,oi.sales_invoice_status
        from `tabProduction Plan Status` oi where sales_order=%s and  product_serial_no=%s
        """,(d.against_sales_order,d.product_serial_no),as_dict=1)
        if order_and_dispatch_list:
            frappe.msgprint(order_and_dispatch_list.sales_invoice_status)
            frappe.db.sql("""update `tabProduction Plan Status` set delivery_status = %s where product_serial_no =%s""",((doc.status),d.product_serial_no))
    return item_list