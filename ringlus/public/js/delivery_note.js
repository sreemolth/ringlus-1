
/*frappe.ui.form.on("Delivery Note", {
    validate:function(frm,cdt,cdn){
        var d=locals[cdt][cdn]
        if(frm.doc.customer){
            //alert("mmm");
            frappe.call({
                method: 'frappe.client.get',
                args:{
                    'doctype': 'Delivery Note Item',           
                },
                callback: function(r) {
                    alert("hiii");
                    if(!r.exc){
                        if(r.message.against_sales_order){
                            alert("kooiiii")
                            frappe.call({
                                method:"frappe.client.get_value",
                                args:{
                                    'doctype':'Product Serial No',
                                    'fieldname': [
                                        "sales_order","serial_no"
                                    ],
                                },
                                callback:function(s){
                                    alert("anu")
                                    if(!s.exc){
                                        if(s.sales_order==r.against_sales_order){
                                            frm.set_value("product_serial_no",r.serial_no)
                                        }
                                    }
                                }
                            })

                        }
                            
                    }
                }
            })
        }
    }
})
frappe.ui.form.on("Delivery Note Item", {
    refresh:function(frm,cdt,cdn){
        var d=locals[cdt][cdn]
        debugger;
        frappe.call({
            method: 'frappe.client.get_value',
            args:{
                'doctype': 'Product Serial No', 
                'filters': {
                    sales_order:frm.doc.against_sales_order
                },
                'fieldname': [
                    "sales_order","serial_no"
                ],          
            },
            callback: function(r) {
                alert("hiii");
                if(!r.exc){
                   if(r.message.sales_order==frm.doc.against_sales_order){
                       frappe.model.set_value(d.doctype, d.name,"product_serial_no",r.message.serial_no)
                   }
                }
            }
        })
        
    }
})*/



/*frappe.ui.form.on("Delivery Note Item", {

    item_code:function(frm,cdt,cdn){
        alert("hai")
        var d =locals[cdt][cdn];
        alert("hii");
        frappe.call({
            method: 'frappe.client.get_value',
            args:{
                'doctype': 'Sales Order', 
                'filters': {
                    name:frm.doc.against_sales_order
                },
                'fieldname':[
                    'warranty'
                ]
                         
            },
            callback: function(r) {
                alert("hiii");
                if(!r.exc){
                    alert(r.message.warranty);
                    frm.set_value("warranty",r.message.warranty);
                }
            }

        })
    }

})

frappe.ui.form.on("Delivery Note Item", {
    reload:function(frm,cdt,cdn){
        alert("kkkkk");
    }
})*/


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
                    alert("No Warranty");
                    var x = d.po_date;
                    var date = new Date(x);
                    date.setDate(date.getDate() + 1);
                    frappe.model.set_value(d.doctype, d.name,"end_date",frappe.datetime.add_days(date))
                }
                else if(d.warranty == '6 Months'){
                    alert("6 Months");
                    var x = d.po_date;
                    var date = new Date(x);
                    date.setMonth(date.getMonth() +6);
                    frappe.model.set_value(d.doctype, d.name,"end_date",frappe.datetime.add_days(date))
                }
                else if(d.warranty == '12 Months'){
                    alert("12 Months");
                    var x = d.po_date;
                    var date = new Date(x);
                    date.setFullYear( date.getFullYear() + 1 );
                    frappe.model.set_value(d.doctype, d.name,"end_date",frappe.datetime.add_days(date))
                }
                else if(d.warranty == '18 Months'){
                    alert("18 Months");
                    var x = d.po_date;
                    var date = new Date(x);
                    var z= date.setFullYear( date.getFullYear() + 1 );
                    var c =new Date(z)
                    var y=c.setMonth( c.getMonth() + 6 );
                    frappe.model.set_value(d.doctype, d.name,"end_date",frappe.datetime.add_days(y))
                }
                else if(d.warranty == '24 Months'){
                    alert("24 Months");
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

/*frappe.ui.form.on('Delivery Note', {
    validate: function(frm) {
        alert("hiii");
        var war=0;
        $.each(frm.doc.items || [], function(i, d) {
            war = d.warranty;
        });
        frm.doc.warranty = war;
        frm.doc.posting_date = new Date();
        //var d = frm.doc.posting_date.getDate();
        //var m = frm.doc.posting_date.getMonth() + 1;
        //var y = frm.doc.posting_date.getFullYear();
        //var z = d+'-'+m+'-'+y;
        //alert(z);
        if (frm.doc.warranty == 'No Warranty'){
            alert("no warranty")
            frm.set_value("end_date",frm.doc.posting_date);
            //frm.doc.end_date = z;
        }
        else if(frm.doc.warranty == '6 Months'){
            alert("6 month warranty");
            var d=frm.doc.posting_date;
            var date =new Date(d);
            date.setMonth( date.getMonth() + 6 );
            frm.set_value("end_date",frappe.datetime.add_days(date));
            
        }
        else if(frm.doc.warranty == '12 Months'){
            alert("12 month warranty");
            var d=frm.doc.posting_date;
            var date =new Date(d);
            date.setFullYear( date.getFullYear() + 1 );
            frm.set_value("end_date",frappe.datetime.add_days(date));
        }
        else if(frm.doc.warranty == '18 Months'){
            alert("18 month warranty");
            var d=frm.doc.posting_date;
            var date =new Date(d);
            var x= date.setFullYear( date.getFullYear() + 1 );
            var c =new Date(x)
            var y=c.setMonth( c.getMonth() + 6 );
            frm.set_value("end_date",frappe.datetime.add_days(y));
        }
        else if(frm.doc.warranty == '24 Months'){
            alert("24 month warranty");
            var d=frm.doc.posting_date;
            var date =new Date(d);
            date.setFullYear( date.getFullYear() + 2 );
            frm.set_value("end_date",frappe.datetime.add_days(date));
        }
    }
});*/

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
/*frappe.ui.form.on('Delivery Note', {
    refresh: function(frm) {
        if (!frm.doc.__islocal && frm.doc.docstatus<2) {
       frm.add_custom_button(__('Get '),
		 cur_frm.cscript['create_tickets'], __("Make1"));
    } 
}
});
cur_frm.cscript.create_tickets = function(doc) {
   frappe.model.open_mapped_doc({
			method: "ringlus.ringlus.doctype.sales_order.sales_order.make_delivery_note1",
			frm: cur_frm
		}) 
};
 
frappe.ui.form.on('Delivery Note Item', {
    setup: function(frm) {
        var grid_row = cur_frm.open_grid_row();
		if(!grid_row || !grid_row.grid_form.fields_dict.serial_no ||
			grid_row.grid_form.fields_dict.serial_no.get_status()!=="Write") return;
        
		var $btn = $('<button class="btn btn-sm btn-default">'+__("Add Srl No")+'</button>')
			.appendTo($("<div>")
				.css({"margin-bottom": "10px", "margin-top": "10px"})
				.appendTo(grid_row.grid_form.fields_dict.serial_no.$wrapper));

		var me = this;
		$btn.on("click", function() {
			let callback = '';
			let on_close = '';

			frappe.model.get_value('Item', {'name':grid_row.doc.item_code}, 'has_serial_no',
				(data) => {
					if(data) {
						grid_row.doc.has_serial_no = data.has_serial_no;
						me.show_serial_batch_selector(grid_row.frm, grid_row.doc,
							callback, on_close, true);
					}
				}
			);
		});
    }
})*/