# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    current_location_id = fields.Many2one(
        "res.partner", string="Current Location")
    current_location_boolean = fields.Boolean(
        compute="_compute_current_location_id")

    def _compute_current_location_id(self):
        if self:
            for rec in self:
                rec.current_location_boolean = False
                if rec.has_group("base.group_portal"):
                    rec.current_location_boolean = True
