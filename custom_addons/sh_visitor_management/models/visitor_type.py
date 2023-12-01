# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShVisitorType(models.Model):
    _name = 'sh.visitor.type'
    _description = 'Visitor Type'
    _order = 'id desc'

    name = fields.Char('Name', required=True)
