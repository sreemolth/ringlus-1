/*frappe.ui.form.on('Production Plan', {
    validate:function(frm, cdt, cdn){
        frappe.call({
            method: 'ringlus.ringlus.doctype.production_plan.production_plan.production_plan_status',
            args: {
            },
            callback: function(r) {
                if(!r.exc){
                    alert(r.message);
                    frm.set_value("product_serial_no",r.message.product_serial_no)
                }
            }
        })

    }
})*/