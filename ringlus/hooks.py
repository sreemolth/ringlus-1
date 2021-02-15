# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "ringlus"
app_title = "Ringlus"
app_publisher = "Momscode Technologies"
app_description = "Custom App for Ringlus"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@momscode.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ringlus/css/ringlus.css"
# app_include_js = "/assets/ringlus/js/ringlus.js"

# include js, css files in header of web template
# web_include_css = "/assets/ringlus/css/ringlus.css"
# web_include_js = "/assets/ringlus/js/ringlus.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"BOM" : "public/js/bom.js",
"Production Plan":"public/js/production_plan.js",
#"Purchase Receipt":"public/js/purchase_receipt.js",
"Quotation":"public/js/quotation.js",
"Sales Order":"public/js/sales_order.js",
"Delivery Note":"public/js/delivery_note.js",
"Issue":"public/js/issue.js",
"Material Reques":"public/js/material_request.js"}


doctype_list_js = {"Opportunity":"public/js/opportunity_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "ringlus.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "ringlus.install.before_install"
# after_install = "ringlus.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ringlus.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
 	"BOM": { 
        "on_change": "ringlus.ringlus.doctype.bom.bom_custom.on_BOM_after_submit",
    },
    "Sales Order":{
        "on_submit":"ringlus.ringlus.doctype.sales_order.sales_order.on_sales_order_on_submit"
    },
    "Delivery Note":{
        "on_change":"ringlus.ringlus.doctype.delivery_note.delivery_note.delivery_note_on_save",
        "on_submit":"ringlus.ringlus.doctype.delivery_note.delivery_note.delivery_note_on_approve"
    },
   "Sales Invoice":{
        "on_change":"ringlus.ringlus.doctype.sales_invoice.sales_invoice.sales_invoice_on_save"
    },
    "Production Plan":{
        "on_change":"ringlus.ringlus.doctype.production_plan.production_plan.production_plan_on_save",
        #"on_submit":"ringlus.ringlus.doctype.production_plan.production_plan.make"
    }

}


# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ringlus.tasks.all"
# 	],
# 	"daily": [
# 		"ringlus.tasks.daily"
# 	],
# 	"hourly": [
# 		"ringlus.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ringlus.tasks.weekly"
# 	]
# 	"monthly": [
# 		"ringlus.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "ringlus.install.before_tests"

# Overriding Methods
# ------------------------------
#

# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ringlus.task.get_dashboard_data"
# }
fixtures = ["Custom Field"]
