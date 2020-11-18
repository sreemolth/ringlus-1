frappe.ui.form.on('Sales Order Item', {
    item_code: function(frm,cdt,cdn){
        var d = locals[cdt][cdn];
        var item_code = d.item_code;
        frappe.call({
            method:"frappe.client.get_value",
            args: {
                doctype:"BOM",
                filters: {
                    item: item_code,
                    is_default : 1
                },
                fieldname:["name","nested_operating_cost","nested_material_cost"]
            }, 
            callback: function(r) { 
                frappe.model.set_value(d.doctype, d.name,"bom_no",r.message.name)
            }
        })
    }
});