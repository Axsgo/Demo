# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, api, _
from datetime import datetime, timedelta


class MeetingCall(models.Model):
    _name = "meeting.call"
    _order = "id desc"

    customer_type = fields.Selection([('walk_in','Walk-In'),('regular','Regular')],string='Type')
    name = fields.Char(
        string="Call for Meeting Serial Number",
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _("New"),
        tracking=True
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        tracking=True
    )
    visitor_name = fields.Char(
        "Name",
        required=True,
        tracking=True
    )
    company = fields.Char("Company", tracking=True)
    phone = fields.Char("Phone", tracking=True)
    mobile = fields.Char("Mobile", tracking=True)
    mail = fields.Char("Email", tracking=True)

    destination_id = fields.Many2one(
        "res.partner",
        string="Visit Destination",
        tracking=True,
        default=lambda self: self.env.user.partner_id.id
    )
    visit_type_id = fields.Many2one(
        "sh.visitor.type",
        string="Visit Type",
        tracking=True
    )
    visit_categ_id = fields.Many2one(
        "sh.visitor.category",
        string="Visit Category",
        tracking=True
    )

    reference = fields.Char("Reference", tracking=True)
    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
        tracking=True
    )
    department = fields.Many2one(
        "hr.department",
        related="employee_id.department_id",
        string="Department",
        tracking=True
    )
    user_id = fields.Many2one(
        "res.users",
        string="Requested By",
        default=lambda self: self.env.user.id,
        tracking=True
    )
    company_id = fields.Many2one(
        "res.company",
        string=" Company ",
        default=lambda self: self.env.user.company_id.id,
        tracking=True
    )

    purpose = fields.Text("Purpose", tracking=True)
    state = fields.Selection([('draft','Draft'),('meeting_invite_sent','Meeting Invite Sent'),('invite_agreed','Invite Agreed')],'Status',default='draft')
    meeting_date = fields.Date(
        "Meeting Date"
    )
    meeting_time = fields.Char(
        "Meeting Time"
    )

    @api.model
    def create(self, vals):
        if vals.get("name", _("New")) == _("New"):
            vals["name"] = self.env["ir.sequence"].next_by_code(
                "meeting.call") or _("New")
        result = super(MeetingCall, self).create(vals)
        return result

    @api.onchange("partner_id")
    def visitor_detials_onchange(self):
        phone = self.partner_id.phone
        email = self.partner_id.email
        mobile = self.partner_id.mobile
        self.phone = phone
        self.mail = email
        self.mobile = mobile
        if self.partner_id.parent_id:
            self.visitor_name = self.partner_id.name
            self.company = self.partner_id.parent_id.name
        else:
            self.visitor_name = self.partner_id.name
            self.company = self.partner_id.company_id.name

    def send_mail(self):
        template = False
        if self.employee_id and self.partner_id:
            if self.employee_id.work_email and self.partner_id.email:         
                template = self.env['ir.model.data'].get_object('sh_visitor_management', 'ax_meeting_call_mail_template')
                email_from = self.employee_id.work_email
                email_to = self.partner_id.email
                email_values = {'email_to': email_to,
                           'email_from': email_from}
                if template:
                    self.env['mail.template'].browse(template.id).send_mail(self.id,email_values=email_values,force_send=True)
                self.write({'state': 'meeting_invite_sent',
                        })

    def action_invite(self):
        self.write({'state': 'invite_agreed',
                        })
