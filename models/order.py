# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import UserError
from odoo.addons.base.models.res_country import Country

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class OrderLine(models.Model):

    _name = 'delivery.order.line'
    _description = 'Linea de pedido'

    # many2one pq un producto puede estar en varias lineas pero cada linea solo un producto
    product_id=fields.Many2one('delivery.product',string='Productos')
    amount=fields.Integer('Cantidad') 

class Order(models.Model):

    _name = 'delivery.order'
    _description = 'Pedido'

    programmed_date = fields.Date('Fecha comienzo',required=True)
    
    # many2many pq un pedido puede tener varias lineas y estar en otros pedidos
    order_lines=fields.Many2many('delivery.order.line',string='Lineas del pedido',required=True)

    frecuency = fields.Integer('Repartir cada',required=True)

    @api.constrains('frecuency')
    def _check_frecuency(self):
        for order in self:
            if order.frecuency==0:
                raise UserError('La frecuencia de un pedido no puede ser 0')


    frecuency_states = fields.Selection([
        ('daily', 'Dias'),
        ('monthly', 'Meses'),
        ('weekly', 'Semanas')],
        'Espacio de tiempo', default="weekly",required=True)
    
    next_delivery_date=fields.Date('Fecha entrega',compute='calculate_delivery_date',readonly=True)

    def calculate_delivery_date(self):
        for order in self:
            if(order.active_order==False):
                order.next_delivery_date=False
                return
            
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

    active_order=fields.Boolean('Pedido Activo',default=True,readonly=True)

    delivery_adress_id=fields.Many2one('delivery.adress',string='Dirección de entrega')
    delivery_adress_name=fields.Char(string='DIrección de entrega',compute='_compute_adress_name')

    @api.depends('delivery_adress_id')
    def _compute_adress_name(self):
        for order in self:
            order.delivery_adress_name = str(order.delivery_adress_id.adress)+' - '+order.delivery_adress_id.country_id.name + ' (delivery.adress,' + str(order.delivery_adress_id.id) + ')'


    # Borrar un registro
    def delete_order(self):
        for order in self:
            order.unlink()
            
    
    def deactivate_order(self):
        for order in self:
            order.active_order=not(order.active_order)

    def make_copy(self):
        for order in self:
            new_order=order.copy()

        return {'message': 'Se ha creado una copia del/os registro/s seleccionado/s.'}

    def delete_all_orders(self):

        all_records = self.search([])
        all_records.unlink()

class Adress(models.Model):

    _name = 'delivery.adress'

    adress=fields.Char('Dirección de entrega',required=True)
    country_id = fields.Many2one('res.country', string='Country')
    