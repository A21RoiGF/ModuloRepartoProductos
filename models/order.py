# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class OrderLine(models.Model):

    _name = 'order.line'
    _description = 'Linea de pedido'

    # many2one pq un producto puede estar en varias lineas y ???
    product_id=fields.Many2one('product',string='Productos')
    amount=fields.Integer('Cantidad') 

class Order(models.Model):

    _name = 'order'
    _description = 'Pedido'

    programmed_date = fields.Date('Fecha comienzo',required=True)
    
    # many2many pq un pedido puede tener varias lineas y estar en otros pedidos
    order_lines=fields.Many2many('order.line',string='Lineas del pedido',required=True)

    frecuency = fields.Integer('Repartir cada',required=True)
    frecuency_states = fields.Selection([
        ('daily', 'Dias'),
        ('monthly', 'Meses'),
        ('weekly', 'Semanas')],
        'Espacio de tiempo', default="weekly",required=True)
    
    next_delivery_date=fields.Date('Fecha entrega',compute='calculate_delivery_date',readonly=True)

    def calculate_delivery_date(self):
        for order in self:
            if(order.frecuency_states=='daily'):
                order.next_delivery_date=order.programmed_date+timedelta(days=order.frecuency)
            elif(order.frecuency_states=='monthly'):
                order.next_delivery_date=order.programmed_date+relativedelta(months=order.frecuency)
            elif(order.frecuency_states=='weekly'):
                order.next_delivery_date=order.programmed_date+timedelta(weeks=order.frecuency)

    total_price=fields.Float('Precio total',compute='calculate_total_price',readonly=True)

    def calculate_total_price(self):
        for order in self:
            totalPrice=0
            for order_line in order.order_lines:
                totalPrice+=order_line.product_id.current_price*order_line.amount
            order.total_price+=totalPrice