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

    old_prices = fields.Many2many(
        'product.price', string='Precios anteriores €')


class ProductPrice(models.Model):
    _name = 'product.price'

    value = fields.Float('Precio')
    date = fields.Date('Fecha')
