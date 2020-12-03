frappe.ui.form.on('BOM', {
    onload:function(frm, cdt, cdn){
        var d=locals[cdt][cdn]
        frm.set_query("product_serial_no", function() {
            return {
                filters: [
                    ["Serial No","sales_order", "=", d.against_sales_order]
                ]
            }
        });
}
})