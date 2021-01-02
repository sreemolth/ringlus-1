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