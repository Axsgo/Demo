# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, api, _
from datetime import datetime, timedelta


class ShVisitorDetails(models.Model):
    _name = "sh.visitor.details"
    _inherit = ["portal.mixin",
                "mail.thread",
                "mail.activity.mixin",
                "utm.mixin"]
    _description = "Visitor Details"
    _order = "id desc"


    customer_type = fields.Selection([('walk_in','Walk-In'),('regular','Regular')],string='Type')
    name = fields.Char(
        string="Visitor Serial Number",
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

    check_in = fields.Datetime(
        "Check In",
        tracking=True
    )
    check_out = fields.Datetime("Check Out", tracking=True)

    check_in_str = fields.Char("Check In string")
    check_out_str = fields.Char("Check Out string")

    duration = fields.Float(
        "Duration",
        readonly=True,
        compute="_compute_time_duration",
        default=0.0,
        tracking=True
    )

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

    visitor_sign = fields.Image(
        string="Visitor",
        copy=False,
        attachment=True,
        max_width=1024,
        max_height=1024
    )
    whom_to_meet_sign = fields.Image(
        string="Whom to meet",
        copy=False,
        attachment=True,
        max_width=1024,
        max_height=1024
    )
    state = fields.Selection([('requested','Requested'),('mail_sent','Mail Sent'),('approved','Approved'),('closed','Closed')],'Status',default='requested')
    visitors_type = fields.Selection([('direct','Direct'),('invited','Invited')],'Type of Visitors')
    request_ref = fields.Many2one('meeting.request',string="Meeting Request Ref")
    call_ref = fields.Char("Meeting Call Ref")
    
    def _compute_access_url(self):
        super(ShVisitorDetails, self)._compute_access_url()
        for rec in self:
            rec.access_url = "/my/visitor/%s" % (rec.id)

    def _get_report_base_filename(self):
        self.ensure_one()
        return "%s %s" % ("Visitor", self.name)

    @api.model
    def create(self, vals):
        if vals.get("name", _("New")) == _("New"):
            vals["name"] = self.env["ir.sequence"].next_by_code(
                "sh.visitor.details") or _("New")
        result = super(ShVisitorDetails, self).create(vals)
        check_in = result.check_in
        if check_in:
            check_in_date_time_str = datetime.strftime(
                check_in, '%m/%d/%Y %I:%M %p')
            check_in_date_obj = datetime.strptime(
                check_in_date_time_str, '%m/%d/%Y %I:%M %p')
            check_in_datetime_obj_1 = check_in_date_obj + \
                timedelta(hours=5, minutes=30)
            check_in_date_time_str = datetime.strftime(
                check_in_datetime_obj_1, '%m/%d/%Y %I:%M %p')
            result.check_in_str = check_in_date_time_str
        if result.check_out:
            check_out = result.check_out
            check_out_date_time_str = datetime.strftime(
                check_out, '%m/%d/%Y %I:%M %p')
            check_out_date_obj = datetime.strptime(
                check_out_date_time_str, '%m/%d/%Y %I:%M %p')
            check_out_datetime_obj_1 = check_out_date_obj + \
                timedelta(hours=5, minutes=30)
            check_out_date_time_str = datetime.strftime(
                check_out_datetime_obj_1, '%m/%d/%Y %I:%M %p')
            result.check_out_str = check_out_date_time_str
        return result

    def write(self, vals):
        if vals.get('check_out'):
            check_out = vals.get('check_out')
            if str(type(check_out)) == "<class 'str'>":
                check_out_obj = datetime.strptime(
                    check_out, "%Y-%m-%d %H:%M:%S")
                check_out_date_time_str = datetime.strftime(
                    check_out_obj, '%m/%d/%Y %I:%M %p')
                check_out_date_obj = datetime.strptime(
                    check_out_date_time_str, '%m/%d/%Y %I:%M %p')
                check_out_datetime_obj_1 = check_out_date_obj + \
                    timedelta(hours=5, minutes=30)
                check_out_date_time_str = datetime.strftime(
                    check_out_datetime_obj_1, '%m/%d/%Y %I:%M %p')
                vals.update({
                    'check_out_str': check_out_date_time_str
                })
        return super(ShVisitorDetails, self).write(vals)

    @api.depends("check_in", "check_out")
    def _compute_time_duration(self):
        for rec in self:
            rec.duration = 0.0
            if rec.check_in and rec.check_out:
                diff_time = rec.check_out - rec.check_in
                duration = float(diff_time.days) * 24 + \
                    (float(diff_time.seconds) / 3600)
                rec.duration = round(duration, 2)

    @api.onchange("partner_id")
    def visitor_detials(self):
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
        if self.employee_id:
            if self.employee_id.work_email:         
                template = self.env['ir.model.data'].get_object('sh_visitor_management', 'ax_visitor_details_mail_template')
                email_to = self.employee_id.work_email
                email_values = {'email_to': email_to,
                           'email_from': self.env.user.partner_id.email}
                if template:
                    self.env['mail.template'].browse(template.id).send_mail(self.id,email_values=email_values,force_send=True)
                self.write({'state': 'mail_sent',
                        })

    def action_visitor(self):
        self.write({'state': 'approved',
                        })

    def entry_approve(self):
        self.write({'state': 'approved',
                        })
    def entry_close(self):
        self.write({'state': 'closed',
                        })