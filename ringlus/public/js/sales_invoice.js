frappe.ui.form.on("Sales Invoice", {
    
    refresh:function(frm,cdt,cdn){
        var d =locals[cdt][cdn]
        alert("hiiiii");
        var opp=d.opportunity
            frm.set_query("party_name", function() {
                return {
                    filters: [
						["Customer","docstatus", "=", 1]
						//["is_group","=",1]
                    ]
                }
            });
            frm.fields_dict['items'].grid.get_field('item_code').get_query = function(doc, cdt, cdn) {
                var child = locals[cdt][cdn];
                return {    
                    filters:[
                        ['item_code' ,'like' ,'opp_%']
                        //['item_group', 'in', ['Generic Component Item']]
                    ]
                }
            }
            frm.refresh_field("items");
            
            frm.fields_dict['optional_item'].grid.get_field('item_code').get_query = function(doc, cdt, cdn) {
                var child = locals[cdt][cdn];
                return {    
                    filters:[
                        ['item_code' ,'like' ,'opp_%']
                        //['item_group', 'in', ['Generic Component Item']]
                    ]
                }
            }
            frm.refresh_field("optional_item");
    } 
})