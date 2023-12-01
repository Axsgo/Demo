# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    from_date = fields.Datetime("From Date")
    to_date = fields.Datetime("To Date")

    @api.onchange('name')
    def _onchange_date(self):
        if self.to_date:
            self.date = self.to_date.date()
