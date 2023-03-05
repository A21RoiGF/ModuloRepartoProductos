# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _


class Order(models.Model):

    _name = 'order'
    _description = 'Pedido'

    programmed_date = fields.Date('Fecha programada')
    product_ids=fields.Many2many('product',string='Producto')
    frecuency = fields.Integer('Repartir cada')
    frecuency_states = fields.Selection([
        ('daily', 'Dias'),
        ('monthly', 'Meses'),
        ('weekly', 'Semanas')],
        'Espacio de tiempo', default="weekly")
    