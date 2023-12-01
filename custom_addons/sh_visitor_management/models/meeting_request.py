# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, api, _
from datetime import datetime, timedelta
import time


class MeetingRequest(models.Model):
    _name = "meeting.request"
    _description = "Meeting Request"
    _order = "id desc"

    name = fields.Char(
        string="Doc No.",
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _("New"),
        tracking=True
    )
    meeting_call_no = fields.Char('Meeting Invite No')
    partner_name = fields.Char(
        "Name",
        tracking=True
    )
    mobile = fields.Char("Mobile", tracking=True)
    mail = fields.Char("Email", tracking=True)
    company_name = fields.Char("Company", tracking=True)
    employee_id = fields.Many2one(
        "hr.employee",
        string="Meet to whom?",
        tracking=True)
    purpose = fields.Text("Purpose", tracking=True)
    crt_date = fields.Datetime(
    'Creation Date',
    readonly = True,
    default = lambda * a: time.strftime('%Y-%m-%d %H:%M:%S'))
    state = fields.Selection([('draft','Draft'),('submitted','Submitted')],'Status',default='draft')
    appointment = fields.Selection([('yes','Yes'),('no','No')],'Appointment')
    pass_details_no = fields.Char("Pass Details No", tracking=True)


    @api.model
    def create(self, vals):
        if vals.get("name", _("New")) == _("New"):
            vals["name"] = self.env["ir.sequence"].next_by_code(
                "meeting.request") or _("New")
        result = super(MeetingRequest, self).create(vals)
        return result

    @api.onchange("meeting_call_no")
    def visitor_detials_onchange_call_no(self):
        if self.meeting_call_no:
            call_id = self.env['meeting.call'].search([('name', '=', self.meeting_call_no)],limit=1)
            if call_id:
                self.partner_name = call_id.visitor_name
                self.mobile = call_id.mobile
                self.mail = call_id.mail
                self.employee_id = call_id.employee_id.id or False
                self.purpose = call_id.purpose
                self.company_name = call_id.company
            else:
                self.partner_name = ''
                self.mobile = ''
                self.mail = ''
                self.employee_id = False
                self.purpose = ''
                self.company_name = ''
        else:
            self.partner_name = ''
            self.mobile = ''
            self.mail = ''
            self.employee_id = False
            self.purpose = ''
            self.company_name = ''

    @api.onchange("mobile")
    def visitor_detials_onchange_mobile(self):
        if not self.meeting_call_no:
            if self.mobile:
                request_id = self.env['meeting.request'].search([('mobile', '=', self.mobile)],order='id desc',limit=1)
                if request_id:
                    self.partner_name = request_id.partner_name
                    self.mail = request_id.mail
                    self.company_name = request_id.company_name
                else:
                    self.partner_name = ''
                    self.mail = ''
                    self.company_name = ''
            else:
                self.partner_name = ''
                self.mail = ''
                self.company_name = ''

    def entry_submit(self):
        if self.meeting_call_no:
            call_id = self.env['meeting.call'].search([('name', '=', self.meeting_call_no)],limit=1)
            if call_id:
                visitor_id = self.env['sh.visitor.details'].create({
                        'call_ref': self.meeting_call_no,
                        'visitor_name': self.partner_name,
                        'mobile': self.mobile,
                        'mail': self.mail,
                        'employee_id': self.employee_id.id or False,
                        'purpose': self.purpose,
                        'visitors_type': 'invited',
                        'request_ref': self.id,
                        'state': 'requested',
                        'customer_type' : call_id.customer_type,
                        'partner_id': call_id.partner_id.id or False,
                        'company': self.company_name,
                        'phone': call_id.phone,
                        'visit_type_id': call_id.visit_type_id.id or False,
                        'visit_categ_id': call_id.visit_categ_id.id or False,
                        'reference': call_id.reference,
                        'department': call_id.department.id or False,
                        'user_id': call_id.user_id.id or False,
                        'company_id': call_id.company_id.id or False,
                    })
                self.pass_details_no = visitor_id.name
        else:
            visitor_id = self.env['sh.visitor.details'].create({
                    'visitor_name': self.partner_name,
                    'mobile': self.mobile,
                    'mail': self.mail,
                    'employee_id': self.employee_id.id or False,
                    'purpose': self.purpose,
                    'visitors_type': 'direct',
                    'request_ref': self.id,
                    'state': 'requested',
                    'company':self.company_name,
                })
            self.pass_details_no = visitor_id.name
        self.write({'state': 'submitted',
                        })

    def print_pdf(self):
        return self.env.ref('sh_visitor_management.pass_details_initial_report_pdf').report_action(self)
