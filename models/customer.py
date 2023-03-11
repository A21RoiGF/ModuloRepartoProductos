# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Customer(models.Model):
    _name = 'delivery.customer'
    _description = 'Cliente'

    name=fields.Char('Nombre y Apellidos')
    birth_date=fields.Date('Fecha de nacimiento')