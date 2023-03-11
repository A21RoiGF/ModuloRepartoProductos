# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _


class Product(models.Model):
    _name = 'delivery.product'
    _description = 'Producto'

    name = fields.Char('Nombre', required=True)

    # SELECCIONA SOLO A LOS FABRICANTES DEL MODELO RES.PARTNER
    #manufacturer = fields.Many2many('res.partner', string='Fabricantes',domain="[('supplier_rank', '>', 0)]")

    manufacturer = fields.Many2many('res.partner', string='Fabricantes')
    current_price = fields.Float('Precio actual por unidad €', required=True)

    current_cost=fields.Float('Coste actual por unidad €')

    old_prices = fields.Many2many('delivery.product.price', string='Precios anteriores €')

    image=fields.Binary('Imagen del producto')


class ProductPrice(models.Model):
    _name = 'delivery.product.price'

    value = fields.Float('Precio')
    date = fields.Date('Fecha')
