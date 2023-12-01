# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Visitor Management System",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "license": "OPL-1",
    "version": "14.0.3",
    "category": "Industries",
    "summary": """
Residential Visitor Management System, Visitor Pass System Module,
Industrial Visitors Management, Visit Management App,
Visitor Check-In Detail, Tourist Management,
Guest Management, Visitor Check-Out Detail Odoo
""",
    "description": """
The "Visitor Management System" gives an efficient way to manage visitors.
You can keep track of who meets whom.
You can know the purpose of the visitors
with details like visitors contact details,
check-in/out detail, visit destination, visit type, visit category,
reference name, employee name & department name.
You can see visitors details in the tree view & form view.
You can print visitors pass with full information.
Visitor Management System Odoo, Residential Visitor Management System,
Visitor Pass System Module, Industrial Visitors Management, Visit Management,
Visitor Check-In Detail, Tourist Management, Guest Management,
Visitor Check-Out Detail Odoo, Residential Visitor Management System,
Visitor Pass System Module, Industrial Visitors Management,
Visit Management App, Visitor Check-In Detail, Tourist Management,
Guest Management, Visitor Check-Out Detail Odoo
""",
    "depends": [
        "hr",
        "utm",
        "portal"
    ],
    "data": [
        "security/sh_visitor_management_security.xml",
        "security/ir.model.access.csv",
        "reports/visitor_report_view.xml",
        "reports/print_pass_report_view.xml",
        "data/ir_sequence_data.xml",
        "views/controllers.xml",
        "views/visitor_details_view.xml",
        "views/visitor_category_view.xml",
        "views/visitor_type_view.xml",
        "views/meeting_request_view.xml",
        "views/meeting_call_view.xml",
    ],
    "images": ["static/description/background.png", ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": "30",
    "currency": "EUR"
}
