# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons.base.models.res_country import Country


class Adress(models.Model):

    _name = 'delivery.adress'

    delivery_adress=fields.Char('Dirección de entrega',required=True)
    country_id = fields.Many2one('res.country', string='Country')

    
