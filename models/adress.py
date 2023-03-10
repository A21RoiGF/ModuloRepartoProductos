# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import UserError

class Adress(models.Model):

    _name = 'delivery.adress'

    adress=fields.Char('Dirección de entrega',required=True)
    country_id = fields.Many2one('res.country', string='Country', required=True)