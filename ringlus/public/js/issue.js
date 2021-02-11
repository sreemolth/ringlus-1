frappe.ui.form.on('Issue', {
    refresh: function (frm, cdt, cdn) {
        if (frm.doc.issue_type == 'Onsite Support'){
            frm.add_custom_button(__('Expense Claim'),
            cur_frm.cscript['make_expense_claim'], __("Make"));
            
        }
        if (frm.doc.warranty == 'No Warranty' && frm.doc.material_required == 1){
            frm.add_custom_button(__('Material Request'),
            cur_frm.cscript['make_material_request'], __("Make"));
        } 

    }

    
});
cur_frm.cscript.make_expense_claim = function(doc) {
    frappe.model.open_mapped_doc({
        method: "ringlus.ringlus.doctype.issue.issue.make_expense_claim",
        frm: cur_frm    
    }) 
};
cur_frm.cscript.make_material_request = function(doc){
    frappe.model.open_mapped_doc({
        method: "ringlus.ringlus.doctype.issue.issue.make_material_request",
        frm: cur_frm
    }) 
};




/*frappe.ui.form.on('Issue',{
    validate: function(frm, cdt, cdn){
        var d = locals[cdt][cdn];
        frappe.call({
            method:"frappe.client.get_value",
            args: {
                doctype:"Service Level Agreement",
                filters: {
                    'name': frm.doc.service_level_agreement,
                },
                fieldname:['warranty']
            }, 
            callback: function(r) { 
                if(!r.exc){
                    frappe.model.set_value(d.doctype, d.name,"warranty",r.message.warranty)
                }
            }
        })
        
    }
})*/





frappe.ui.form.on('Issue',{
    sales_order:function(frm,cdt,cdn){
        
        var d = locals[cdt][cdn];
        frappe.call({
            method:"frappe.client.get_value",
            args: {
                doctype:"Service Level Agreement",
                filters: {
                    'sales_order': d.sales_order,
                },
            fieldname:['name','warranty','end_date','product_serial_number']
            }, 
            callback: function(r){
                if(!r.exc){
                    frappe.model.set_value(d.doctype, d.name,"service_level_agreement",r.message.name)
                    frappe.model.set_value(d.doctype, d.name,"warranty",r.message.warranty)
                    frappe.model.set_value(d.doctype, d.name,"end_date",r.message.end_date)
                    frappe.model.set_value(d.doctype, d.name,"product_serial_no",r.message.product_serial_number)
                }
            }
        })
    },
    customer: function(frm,cdt,cdn){
        var d = locals[cdt][cdn];
        var customer =d.customer;
        frappe.call({
            method: "ringlus.ringlus.doctype.issue.issue.get_sales_order_details",
            args:{
                'customer': d.customer
            },
            callback:function(r){
                if(!r.exc){
                    var df = frappe.meta.get_docfield("Issue","sales_order", cur_frm.doc.name);
                    var q_options = [];
                    for (var i=0; i<r.message.length; i++){
                        var a = r.message[i].sales_order;
                        q_options.push(a)
                    }
                    df.options = q_options;
                    frm.refresh_field("sales_order");
                }
            }
        });
    }
})