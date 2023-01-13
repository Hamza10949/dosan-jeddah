# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Purchase order restriction",

    "author": "odolution",
    "developer": "fizra azhar",
    "category": "",

    "license": "OPL-1",

    "version": "15.0.1",

    "depends": [
        'account_accountant'
    ],

    "data": [
        'security/ir.model.access.csv',
        'security/p_restrict.xml',
        'view/restrict.xml',
        'view/project_fields.xml',
        'view/inventory_custom_fields.xml',
        'view/contractor.xml',
        'view/product_cus_chngs.xml',
        'view/project_type.xml',
        'view/proj_type.xml',



    ],

    "auto_install": False,
    "application": True,
    "installable": True,


}
