import frappe

#from frappe.model.naming import set_name_by_naming_series
#def sales_invoice_on_save(Anddoc,Handler=""):
#    for i in doc.items:
#        item_list = frappe.db.sql("""select so.item_code,so.sales_order,so.product_serial_no
#        from `tabSales Invoice Item` so where sales_order=%s and product_serial_no=%s
#        """,(doc.sales_order,i.product_serial_no),as_dict=1)
#        for d in item_list:
#            sales_invoice_list=frappe.db.sql("""select oi.product_serial_no
#            from `tabProduction Plan Status` oi where sales_order=%s and product_serial_no=%s
#            """,(d.sales_order,d.product_serial_no),as_dict=1)
#        if  sales_invoice_list:
#            frappe.db.sql("""update `tabProduction Plan Status` set sales_invoice_status = %s  where product_serial_no =%s""",((doc.status),i.product_serial_no))
#            frappe.db.sql("""update `tabProduction Plan Status` set sales_invoice_date = %s  where product_serial_no =%s""",((doc.posting_date),i.product_serial_no))
#    return item_list
    