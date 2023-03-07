# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _


class Product(models.Model):
    _name = 'delivery.product'
    _description = 'Producto'

    name = fields.Char('Nombre', required=True)
    manufacturer = fields.Char('Fabricante', required=True)
    current_price = fields.Float('Precio actual por unidad €', required=True)

    old_prices = fields.Many2many(
        'delivery.product.price', string='Precios anteriores €')


class ProductPrice(models.Model):
    _name = 'delivery.product.price'

    value = fields.Float('Precio')
    date = fields.Date('Fecha')
