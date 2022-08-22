# -*- coding: utf-8 -*-
{
    'name': "Purchase Dynamic Approvals",
    'summary': "Based on define approval rules, purchase order dynamic approvals are created and You can also define sequence of user to approve from that approvals list",
    'description': "Based on define approval rules, purchase order dynamic approvals are created and You can also define sequence of user to approve from that approvals list",
    'category': 'Purchases',
    'author':'Preciseways',
    'version': '15.0.0',
    'depends': ['purchase'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/purchase_approval_reject_wizard.xml',
        'views/purchase_approval_view.xml',
        'views/purchase_order_view.xml',
    ],
    "installable": True,
    "application": True,
    'price': 20.0,
    'currency': 'EUR',
    'images':['static/description/banner.png'],
    'license': 'OPL-1',
}
