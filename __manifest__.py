# -*- coding: utf-8 -*-
{
    'name': "Reparto de productos",

    'summary': """ Modulo para la gestión de repartos """,

    'description': """ Descripcion de prueba """,

    'author': "A21RoiGF",
    'website': "https://sparcival.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/delivery_order.xml',
        'views/delivery_order_line.xml',
        'views/delivery_product.xml',
        'views/delivery_product_price.xml',
        
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo/demo.xml',
    #],
}
