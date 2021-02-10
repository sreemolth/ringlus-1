
frappe.ui.form.on('BOM', {
   
    validate: function (frm, cdt, cdn) {
        var total_oc = 0;
        var total_mc = 0;
        var nested_material_cost = 0;
        var nested_operating_cost = 0;
        var amc = 0;
       var flag=0;
        $.each(frm.doc.items || [], function (i, s) {
            if (s.bom_no != '') {
                var bom = s.bom_no
                flag=1
                frappe.call({
                    method: 'frappe.client.get_value',
                    args: {
                        'doctype': 'BOM',
                        'filters': {
                            'name': bom,
                        },
                        'fieldname': ['name', 'raw_material_cost', 'operating_cost']
                    },
                    callback: function (r) {
                        if (!r.exc) {
                            var mc = (r.message.raw_material_cost) * (s.qty);
                            var oc = (r.message.operating_cost) * (s.qty);
                            total_mc += mc;
                            total_oc += oc;
                            frm.set_value("mc_cost", total_mc);
                            frm.set_value("oc_cost", total_oc);
                        }
                        //frm.set_value("mc_cost", total_mc);
                    }
                });
            }
            else {
                amc += s.amount;
                frm.set_value("ncost", amc);
            }
        });
       if(flag==0)
       {
        frm.set_value("nested_material_cost", frm.doc.raw_material_cost) 
        frm.set_value("nested_operating_cost", frm.doc.operating_cost);
        var tot=frm.doc.nested_material_cost+frm.doc.nested_operating_cost;
        frm.set_value("total_nested_bom_cost",tot)
       }
    },
    mc_cost: function (frm) {
        var nmc = frm.doc.mc_cost + frm.doc.ncost
        frm.set_value("nested_material_cost", nmc)
        var nested_operating_cost = 0;
        nested_operating_cost = frm.doc.operating_cost + frm.doc.oc_cost
        frm.set_value("nested_operating_cost", nested_operating_cost);
        var total=nested_operating_cost+nmc
        frm.set_value("total_nested_bom_cost",total)
    },
    /*refresh:function(frm, cdt, cdn){
        frappe.call({
            method:"ringlus.ringlus.doctype.bom.bom_custom.get_sellable_item_name",
            args:{
            },
            callback: function(s) {
                if(!s.exc){
                    console.log(s.message);                        
                    for (var i=0; i<=s.message.length; i++){
                        item.push(s.message[i].item_name);
                    }
                }
                
            }
            
        });
        frm.fields_dict['items'].grid.get_field('item_code').get_query = function(doc, cdt, cdn) {
            var child = locals[cdt][cdn];
            return {    
                filters:[
                    ['item_name', 'like', 'opp_%']
                ]
            }
        }
        frm.refresh_field("items");
    
    }*/
});
