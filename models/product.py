# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _


class Product(models.Model):
    _name = 'product'
    _description = 'Producto'

    name = fields.Char('Nombre', required=True)
    manufacturer = fields.Char('Fabricante', required=True)
    stock = fields.Integer('Stock')
    current_price = fields.Float('Precio actual €', required=True)

    old_prices = fields.One2many(
        'product.price', inverse_name='price_id', string='Precios anteriores €')
    
    product_id=fields.Many2one('order')


class ProductPrice(models.Model):
    _name = 'product.price'

    price_id = fields.Many2one('product', required=True)
    value = fields.Float('Precio')
    date = fields.Date('Fecha')
