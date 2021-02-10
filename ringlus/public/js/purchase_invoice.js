frappe.ui.form.on('Purchase Invoice', {
    validate: function(frm) {
        alert("hiii");
        var total_rate = 0;
        $.each(frm.doc.taxes || [], function(i, d) {
            total_rate += flt(d.rate);
        });
        frm.doc.gst_rate = total_rate;
    }
});
    



















/*frappe.ui.form.on('Purchase Invoice', {
    validate: function(frm) {
        alert("hii");
        debugger;
        frappe.call({
            method: 'frappe.client.get_value',
            args:{
                'doctype': 'Purchase Taxes and Charges', 
                parent: frm.doc.name,
                'fieldname': [
                    "rate"
                ],          
            },
            callback: function(r){
                alert("hiii");
                if(!r.exc){
                    var gstrate=[];
                    for (var i=0; i<r.message.length; i++){
                        gstrate.push(r.message[i].rate);
                        var sum = gstrate.reduce(function(a, b){
                            var m = a + b;
                        }, 0);
                        
                    }
                    frm.set_value("gst_rate",m);
                }
                   //$.each(r.message.rate || [], function(i, v) {
                    //     i=i+d.rate
                   // }
            }
        })
    }
        
})*/