import frappe
from frappe import _
from frappe import _, msgprint


def on_BOM_after_submit(doc,Handler= ""):
    op_cost=0
    mc_cost=0
    sub_op_cost=0
    total_cost=0
    total_material_cost=0
    total_nested_bom_cost=0
    bom_activity_list = frappe.db.sql("""select ba.bom_no,ba.qty
    from `tabBOM Item` ba, `tabBOM` b
    where b.name = ba.parent and ba.parenttype = 'BOM'
    and  ba.parent = %s and ba.bom_no!="" order by ba.idx asc """,(doc.name),as_dict=1)
    for x in bom_activity_list:
        bom_operating_cost=frappe.db.sql("""select ba.operating_cost from `tabBOM Operation` ba, `tabBOM` b
        where b.name = ba.parent and ba.parenttype = 'BOM'
        and  ba.parent = %s order by ba.idx asc """,(x.bom_no),as_dict=1)
        for k in bom_operating_cost:
            sub_op_cost+=(k.operating_cost)*(float(x.qty))
        bom_child_list = frappe.db.sql("""select ba.bom_no,ba.qty,ba.amount
        from `tabBOM Item` ba, `tabBOM` b
        where b.name = ba.parent and ba.parenttype = 'BOM'
        and  ba.parent = %s and ba.bom_no!="" order by ba.idx asc """,(x.bom_no),as_dict=1)
        if bom_child_list:
            for d in bom_child_list:
                bom_cost = frappe.db.sql("""select b.name,b.operating_cost,b.raw_material_cost
                from `tabBOM` b where b.name = %s """,(d.bom_no),as_dict=1)
                for h in bom_cost:
                    op_cost+=(h.operating_cost)*(float(x.qty))*(d.qty)
                    mc_cost+=h.raw_material_cost
        
        else:
            bom_child_list1 = frappe.db.sql("""select ba.bom_no,ba.qty,ba.amount
            from `tabBOM Item` ba, `tabBOM` b
            where b.name = ba.parent and ba.parenttype = 'BOM'
            and  ba.parent = %s and ba.bom_no="" order by ba.idx asc """,(x.bom_no),as_dict=1)
            for b in bom_child_list1:
                mc_cost+=b.amount
    total_cost=op_cost+sub_op_cost+doc.operating_cost
    total_material_cost=doc.raw_material_cost-op_cost-sub_op_cost
    total_nested_bom_cost=total_cost+total_material_cost
    frappe.db.sql("""update `tabBOM` set nested_operating_cost = %s where name =%s""",((total_cost), doc.name))
    frappe.db.sql("""update `tabBOM` set nested_material_cost = %s where name =%s""",((total_material_cost), doc.name))
    frappe.db.sql("""update `tabBOM` set total_nested_bom_cost = %s where name =%s""",((total_nested_bom_cost), doc.name))
    
    bom_item_list = frappe.db.sql("""select item_code from `tabItem Price` where item_code= %s """,(doc.item),as_dict=1)
    if not bom_item_list:
            project = frappe.new_doc('Item Price')
            project.Item_code = doc.item
            project.uom = doc.uom
            project.price_list = 'Standard Selling'
            project.quantity=doc.quantity
            project.price_list_rate = doc.total_cost/doc.quantity
            project.flags.ignore_permissions  = True
            project.update({
            'item_code': project.Item_code,
            'uom': project.uom,
            'price_list': project.price_list,
            'price_list_rate': project.price_list_rate
            }).insert()
            frappe.msgprint(msg = 'Item Price Created',
            title = 'Notification',
            indicator = 'green')
    else:
        
            frappe.db.sql("""update `tabItem Price` set price_list_rate = %s where item_code =%s""",((doc.total_cost/doc.quantity), doc.item))
            frappe.msgprint(msg = 'Item Price Updated',
            title = 'Notification',
            indicator = 'green')
   
    doc.reload()
    return bom_activity_list

