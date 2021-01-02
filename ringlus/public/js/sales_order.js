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
    },
    
});
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
frappe.ui.form.on('Sales Order', {
    
        refresh: function(frm) {
            if (!frm.doc.__islocal && frm.doc.docstatus<2) {
           frm.add_custom_button(__('Proforma Invoice'),
             cur_frm.cscript['make_proforma_invoice'], __("Create"));
        } 
    }
    });
    cur_frm.cscript.make_proforma_invoice = function(doc) {
       frappe.model.open_mapped_doc({
                method: "ringlus.ringlus.doctype.sales_order.sales_order.make_proforma_invoice",
                frm: cur_frm
            }) 
    };


    frappe.ui.form.on('Sales Order', {
    validate:function(frm,cdt,cdn)   {

     $.each(frm.doc.items || [], function(i, v) {
            if(v.bom_status!=1)
            {
                frappe.msgprint(__("BOM Should Be Approved "));
                frappe.validated = false;
            }
        })
    }
    })