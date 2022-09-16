# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'ABS PODownPay',
    'version': '13.0.1.1.2',
    'category': 'Purchase',
    'summary': 'Module for Down Payment In Purchase Orders',
    'sequence': '4',
    'author': 'Asir And Huzaifa',
    'maintainer': 'ABS',
    'depends': ['purchase'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'DownPay.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/logo.png'],
}
