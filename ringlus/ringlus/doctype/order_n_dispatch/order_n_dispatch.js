// Copyright (c) 2020, Momscode Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Order n Dispatch', {
	sales_order: function(frm){
        if(frm.doc.sales_order){
            frappe.call({
				method: "ringlus.ringlus.doctype.sales_order.sales_order.get_sales_order_items",
                args:{
                    'sales_order': frm.doc.sales_order
                },	
                callback:function(r){
                    if(!r.exc){
						
                        frm.clear_table("od_items");
                        frm.refresh_field("od_items");
                        for (var i=0; i<r.message.length; i++){
                            var d = frm.add_child("od_items");
                            var item = r.message[i];
                            frappe.model.set_value(d.doctype, d.name, "item", item.item_code);
                            frappe.model.set_value(d.doctype, d.name, "delivery_date", item.delivery_date);
                            frappe.model.set_value(d.doctype, d.name, "sales_order", frm.doc.sales_order);
                            //frappe.model.set_value(d.doctype, d.name, "uom", item.uom);
                            frm.refresh_field("od_items");
                        }
                    }
                }
			})

			
		}
    },
    /*validate: function(frm,cdt,cdn){
        debugger;
        var d=locals[cdt][cdn]
          if(d.sales_order){
                    frappe.call({
                        method: 'frappe.client.get_value',
                         args:{
                            'doctype':'Order n Dispatch',
                            'filters':{
                                'sales_order':d.sales_order, 
                                
                            },
                            'fieldname':['name','sales_order',]
                        },
                    callback:function(r){
                        if (!r.exc) {
                            if(r.message.sales_order==d.sales_order&& r.message.length>0){ 
                                frappe.msgprint(__(d.sales_order +`  is Already Created `));
                                frappe.validated = false;
                            }
                            else
                            {
                                
                            }
                           
                        }
                    
                }
                    })  
                }
    },*/

    before_submit:function(frm)
    {
        debugger;
        var flag=0;
        var count=0
        var count1=0
        var pflag=0
        $.each(frm.doc.production_plan_no || [], function(i, s) {
            count1 ++
        });
        $.each(frm.doc.production_plan_no || [], function(i, s) {
            if(s.production_plan_status=='Completed'&&s.delivery_status=='Completed'&&s.sales_invoice_status=='Paid')
            {
                pflag=pflag+1
            }
        });
       
        if(count1!=pflag)
        {
            frappe.msgprint(__(`Need to Complete Sales Order Actions `));
            frappe.validated = false; 
        }
        frm.set_value( "status",'Completed');
    },
	
   
});
