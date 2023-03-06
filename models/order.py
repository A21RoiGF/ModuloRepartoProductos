# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _

from datetime import datetime, timedelta


class Order(models.Model):

    _name = 'order'
    _description = 'Pedido'

    programmed_date = fields.Date('Fecha comienzo')
    # many2many pq un pedido puede tener varios productos y un producto estar en varios pedidos
    product_ids=fields.Many2many('product',string='Producto')
    frecuency = fields.Integer('Repartir cada')
    frecuency_states = fields.Selection([
        ('daily', 'Dias'),
        ('monthly', 'Meses'),
        ('weekly', 'Semanas')],
        'Espacio de tiempo', default="weekly")
    
    next_delivery_date=fields.Date('Fecha entrega',compute='calculate_delivery_date',readonly=True)

    def calculate_delivery_date(self):
        for order in self:
            order.next_delivery_date=order.programmed_date+timedelta(days=10)
    
