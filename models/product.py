# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _

class Product(models.Model):
    _name = 'product'
    _description = 'Producto'

    name=fields.Char('Nombre',required=True)
    manufacturer=fields.Char('Fabricante',required=True)
    stock=fields.Integer('Stock')
    price=fields.One2many('product.price',inverse_name='price_id',string='Precios')




class ProductPrice(models.Model):
    _name='product.price'

    price_id=fields.Many2one('product',required=True)
    value=fields.Integer('Precio')
    date=fields.Date('Fecha')
    active=fields.Boolean('Actual')