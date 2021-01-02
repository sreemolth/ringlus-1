// Copyright (c) 2020, Momscode Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer Factory Visit', {
	// refresh: function(frm) {
        onload:function(frm,cdt,cdn){
            var d =locals[cdt][cdn]
                frm.set_query("opportunity", function() {
                    return {
                        filters: [
                            ["Opportunity","party_name", "=", d.customer]  
                            //["is_group","=",1]
                        ]
                    }
                });
                frm.refresh_field("opportunity");
            
        }, 
        validate:function(frm,cdt,cdn){
            var d=locals[cdt][cdn]
            var visit_date=d.visit_date
                frappe.call({
                    method: 'ringlus.ringlus.doctype.customer_factory_visit.customer_factory_visit.holidays_visit_date',
                    args: { 
                        'visit_date': d.visit_date,
                    },
                    callback: function(r) {
                        if(!r.exc){
                            for (var i=0; i<r.message.length; i++){
                                var a = r.message[i].holiday_date;
                                if(d.visit_date==a){
                                    frappe.msgprint(__("Expected Start Date Should not be Holiday"));
                                    //frm.set_value('visit_date', '');
                                    frappe.validated = false;
                                }
                            }
                            
                        }
                    }
                }) 
           
        },
       
  
    
        visit_date:function(frm,cdt,cdn){
        var d=locals[cdt][cdn]
        var visit_date=d.visit_date
            frappe.call({
                method: 'ringlus.ringlus.doctype.customer_factory_visit.customer_factory_visit.holidays_visit_date',
                args: { 
                    'visit_date': d.visit_date,
                },
                callback: function(r) {
                    if(!r.exc){
                        for (var i=0; i<r.message.length; i++){
                            var a = r.message[i].holiday_date;
                            if(d.visit_date==a){
                                frappe.msgprint(__("Expected Start Date Should not be Holiday"));
                                //frm.set_value('visit_date', '');
                                frappe.validated = false;
                            }
                        }
                        
                    }
                }
            }) 
       
    },
	// }
});
