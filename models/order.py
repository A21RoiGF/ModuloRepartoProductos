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

    order_id=fields.Many2one('delivery.order',required=True,ondelete='cascade')

class Order(models.Model):

    _name = 'delivery.order'
    _description = 'Pedido'
    _order = 'next_delivery_date asc'

    programmed_date = fields.Date('Fecha comienzo',required=True)

    @api.constrains('programmed_date')
    def check_programmed_date(self):
        for order in self:
            if(order.programmed_date < fields.Date.today()):
                raise UserError('La fecha de comienzo del pedido no puede ser anterior a la fecha actual')
    
    # one2many pq un pedido puede tener varias lineas y las lineas no pueden estar en otros pedidos
    order_lines=fields.One2many('delivery.order.line',string='Lineas del pedido',inverse_name='order_id',required=True,ondelete='cascade')

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
    
    next_delivery_date=fields.Date('Fecha entrega',compute='_calculate_delivery_date',store=True,readonly=True)

    @api.depends('active_order','frecuency_states','programmed_date','frecuency')
    def _calculate_delivery_date(self):
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

    remaining_days = fields.Integer(string='Días restantes',compute='compute_remaining_days',readonly=True)

    def compute_remaining_days(self):
        actual_date=datetime.now().date()
        for order in self:
            if order.next_delivery_date:
                delivery_date=datetime.strptime(order.next_delivery_date.strftime('%Y-%m-%d'), '%Y-%m-%d').date()
                remaining_days = (delivery_date - actual_date).days
                order.remaining_days = remaining_days if remaining_days >= 0 else 0
            else:
                order.remaining_days = 0

    total_price=fields.Float('Precio por entrega',compute='calculate_total_price',readonly=True)

    def calculate_total_price(self):
        for order in self:
            totalPrice=0
            for order_line in order.order_lines:
                totalPrice+=order_line.product_id.current_price*order_line.amount
            order.total_price+=totalPrice

    total_cost=fields.Float('Coste por entrega',compute='calculate_total_cost',readonly=True)

    def calculate_total_cost(self):
        for order in self:
            totalCost=0
            for order_line in order.order_lines:
                totalCost+=order_line.product_id.current_cost*order_line.amount
            order.total_cost+=totalCost

    weekly_price=fields.Float('Precio semanal',compute='calculate_weekly_price',readonly=True)

    def calculate_weekly_price(self):
        for order in self:
            if(order.frecuency_states=='daily'):
                daily_price=order.total_price/order.frecuency
                order.weekly_price=daily_price*7
            elif(order.frecuency_states=='weekly'):
                order.weekly_price=order.total_price/order.frecuency
            elif(order.frecuency_states=='monthly'):
                order.weekly_price=(order.total_price/order.frecuency)*4 

    active_order=fields.Boolean('Pedido Activo',default=True,readonly=True)

    delivery_adress_id=fields.Many2one('delivery.adress',string='Dirección de entrega',required=True)
    delivery_adress_name=fields.Char(string='Dirección de entrega',compute='_compute_adress_name')

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