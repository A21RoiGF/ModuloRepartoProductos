# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
import re

dni_pattern = re.compile(r'^\d{8}[A-Z]$')

class Customer(models.Model):
    _name = 'delivery.customer'
    _description = 'Cliente'

    name=fields.Char('DNI',required=True)

    @api.constrains('name')
    def _check_dni(self):
        for customer in self:
            if customer.name and not dni_pattern.match(customer.name):
                raise UserError('El DNI tiene que tener un formato valido')

    name_surnames=fields.Char('Nombre y Apellidos',required=True)
    birth_date=fields.Date('Fecha de nacimiento')