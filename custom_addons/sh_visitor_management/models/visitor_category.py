# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ShVisitorCategory(models.Model):
    _name = 'sh.visitor.category'
    _description = 'Visitor Category'
    _order = 'id desc'

    name = fields.Char('Name', required=True)
