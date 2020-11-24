frappe.ui.form.on('BOM', {
    onload:function(frm, cdt, cdn){
        alert("hi")
        var d=locals[cdt][cdn]
        frm.set_query("product_serial_no", function() {
            alert("hai")
            return {
                filters: [
                    ["Serial No","sales_order", "=", d.against_sales_order]
                ]
            }
        });
}
})