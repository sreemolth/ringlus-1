frappe.ui.form.on('Material Request', {
    before_submit: function (frm, cdt, cdn) {
        var d =locals[cdt][cdn];
        alert("hiiiiii");
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                'doctype': 'Material Request Item',
                'filters': {
                    'name':frm.doc.name,
                    'parent':d.name              
                },
                'fieldname': [
                   'production_plan'
                ]     
            },
            callback: function (r) {
                if (!r.exc) {
                    alert(r.message.production_plan);
                    frm.set_value("production_plan_no",r.message.production_plan);
                }
            }
           
        })     
   }
})