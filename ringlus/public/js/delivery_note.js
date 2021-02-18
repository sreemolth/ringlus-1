frappe.ui.form.on('Delivery Note', {
    product_serial_no:function(frm, cdt, cdn){
        var d=locals[cdt][cdn]
        alert(d.name)
        
        
        frm.set_query("product_serial_no", function() {
            return {
                filters: [
                    ["Serial No","sales_order", "=", d.against_sales_order]
                ]
            }
        });
}
})

frappe.ui.form.on('Delivery Note', {
    validate: function(frm) {
        var date = frm.doc.posting_date;
        $.each(frm.doc.items || [], function(i, d) {
            frappe.model.set_value(d.doctype, d.name,"po_date",frappe.datetime.add_days(date))
            
            /*if(d.qty>1){
                alert("kkk");
                var x = frappe.model.add_child(cur_frm.doc, "Delivery Note Item", "items");
               
            }*/
            

                if (d.warranty == 'No Warranty'){
                    var x = d.po_date;
                    var date = new Date(x);
                    date.setDate(date.getDate() + 1);
                    frappe.model.set_value(d.doctype, d.name,"end_date",frappe.datetime.add_days(date))
                }
                else if(d.warranty == '6 Months'){
                    var x = d.po_date;
                    var date = new Date(x);
                    date.setMonth(date.getMonth() +6);
                    frappe.model.set_value(d.doctype, d.name,"end_date",frappe.datetime.add_days(date))
                }
                else if(d.warranty == '12 Months'){
                    var x = d.po_date;
                    var date = new Date(x);
                    date.setFullYear( date.getFullYear() + 1 );
                    frappe.model.set_value(d.doctype, d.name,"end_date",frappe.datetime.add_days(date))
                }
                else if(d.warranty == '18 Months'){
                    var x = d.po_date;
                    var date = new Date(x);
                    var z= date.setFullYear( date.getFullYear() + 1 );
                    var c =new Date(z)
                    var y=c.setMonth( c.getMonth() + 6 );
                    frappe.model.set_value(d.doctype, d.name,"end_date",frappe.datetime.add_days(y))
                }
                else if(d.warranty == '24 Months'){
                    var x = d.po_date;
                    var date = new Date(x);
                    date.setFullYear( date.getFullYear() + 2 );
                    frappe.model.set_value(d.doctype, d.name,"end_date",frappe.datetime.add_days(date))
                }
                else{
                    frappe.validated=false;
                }
        })
    }
})
frappe.ui.form.on('Delivery Note', {
    
    refresh: function(frm) {
        //if ((!frm.doc.is_return) && (doc.status!="Closed" || frm.is_new())) {
        //    if (frm.doc.docstatus===0) {
       if (!frm.doc.__islocal && frm.doc.docstatus<2) {
        //if (frm.doc.docstatus===0) {
        //if (frm.doc.docstatus<2) {
            frm.add_custom_button(__('Sales Order'),
            cur_frm.cscript['make_delivery_note'], __("Get items from"));
        }
        
    } 

});
cur_frm.cscript.make_delivery_note = function(doc) {
    frappe.model.open_mapped_doc({
        method: "ringlus.ringlus.doctype.sales_order.sales_order.make_delivery_note",
        frm: cur_frm    
    }) 
};
